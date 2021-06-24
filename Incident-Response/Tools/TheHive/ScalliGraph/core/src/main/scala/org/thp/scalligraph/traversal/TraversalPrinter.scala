package org.thp.scalligraph.traversal

import org.apache.tinkerpop.gremlin.process.traversal.lambda.{ColumnTraversal, ElementValueTraversal, IdentityTraversal, TokenTraversal}
import org.apache.tinkerpop.gremlin.process.traversal.step.TraversalParent
import org.apache.tinkerpop.gremlin.process.traversal.step.branch.{ChooseStep, OptionalStep, UnionStep}
import org.apache.tinkerpop.gremlin.process.traversal.step.filter.WhereTraversalStep.{WhereEndStep, WhereStartStep}
import org.apache.tinkerpop.gremlin.process.traversal.step.filter._
import org.apache.tinkerpop.gremlin.process.traversal.step.map._
import org.apache.tinkerpop.gremlin.process.traversal.step.sideEffect.{
  AddPropertyStep,
  AggregateStep,
  IdentityStep,
  InjectStep,
  StoreStep,
  TraversalSideEffectStep
}
import org.apache.tinkerpop.gremlin.process.traversal.step.util.ComputerAwareStep.EndStep
import org.apache.tinkerpop.gremlin.process.traversal.{P, Pop, Step, Traversal => TinkerTraversal}
import org.apache.tinkerpop.gremlin.structure.PropertyType

import java.util.{Comparator, Date}
import scala.collection.JavaConverters._
import scala.util.Try

trait TraversalPrinter {

  implicit class TraversalPrinterDefs(traversal: Traversal[_, _, _]) {
    def printGremlin: String = printTraversal(traversal.raw.asAdmin())

    def printByteCode: String = traversal.raw.toString

    def printStrategies: String =
      traversal.raw.asAdmin().getStrategies.toList.asScala.map(_.getClass.getSimpleName).mkString("Strategies: [", ", ", "]")

    def printProfile: String = traversal.clone().raw.profile().next().toString

    def printExplain: String = traversal.raw.explain().toString

    def printTraversal[A, B](traversal: TinkerTraversal.Admin[A, B]): String =
      traversal match {
        case e: ElementValueTraversal[_] => s"""values("${e.getPropertyKey}")"""
        case e: TokenTraversal[_, _]     => s"${e.getToken}"
        case _: IdentityTraversal[_]     => s"identity()"
        case e: ColumnTraversal          => s"${e.getColumn}"
        case t =>
          t.getSteps
            .asScala
            .map(printStep)
            .mkString(".")
//        case other => s"{UNKNOWN:$other}"

      }

    def printStep(step: Step[_, _]): String =
      Try {
        val stepStr: String = step match {
          case s: GraphStep[_, _] =>
            val sb = new StringBuilder
            if (s.returnsVertex()) sb.append("V")
            else if (s.returnsEdge()) sb.append("E")
            else sb.append("???")
            sb.append(s.getIds.map(i => '"' + i.toString + '"').mkString("(", ", ", ")"))
            sb.toString
          case s: HasStep[_] =>
            s.getHasContainers
              .asScala
              .map {
                case hc if hc.getKey == "~label" => s"hasLabel(${printValue(hc.getValue)})"
                case hc                          => s"""has("${hc.getKey}", ${printPredicate(hc.getPredicate)})"""
              }
              .mkString(".")
          case s: VertexStep[_] =>
            val sb = new StringBuilder
            sb.append(s.getDirection.toString.toLowerCase)
            if (s.returnsEdge()) sb.append("E")
            sb.append(s"(${s.getEdgeLabels.map('"' + _ + '"').mkString(", ")})")
            sb.toString
          case s: EdgeVertexStep         => s"${s.getDirection.toString.toLowerCase}V()"
          case s: TraversalFilterStep[_] => s"filter(${printLocalChildren(s)})"
          case s: WherePredicateStep[_] =>
            val sb = new StringBuilder
            sb.append("where(")
            s.getStartKey.ifPresent(k => sb.append(s"$k, "))
            s.getPredicate.ifPresent(predicate => sb.append(printPredicate(predicate)))
            sb.append(")")
            sb.toString
          case s: WhereTraversalStep[_] => s"where(${printLocalChildren(s)})"
          case s: WhereStartStep[_] =>
            val keys = s.getScopeKeys.asScala
            if (keys.nonEmpty)
              s"__.as(${keys.map('"' + _ + '"').mkString(", ")})"
            else "__"
          case s: WhereEndStep =>
            val keys = s.getScopeKeys.asScala
            if (keys.nonEmpty)
              s"as(${keys.map('"' + _ + '"').mkString(", ")})"
            else ""
          case s: TraversalFlatMapStep[_, _] => s"flatMap(${printLocalChildren(s)})"
          case s: GroupStep[_, _, _]         => s"group()${printChildrenBy(s)}"
          case _: UnfoldStep[_, _]           => "unfold()"
          case _: FoldStep[_, _]             => "fold()"
          case s: TraversalMapStep[_, _] =>
            val subTraversal = s.getLocalChildren.get(0)
            if (subTraversal.isInstanceOf[ColumnTraversal])
              s"select(${printTraversal(subTraversal)})"
            else
              s"map(${printTraversal(subTraversal)})"
          case _: CountLocalStep[_]  => "count()"
          case _: CountGlobalStep[_] => "count()"
          case s: IsStep[_]          => s"is(${printPredicate(s.getPredicate)})"
          case _: IdStep[_]          => "id()"
          case s: ProjectStep[_, _] =>
            s"project(${s.getProjectKeys.asScala.map('"' + _ + '"').mkString(", ")})${s.getLocalChildren.asScala.map(printBy(_, None)).mkString}"
          case s: SelectStep[_, _] =>
            val pop =
              if (s.getPop == Pop.last) ""
              else s"${s.getPop}, "
            val selectEntries = s.getByTraversals.asScala.toSeq
            s"select($pop${selectEntries.map(e => '"' + e._1 + '"').mkString(", ")})${selectEntries.map(e => printBy(e._2, None)).mkString}"
          case s: SelectOneStep[_, _] =>
            val pop =
              if (s.getPop == Pop.last) ""
              else s"${s.getPop}, "
            s"select($pop${s.getScopeKeys.asScala.map('"' + _ + '"').mkString(", ")})${s.getLocalChildren.asScala.map(printBy(_, None)).mkString}"
          case s: StoreStep[_] =>
            s"aggregate(local, ${s.getLabels.asScala.map('"' + _ + '"').mkString(", ")})${s.getLocalChildren.asScala.map(printBy(_, None)).mkString}"
          case s: AggregateStep[_] =>
            s"aggregate(global, ${s.getLabels.asScala.map('"' + _ + '"').mkString(", ")})${s.getLocalChildren.asScala.map(printBy(_, None)).mkString}"
          case s: OrderGlobalStep[_, _] => s"order()${s.getComparators.asScala.map(p => printBy(p.getValue0, Some(p.getValue1))).mkString}"
          case s: PropertiesStep[_] =>
            s.getReturnType match {
              case PropertyType.VALUE    => s"values(${s.getPropertyKeys.map('"' + _ + '"').mkString(", ")})"
              case PropertyType.PROPERTY => s"properties(${s.getPropertyKeys.map('"' + _ + '"').mkString(", ")})"
            }
          case s: DedupGlobalStep[_]         => s"dedup(${s.getScopeKeys.asScala.map('"' + _ + '"').mkString(",")})"
          case s: UnionStep[_, _]            => s"union(${printGlobalChildren(s)})"
          case s: CoalesceStep[_, _]         => s"coalesce(${printLocalChildren(s)})"
          case _: EndStep[_]                 => "identity()"
          case s: OrStep[_]                  => s"or(${printLocalChildren(s)})"
          case s: AndStep[_]                 => s"and(${printLocalChildren(s)})"
          case s: RangeGlobalStep[_]         => s"range(${s.getLowRange}, ${s.getHighRange})"
          case s: GroupCountStep[_, _]       => s"group()${printChildrenBy(s)}"
          case s: ConstantStep[_, _]         => s"constant(${printValue(s.getConstant)})"
          case s: ChooseStep[_, _, _]        => s"choose(${printLocalChildren(s)}, ${printGlobalChildren(s)})"
          case _: HasNextStep[_]             => "identity()"
          case s: NotStep[_]                 => s"not(${printLocalChildren(s)})"
          case _: LabelStep[_]               => "label()"
          case _: IdentityStep[_]            => "identity()"
          case s: AddPropertyStep[_]         => s"property(${s.getParameters.toString})"
          case _: EdgeOtherVertexStep        => "otherV()"
          case s: InjectStep[_]              => s"inject(${s.getInjections.mkString(",")})"
          case s: OptionalStep[_]            => s"optional(${printLocalChildren(s)})"
          case s: PropertyMapStep[_, _]      => s"valueMap(${s.getPropertyKeys().mkString(",")})"
          case s: TraversalSideEffectStep[_] => s"sideEffect(${printLocalChildren(s)})"
          case s: DropStep[_]                => "remove()"
          case other                         => s"{UNKNOWN:$other}"
        }
        val labels = step.getLabels.asScala
        if (labels.nonEmpty)
          s"$stepStr.as(${labels.map('"' + _ + '"').mkString(", ")})"
        else
          stepStr
      }.getOrElse(s"{UNKNOWN-FAIL:$step}")

    def printLocalChildren(step: TraversalParent): String =
      step.getLocalChildren.asScala.map(c => s"__.${printTraversal(c)}").mkString(", ")
    def printGlobalChildren(step: TraversalParent): String =
      step.getGlobalChildren.asScala.map(c => s"__.${printTraversal(c)}").mkString(", ")
    def printChildrenBy(step: TraversalParent): String =
      step.getLocalChildren.asScala.map(printBy(_, None)).mkString(", ")

    def printBy[A, B, C](traversal: TinkerTraversal.Admin[A, B], comparator: Option[Comparator[C]]): String = {
      val cmpStr = comparator.fold("")(c => s", $c")
      traversal match {
        case e: ElementValueTraversal[_] => s""".by("${e.getPropertyKey}"$cmpStr)"""
        case e: TokenTraversal[_, _]     => s".by(${e.getToken}$cmpStr)"
        case _: IdentityTraversal[_]     => s".by(${comparator.getOrElse("")})"
        case e: ColumnTraversal          => s".by(${e.getColumn}$cmpStr)"
        case t                           => s".by(__.${printTraversal(t)}$cmpStr)"
      }
    }

    def printPredicate(predicate: P[_]): String =
      s"P.${predicate.getBiPredicate}(${printValue(predicate.getValue)})"

    def printValue(value: Any): String =
      value match {
        case s: String          => '"' + s + '"'
        case d: Date            => s"new Date(${d.getTime})"
        case v if v == NO_VALUE => """"<NO_VALUE>"""""
        case null               => "null"
        case other              => other.toString
      }
  }

}
