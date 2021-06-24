package org.thp.scalligraph.arangodb
import com.typesafe.config.ConfigFactory
import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.models._
import org.thp.scalligraph.utils.Config
import play.api.Configuration

import scala.util.Random

object ArangoDatabase {
  def randomName           = new String(Array.fill(10)(('A' + Random.nextInt(26)).toChar))
  val defaultConfiguration = Configuration(ConfigFactory.parseString(s"""
                                                                        |gremlin.arangodb.conf.graph.db: scalligraph
                                                                        |gremlin.arangodb.conf.graph.name: $randomName
                                                                        |gremlin.arangodb.conf.arangodb.password: gremlin
                                                                        |gremlin.arangodb.conf.arangodb.user: gremlin
                                                                        |gremlin.arangodb.conf.arangodb.hosts: "127.0.0.1:8529"
                                                                        |gremlin.arangodb.conf.graph.vertex: vertex
                                                                        |gremlin.arangodb.conf.graph.edge: edge
                                                                        |gremlin.arangodb.conf.graph.relation: []
                                                                        |#gremlin.arangodb.conf.graph.timeout:
                                                                        |#gremlin.arangodb.conf.graph.usessl:
                                                                        |#gremlin.arangodb.conf.graph.chunksize:
                                                                        |#gremlin.arangodb.conf.graph.connections.max:
                                                                        |#gremlin.arangodb.conf.graph.connections.ttl:
                                                                        |#gremlin.arangodb.conf.graph.acquireHostList:
                                                                        |#gremlin.arangodb.conf.graph.loadBalancingStrategy:
                                                                        |#gremlin.arangodb.conf.graph.protocol:
   """.stripMargin))

  def getGraph(configuration: Configuration, schema: Schema): ArangoDBGraph = {
    val vertexNames = schema.modelList.collect {
      case vm: VertexModel => vm.label
    }
    val edgeNames = schema.modelList.collect {
      case em: EdgeModel[_, _] => em.label
    }
    val relations = for {
      em        <- schema.modelList.collect { case em: EdgeModel[_, _] => em }
      fromLabel <- if (em.fromLabel.isEmpty) vertexNames else Seq(em.fromLabel)
      toLabel   <- if (em.toLabel.isEmpty) vertexNames else Seq(em.toLabel)
      edgeLabelPrefix = if (em.fromLabel.isEmpty) s"$fromLabel-" else ""
      edgeLabelSuffix = if (em.toLabel.isEmpty) s"-$toLabel" else ""
    } yield s"$edgeLabelPrefix${em.label}$edgeLabelSuffix:$fromLabel->$toLabel"

    val schemaConfig = Configuration.from(
      Map(
        "gremlin.arangodb.conf.graph.vertex"   -> vertexNames,
        "gremlin.arangodb.conf.graph.edge"     -> edgeNames,
        "gremlin.arangodb.conf.graph.relation" -> relations
      )
    )
    new ArangoDBGraph(new Config(defaultConfiguration ++ configuration ++ schemaConfig))
  }
}

@Singleton
class ArangoDatabase @Inject()(configuration: Configuration) extends BaseDatabase {
  private var graph = new ArangoDBGraph(new Config(ArangoDatabase.defaultConfiguration ++ configuration))

  override def createSchema(models: Seq[Model]): Unit = {
    val vertexNames = models.collect {
      case vm: VertexModel => vm.label
    }
    val edgeNames = models.collect {
      case em: EdgeModel[_, _] => em.label
    }
    val relations = for {
      em <- models.collect { case em: EdgeModel[_, _] => em }
      fromLabel = if (em.fromLabel.isEmpty) vertexNames.mkString(",") else em.fromLabel
      toLabel   = if (em.toLabel.isEmpty) vertexNames.mkString(",") else em.toLabel
    } yield s"${em.label}:$fromLabel->$toLabel"

    val schemaConfig = Configuration.from(
      Map(
        "gremlin.arangodb.conf.graph.vertex"   -> vertexNames,
        "gremlin.arangodb.conf.graph.edge"     -> edgeNames,
        "gremlin.arangodb.conf.graph.relation" -> relations
      )
    )
    graph = new ArangoDBGraph(new Config(ArangoDatabase.defaultConfiguration ++ configuration ++ schemaConfig))
  }

  override def noTransaction[A](body: Graph => A): A = body(graph)
  override def transaction[A](body: Graph => A): A   = noTransaction(body)
  override def drop(): Unit = {
    graph.getClient.deleteGraph(graph.name())
    ()
  }
}
