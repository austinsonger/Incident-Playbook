package org.thp.scalligraph.janus

import org.apache.tinkerpop.gremlin.structure.{Edge, Element, Vertex}
import org.janusgraph.core.schema.JanusGraphManagement.IndexJobFuture
import org.janusgraph.core.schema.{JanusGraphManagement, Parameter, SchemaAction, SchemaStatus, Mapping => JanusMapping}
import org.janusgraph.graphdb.database.management.ManagementSystem
import org.janusgraph.graphdb.types.ParameterType
import org.thp.scalligraph.models.{IndexType, Model, VertexModel}
import org.thp.scalligraph.{InternalError, RichSeq}

import java.util.regex.Pattern
import scala.annotation.tailrec
import scala.collection.JavaConverters._
import scala.util.{Failure, Success, Try}

trait IndexOps {
  _: JanusDatabase =>
  @tailrec
  private def showIndexProgress(jobId: String, job: IndexJobFuture): Unit =
    if (job.isCancelled)
      logger.warn(s"Reindex job $jobId has been cancelled")
    else if (job.isDone)
      logger.info(s"Reindex job $jobId is finished")
    else {
      logger.info(s"Reindex job $jobId is running")
      Thread.sleep(1000)
      showIndexProgress(jobId, job)
    }

  def listIndexesWithStatus(status: SchemaStatus): Try[Iterable[String]] =
    managementTransaction { mgmt => // wait for the index to become available
      Try {
        (mgmt.getGraphIndexes(classOf[Vertex]).asScala ++ mgmt.getGraphIndexes(classOf[Edge]).asScala).collect {
          case index if index.getFieldKeys.map(index.getIndexStatus).contains(status) => index.name()
        }
      }
    }

  private def waitRegistration(indexName: String): Unit =
    scala.concurrent.blocking {
      logger.info(s"Wait for the index $indexName to become available")
      ManagementSystem.awaitGraphIndexStatus(janusGraph, indexName).status(SchemaStatus.REGISTERED, SchemaStatus.ENABLED).call()
      ()
    }

  private def forceRegistration(indexName: String): Try[Unit] =
    managementTransaction { mgmt =>
      Try {
        logger.info(s"Force registration of index $indexName")
        val index = mgmt.getGraphIndex(indexName)
        scala.concurrent.blocking {
          mgmt.updateIndex(index, SchemaAction.REGISTER_INDEX).get()
        }
        ()
      }
    }

  private def reindex(indexName: String): Try[Unit] =
    managementTransaction { mgmt => // enable index by reindexing the existing data
      Try {
        val index = mgmt.getGraphIndex(indexName)
        scala.concurrent.blocking {
          val job   = mgmt.updateIndex(index, SchemaAction.REINDEX)
          val jobId = f"${System.identityHashCode(job)}%08x"
          logger.info(s"Reindex data for $indexName (job: $jobId)")
          showIndexProgress(jobId, job)
        }
      }
    }

  override def reindexData(model: String): Try[Unit] = {
    logger.info(s"Reindex data of model $model")
    for {
      indexList <- listIndexesWithStatus(SchemaStatus.ENABLED)
      _         <- indexList.filter(_.startsWith(model)).toTry(reindex)
    } yield ()
  }

  override def rebuildIndexes(): Unit = {
    listIndexesWithStatus(SchemaStatus.ENABLED)
      .foreach(_.foreach(reindex))
    ()
  }

  private def enableIndexes(): Try[Unit] =
    for {
      installedIndexes <- listIndexesWithStatus(SchemaStatus.INSTALLED)
      _ = installedIndexes.foreach(waitRegistration)
      blockedIndexes <- listIndexesWithStatus(SchemaStatus.INSTALLED)
      _ = blockedIndexes.foreach(forceRegistration)
      registeredIndexes <- listIndexesWithStatus(SchemaStatus.REGISTERED)
      _ = registeredIndexes.foreach(reindex)
    } yield ()

  override def addIndex(model: String, indexDefinition: Seq[(IndexType.Value, Seq[String])]): Try[Unit] =
    managementTransaction { mgmt =>
      Option(mgmt.getVertexLabel(model))
        .map(_ => classOf[Vertex])
        .orElse(Option(mgmt.getEdgeLabel(model)).map(_ => classOf[Edge]))
        .fold[Try[Unit]](Failure(InternalError(s"Model $model not found"))) { elementClass =>
          createIndex(mgmt, elementClass, indexDefinition.map(i => (model, i._1, i._2)))
          Success(())
        }
    }

  /**
    * Find the available index name for the specified index base name. If this index is already present and not disable, return None
    *
    * @param mgmt          JanusGraph management
    * @param baseIndexName Base index name
    * @return the available index name or Right if index is present
    */
  private def findFirstAvailableCompositeIndex(mgmt: JanusGraphManagement, baseIndexName: String): Either[String, String] = {
    val indexNamePattern: Pattern = s"$baseIndexName(?:_\\p{Digit}+)?".r.pattern
    val availableIndexes = (mgmt.getGraphIndexes(classOf[Vertex]).asScala ++ mgmt.getGraphIndexes(classOf[Edge]).asScala).filter(i =>
      i.isCompositeIndex && indexNamePattern.matcher(i.name()).matches()
    )
    if (availableIndexes.isEmpty) Left(baseIndexName)
    else
      availableIndexes
        .find(index => !index.getFieldKeys.map(index.getIndexStatus).contains(SchemaStatus.DISABLED))
        .fold[Either[String, String]] {
          val lastIndex = availableIndexes.map(_.name()).toSeq.max
          val version   = lastIndex.drop(baseIndexName.length)
          if (version.isEmpty) Left(s"${baseIndexName}_1")
          else Left(s"${baseIndexName}_${version.tail.toInt + 1}")
        }(index => Right(index.name()))
  }

  /**
    * Find the available index name for the specified index base name. If this index is already present and not disable, return None
    *
    * @param mgmt          JanusGraph management
    * @param baseIndexName Base index name
    * @return the available index name or Right if index is present
    */
  protected def findFirstAvailableMixedIndex(mgmt: JanusGraphManagement, baseIndexName: String): Either[String, String] = {
    val validBaseIndexName        = baseIndexName.replaceAll("[^\\p{Alnum}]", baseIndexName)
    val indexNamePattern: Pattern = s"$validBaseIndexName(?:\\p{Digit}+)?".r.pattern
    val availableIndexes = (mgmt.getGraphIndexes(classOf[Vertex]).asScala ++ mgmt.getGraphIndexes(classOf[Edge]).asScala).filter(i =>
      i.isMixedIndex && indexNamePattern.matcher(i.name()).matches()
    )
    if (availableIndexes.isEmpty) Left(baseIndexName)
    else
      availableIndexes
        .find(index => !index.getFieldKeys.map(index.getIndexStatus).contains(SchemaStatus.DISABLED))
        .fold[Either[String, String]] {
          val lastIndex = availableIndexes.map(_.name()).toSeq.max
          val version   = lastIndex.drop(baseIndexName.length)
          if (version.isEmpty) Left(s"${baseIndexName}1")
          else Left(s"$baseIndexName${version.toInt + 1}")
        }(index => Right(index.name()))
  }

  private def createMixedIndex(
      mgmt: JanusGraphManagement,
      elementClass: Class[_ <: Element],
      indexDefinitions: Seq[(String, IndexType.Value, Seq[String])]
  ): Unit = {
    def getPropertyKey(name: String) = Option(mgmt.getPropertyKey(name)).getOrElse(throw InternalError(s"Property $name doesn't exist"))

    // check if a property hasn't different index types
    val groupedIndex: Map[String, Seq[IndexType.Value]] = indexDefinitions
      .flatMap {
        case (_, IndexType.basic, props) => props.map(_ -> IndexType.standard)
        case (_, IndexType.unique, _)    => Nil
        case (_, indexType, props)       => props.map(_ -> indexType)
      }
      .groupBy(_._1)
      .filterKeys(!_.startsWith("_"))
      .mapValues(_.map(_._2).distinct) ++ Seq(
      "_label"     -> Seq(IndexType.standard),
      "_createdAt" -> Seq(IndexType.standard),
      "_createdBy" -> Seq(IndexType.standard),
      "_updatedAt" -> Seq(IndexType.standard),
      "_updatedBy" -> Seq(IndexType.standard)
    )

    findFirstAvailableMixedIndex(mgmt, "global") match {
      case Left(indexName) =>
        logger.debug(s"Creating index on fields $indexName")

        val index = mgmt.buildIndex(indexName, elementClass) //.indexOnly(elementLabel)
        groupedIndex.foreach {
          case (p, Seq(IndexType.fulltextOnly)) =>
            index.addKey(getPropertyKey(p), JanusMapping.TEXT.asParameter(), Parameter.of(ParameterType.customParameterName("fielddata"), true))
          case (p, Seq(IndexType.standard)) =>
            val prop = getPropertyKey(p)
            if (prop.dataType() == classOf[String]) index.addKey(prop, JanusMapping.STRING.asParameter())
            else index.addKey(prop, JanusMapping.DEFAULT.asParameter())
          // otherwise: IndexType.fulltext of multiple index types
          case (p, _) =>
            index.addKey(getPropertyKey(p), JanusMapping.TEXTSTRING.asParameter(), Parameter.of(ParameterType.customParameterName("fielddata"), true))
        }
        index.buildMixedIndex("search")
        ()
      case Right(indexName) =>
        val index           = mgmt.getGraphIndex(indexName)
        val indexProperties = index.getFieldKeys.map(_.name())

        groupedIndex
          .flatMap {
            case (prop, indexType) if !indexProperties.contains(prop) => Option(getPropertyKey(prop)).map(_ -> indexType)
            case _                                                    => None
          }
          .foreach {
            case (p, Seq(IndexType.fulltextOnly)) =>
              logger.debug(s"Add full-text only index on property ${p.name()}:${p.dataType().getSimpleName} (${p.cardinality()})")
              mgmt.addIndexKey(index, p, JanusMapping.TEXT.asParameter())
            case (p, Seq(IndexType.standard)) =>
              logger.debug(s"Add index on property ${p.name()}:${p.dataType().getSimpleName} (${p.cardinality()})")
              if (p.dataType() == classOf[String]) mgmt.addIndexKey(index, p, JanusMapping.STRING.asParameter())
              else mgmt.addIndexKey(index, p, JanusMapping.DEFAULT.asParameter())
            // otherwise: IndexType.fulltext of multiple index types
            case (p, _) =>
              logger.debug(s"Add full-tex index on property ${p.name()}:${p.dataType().getSimpleName} (${p.cardinality()})")
              mgmt.addIndexKey(index, p, JanusMapping.TEXTSTRING.asParameter())
          }
    }
  }

  private def createIndex(
      mgmt: JanusGraphManagement,
      elementClass: Class[_ <: Element],
      indexDefinitions: Seq[(String, IndexType.Value, Seq[String])]
  ): Unit = {

    def getPropertyKey(name: String) = Option(mgmt.getPropertyKey(name)).getOrElse(throw InternalError(s"Property $name doesnt exist"))

    val labelProperty = getPropertyKey("_label")

    val (mixedIndexes, compositeIndexes) =
      indexDefinitions.partition(i => i._2 != IndexType.unique)
    if (mixedIndexes.nonEmpty)
      if (fullTextIndexAvailable) createMixedIndex(mgmt, elementClass, indexDefinitions)
      else logger.warn(s"Mixed index is not available.")
    compositeIndexes.foreach {
      case (label, indexType, properties) =>
        val elementLabel  = mgmt.getVertexLabel(label)
        val baseIndexName = (label +: properties).map(_.replaceAll("[^\\p{Alnum}]", "").toLowerCase().capitalize).mkString
        findFirstAvailableCompositeIndex(mgmt, baseIndexName).left.foreach { indexName =>
          val index = mgmt.buildIndex(indexName, elementClass).indexOnly(elementLabel)
          index.addKey(labelProperty)
          properties.foreach(p => index.addKey(getPropertyKey(p)))
          if (indexType == IndexType.unique) {
            logger.debug(s"Creating unique index on fields $elementLabel:${properties.mkString(",")}")
            index.unique()
          } else logger.debug(s"Creating basic index on fields $elementLabel:${properties.mkString(",")}")
          index.buildCompositeIndex()
        }
    }
  }

  override def addSchemaIndexes(models: Seq[Model]): Try[Unit] =
    managementTransaction { mgmt =>
//      findFirstAvailableCompositeIndex(mgmt, "_label_vertex_index").left.foreach { indexName =>
//      findFirstAvailableMixedIndex(mgmt, "label").left.foreach { indexName =>
//        mgmt
//          .buildIndex(indexName, classOf[Vertex])
//          .addKey(mgmt.getPropertyKey("_label"))
//          .buildMixedIndex("search")
//      }

      val (vertexModels, edgeModels) = models.partition(_.isInstanceOf[VertexModel])
      createIndex(mgmt, classOf[Vertex], vertexModels.flatMap(m => m.indexes.map(i => (m.label, i._1, i._2))))
      createIndex(mgmt, classOf[Edge], edgeModels.flatMap(m => m.indexes.map(i => (m.label, i._1, i._2))))
      Success(())
    }.flatMap(_ => enableIndexes())

  override def removeIndex(model: String, indexType: IndexType.Value, fields: Seq[String]): Try[Unit] =
    managementTransaction { mgmt =>
      val eitherIndex = indexType match {
        case IndexType.basic | IndexType.unique =>
          val baseIndexName =
            if (model == "_label_vertex_index") "_label_vertex_index"
            else (model +: fields).map(_.replaceAll("[^\\p{Alnum}]", "").toLowerCase().capitalize).mkString
          findFirstAvailableCompositeIndex(mgmt, baseIndexName)
        case IndexType.standard | IndexType.fulltext | IndexType.fulltextOnly =>
          findFirstAvailableMixedIndex(mgmt, model)
      }
      Success {
        eitherIndex
          .toOption
          .flatMap(indexName => Option(mgmt.getGraphIndex(indexName)))
          .map { index =>
            mgmt.updateIndex(index, SchemaAction.DISABLE_INDEX).get()
            index.name
          }
      }
    }
      .map {
        case Some(indexName) =>
          scala.concurrent.blocking {
            logger.info(s"Wait for the index $indexName to become disabled")
            ManagementSystem.awaitGraphIndexStatus(janusGraph, indexName).status(SchemaStatus.DISABLED).call()
          }
          ()
        case None =>
      }
}
