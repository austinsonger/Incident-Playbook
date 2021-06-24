package org.thp.scalligraph.neo4j

import java.nio.file.{Files, Paths}
import java.util.Date

import akka.NotUsed
import akka.actor.ActorSystem
import akka.stream.scaladsl.Source
import javax.inject.Singleton

import org.thp.scalligraph.models._
import org.thp.scalligraph.utils.{Config, Retry}
import play.api.Configuration

import scala.concurrent.duration.FiniteDuration
import scala.reflect.ClassTag
import scala.util.{Failure, Success, Try}

object Neo4jDatabase {

  def defaultConfiguration: Configuration = Configuration(
    Neo4jGraph.CONFIG_DIRECTORY -> {
      val dbDir      = s"db-${math.random}"
      val targetPath = Paths.get("target")
      val dbPath     = targetPath.resolve(dbDir)
      Try(FileUtils.deletePathRecursively(dbPath))
      Try(Files.createDirectory(targetPath))
      Try(Files.createDirectory(dbPath))
      s"target/$dbDir"
    },
    Neo4jGraph.CONFIG_MULTI_PROPERTIES -> true,
    Neo4jGraph.CONFIG_META_PROPERTIES  -> true
  )
}

@Singleton
class Neo4jDatabase(
    graph: Neo4jGraph,
    maxAttempts: Int,
    minBackoff: FiniteDuration,
    maxBackoff: FiniteDuration,
    randomFactor: Double,
    system: ActorSystem
) extends BaseDatabase {

  def this(dbPath: String, maxAttempts: Int, minBackoff: FiniteDuration, maxBackoff: FiniteDuration, randomFactor: Double, system: ActorSystem) =
    this(Neo4jGraph.open(dbPath), maxAttempts, minBackoff, maxBackoff, randomFactor, system)

  def this(configuration: Configuration, system: ActorSystem) =
    this(
      Neo4jGraph.open(new Config(configuration withFallback Neo4jDatabase.defaultConfiguration)),
      configuration.get[Int]("db.onConflict.maxAttempts"),
      configuration.get[FiniteDuration]("db.onConflict.minBackoff"),
      configuration.get[FiniteDuration]("db.onConflict.maxBackoff"),
      configuration.get[Double]("db.onConflict.randomFactor"),
      system
    )

  def this(system: ActorSystem) = this(Configuration.empty, system)

  override def close(): Unit = graph.close()

  override def roTransaction[A](body: Graph => A): A = graph.synchronized {
    body(graph)
  }

  override def tryTransaction[A](body: Graph => Try[A]): Try[A] =
    Retry(maxAttempts)
      .on[ConstraintViolationException]
      .withBackoff(minBackoff, maxBackoff, randomFactor)(system)
      .withTry {
        val tx = graph.tx
        val r =
          if (tx.isOpen) Try(body(graph)).flatten
          else
            graph.synchronized {
              logger.debug(s"[$tx] Begin of transaction")
              tx.open()
              val r2 = Try {
                val a = body(graph)
                tx.commit()
                a
              }.flatten
                .recoverWith {
                  case e: Throwable =>
                    Try(tx.rollback())
                    Failure(e)
                }
              logger.debug(s"[$tx] End of transaction")
              tx.close()
              r2
            }
        r.recoverWith {
          case t: ConstraintViolationException => Failure(new DatabaseException(cause = t))
          case t                               => Failure(t)

        }
      }

  override def source[A](query: Graph => Iterator[A]): Source[A, NotUsed]             = ???
  override def source[A, B](body: Graph => (Iterator[A], B)): (Source[A, NotUsed], B) = ???

  override def createSchema(models: Seq[Model]): Try[Unit] =
    // Cypher can't be used here to create schema as it is not compatible with scala 2.12
    // https://github.com/neo4j/neo4j/issues/8832
    tryTransaction { _ =>
      val neo4jGraph = graph.getBaseGraph.asInstanceOf[Neo4jGraphAPIImpl].getGraphDatabase
      for {
        model <- models
        _ = neo4jGraph
          .schema()
          .constraintFor(Label.label(model.label))
          .assertPropertyIsUnique("_id") // FIXME:ID
          .create()
        (indexType, properties) <- model.indexes
      } {
        if (properties.size != 1)
          logger.error(s"Neo4j index can contain only one property, found ${properties.size} for ${model.label}:${properties.mkString(",")}")
        properties.headOption.foreach { property =>
          indexType match {
            case IndexType.`basic` =>
              neo4jGraph
                .schema()
                .indexFor(Label.label(model.label))
                .on(property)
                .create()
            // graph.cypher(s"CREATE INDEX ON: ${model.label}(${properties.mkString(",")})")
            case IndexType.unique | IndexType.tryUnique =>
              neo4jGraph
                .schema()
                .constraintFor(Label.label(model.label))
                .assertPropertyIsUnique(property)
                .create()
            // NodeKey constraint should be used but it is not accessible using java API
            // graph.cypher(s"CREATE CONSTRAINT ON (${model.label}:${properties.head}) ASSERT ${model.label}.${properties.head} IS UNIQUE")
            case IndexType.fulltext =>
              logger.error(s"Neo4j doesn't support fulltext index, fallback to standard index")
              neo4jGraph
                .schema()
                .constraintFor(Label.label(model.label))
                .assertPropertyIsUnique(property)
                .create()
            // graph.cypher(s"CREATE INDEX ON: ${model.label}(${properties.mkString(",")})")
          }
        }
      }
      Success(())
    }

  override def addProperty[T](model: String, propertyName: String, mapping: Mapping[_, _, _]): Try[Unit]    = Failure(new NotImplementedError)
  override def removeProperty(model: String, propertyName: String, usedOnlyByThisModel: Boolean): Try[Unit] = Failure(new NotImplementedError)
  override def addIndex(model: String, indexType: IndexType.Value, properties: Seq[String]): Try[Unit]      = Failure(new NotImplementedError)

  override def drop(): Unit = graph.getBaseGraph.shutdown() // FIXME this is not a real drop

  val dateMapping: SingleMapping[Date, Long] = SingleMapping[Date, Long](d => Some(d.getTime), new Date(_))

  def fixMapping[M <: Mapping[_, _, _]](mapping: M): M =
    if (mapping.domainTypeClass == classOf[Date]) {
      mapping.cardinality match {
        case MappingCardinality.single => dateMapping.asInstanceOf[M]
        case MappingCardinality.option => dateMapping.optional.asInstanceOf[M]
        case MappingCardinality.list   => dateMapping.sequence.asInstanceOf[M]
        case MappingCardinality.set    => dateMapping.set.asInstanceOf[M]
      }
    } else mapping

  override def getSingleProperty[D, G](element: Element, key: String, mapping: SingleMapping[D, G]): D =
    super.getSingleProperty(element, key, fixMapping(mapping))

  override def getOptionProperty[D, G](element: Element, key: String, mapping: OptionMapping[D, G]): Option[D] =
    super.getOptionProperty(element, key, fixMapping(mapping))

  override def getListProperty[D, G](element: Element, key: String, mapping: ListMapping[D, G]): Seq[D] =
    element
      .value[Array[G]](key)
      .map(fixMapping(mapping).toDomain)

  // super.getListProperty(element, key, fixMapping(mapping))

  override def getSetProperty[D, G](element: Element, key: String, mapping: SetMapping[D, G]): Set[D] = {
    implicit val dClassTag: ClassTag[D] = ClassTag(mapping.domainTypeClass)
    element
      .value[Array[G]](key)
      .map(fixMapping(mapping).toDomain)
      .toSet
  }

  // super.getSetProperty(element, key, fixMapping(mapping))

  override def setListProperty[D, G](element: Element, key: String, values: Seq[D], mapping: ListMapping[D, _]): Unit = {
    element.property(key, values.flatMap(fixMapping(mapping).toGraphOpt).toArray(ClassTag(mapping.graphTypeClass)))
    ()
    // super.setListProperty(element, key, values, fixMapping(mapping))
  }

  override def setSetProperty[D, G](element: Element, key: String, values: Set[D], mapping: SetMapping[D, _]): Unit = {
    element.property(key, values.flatMap(fixMapping(mapping).toGraphOpt).toArray(ClassTag(mapping.graphTypeClass)))
    ()
    // super.setSetProperty(element, key, values, fixMapping(mapping))
  }

  override def setSingleProperty[D, G](element: Element, key: String, value: D, mapping: SingleMapping[D, _]): Unit =
    super.setSingleProperty(element, key, value, fixMapping(mapping))

  override def setOptionProperty[D, G](element: Element, key: String, value: Option[D], mapping: OptionMapping[D, _]): Unit =
    super.setOptionProperty(element, key, value, fixMapping(mapping))
  override def currentTransactionId(graph: Graph): AnyRef = ???
}
