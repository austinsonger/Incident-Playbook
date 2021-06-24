package org.thp.scalligraph.traversal

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal
import org.apache.tinkerpop.gremlin.process.traversal.step.TraversalOptionParent.Pick

class BranchSelector[D, G, C <: Converter[D, G], GG](traversal: Traversal[D, G, C]) {
  def on[S](f: Traversal[D, G, C] => Traversal[_, S, _]) = new BranchSelectorOn[D, G, C, S, GG](traversal, f, Nil)
}

class BranchSelectorOn[D, G, C <: Converter[D, G], S, GG](
    traversal: Traversal[D, G, C],
    on: Traversal[D, G, C] => Traversal[_, S, _],
    options: Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[_, GG, _])]
) {
  def option(o: S, f: Traversal[D, G, C] => Traversal[_, GG, _]) =
    new BranchSelectorOn[D, G, C, S, GG](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[_, GG, _])]] :+ (Right(o) -> f)
    )

  def any(f: Traversal[D, G, C] => Traversal[_, GG, _]) =
    new BranchSelectorOn[D, G, C, S, GG](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[_, GG, _])]] :+ (Left(Pick.any) -> f)
    )

  def none(f: Traversal[D, G, C] => Traversal[_, GG, _]) =
    new BranchSelectorOn[D, G, C, S, GG](
      traversal,
      on,
      options.asInstanceOf[Seq[(Either[Pick, S], Traversal[D, G, C] => Traversal[_, GG, _])]] :+ (Left(Pick.none) -> f)
    )

  private[traversal] def build: Traversal[GG, GG, IdentityConverter[GG]] =
    traversal.onRawMap[GG, GG, IdentityConverter[GG]](gt =>
      options
        .foldLeft(gt.choose(on(traversal.start).raw)) {
          case (acc, (Left(pick), t))   => acc.option(pick, t(traversal.start).raw)
          case (acc, (Right(value), t)) => acc.option(value, t(traversal.start).raw)
        }
        .asInstanceOf[GraphTraversal[_, GG]]
    )(Converter.identity[GG])
}
