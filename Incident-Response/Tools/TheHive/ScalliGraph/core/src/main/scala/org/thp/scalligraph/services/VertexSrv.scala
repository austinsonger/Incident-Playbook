package org.thp.scalligraph.services

import org.apache.tinkerpop.gremlin.structure.Vertex
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models._
import org.thp.scalligraph.query.PropertyUpdater
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph, IdentityConverter, Traversal}
import org.thp.scalligraph.{EntityId, EntityIdOrName, NotFoundError}
import play.api.libs.json.JsObject

import java.util.Date
import scala.util.{Failure, Success, Try}

abstract class VertexSrv[V <: Product](implicit val model: Model.Vertex[V]) extends ElementSrv[V, Vertex] {
  override def startTraversal(implicit graph: Graph): Traversal[V with Entity, Vertex, Converter[V with Entity, Vertex]] =
    graph.V[V]()(model)

//  override def startTraversal(strategy: GraphStrategy)(implicit graph: Graph): Traversal.V[V] =
//    filterTraversal(Traversal.strategedV(strategy))

  override def getByIds(ids: EntityId*)(implicit graph: Graph): Traversal.V[V] =
    if (ids.isEmpty) graph.empty
    else graph.V[V](ids: _*)(model)

  def get(vertex: Vertex)(implicit graph: Graph): Traversal.V[V] =
    graph.V[V](EntityId(vertex.id()))(model)

  def getOrFail(idOrName: EntityIdOrName)(implicit graph: Graph): Try[V with Entity] =
    get(idOrName)
      .headOption
      .fold[Try[V with Entity]](Failure(NotFoundError(s"${model.label} $idOrName not found")))(Success.apply)

  def getOrFail(vertex: Vertex)(implicit graph: Graph): Try[V with Entity] =
    get(vertex)
      .headOption
      .fold[Try[V with Entity]](Failure(NotFoundError(s"${model.label} ${vertex.id()} not found")))(Success.apply)

  def createEntity(e: V)(implicit graph: Graph, authContext: AuthContext): Try[V with Entity] =
    Success(graph.db.createVertex[V](graph, authContext, model, e))

  def exists(e: V)(implicit graph: Graph): Boolean = false

  def update(
      traversalSelect: Traversal[V with Entity, Vertex, Converter[V with Entity, Vertex]] => Traversal[
        V with Entity,
        Vertex,
        Converter[V with Entity, Vertex]
      ],
      propertyUpdaters: Seq[PropertyUpdater]
  )(implicit graph: Graph, authContext: AuthContext): Try[(Traversal.V[V], JsObject)] =
    update(traversalSelect(startTraversal), propertyUpdaters)

  def update(traversal: Traversal.V[V], propertyUpdaters: Seq[PropertyUpdater])(implicit
      graph: Graph,
      authContext: AuthContext
  ): Try[(Traversal[V with Entity, Vertex, Converter[V with Entity, Vertex]], JsObject)] = {
    val myClone = traversal.clone()
    traversal.debug("update")
    traversal
      .setConverter[Vertex, IdentityConverter[Vertex]](Converter.identity)
      .headOption
      .fold[Try[(Traversal.V[V], JsObject)]](Failure(NotFoundError(s"${model.label} not found"))) { vertex =>
        logger.trace(s"Update ${vertex.id()} by ${authContext.userId}")
        propertyUpdaters
          .toTry(u => u(vertex, graph, authContext))
          .map { o =>
            graph.db.updatedAtMapping.setProperty(vertex, "_updatedAt", Some(new Date))
            graph.db.updatedByMapping.setProperty(vertex, "_updatedBy", Some(authContext.userId))
            myClone -> o.reduceOption(_ ++ _).getOrElse(JsObject.empty)
          }
      }
  }

  def delete(e: V with Entity)(implicit graph: Graph, authContext: AuthContext): Try[Unit] =
    Try(get(e).remove())
}
