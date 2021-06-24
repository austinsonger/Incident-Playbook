package org.thp.scalligraph.orientdb
import java.io.InputStream
import java.util.{Base64, List => JList}

import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.services.StorageSrv
import play.api.Configuration

import scala.collection.JavaConverters._
import scala.util.{Success, Try}

@Singleton
class OrientDatabaseStorageSrv(db: OrientDatabase, chunkSize: Int) extends StorageSrv {

  case class State(recordIds: List[OIdentifiable], buffer: Array[Byte]) {

    def next: Option[State] = recordIds match {
      case head :: tail =>
        val buffer = head.getRecord[ORecordBytes].toStream
        Some(State(tail, buffer))
      case _ => None
    }
  }

  object State {
    val b64decoder: Base64.Decoder = Base64.getDecoder

    def apply(id: String): Option[State] = db.roTransaction { implicit graph =>
      graph
        .V()
        .hasId(id)
        .value[JList[OIdentifiable]]("binary")
        .headOption
        .fold(List.empty[OIdentifiable])(_.asScala.toList) match {
        case head :: tail =>
          val buffer = head.getRecord[ORecordBytes].toStream
          Some(State(tail, buffer))
        case _ => None
      }
    }
  }

  @Inject
  def this(db: OrientDatabase, configuration: Configuration) = this(db, configuration.underlying.getBytes("storage.database.chunkSize").toInt)

  override def loadBinary(folder: String, id: String): InputStream =
    new InputStream {
      private var state = State(id)
      private var index = 0

      @scala.annotation.tailrec
      override def read(): Int =
        state match {
          case Some(State(_, b)) if b.length > index =>
            val d = b(index)
            index += 1
            d.toInt & 0xff
          case None => -1
          case Some(s) =>
            state = s.next
            index = 0
            read()
        }
    }

  override def exists(folder: String, id: String): Boolean = db.roTransaction { implicit graph =>
    graph.V(id).exists
  }

  override def saveBinary(folder: String, id: String, is: InputStream)(implicit graph: Graph): Try[Unit] = {
    val odb = graph.asInstanceOf[OrientGraph].database()

    odb.declareIntent(new OIntentMassiveInsert)
    val chunkIds = Iterator
      .continually {
        val chunk = new ORecordBytes
        val len   = chunk.fromInputStream(is, chunkSize)
        odb.save[ORecordBytes](chunk)
        len -> chunk.getIdentity.asInstanceOf[OIdentifiable]
      }
      .takeWhile(_._1 > 0)
      .map(_._2)
      .toSeq
    odb.declareIntent(null)
    val v = graph.addVertex(db.attachmentVertexLabel)
    v.property("_id", id) // FIXME:ID
    v.property(db.attachmentPropertyName, chunkIds.asJava)
    Success(())
  }
}
