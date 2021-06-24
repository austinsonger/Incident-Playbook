package org.thp.scalligraph.traversal

import java.util.{UUID, List => JList}

import org.apache.tinkerpop.gremlin.structure.{Edge, Vertex}
import org.thp.scalligraph.InternalError
import org.thp.scalligraph.models.{Entity, Model}

class StepLabel[D, G, C <: Converter[D, G]](private var _converter: Option[C]) {
  def this() = this(None)
  def this(converter: C) = this(Some(converter))
  val name: String = UUID.randomUUID().toString

  def converter: C                = _converter.getOrElse(throw InternalError(s"StepLabel $name is use before set"))
  def setConverter(conv: C): Unit = _converter = Some(conv)
}

object StepLabel {
  def apply[D, G, C <: Converter[D, G]]: StepLabel[D, G, C] = new StepLabel[D, G, C]
  def v[V <: Product](implicit model: Model.Vertex[V]): StepLabel[V with Entity, Vertex, Converter[V with Entity, Vertex]] =
    new StepLabel[V with Entity, Vertex, Converter[V with Entity, Vertex]](model.converter)
  def vs[V <: Product](
      implicit model: Model.Vertex[V]
  ): StepLabel[Seq[V with Entity], JList[Vertex], Converter.CList[V with Entity, Vertex, Converter[V with Entity, Vertex]]] =
    new StepLabel[Seq[V with Entity], JList[Vertex], Converter.CList[V with Entity, Vertex, Converter[V with Entity, Vertex]]](
      Converter.clist[V with Entity, Vertex, Converter[V with Entity, Vertex]](model.converter)
    )
  def e[E <: Product](implicit model: Model.Edge[E]): StepLabel[E with Entity, Edge, Converter[E with Entity, Edge]] =
    new StepLabel[E with Entity, Edge, Converter[E with Entity, Edge]](model.converter)
  def identity[E]: StepLabel[E, E, Converter.Identity[E]] = new StepLabel[E, E, IdentityConverter[E]](Converter.identity[E])
}
