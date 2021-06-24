package org.thp.scalligraph.models

import java.lang.{Boolean => JBoolean, Double => JDouble, Float => JFloat, Integer => JInteger, Long => JLong}
import java.util.Date

abstract class NoValue[A] {
  def apply(): A
}

object NoValue {
  def apply[A](zero: A): NoValue[A]       = () => zero
  implicit val anyRef: NoValue[AnyRef]    = NoValue[AnyRef]("") // for ID
  implicit val string: NoValue[String]    = NoValue[String]("")
  implicit val long: NoValue[JLong]       = NoValue[JLong](0L)
  implicit val int: NoValue[JInteger]     = NoValue[JInteger](0)
  implicit val date: NoValue[Date]        = NoValue[Date](new Date(0))
  implicit val boolean: NoValue[JBoolean] = NoValue[JBoolean](false)
  implicit val double: NoValue[JDouble]   = NoValue[JDouble](0.0)
  implicit val float: NoValue[JFloat]     = NoValue[JFloat](0f)
}
