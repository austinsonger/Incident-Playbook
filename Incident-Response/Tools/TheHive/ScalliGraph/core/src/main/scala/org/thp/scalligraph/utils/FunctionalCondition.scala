package org.thp.scalligraph.utils

object FunctionalCondition {
  implicit class When[A](a: A) {
    def whenValue(cond: A => Boolean)(f: A => A): A = if (cond(a)) f(a) else a
    def when(cond: Boolean)(f: A => A): A           = if (cond) f(a) else a
    def merge[B](opt: Option[B])(f: (A, B) => A): A = opt.fold(a)(f(a, _))
  }

  implicit class When2[A, B](ab: (A, B)) {
    def when(cond: Boolean)(fa: A => A, fb: B => B): (A, B) = if (cond) (fa(ab._1), fb(ab._2)) else ab
  }
}
