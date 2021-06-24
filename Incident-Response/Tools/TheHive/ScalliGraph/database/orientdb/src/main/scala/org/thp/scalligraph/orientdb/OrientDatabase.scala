package org.thp.scalligraph.orientdb

import java.util.{List => JList, Set => JSet}

import akka.NotUsed
import akka.actor.ActorSystem
import akka.stream.scaladsl.Source
import javax.inject.{Inject, Singleton}

import org.slf4j.MDC
import org.thp.scalligraph.InternalError
import org.thp.scalligraph.models._
import org.thp.scalligraph.utils.Retry
import play.api.{Configuration, Environment}

import scala.collection.JavaConverters._
import scala.concurrent.duration.FiniteDuration
import scala.util.{Failure, Success, Try}

@Singleton
class OrientDatabase(
    graphFactory: OrientGraphFactory,
    maxAttempts: Int,
    minBackoff: FiniteDuration,
    maxBackoff: FiniteDuration,
    randomFactor: Double,
    override val chunkSize: Int,
    system: ActorSystem
) extends BaseDatabase {
  val attachmentVertexLabel  = "binaryData"
  val attachmentPropertyName = "binary"

  def this(
      url: String,
      user: String,
      password: String,
      maxAttempts: Int,
      minBackoff: FiniteDuration,
      maxBackoff: FiniteDuration,
      randomFactor: Double,
      chunkSize: Int,
      system: ActorSystem
  ) =
    this(new OrientGraphFactory(url, user, password), maxAttempts, minBackoff, maxBackoff, randomFactor, chunkSize, system)

  @Inject()
  def this(configuration: Configuration, system: ActorSystem) =
    this(
      configuration.get[String]("db.orientdb.url"),
      configuration.get[String]("db.orientdb.user"),
      configuration.get[String]("db.orientdb.password"),
      configuration.get[Int]("db.onConflict.maxAttempts"),
      configuration.get[FiniteDuration]("db.onConflict.minBackoff"),
      configuration.get[FiniteDuration]("db.onConflict.maxBackoff"),
      configuration.get[Double]("db.onConflict.randomFactor"),
      configuration.underlying.getBytes("db.chunkSize").toInt,
      system
    )

  def this(system: ActorSystem) = this(Configuration.load(Environment.simple()), system)

  override def close(): Unit = graphFactory.close()

  override def roTransaction[A](body: Graph => A): A = body(graphFactory.getNoTx)

  override def tryTransaction[A](body: Graph => Try[A]): Try[A] =
    Retry(maxAttempts)
      .on[OConcurrentModificationException]
      .on[ORecordDuplicatedException]
      .withBackoff(minBackoff, maxBackoff, randomFactor)(system)
      .withTry {
        val tx = graphFactory.getTx
        MDC.put("tx", f"${tx.hashCode()}%08x")
        logger.debug(s"[$tx] Begin of transaction")
        val r = Try {
          val a = body(tx)
          tx.commit()
          logger.debug(s"[$tx] End of transaction")
          MDC.remove("tx")
          a
        }.flatten
          .recoverWith {
            case t: OConcurrentModificationException => Failure(new DatabaseException(cause = t))
            case t: ORecordDuplicatedException       => Failure(new DatabaseException(cause = t))
            case e: Throwable =>
              logger.error(s"Exception raised, rollback (${e.getMessage})")
              Try(tx.rollback())
              MDC.remove("tx")
              Failure(e)
          }
        tx.close()
        r
      }

  override def source[A](query: Graph => Iterator[A]): Source[A, NotUsed]             = ???
  override def source[A, B](body: Graph => (Iterator[A], B)): (Source[A, NotUsed], B) = ???

  private def getVariablesVertex(implicit graph: Graph): Option[Vertex] = graph.traversal().V().hasLabel("variables").headOption

  override def version(module: String): Int =
    roTransaction { implicit graph =>
      getVariablesVertex.fold(0)(v => getSingleProperty(v, s"${module}_version", UMapping.int))
    }

  override def setVersion(module: String, v: Int): Try[Unit] =
    tryTransaction { implicit graph =>
      Try {
        val variables = getVariablesVertex.getOrElse(graph.addVertex("variables"))
        setSingleProperty(variables, s"${module}_version", v, UMapping.int)
      }
    }

  private def createElementSchema(schema: OSchema, model: Model, superClassName: String, strict: Boolean): OClass = {
    val superClass = schema.getClass(superClassName)
    val clazz      = schema.createClass(model.label, superClass)
    model.fields.foreach {
      case (field, sm: SingleMapping[_, _]) =>
        clazz.createProperty(field, OType.getTypeByClass(sm.graphTypeClass)).setMandatory(strict).setNotNull(true).setReadonly(sm.isReadonly)
      case (field, om: OptionMapping[_, _]) =>
        clazz.createProperty(field, OType.getTypeByClass(om.graphTypeClass)).setMandatory(false).setNotNull(false).setReadonly(om.isReadonly)
      case (field, lm: ListMapping[_, _]) =>
        clazz
          .createProperty(field, OType.EMBEDDEDLIST, OType.getTypeByClass(lm.graphTypeClass))
          .setMandatory(false)
          .setNotNull(false)
          .setReadonly(lm.isReadonly)
      case (field, sm: SetMapping[_, _]) =>
        clazz
          .createProperty(field, OType.EMBEDDEDSET, OType.getTypeByClass(sm.graphTypeClass))
          .setMandatory(false)
          .setNotNull(false)
          .setReadonly(sm.isReadonly)
      case (field, mapping) => throw InternalError(s"Unknown mapping for $field ($mapping)")
    }
    clazz.createProperty("_id", OType.STRING).setMandatory(strict).setNotNull(true).setReadonly(true)
    clazz.createProperty("_createdBy", OType.STRING).setMandatory(strict).setNotNull(true).setReadonly(true)
    clazz.createProperty("_createdAt", OType.DATETIME).setMandatory(strict).setNotNull(true).setReadonly(true)
    clazz.createProperty("_updatedBy", OType.STRING).setMandatory(false).setNotNull(false)
    clazz.createProperty("_updatedAt", OType.DATETIME).setMandatory(false).setNotNull(false)
    clazz.setStrictMode(strict)

    clazz.createIndex(s"${model.label}__id", INDEX_TYPE.UNIQUE, "_id")

    model.indexes.foreach {
      case (IndexType.unique | IndexType.tryUnique, fields) =>
        clazz.createIndex(s"${model.label}_${fields.mkString("_")}", INDEX_TYPE.UNIQUE, fields: _*)
      case (IndexType.`basic`, fields) =>
        clazz.createIndex(s"${model.label}_${fields.mkString("_")}", INDEX_TYPE.DICTIONARY, fields: _*)
      case (IndexType.fulltext, fields) =>
        clazz.createIndex(s"${model.label}_${fields.mkString("_")}", INDEX_TYPE.FULLTEXT, fields: _*)
      case indexType => throw InternalError(s"Unrecognized index type: $indexType")
    }
    clazz
  }

  private def createEdgeProperties(schema: OSchema, model: EdgeModel[_, _], edgeClass: OClass): Unit =
    for {
      fromClass <- Option(schema.getClass(model.fromLabel))
      toClass   <- Option(schema.getClass(model.toLabel))
      className = edgeClass.getName
    } {
      fromClass.createProperty(s"out_$className", OType.LINKBAG, edgeClass)
      toClass.createProperty(s"in_$className", OType.LINKBAG, edgeClass)
      edgeClass.createProperty("in", OType.LINK, toClass)
      edgeClass.createProperty("out", OType.LINK, fromClass)
    }

  override def createSchema(models: Seq[Model]): Try[Unit] = {
    val schema = graphFactory.getNoTx.database().getMetadata.getSchema
    models.foreach {
      case model: VertexModel => createElementSchema(schema, model, OClass.VERTEX_CLASS_NAME, strict = false)
      case model: EdgeModel[_, _] =>
        val edgeClass = createElementSchema(schema, model, OClass.EDGE_CLASS_NAME, strict = false)
        createEdgeProperties(schema, model, edgeClass)
    }

    /* create the vertex for attachments */
    val superClass = schema.getClass(OClass.VERTEX_CLASS_NAME)
    val clazz      = schema.createClass(attachmentVertexLabel, superClass)
    clazz.createProperty(attachmentPropertyName, OType.LINKLIST)
    Success(())
  }
  override def addProperty[T](model: String, propertyName: String, mapping: Mapping[_, _, _]): Try[Unit]    = Failure(new NotImplementedError)
  override def removeProperty(model: String, propertyName: String, usedOnlyByThisModel: Boolean): Try[Unit] = Failure(new NotImplementedError)
  override def addIndex(model: String, indexType: IndexType.Value, properties: Seq[String]): Try[Unit]      = Failure(new NotImplementedError)

  override def drop(): Unit = graphFactory.drop()

  override def getListProperty[D, G](element: Element, key: String, mapping: ListMapping[D, G]): Seq[D] =
    element
      .value[JList[G]](key)
      .asScala
      .map(mapping.toDomain)

  override def getSetProperty[D, G](element: Element, key: String, mapping: SetMapping[D, G]): Set[D] =
    element
      .value[JSet[G]](key)
      .asScala
      .map(mapping.toDomain)
      .toSet

  override def setListProperty[D, G](element: Element, key: String, values: Seq[D], mapping: ListMapping[D, _]): Unit = {
    element.property(key, values.flatMap(mapping.toGraphOpt).asJava)
    ()
  }

  override def setSetProperty[D, G](element: Element, key: String, values: Set[D], mapping: SetMapping[D, _]): Unit = {
    element.property(key, values.flatMap(mapping.toGraphOpt).asJava)
    ()
  }

//  override def loadBinary(id: String)(implicit graph: Graph): InputStream =
//    new InputStream {
//      val vertex = graph.V().has("_id" of id).head
//      private var recordIds                   = vertex.value[JList[OIdentifiable]]("binary").asScala.toList
//      private var buffer: Option[Array[Byte]] = _
//      private var index                       = 0
//      private def getNextChunk(): Unit =
//        recordIds match {
//          case first :: tail =>
//            recordIds = tail
//            buffer = Some(first.getRecord[ORecordBytes].toStream)
//            index = 0
//          case _ => buffer = None
//        }
//      override def read(): Int =
//        buffer match {
//          case Some(b) if b.length > index =>
//            val d = b(index)
//            index += 1
//            d.toInt & 0xff
//          case None => -1
//          case _ =>
//            getNextChunk()
//            read()
//        }
//    }
//
//  override def saveBinary(id: String, is: InputStream)(implicit graph: Graph): Vertex = {
//    val db = graph.asInstanceOf[OrientGraph].database()
//
//    db.declareIntent(new OIntentMassiveInsert)
//    val chunkIds = Iterator
//      .continually {
//        val chunk = new ORecordBytes
//        val len   = chunk.fromInputStream(is, chunkSize)
//        db.save[ORecordBytes](chunk)
//        len → chunk.getIdentity.asInstanceOf[OIdentifiable]
//      }
//      .takeWhile(_._1 > 0)
//      .map(_._2)
//      .to[Seq]
//    db.declareIntent(null)
//    val v = graph.addVertex(attachmentVertexLabel)
//    v.property("_id", id)
//    v.property(attachmentPropertyName, chunkIds.asJava)
//    v
//  }
  override def currentTransactionId(graph: Graph): AnyRef = graph
}
