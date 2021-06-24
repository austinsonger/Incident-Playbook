package org.thp.scalligraph.traversal

import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.{__, GraphTraversal}

object MatchElementBuilder {
  def as[FD, FG, FC <: Converter[FD, FG]](fromLabel: StepLabel[FD, FG, FC]): MatchElementAs[FD, FG, FC] =
    new MatchElementAs[FD, FG, FC](fromLabel)
  def dedup /*[FD, FG, FC <: Converter[FD, FG]]*/ (labels: StepLabel[_, _, _]* /*[FD, FG, FC]*/ ): MatchElementDedup =
    new MatchElementDedup(labels.map(_.name))
}

class MatchElementAs[FD, FG, FC <: Converter[FD, FG]](fromLabel: StepLabel[FD, FG, FC]) {
  def apply[TD, TG, TC <: Converter[TD, TG]](f: Traversal[FD, FG, FC] => Traversal[TD, TG, TC]) =
    new MatchElementTraversal[FD, FG, FC, TD, TG, TC](fromLabel, f)
}

class MatchElementTraversal[FD, FG, FC <: Converter[FD, FG], TD, TG, TC <: Converter[TD, TG]](
    fromLabel: StepLabel[FD, FG, FC],
    f: Traversal[FD, FG, FC] => Traversal[TD, TG, TC]
) {
  def as(toLabel: StepLabel[TD, TG, TC]) = new MatchElementTraversalAs[FD, FG, FC, TD, TG, TC](fromLabel, f, toLabel)
}

trait MatchElement {
  private[traversal] def traversal: GraphTraversal[_, _]
}

class MatchElementTraversalAs[FD, FG, FC <: Converter[FD, FG], TD, TG, TC <: Converter[TD, TG]](
    val fromLabel: StepLabel[FD, FG, FC],
    val f: Traversal[FD, FG, FC] => Traversal[TD, TG, TC],
    val toLabel: StepLabel[TD, TG, TC]
) extends MatchElement {

  import TraversalOps._

  private[traversal] def traversal: GraphTraversal[_, _] = f(fromLabel.converter.startTraversal.as(fromLabel)).as(toLabel).raw
}

class MatchElementDedup(labels: Seq[String]) extends MatchElement {
  override private[traversal] def traversal: GraphTraversal[_, _] = __.start().dedup(labels: _*)
}
