package org.thp.scalligraph.traversal

import java.util.{Collection => JCollection, Map => JMap}

import org.apache.tinkerpop.gremlin.process.traversal.Order
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.GraphTraversal
import org.apache.tinkerpop.gremlin.structure.{Element, T}
import org.thp.scalligraph.`macro`.TraversalMacro
import org.thp.scalligraph.models.{Entity, Mapping}
import shapeless.PolyDefns.->
import shapeless.ops.tuple.Prepend
import shapeless.{HList, Poly2, :: => :-:}

import scala.language.experimental.macros

class GenericBySelector[D, G, C <: Converter[D, G]](origin: Traversal[D, G, C]) {
  def by: ByResult[G, D, G, C] = ByResult[G, D, G, C](origin.converter)(_.by())

  def byValue[DD, DU, GG](
      selector: D => DD
  )(implicit
      mapping: Mapping[DD, DU, GG],
      ev1: D <:< Product with Entity,
      ev2: G <:< Element
  ): ByResult[G, DU, GG, Converter[DU, GG]] = macro TraversalMacro.genericSelectorByValue[G, DD, DU, GG]

  def byLabel(implicit ev: G <:< Element): ByResult[G, String, String, Converter.Identity[String]] =
    ByResult[G, String, String, Converter.Identity[String]](Converter.identity)(_.by(T.label).asInstanceOf[GraphTraversal[_, String]])

  def byId(implicit ev: G <:< Element): ByResult[G, String, AnyRef, Converter[String, AnyRef]] =
    ByResult[G, String, AnyRef, Converter[String, AnyRef]](Converter.cid)(_.by(T.id).asInstanceOf[GraphTraversal[_, AnyRef]])

  //    ByResult[G, DD, GG, CC](Converter.identity[String])(_.as(stepLabel.name).asInstanceOf[GraphTraversal[_, GG]])
  def by[DD, GG, CC <: Converter[DD, GG]](f: Traversal[D, G, C] => Traversal[DD, GG, CC]): ByResult[G, DD, GG, CC] = {
    val x = f(origin.start)
    ByResult[G, DD, GG, CC](x.converter)(_.by(x.raw).asInstanceOf[GraphTraversal[_, GG]])
  }
}

class GroupBySelector[D, G, C <: Converter[D, G]](origin: Traversal[D, G, C]) {
  def by: ByResult[G, D, G, C] = ByResult[G, D, G, C](origin.converter)(_.by())

  def byValue[DD, DU, GG](
      selector: D => DD
  )(implicit
      mapping: Mapping[DD, DU, GG],
      ev1: D <:< Product with Entity,
      ev2: G <:< Element
  ): ByResult[G, Seq[DU], JCollection[GG], Converter.CCollection[DU, GG, _ <: Converter[DU, GG]]] =
    macro TraversalMacro.groupBySelectorByValue[G, DD, DU, GG]

  def byLabel(implicit ev: G <:< Element): ByResult[G, String, String, Converter.Identity[String]] =
    ByResult[G, String, String, Converter.Identity[String]](Converter.identity)(_.by(T.label).asInstanceOf[GraphTraversal[_, String]])

  def byId(implicit ev: G <:< Element): ByResult[G, String, AnyRef, Converter[String, AnyRef]] =
    ByResult[G, String, AnyRef, Converter[String, AnyRef]](Converter.cid)(_.by(T.id).asInstanceOf[GraphTraversal[_, AnyRef]])

  //    ByResult[G, DD, GG, CC](Converter.identity[String])(_.as(stepLabel.name).asInstanceOf[GraphTraversal[_, GG]])
  def by[DD, GG, CC <: Converter[DD, GG]](f: Traversal[D, G, C] => Traversal[DD, GG, CC]): ByResult[G, DD, GG, CC] = {
    val x = f(origin.start)
    ByResult[G, DD, GG, CC](x.converter)(_.by(x.raw).asInstanceOf[GraphTraversal[_, GG]])
  }
}

class SelectBySelector[S](
    val labels: List[String],
    val addBys: GraphTraversal[_, JMap[String, Any]] => GraphTraversal[_, JMap[String, Any]],
    val converter: JMap[String, Any] => S
) {
  def apply[D, G, C <: Converter[D, G], DD, GG, CC <: Converter[DD, GG], TR](label: StepLabel[D, G, C])(
      by: GenericBySelector[D, G, C] => ByResult[G, DD, GG, CC]
  )(implicit prepend: Prepend.Aux[S, Tuple1[DD], TR]): SelectBySelector[TR] = {
    val byResult = by(new GenericBySelector[D, G, C](label.converter.startTraversal))

    new SelectBySelector(
      labels :+ label.name,
      addBys.andThen(byResult.asInstanceOf[ByResult[JMap[String, Any], DD, JMap[String, Any], Converter[DD, JMap[String, Any]]]]),
      jmap =>
        prepend(
          converter(jmap),
          Tuple1(byResult.converter(jmap.get(label.name).asInstanceOf[GG]))
        )
    )
  }
}

object SelectLabelConverter extends Poly2 {
  implicit def getConverter[HL <: HList, LD, LG, LC <: Converter[LD, LG]]
      : Case.Aux[StepLabel[LD, LG, LC], (JMap[String, Any], HL), (JMap[String, Any], LD :-: HL)] =
    at[StepLabel[LD, LG, LC], (JMap[String, Any], HL)] {
      case (label, (jmap, hl)) =>
        (jmap, label.converter(jmap.get(label.name).asInstanceOf[LG]) :: hl)
    }
}

object SelectLabelName extends ->((_: StepLabel[_, _, _]).name)

class SortBySelector[D, G, C <: Converter[D, G]](origin: Traversal[D, G, C]) {
  //  def by[B](f: Traversal[D, G] => Traversal[_, B]): ByResult[G, G]               = (_: GraphTraversal[_, G]).by(f(origin.start).raw)
//  def by[DD, GG](f: Traversal[D, G, C] => Traversal[DD, GG, _], order: Order): ByResult[G, G, G, IdentityConverter[G]] =
//    ByResult[G, G, G, IdentityConverter[G]](Converter.identity)(_.by(f(origin.start).raw, order))
  def by(f: Traversal[D, G, C] => Traversal[_, _, _], order: Order): ByResult[G, G, G, IdentityConverter[G]] =
    ByResult[G, G, G, IdentityConverter[G]](Converter.identity)(_.by(f(origin.start).raw, order))
  def by(key: String, order: Order): ByResult[G, G, G, IdentityConverter[G]] =
    ByResult[G, G, G, IdentityConverter[G]](Converter.identity)(_.by(key, order))
}

abstract class ByResult[F, DD, GG, +C <: Converter[DD, GG]](val converter: C) extends (GraphTraversal[_, F] => GraphTraversal[_, GG]) {
  def app[A](t: GraphTraversal[A, F]): GraphTraversal[A, GG] = apply(t).asInstanceOf[GraphTraversal[A, GG]]
}

object ByResult {
  def apply[G, DD, GG, C <: Converter[DD, GG]](converter: C)(f: GraphTraversal[_, G] => GraphTraversal[_, GG]): ByResult[G, DD, GG, C] =
    new ByResult[G, DD, GG, C](converter) {
      override def apply(g: GraphTraversal[_, G]): GraphTraversal[_, GG] = f(g)
    }
}
