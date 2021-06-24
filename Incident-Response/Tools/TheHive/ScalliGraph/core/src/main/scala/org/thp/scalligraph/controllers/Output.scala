package org.thp.scalligraph.controllers

import org.thp.scalligraph.traversal.IteratorOutput
import play.api.libs.json._

trait Renderer[V] { renderer =>
  type O
  def toOutput(value: V): Output[O]
  def toValue(value: V): O      = toOutput(value).toValue
  def toJson(value: V): JsValue = toOutput(value).toJson

  def opt: Renderer[Option[V]] =
    new Renderer[Option[V]] {
      type O = Option[renderer.O]
      override def toOutput(value: Option[V]): Output[O] =
        new Output[O] {
          override def toValue: O      = value.map(renderer.toValue)
          override def toJson: JsValue = value.fold[JsValue](JsNull)(renderer.toJson)
        }
    }

  def list: Renderer[Seq[V]] =
    new Renderer[Seq[V]] {
      type O = Seq[renderer.O]
      override def toOutput(value: Seq[V]): Output[O] =
        new Output[O] {
          override def toValue: O      = value.map(renderer.toValue)
          override def toJson: JsValue = JsArray(value.map(renderer.toJson))
        }
    }

  def set: Renderer[Set[V]] =
    new Renderer[Set[V]] {
      type O = Set[renderer.O]
      override def toOutput(value: Set[V]): Output[O] =
        new Output[O] {
          override def toValue: O      = value.map(renderer.toValue)
          override def toJson: JsValue = JsArray(value.map(renderer.toJson).toSeq)
        }
    }
}

class StreamRenderer[F](f: F => IteratorOutput) extends Renderer[F] {
  type O = JsValue
  override def toOutput(value: F): IteratorOutput = f(value)
}

trait RendererLowPriority {
  implicit def json[V: Writes]: Renderer.Aux[V, V] =
    new Renderer[V] {
      type O = V
      override def toOutput(value: V): Output[O] = Output(value)
    }
}

//class StreamRenderer[F](f: F => IteratorOutput) extends Renderer[F] {
//  type O = F
//  override def toOutput(value: F): Output[F] = new Output[F] {
//    override def toValue: F      = value
//    override def toJson: JsValue = JsArray(f(value).iterator.map(renderer.toJson).toSeq)
//  }
//  def toStream(value: F): (Iterator[JsValue], Option[Long]) = {
//    val iteratorOutput = f(value)
//    iteratorOutput.iterator.map(renderer.toJson) -> iteratorOutput.totalSize.map(_.apply())
//  }
//}

object Renderer extends RendererLowPriority {
  type Aux[V, OO] = Renderer[V] { type O = OO }
  implicit def jsValue[J <: JsValue]: Renderer.Aux[J, J] =
    new Renderer[J] {
      override type O = J
      override def toOutput(value: J): Output[O] = Output(value, Json.toJson(value))
    }

  def toJson[F, V: Writes](f: F => V): Renderer.Aux[F, V] =
    new Renderer[F] {
      override type O = V
      override def toOutput(value: F): Output[O] = Output(f(value), Json.toJson(f(value)))
    }

  def stream[F](f: F => IteratorOutput): StreamRenderer[F] = new StreamRenderer[F](f)

//  def stream[F, V](f: F => IteratorOutput)(implicit renderer: Renderer[V]): Renderer[F] = new StreamRenderer[F, V](f)
//  def stream[T](t: Traversal[T, _, _], renderer: Renderer[T]): Renderer[Traversal[T, _, _]] = new Renderer[Traversal[T, _, _]] {
//    override type O = Traversal[T, _, _]
//
//    override def toOutput2(value: Traversal[T, _, _]): Output[Traversal[T, _, _]] = new Output[Traversal[T, _, _]] {
//      override def toValue: Traversal[T, _, _] = t
//
//      override def toJson: JsValue = t.map(renderer.toJson)
//    }
//  }

  def apply[V](f: V => Output[V]): Renderer[V] =
    new Renderer[V] {
      override type O = V
      override def toOutput(value: V): Output[O] = f(value)
    }

  implicit def seqRenderer[F, OO](implicit aRenderer: Renderer.Aux[F, OO]): Renderer.Aux[Seq[F], Seq[OO]] =
    new Renderer[Seq[F]] {
      type O = Seq[OO]

      override def toOutput(value: Seq[F]): Output[Seq[OO]] =
        Output[Seq[OO]](value.map(aRenderer.toOutput(_).toValue), JsArray(value.map(aRenderer.toOutput(_).toJson)))
    }

//  implicit def listRenderer[F, OO](implicit aRenderer: Renderer.Aux[F, OO]): Renderer.Aux[List[F], List[OO]] = new Renderer[List[F]] {
//    override def toOutput(m: List[F]): Output[O] = {
//      val o = m.map(aRenderer.toOutput(_).toValue)
//      val j = JsArray(m.map(aRenderer.toOutput(_).toJson))
//      Output[List[O]](o, j)
//    }
//  }

//  implicit def setRenderer[V](implicit aRenderer: Renderer[V]): Renderer[Set[V]] = new Renderer[Set[V]] {
//    override def toOutput(value: Set[V]): Output[Set[V]] =
//      Output[Set[V]](value.map(aRenderer.toOutput(_).toValue), JsArray(value.map(aRenderer.toOutput(_).toJson).toSeq))
//  }
}

trait Output[+O] {
  def toValue: O
  def toJson: JsValue
}

class SimpleOutput[O](getValue: () => O, getJson: () => JsValue) extends Output[O] {
  lazy val toValue: O      = getValue()
  lazy val toJson: JsValue = getJson()
}

object Output {
  def apply[O](native: => O, json: => JsValue): Output[O] = new SimpleOutput[O](() => native, () => json)

  def apply[O](native: => O)(implicit writes: Writes[O]): Output[O] = {
    lazy val n = native
    new SimpleOutput[O](() => n, () => writes.writes(n))
  }
}
