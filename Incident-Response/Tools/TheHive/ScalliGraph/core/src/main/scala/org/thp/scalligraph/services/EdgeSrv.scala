package org.thp.scalligraph.services

import org.apache.tinkerpop.gremlin.structure.Edge
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models._
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph, Traversal}
import org.thp.scalligraph.{EntityId, EntityIdOrName, NotFoundError}

import scala.util.{Failure, Success, Try}

class EdgeSrv[E <: Product, FROM <: Product, TO <: Product](implicit val model: Model.Edge[E]) extends ElementSrv[E, Edge] {
  override def startTraversal(implicit graph: Graph): Traversal[E with Entity, Edge, Converter[E with Entity, Edge]] =
    graph.E[E]()(model)

//  override def startTraversal(strategy: GraphStrategy)(implicit graph: Graph): Traversal.E[E] =
//    filterTraversal(Traversal.strategedE(strategy))

  override def getByIds(ids: EntityId*)(implicit graph: Graph): Traversal.E[E] =
    if (ids.isEmpty) graph.empty
    else graph.E[E](ids: _*)(model)

  def getOrFail(idOrName: EntityIdOrName)(implicit graph: Graph): Try[E with Entity] =
    get(idOrName)
      .headOption
      .fold[Try[E with Entity]](Failure(NotFoundError(s"${model.label} $idOrName not found")))(Success.apply)

  def get(edge: Edge)(implicit graph: Graph): Traversal[E with Entity, Edge, Converter[E with Entity, Edge]] =
    graph.E[E](EntityId(edge.id()))(model)

  def getOrFail(edge: Edge)(implicit graph: Graph): Try[E with Entity] =
    get(edge)
      .headOption
      .fold[Try[E with Entity]](Failure(NotFoundError(s"${model.label} ${edge.id()} not found")))(Success.apply)

  def create(e: E, from: FROM with Entity, to: TO with Entity)(implicit graph: Graph, authContext: AuthContext): Try[E with Entity] =
    Try(graph.db.createEdge[E, FROM, TO](graph, authContext, model.asInstanceOf[Model.Edge[E]], e, from, to))
}
