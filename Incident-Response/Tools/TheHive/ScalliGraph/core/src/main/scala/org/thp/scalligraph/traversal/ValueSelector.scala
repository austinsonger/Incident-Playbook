package org.thp.scalligraph.traversal

import java.util.{Map => JMap}

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.{__, GraphTraversal}
import org.apache.tinkerpop.gremlin.process.traversal.step.TraversalOptionParent.Pick

class ValueSelector[D, G, C <: Converter[D, G]](traversal: Traversal[D, G, C]) {
  def on[S](f: Traversal[D, G, C] => Traversal[_, S, _]) = new ValueSelectorOn[D, G, C, S, Nothing](traversal, f, Nil)
}

class ValueSelectorOn[D, G, C <: Converter[D, G], S, DD](
    traversal: Traversal[D, G, C],
    on: Traversal[D, G, C] => Traversal[_, S, _],
    options: Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[DD, _, _])]
) {
  private lazy val optionsTraversals: Seq[(Either[Pick, S], GraphTraversal[_, JMap[String, Any]], Converter[DD, Any])] =
    options
      .zipWithIndex
      .map {
        case ((p, t), i) =>
          val nt = t(traversal.start).asInstanceOf[Traversal[DD, Any, Converter[DD, Any]]]
          (
            p,
            __.start().project("chooseIndex", "chooseValue").by(__.start().constant(i)).by(nt.raw).asInstanceOf[GraphTraversal[_, JMap[String, Any]]],
            nt.converter
          )
      }

  def option[OD >: DD, GG, CC <: Converter[OD, GG]](o: S, f: Traversal[D, G, C] => Traversal[OD, GG, CC]) =
    new ValueSelectorOn[D, G, C, S, OD](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[OD, _, _])]] :+ (Right(o) -> f)
    )

  def any[OD >: DD, GG, CC <: Converter[OD, GG]](f: Traversal[D, G, C] => Traversal[OD, GG, CC]) =
    new ValueSelectorOn[D, G, C, S, OD](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[OD, _, _])]] :+ (Left(Pick.any) -> f)
    )

  def none[OD >: DD, GG, CC <: Converter[OD, GG]](f: Traversal[D, G, C] => Traversal[OD, GG, CC]) =
    new ValueSelectorOn[D, G, C, S, OD](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[OD, _, _])]] :+ (Left(Pick.none) -> f)
    )

  private[traversal] def build: Traversal[DD, JMap[String, Any], Converter[DD, JMap[String, Any]]] =
    traversal.onRawMap[DD, JMap[String, Any], Converter[DD, JMap[String, Any]]](gt =>
      optionsTraversals
        .foldLeft(gt.choose(on(traversal.start).raw)) {
          case (acc, (Left(pick), t, _))   => acc.option(pick, t)
          case (acc, (Right(value), t, _)) => acc.option(value, t)
        }
        .asInstanceOf[GraphTraversal[_, JMap[String, Any]]]
    ) { (jmap: JMap[String, Any]) =>
      val index     = jmap.get("chooseIndex").asInstanceOf[Int]
      val converter = optionsTraversals(index)._3
      converter(jmap.get("chooseValue"))
    }
}
