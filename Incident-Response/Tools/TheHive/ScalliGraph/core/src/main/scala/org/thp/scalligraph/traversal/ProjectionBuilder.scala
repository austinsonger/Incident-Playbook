package org.thp.scalligraph.traversal

import java.util.{UUID, Map => JMap}

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal
import org.apache.tinkerpop.gremlin.structure.Element
import org.thp.scalligraph.`macro`.TraversalMacro
import org.thp.scalligraph.models.{Entity, Mapping}
import shapeless.ops.tuple.Prepend
import shapeless.syntax.std.tuple._

import scala.language.experimental.macros

class ProjectionBuilder[E <: Product, D, G, C <: Converter[D, G]](
    traversal: Traversal[D, G, C],
    labels: Seq[String],
    addBy: GraphTraversal[_, JMap[String, Any]] => GraphTraversal[_, JMap[String, Any]],
    buildResult: JMap[String, Any] => E
) {
  //  def apply[U, TR <: Product](by: By[U])(implicit prepend: Prepend.Aux[E, Tuple1[U], TR]): ProjectionBuilder[TR, T] = {
  //    val label = UUID.randomUUID().toString
  //    new ProjectionBuilder[TR, T](traversal, labels :+ label, addBy.andThen(by.apply), map => buildResult(map) :+ map.get(label).asInstanceOf[U])
  //  }

  def by[TR <: Product](implicit prepend: Prepend.Aux[E, Tuple1[D], TR]): ProjectionBuilder[TR, D, G, C] = {
    val label = UUID.randomUUID().toString
    new ProjectionBuilder[TR, D, G, C](
      traversal,
      labels :+ label,
      addBy.andThen(_.by),
      map => buildResult(map) :+ traversal.converter(map.get(label).asInstanceOf[G])
    )
  }

  //  def by[U, TR <: Product](key: Key[U])(implicit prepend: Prepend.Aux[E, Tuple1[U], TR]): ProjectionBuilder[TR, D, G] = {
  //    val label = UUID.randomUUID().toString
  //    new ProjectionBuilder[TR, D, G](
  //      traversal,
  //      labels :+ label,
  //      addBy.andThen(_.by(key.name)),
  //      map => buildResult(map) :+ map.get(label).asInstanceOf[U]
  //    )
  //  }
  def byValue[DD, DU, TR <: Product](
      selector: D => DD
  )(implicit
      mapping: Mapping[DD, DU, _],
      ev1: D <:< Product with Entity,
      ev2: G <:< Element,
      prepend: Prepend.Aux[E, Tuple1[DU], TR]
  ): ProjectionBuilder[TR, D, G, C] = macro TraversalMacro.projectionBuilderByValue[DD, DU, TR]

  def _byValue[DD, GG, TR <: Product](name: String, converter: Converter[DD, GG])(implicit
      prepend: Prepend.Aux[E, Tuple1[DD], TR]
  ): ProjectionBuilder[TR, D, G, C] = {
    val label = UUID.randomUUID().toString
    new ProjectionBuilder[TR, D, G, C](
      traversal,
      labels :+ label,
      addBy.andThen(_.by(name)),
      map => buildResult(map) :+ converter(map.get(label).asInstanceOf[GG])
    )
  }

  def by[DD, GG, TR <: Product](
      f: Traversal[D, G, C] => Traversal[DD, GG, _]
  )(implicit prepend: Prepend.Aux[E, Tuple1[DD], TR]): ProjectionBuilder[TR, D, G, C] = {
    val label = UUID.randomUUID().toString
    val p     = f(traversal.start).asInstanceOf[Traversal[DD, GG, Converter[DD, GG]]]
    new ProjectionBuilder[TR, D, G, C](
      traversal,
      labels :+ label,
      addBy.andThen(_.by(p.raw)),
      map => buildResult(map) :+ p.converter.asInstanceOf[Converter[DD, GG]](map.get(label).asInstanceOf[GG])
    )
  }

  private[traversal] def traversal(g: GraphTraversal[_, _]): GraphTraversal[_, JMap[String, Any]] = addBy(g.project(labels.head, labels.tail: _*))
  private[traversal] def converter: Converter[E, JMap[String, Any]]                               = buildResult(_)
}
