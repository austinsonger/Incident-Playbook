package org.thp.scalligraph.query

import org.thp.scalligraph.controllers._
import org.thp.scalligraph.query.InputFilter.logger

object FObjOne {

  def unapply(field: Field): Option[(String, Field)] = field match {
    case FObject(f) if f.size == 1 => f.headOption
    case _                         => None
  }
}

object FDeprecatedObjOne {
  def unapply(field: Field): Option[(String, Field)] = field match {
    case FObject(f) if f.size == 1 =>
      val (key, value) = f.head
      logger.warn(s"""Use of filter {"$key": "$value"} is deprecated. Please use {"_field": "$key", "_value": "$value"}""")
      f.headOption
    case _ => None
  }
}

object FFieldValue {

  def unapply(field: Field): Option[(String, Field)] = {
    val fieldName  = field.get("_field")
    val fieldValue = field.get("_value")
    (fieldName, fieldValue) match {
      case (FString(name), value) if value.isDefined => Some(name -> value)
      case _                                         => None
    }
  }
}

object FFieldFromTo {

  def unapply(field: Field): Option[(String, Field, Field)] = {
    val fieldName = field.get("_field")
    val from      = field.get("_from")
    val to        = field.get("_to")
    (fieldName, from, to) match {
      case (FString(name), f, t) if from.isDefined && to.isDefined => Some((name, f, t))
      case _                                                       => None
    }

  }
}

object FNamedObj {

  def unapply(field: Field): Option[(String, FObject)] = field match {
    case f: FObject =>
      f.get("_name") match {
        case FString(name) => Some(name -> (f - "_name"))
        case _             => None
      }
    case _ => None
  }
}

object FNative {

  def unapply(field: Field): Option[Any] = field match {
    case FString(s)  => Some(s)
    case FNumber(n)  => Some(n)
    case FBoolean(b) => Some(b)
    case FAny(a)     => Some(a.mkString)
    case _           => None
  }
}
