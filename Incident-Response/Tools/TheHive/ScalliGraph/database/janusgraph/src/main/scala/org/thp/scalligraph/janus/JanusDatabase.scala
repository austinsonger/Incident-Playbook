package org.thp.scalligraph.janus

import akka.NotUsed
import akka.actor.ActorSystem
import akka.stream.scaladsl.{Flow, Source}
import com.typesafe.config.ConfigObject
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversalSource
import org.apache.tinkerpop.gremlin.process.traversal.{P, Text, TraversalSource}
import org.apache.tinkerpop.gremlin.structure.Transaction.READ_WRITE_BEHAVIOR
import org.apache.tinkerpop.gremlin.structure.{Edge, Element, Vertex, Graph => TinkerGraph}
import org.janusgraph.core.attribute.{Text => JanusText}
import org.janusgraph.core.schema.{Mapping => _, _}
import org.janusgraph.core._
import org.janusgraph.diskstorage.PermanentBackendException
import org.janusgraph.diskstorage.locking.PermanentLockingException
import org.janusgraph.graphdb.configuration.GraphDatabaseConfiguration
import org.janusgraph.graphdb.database.StandardJanusGraph
import org.janusgraph.graphdb.relations.RelationIdentifier
import org.janusgraph.graphdb.tinkerpop.optimize.JanusGraphStepStrategy
import org.slf4j.MDC
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.janus.strategies._
import org.thp.scalligraph.models.{MappingCardinality, _}
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph, GraphWrapper, Traversal}
import org.thp.scalligraph.utils.{Config, Retry}
import org.thp.scalligraph.{EntityId, InternalError, SingleInstance}
import play.api.{Configuration, Logger}

import java.lang.{Long => JLong}
import java.nio.file.{Files, Paths}
import java.util.{Date, Properties}
import scala.collection.JavaConverters._
import scala.concurrent.duration.FiniteDuration
import scala.util.{Failure, Success, Try}

object JanusDatabase {
  lazy val logger: Logger = Logger(getClass)

  def openDatabase(configuration: Configuration, system: ActorSystem): JanusGraph = {
    val backend = configuration.get[String]("db.janusgraph.storage.backend")
    if (backend == "berkeleyje") {
      val jePropertyFile = Paths.get(configuration.get[String]("db.janusgraph.storage.directory"), "je.properties")
      configuration.getOptional[ConfigObject]("db.janusgraph.berkeleyje").foreach { configObject =>
        Files.createDirectories(jePropertyFile.getParent)
        val props = new Properties
        configObject.asScala.foreach { case (k, v) => props.put(s"je.$k", v.render()) }
        val propertyOutputStream = Files.newOutputStream(jePropertyFile)
        try props.store(propertyOutputStream, "DO NOT EDIT, FILE GENERATED FROM application.conf")
        finally propertyOutputStream.close()
      }
    }
    val maxAttempts  = configuration.get[Int]("db.janusgraph.connect.maxAttempts")
    val minBackoff   = configuration.get[FiniteDuration]("db.janusgraph.connect.minBackoff")
    val maxBackoff   = configuration.get[FiniteDuration]("db.janusgraph.connect.maxBackoff")
    val randomFactor = configuration.get[Double]("db.janusgraph.connect.randomFactor")

    Retry(maxAttempts)
      .on[IllegalArgumentException]
      .withBackoff(minBackoff, maxBackoff, randomFactor)(system.scheduler, system.dispatcher)
      .sync {
        JanusGraphFactory.open(new Config(configuration.get[Configuration]("db.janusgraph")))
      }
  }

  def fullTextAvailable(db: JanusGraph, singleInstance: SingleInstance): Boolean = {
    val mgmt = db.openManagement()
    try {
      lazy val location = db
        .asInstanceOf[StandardJanusGraph]
        .getConfiguration
        .getConfiguration
        .get(GraphDatabaseConfiguration.INDEX_DIRECTORY, "search") //mgmt.get("index.search.directory")
      mgmt.get("index.search.backend") match {
        case "elasticsearch" =>
          logger.info(s"Full-text index is available (elasticsearch:${mgmt.get("index.search.hostname")}) $singleInstance")
          true
        case "lucene" if singleInstance.value && !location.startsWith("/tmp") =>
          logger.info(s"Full-text index is available (lucene:$location) $singleInstance")
          true
        case "lucene" =>
          val reason =
            if (!singleInstance.value) "lucene index can't be used in cluster mode"
            else if (location.startsWith("/tmp")) "index path must not in /tmp"
            else "no reason ?!"
          logger.warn(s"Full-text index is NOT available (lucene:$location) $singleInstance: $reason")
          false
      }
    } finally mgmt.commit()
  }
}

class JanusDatabase(
    protected val janusGraph: JanusGraph,
    maxAttempts: Int,
    minBackoff: FiniteDuration,
    maxBackoff: FiniteDuration,
    randomFactor: Double,
    override val chunkSize: Int,
    system: ActorSystem,
    override val fullTextIndexAvailable: Boolean
) extends BaseDatabase
    with IndexOps {
  val name = "janus"

  val localTransaction: ThreadLocal[Option[Graph]] = ThreadLocal.withInitial[Option[Graph]](() => None)
  janusGraph.tx.onReadWrite(READ_WRITE_BEHAVIOR.MANUAL)

  def this(
      janusGraph: JanusGraph,
      configuration: Configuration,
      system: ActorSystem,
      fullTextAvailable: Boolean
  ) =
    this(
      janusGraph,
      configuration.get[Int]("db.onConflict.maxAttempts"),
      configuration.get[FiniteDuration]("db.onConflict.minBackoff"),
      configuration.get[FiniteDuration]("db.onConflict.maxBackoff"),
      configuration.get[Double]("db.onConflict.randomFactor"),
      configuration.underlying.getBytes("db.chunkSize").toInt,
      system,
      fullTextAvailable
    )

  def this(
      janusGraph: JanusGraph,
      configuration: Configuration,
      system: ActorSystem,
      singleInstance: SingleInstance
  ) =
    this(
      janusGraph,
      configuration,
      system,
      JanusDatabase.fullTextAvailable(janusGraph, singleInstance)
    )

  def this(configuration: Configuration, system: ActorSystem, singleInstance: SingleInstance) =
    this(JanusDatabase.openDatabase(configuration, system), configuration, system, singleInstance)

  def this(configuration: Configuration, system: ActorSystem, fullTextIndexAvailable: Boolean) =
    this(JanusDatabase.openDatabase(configuration, system), configuration, system, fullTextIndexAvailable)

  def batchMode: JanusDatabase = {
    val config = janusGraph.configuration()
    config.setProperty("storage.batch-loading", true)
    new JanusDatabase(
      JanusGraphFactory.open(config),
      maxAttempts,
      minBackoff,
      maxBackoff,
      randomFactor,
      chunkSize,
      system,
      fullTextIndexAvailable
    )
  }

  override def close(): Unit = janusGraph.close()

  private def parseId(s: String): AnyRef = Try(JLong.valueOf(s)).getOrElse(RelationIdentifier.parse(s))
  override val idMapping: Mapping[EntityId, EntityId, AnyRef] = new Mapping[EntityId, EntityId, AnyRef](id => parseId(id.value), EntityId.apply) {
    override val cardinality: MappingCardinality.Value                = MappingCardinality.single
    override def getProperty(element: Element, key: String): EntityId = throw InternalError(s"ID mapping can't be used for attribute $key")
    override def setProperty(element: Element, key: String, value: EntityId): Unit =
      throw InternalError(s"ID mapping can't be used for attribute $key")
    override def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](
        traversal: Traversal[TD, TG, TC],
        key: String,
        value: EntityId
    ): Traversal[TD, TG, TC] =
      throw InternalError(s"ID mapping can't be used for attribute $key")
    override def wrap(us: Seq[EntityId]): EntityId = us.head
  }

  override def roTransaction[R](body: Graph => R): R = {
    val graph    = new GraphWrapper(this, janusGraph.buildTransaction().readOnly().start())
    val oldGraph = localTransaction.get()
    try {
      localTransaction.set(Some(graph))
      val r = body(graph)
      graph.commit()
      r
    } finally {
      if (graph.isOpen) graph.rollback()
      localTransaction.set(oldGraph)
    }
  }

  override def source[A](query: Graph => Iterator[A]): Source[A, NotUsed] =
    TransactionHandler[JanusGraphTransaction, A, NotUsed](
      () => janusGraph.buildTransaction().readOnly().start(),
      _.commit(),
      _.rollback(),
      Flow[TinkerGraph].flatMapConcat(g => Source.fromIterator(() => query(new GraphWrapper(this, g))))
    )

  override def source[A, B](body: Graph => (Iterator[A], B)): (Source[A, NotUsed], B) = {
    val graph    = new GraphWrapper(this, janusGraph.buildTransaction().readOnly().start())
    val (ite, v) = body(graph)
    val src = TransactionHandler[Graph, A, NotUsed](
      () => graph,
      _.commit(),
      _.rollback(),
      Flow[Graph].flatMapConcat(_ => Source.fromIterator(() => ite))
    )
    src -> v
  }

  override def tryTransaction[R](body: Graph => Try[R]): Try[R] = {
    def executeCallbacks(graph: Graph): R => Try[R] = { r =>
      val currentCallbacks = takeCallbacks(graph)
      currentCallbacks
        .foldRight[Try[Unit]](Success(()))((cb, a) => a.flatMap(_ => cb()))
        .map(_ => r)
    }

    def commitTransaction(graph: Graph): R => R = { r =>
      graph.commit()
      r
    }

    def rollbackTransaction(graph: Graph): PartialFunction[Throwable, Failure[R]] = {
      case t =>
        Try(graph.rollback())
        Failure(t)
    }

    val oldGraph = localTransaction.get()
    val result =
      Retry(maxAttempts)
        .on[DatabaseException]
        .on[SchemaViolationException]
        .on[PermanentBackendException]
        .on[PermanentLockingException]
        .withBackoff(minBackoff, maxBackoff, randomFactor)(system.scheduler, system.dispatcher)
        .withTry {
          val graph = new GraphWrapper(this, janusGraph.buildTransaction().start())
          localTransaction.set(Some(graph))
          Try(body(graph))
            .flatten
            .flatMap(executeCallbacks(graph))
            .map(commitTransaction(graph))
            .recoverWith(rollbackTransaction(graph))
        }
        .recoverWith {
          case t: PermanentLockingException => Failure(new DatabaseException(cause = t))
          case t: SchemaViolationException  => Failure(new DatabaseException(cause = t))
          case t: PermanentBackendException => Failure(new DatabaseException(cause = t))
          case e: Throwable =>
            logger.error(s"Exception raised, rollback (${e.getMessage})")
            Failure(e)
        }
    localTransaction.set(oldGraph)
    result
  }

  lazy val globalIndexName: String = managementTransaction(mgmt => Try(findFirstAvailableMixedIndex(mgmt, "global")))
    .toOption
    .flatMap(_.toOption)
    .getOrElse("global")
  override def indexCountQuery(graph: Graph, query: String): Long =
    graph.underlying match {
      case t: Transaction =>
        logger.debug(s"Execute(indexCountQuery): $query")
        t.indexQuery(globalIndexName, query).vertexTotals()
      case _ => throw InternalError("Index query is now available")
    }

  def managementTransaction[R](body: JanusGraphManagement => Try[R]): Try[R] = {
    def commitTransaction(mgmt: JanusGraphManagement): R => R = { r =>
      logger.debug("Committing transaction")
      mgmt.commit()
      logger.debug("End of transaction")
      r
    }

    def rollbackTransaction(mgmt: JanusGraphManagement): PartialFunction[Throwable, Failure[R]] = {
      case t =>
        Try(mgmt.rollback())
        Failure(t)
    }

    Retry(maxAttempts)
      .on[PermanentLockingException]
      .withTry {
        janusGraph.synchronized {
          val mgmt = janusGraph.openManagement()
          MDC.put("tx", f"mgmt-${System.identityHashCode(mgmt)}%08x")
          logger.debug("Begin of management transaction")
          val result = Try(body(mgmt))
            .flatten
            .map(commitTransaction(mgmt))
            .recoverWith(rollbackTransaction(mgmt))
          MDC.remove("tx")
          result
        }
      }
  }

  def currentTransactionId(graph: Graph): AnyRef = graph

  override def createSchema(models: Seq[Model]): Try[Unit] =
    managementTransaction { mgmt =>
      logger.info("Creating database schema")
      createElementLabels(mgmt, models)
      createEntityProperties(mgmt)
      addProperties(mgmt, models)
      Success(())
    }

  override def addVertexModel(label: String, properties: Map[String, Mapping[_, _, _]]): Try[Unit] =
    managementTransaction { mgmt =>
      mgmt.getOrCreateVertexLabel(label)
      properties.toTry {
        case (property, mapping) => addProperty(mgmt, property, mapping)
      }
    }.map(_ => ())

  override def addEdgeModel(label: String, properties: Map[String, Mapping[_, _, _]]): Try[Unit] =
    managementTransaction { mgmt =>
      mgmt.getOrCreateEdgeLabel(label)
      properties.toTry {
        case (property, mapping) => addProperty(mgmt, property, mapping)
      }
    }.map(_ => ())

  private def createEntityProperties(mgmt: JanusGraphManagement): Unit =
    if (Option(mgmt.getPropertyKey("_label")).isEmpty) {
      mgmt
        .makePropertyKey("_label")
        .dataType(classOf[String])
        .cardinality(Cardinality.SINGLE)
        .make()
      mgmt
        .makePropertyKey("_createdBy")
        .dataType(classOf[String])
        .cardinality(Cardinality.SINGLE)
        .make()
      mgmt
        .makePropertyKey("_createdAt")
        .dataType(classOf[Date])
        .cardinality(Cardinality.SINGLE)
        .make()
      mgmt
        .makePropertyKey("_updatedBy")
        .dataType(classOf[String])
        .cardinality(Cardinality.SINGLE)
        .make()
      mgmt
        .makePropertyKey("_updatedAt")
        .dataType(classOf[Date])
        .cardinality(Cardinality.SINGLE)
        .make()
      ()
    }

  private def createElementLabels(mgmt: JanusGraphManagement, models: Seq[Model]): Unit =
    models.foreach {
      case m: VertexModel if Option(mgmt.getVertexLabel(m.label)).isEmpty =>
        logger.trace(s"mgmt.getOrCreateVertexLabel(${m.label})")
        mgmt.getOrCreateVertexLabel(m.label)
      case m: EdgeModel if Option(mgmt.getEdgeLabel(m.label)).isEmpty =>
        logger.trace(s"mgmt.getOrCreateEdgeLabel(${m.label})")
        mgmt.getOrCreateEdgeLabel(m.label)
      case m =>
        logger.info(s"Model ${m.label} already exists, ignore it")
    }

  private def addProperties(mgmt: JanusGraphManagement, models: Seq[Model]): Unit =
    models
      .flatMap(model => model.fields.map(f => (f._1, model, f._2)))
      .groupBy(_._1)
      .map {
        case (fieldName, mappings) =>
          val firstMapping = mappings.head._3
          if (!mappings.tail.forall(_._3 isCompatibleWith firstMapping)) {
            val msg = mappings.map {
              case (_, model, mapping) => s"  in model ${model.label}: ${mapping.graphTypeClass} (${mapping.cardinality})"
            }
            throw InternalError(s"Mapping of `$fieldName` has incompatible types:\n${msg.mkString("\n")}")
          }
          fieldName -> firstMapping
      }
      .foreach {
        case (propertyName, mapping) =>
          addProperty(mgmt, propertyName, mapping).failed.foreach { error =>
            logger.error(s"Unable to add property $propertyName", error)
          }
      }

  def addProperty(model: String, propertyName: String, mapping: Mapping[_, _, _]): Try[Unit] =
    managementTransaction { mgmt =>
      addProperty(mgmt, propertyName, mapping)
    }

  def addProperty(mgmt: JanusGraphManagement, propertyName: String, mapping: Mapping[_, _, _]): Try[Unit] = {
    logger.debug(s"Create property $propertyName of type ${mapping.graphTypeClass} (${mapping.cardinality})")

    val cardinality = mapping.cardinality match {
      case MappingCardinality.single => Cardinality.SINGLE
      case MappingCardinality.option => Cardinality.SINGLE
      case MappingCardinality.list   => Cardinality.LIST
      case MappingCardinality.set    => Cardinality.SET
    }
    logger.trace(s"mgmt.makePropertyKey($propertyName).dataType(${mapping.graphTypeClass.getSimpleName}.class).cardinality($cardinality).make()")
    Option(mgmt.getPropertyKey(propertyName)) match {
      case None =>
        Try {
          mgmt
            .makePropertyKey(propertyName)
            .dataType(mapping.graphTypeClass)
            .cardinality(cardinality)
            .make()
          ()
        }
      case Some(p) =>
        if (p.dataType() == mapping.graphTypeClass && p.cardinality() == cardinality) {
          logger.info(s"Property $propertyName $cardinality:${mapping.graphTypeClass} already exists, ignore it")
          Success(())
        } else
          Failure(
            InternalError(
              s"Property $propertyName exists with incompatible type: $cardinality:${mapping.graphTypeClass} Vs ${p.cardinality()}:${p.dataType()}"
            )
          )
    }
  }

  override def removeProperty(model: String, propertyName: String, usedOnlyByThisModel: Boolean): Try[Unit] =
    if (usedOnlyByThisModel)
      managementTransaction(mgmt => removeProperty(mgmt, propertyName))
    else Success(())

  def removeProperty(mgmt: JanusGraphManagement, propertyName: String): Try[Unit] =
    Try {
      Option(mgmt.getPropertyKey(propertyName)).fold(logger.info(s"Cannot remove the property $propertyName, it doesn't exist")) { prop =>
        val newName = s"propertyName-removed-${System.currentTimeMillis()}"
        logger.info(s"Rename the property $propertyName to $newName")
        mgmt.changeName(prop, newName)
      }
    }

  override def createVertex[V <: Product](graph: Graph, authContext: AuthContext, model: Model.Vertex[V], v: V): V with Entity = {
    val createdVertex = model.create(v)(graph)
    val entity        = DummyEntity(model.label, createdVertex.id(), authContext.userId)
    createdAtMapping.setProperty(createdVertex, "_createdAt", entity._createdAt)
    createdByMapping.setProperty(createdVertex, "_createdBy", entity._createdBy)
    UMapping.string.setProperty(createdVertex, "_label", model.label)
    logger.trace(s"Created vertex is ${Model.printElement(createdVertex)}")
    model.addEntity(v, entity)
  }

  override def createEdge[E <: Product, FROM <: Product, TO <: Product](
      graph: Graph,
      authContext: AuthContext,
      model: Model.Edge[E],
      e: E,
      from: FROM with Entity,
      to: TO with Entity
  ): E with Entity = {
    val edgeMaybe = for {
      f <- graph.V(from._label, from._id).headOption
      t <- graph.V(to._label, to._id).headOption
    } yield {
      val createdEdge = model.create(e, f, t)(graph)
      val entity      = DummyEntity(model.label, createdEdge.id(), authContext.userId)
      createdAtMapping.setProperty(createdEdge, "_createdAt", entity._createdAt)
      createdByMapping.setProperty(createdEdge, "_createdBy", entity._createdBy)
      UMapping.string.setProperty(createdEdge, "_label", model.label)
      logger.trace(s"Create edge ${model.label} from $f to $t: ${Model.printElement(createdEdge)}")
      model.addEntity(e, entity)
    }
    edgeMaybe.getOrElse {
      val error = graph.V(from._label, from._id).headOption.map(_ => "").getOrElse(s"${from._label}:${from._id} not found ") +
        graph.V(to._label, to._id).headOption.map(_ => "").getOrElse(s"${to._label}:${to._id} not found")
      throw InternalError(s"Fail to create edge between ${from._label}:${from._id} and ${to._label}:${to._id}, $error")
    }
  }

  override def labelFilter[D, G, C <: Converter[D, G]](label: String, traversal: Traversal[D, G, C]): Traversal[D, G, C] =
    traversal.onRaw(_.hasLabel(label).has("_label", label))

  override def mapPredicate[T](predicate: P[T]): P[T] =
    predicate.getBiPredicate match {
      case Text.containing    => JanusText.textContainsRegex(s".*${predicate.getValue}.*").asInstanceOf[P[T]]
      case Text.notContaining => JanusText.textContainsRegex(s".*${predicate.getValue}.*").negate().asInstanceOf[P[T]]
      //      case Text.endingWith      => JanusText.textRegex(s"${predicate.getValue}.*")
      //      case Text.notEndingWith   => JanusText.textRegex(s"${predicate.getValue}.*").negate()
      case Text.startingWith    => JanusText.textPrefix(predicate.getValue)
      case Text.notStartingWith => JanusText.textPrefix(predicate.getValue).negate()
      case _                    => predicate
    }

  override def V[D <: Product](ids: EntityId*)(implicit model: Model.Vertex[D], graph: Graph): Traversal.V[D] =
    new Traversal[D with Entity, Vertex, Converter[D with Entity, Vertex]](
      graph,
      traversal()
        .V(ids.map(_.value): _*)
        .hasLabel(model.label)
        .has("_label", model.label),
      model.converter
    )

  override def E[D <: Product](ids: EntityId*)(implicit model: Model.Edge[D], graph: Graph): Traversal.E[D] =
    new Traversal[D with Entity, Edge, Converter[D with Entity, Edge]](
      graph,
      traversal()
        .E(ids.map(_.value): _*)
        .hasLabel(model.label)
        .has("_label", model.label),
      model.converter
    )

  override def V(label: String, ids: EntityId*)(implicit graph: Graph): Traversal[Vertex, Vertex, Converter.Identity[Vertex]] =
    new Traversal[Vertex, Vertex, Converter.Identity[Vertex]](
      graph,
      traversal()
        .V(ids.map(_.value): _*)
        .hasLabel(label)
        .has("_label", label),
      Converter.identity[Vertex]
    )

  override def E(label: String, ids: EntityId*)(implicit graph: Graph): Traversal[Edge, Edge, Converter.Identity[Edge]] =
    new Traversal[Edge, Edge, Converter.Identity[Edge]](
      graph,
      traversal()
        .E(ids.map(_.value): _*)
        .hasLabel(label)
        .has("_label", label),
      Converter.identity[Edge]
    )

  override def traversal()(implicit graph: Graph): GraphTraversalSource =
    graph
      .underlying
      .traversal()
      .asInstanceOf[TraversalSource]
      .withoutStrategies(classOf[JanusGraphStepStrategy])
      .withStrategies(IndexOptimizerStrategy.instance(), JanusGraphAcceptNullStrategy.instance(), OrderAcceptNullStrategy.instance())
      .asInstanceOf[GraphTraversalSource]

  override def toId(id: Any): JLong = id.toString.toLong

  override def drop(): Unit = JanusGraphFactory.drop(janusGraph)
}
