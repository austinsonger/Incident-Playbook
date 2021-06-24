package org.thp.scalligraph.traversal

import org.apache.tinkerpop.gremlin.process.traversal.Traverser
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.{__, DefaultGraphTraversal, GraphTraversal}
import org.apache.tinkerpop.gremlin.structure.{Edge, Vertex}
import org.thp.scalligraph.models.Entity

import scala.language.existentials

object Traversal {
  type Identity[T] = Traversal[T, T, Converter.Identity[T]]
  type V[T]        = Traversal[T with Entity, Vertex, Converter[T with Entity, Vertex]]
  type E[T]        = Traversal[T with Entity, Edge, Converter[T with Entity, Edge]]
  type Unk         = Traversal[UnkD, UnkG, Converter[UnkD, UnkG]]
  type UnkD        = Any
  type UnkDU       = Any
  type UnkG        = Any

  type Some          = Traversal[D, G, C] forSome { type D; type G; type C <: Converter[D, G] }
  type SomeDomain[D] = Traversal[D, G, C] forSome { type G; type C <: Converter[D, G] }
  type Domain[D]     = Traversal[D, UnkG, Converter[D, UnkG]]
}

class Traversal[+D, G, +C <: Converter[D, G]](val graph: Graph, val raw: GraphTraversal[_, G], val converter: C) {
  def onRaw(f: GraphTraversal[_, G] => GraphTraversal[_, G]): Traversal[D, G, C] =
    new Traversal[D, G, C](graph, f(raw), converter)
  def onRawMap[DD, GG, CC <: Converter[DD, GG]](f: GraphTraversal[_, G] => GraphTraversal[_, GG])(conv: CC): Traversal[DD, GG, CC] =
    new Traversal[DD, GG, CC](graph, f(raw), conv)
  def domainMap[DD](f: D => DD): Traversal[DD, G, Converter[DD, G]] =
    new Traversal[DD, G, Converter[DD, G]](graph, raw, g => converter.andThen(f).apply(g))
  def graphMap[DD, GG, CC <: Converter[DD, GG]](d: G => GG, conv: CC): Traversal[DD, GG, CC] =
    new Traversal[DD, GG, CC](graph, raw.map[GG]((t: Traverser[G]) => d(t.get)), conv)
  def setConverter[DD, CC <: Converter[DD, G]](conv: CC): Traversal[DD, G, CC] = new Traversal[DD, G, CC](graph, raw, conv)
  def start                                                                    = new Traversal[D, G, C](graph, __.start[G](), converter)
  def mapAsNumber(
      f: Traversal[Number, Number, IdentityConverter[Number]] => Traversal[Number, Number, IdentityConverter[Number]]
  ): Traversal[D, G, C] =
    f(this.asInstanceOf[Traversal[Number, Number, IdentityConverter[Number]]]).asInstanceOf[Traversal[D, G, C]]
  def mapAsComparable(f: Traversal[Comparable[_], Comparable[G], _] => Traversal[Comparable[_], Comparable[G], _]): Traversal[D, G, C] =
    f(this.asInstanceOf[Traversal[Comparable[_], Comparable[G], _]]).asInstanceOf[Traversal[D, G, C]]
  override def clone(): Traversal[D, G, C] =
    raw match {
      case dgt: DefaultGraphTraversal[_, G] => new Traversal[D, G, C](graph, dgt.clone, converter)
    }
}
