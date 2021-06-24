package org.thp.scalligraph.traversal

import org.thp.scalligraph.controllers.{Output, Renderer}
import org.thp.scalligraph.traversal.TraversalOps._
import play.api.libs.json.{JsArray, JsValue}

class IteratorOutput(val iterator: Iterator[JsValue], val totalSize: Option[() => Long]) extends Output[JsValue] {
  override def toValue: JsValue = toJson
  override def toJson: JsValue  = JsArray(iterator.toSeq)
}

object IteratorOutput {
  def apply[V](traversal: Traversal[V, _, _], totalSize: Option[() => Long] = None)(implicit renderer: Renderer[V]) =
    new IteratorOutput(traversal.cast[V, Any].toIterator.map(renderer.toJson), totalSize)
}
