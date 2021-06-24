package org.thp.scalligraph.record

import shapeless.{HList, Witness}

import scala.language.experimental.macros

trait Selector[L <: HList, K] {
  type Out
  def apply(l: L): Out
}

object Selector {
  type Aux[L <: HList, K, Out0] = Selector[L, K] { type Out = Out0 }

  def apply[L <: HList, K](implicit selector: Selector[L, K]): Aux[L, K, selector.Out] = selector

  implicit def mkSelector[L <: HList, K, O]: Aux[L, K, O] =
    macro RecordMacro.mkSelector[L, K]
}

case class Record[C <: HList](list: C) {
  type FSL[K] = Selector[C, K]

  def apply(key: Witness)(implicit selector: Selector[C, key.T]): selector.Out =
    selector(list)
}
