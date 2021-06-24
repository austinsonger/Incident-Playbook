package org.thp.scalligraph.services

import org.apache.tinkerpop.gremlin.structure.Element
import org.thp.scalligraph.models.{Entity, Model}
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph, Traversal}
import org.thp.scalligraph.{EntityId, EntityIdOrName, InternalError}
import play.api.Logger

abstract class ElementSrv[E <: Product, G <: Element] {
  lazy val logger: Logger = Logger(getClass)

  val model: Model.Base[E]

  def startTraversal(implicit graph: Graph): Traversal[E with Entity, G, Converter[E with Entity, G]]

  def filterTraversal(traversal: Traversal[G, G, Converter.Identity[G]]): Traversal[E with Entity, G, Converter[E with Entity, G]] =
    traversal
      .graph
      .db
      .labelFilter(model.label, traversal)
      .setConverter[E with Entity, Converter[E with Entity, G]](model.converter.asInstanceOf[Converter[E with Entity, G]])

  def get(idOrName: EntityIdOrName)(implicit graph: Graph): Traversal[E with Entity, G, Converter[E with Entity, G]] =
    idOrName.fold(getByIds(_), getByName)

  def getByIds(ids: EntityId*)(implicit graph: Graph): Traversal[E with Entity, G, Converter[E with Entity, G]]

  def getByName(name: String)(implicit graph: Graph): Traversal[E with Entity, G, Converter[E with Entity, G]] =
    throw InternalError(s"Entity ${model.label} cannot be retrieve by its name")

  def get(e: Entity)(implicit graph: Graph): Traversal[E with Entity, G, Converter[E with Entity, G]] = getByIds(e._id)

  def count(implicit graph: Graph): Long = startTraversal.getCount
}
