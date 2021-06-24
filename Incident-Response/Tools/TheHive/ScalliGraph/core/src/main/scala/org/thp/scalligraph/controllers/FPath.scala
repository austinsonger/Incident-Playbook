package org.thp.scalligraph.controllers

import org.thp.scalligraph.{InternalError, InvalidFormatAttributeError}

trait FPath {
  val isEmpty: Boolean  = false
  def nonEmpty: Boolean = !isEmpty
  def :/(elem: FPath): FPath
  def :/(elem: String): FPath = this :/ FPath(elem)
  def /:(elem: String): FPath = FPath(elem) :/ this
  def toSeq(index: Int): FPath
  def startsWith(elem: FPath): Option[FPath]
  def matches(elem: FPath): Boolean = startsWith(elem).exists(_.isEmpty)
  def headOption: Option[String]
//  def startsWith(elem: String): Boolean
}

object FPathEmpty extends FPath {
  override val isEmpty: Boolean         = true
  override def :/(elem: FPath): FPath   = elem
  override def toString: String         = ""
  override def toSeq(index: Int): FPath = this // sys.error(s"ERROR: empty.toSeq($index)")
//  override def startsWith(elem: String): Boolean = false
  override def startsWith(elem: FPath): Option[FPath] = if (elem.isEmpty) Some(this) else None
  override def headOption: Option[String]             = None
}

case class FPathElem(head: String, tail: FPath = FPathEmpty) extends FPath {
  override def :/(elem: FPath): FPath = copy(tail = tail :/ elem)
  override def toString: String       = if (tail.isEmpty) s"$head" else s"$head.$tail"
  override def toSeq(index: Int): FPath =
    if (tail.isEmpty) FPathElemInSeq(head, index, tail)
    else copy(tail = tail.toSeq(index))
//  override def startsWith(elem: String): Boolean = head == elem
  override def startsWith(elem: FPath): Option[FPath] =
    elem match {
      case FPathEmpty                   => Some(this)
      case FPathElem(h, t) if h == head => tail.startsWith(t)
      case _                            => None
    }
  override def headOption: Option[String] = Some(head)
}

case class FPathSeq(head: String, tail: FPath) extends FPath {
  override def :/(elem: FPath): FPath = copy(tail = tail :/ elem)
  override def toString: String =
    if (tail.isEmpty) s"$head[]" else s"$head[].$tail"
  override def toSeq(index: Int): FPath =
    if (tail.isEmpty) throw InternalError(s"ERROR: $this.toSeq($index)")
    else copy(tail = tail.toSeq(index))
//  override def startsWith(elem: String): Boolean = head == elem
  override def startsWith(elem: FPath): Option[FPath] =
    elem match {
      case FPathEmpty                           => Some(this)
      case FPathSeq(h, t) if h == head          => tail.startsWith(t)
      case FPathElemInSeq(h, _, t) if h == head => tail.startsWith(t)
      case _                                    => None
    }
  override def headOption: Option[String] = Some(head)
}

case class FPathElemInSeq(head: String, index: Int, tail: FPath) extends FPath {
  override def :/(elem: FPath): FPath = copy(tail = tail :/ elem)
  override def toString: String =
    if (tail.isEmpty) s"$head[$index]" else s"$head[$index].$tail"
  override def toSeq(index: Int): FPath =
    if (tail.isEmpty) throw InternalError(s"ERROR: $this.toSeq($index)")
    else copy(tail = tail.toSeq(index))
//  override def startsWith(elem: String): Boolean = head == elem
  override def startsWith(elem: FPath): Option[FPath] =
    elem match {
      case FPathEmpty                           => Some(this)
      case FPathSeq(h, t) if h == head          => tail.startsWith(t)
      case FPathElemInSeq(h, _, t) if h == head => tail.startsWith(t)
      case _                                    => None
    }
  override def headOption: Option[String] = Some(head)
}

object FPath {
  private val elemInSeqRegex = "(\\w[^.\\[\\]]*)\\[(\\d+)]".r
  private val seqRegex       = "(\\w[^.\\[\\]]*)\\[]".r
  private val elemRegex      = "(\\w[^.\\[\\]]*)".r
  val empty: FPath           = FPathEmpty

  def apply(path: String): FPath =
    path.split("\\.").foldRight[FPath](FPathEmpty) {
      case (elemRegex(p), pathElem)             => FPathElem(p, pathElem)
      case (seqRegex(p), pathElem)              => FPathSeq(p, pathElem)
      case (elemInSeqRegex(p, index), pathElem) => FPathElemInSeq(p, index.toInt, pathElem)
      case (other, pathElem) if other.isEmpty   => pathElem
      case (other, _)                           => throw InvalidFormatAttributeError(path, "attributeName", Set.empty, FString(other))
    }

  def unapplySeq(path: FPath): Option[Seq[String]] =
    path match {
      case FPathEmpty                                => Some(Nil)
      case FPathElem(head, FPath(tail @ _*))         => Some(head +: tail)
      case FPathElemInSeq(head, _, FPath(tail @ _*)) => Some(head +: tail) // TODO add index ?
      case FPathSeq(head, FPath(tail @ _*))          => Some(head +: tail) // TODO add [] ?
    }
}
