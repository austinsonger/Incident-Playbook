package org.thp

import scala.util.{Failure, Success, Try}

package object scalligraph {
  implicit class RichOptionTry[A](o: Option[Try[A]]) {
    def flip: Try[Option[A]] = o.fold[Try[Option[A]]](Success(None))(_.map(Some.apply))
  }

  implicit class RichOption[A](o: Option[A]) {
    def toTry(f: Failure[A]): Try[A] = o.fold[Try[A]](f)(Success.apply)
  }

  implicit class RichSeq[A](s: TraversableOnce[A]) {

    def toTry[B](f: A => Try[B]): Try[Seq[B]] = s.foldLeft[Try[Seq[B]]](Success(Nil)) {
      case (Success(l), a) => f(a).map(l :+ _)
      case (failure, _)    => failure
    }
  }
}
