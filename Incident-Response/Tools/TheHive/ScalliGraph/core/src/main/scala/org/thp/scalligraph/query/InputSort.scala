package org.thp.scalligraph.query

import org.apache.tinkerpop.gremlin.process.traversal.Order
import org.scalactic.Accumulation._
import org.scalactic.{Bad, Good, One}
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers.{FPath, FSeq, FString, FieldsParser}
import org.thp.scalligraph.traversal.Traversal
import org.thp.scalligraph.{BadRequestError, InvalidFormatAttributeError}

import scala.reflect.runtime.{universe => ru}

case class InputSort(fieldOrder: (String, Order)*) extends InputQuery[Traversal.Unk, Traversal.Unk] {
  override def apply(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Unk =
    fieldOrder.foldLeft(traversal.onRaw(_.order)) {
      case (t, (fieldName, order)) =>
        val fieldPath = FPath(fieldName)
        val property = publicProperties
          .get[Traversal.UnkD, Traversal.UnkDU](fieldPath, traversalType)
          .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
        property.sort(fieldPath, t, authContext, order)
    }
}

object InputSort {
  implicit val fieldsParser: FieldsParser[InputSort] = FieldsParser("sort-f") {
    case (_, FObjOne("_fields", FSeq(f))) =>
      f.validatedBy {
        case FObjOne(name, FString(order)) =>
          try Good(new InputSort(name -> Order.valueOf(order)))
          catch {
            case _: IllegalArgumentException =>
              Bad(One(InvalidFormatAttributeError("order", "order", Order.values().map(o => s"field: '$o'").toSet, FString(order))))
          }
        case FString(name) if name(0) == '-' => Good(new InputSort(name -> Order.desc))
        case FString(name) if name(0) == '+' => Good(new InputSort(name -> Order.asc))
        case FString(name)                   => Good(new InputSort(name -> Order.asc))
        case other                           => Bad(One(InvalidFormatAttributeError("order", "order", Order.values.map(o => s"field: '$o'").toSet, other)))
      }.map(x => new InputSort(x.flatMap(_.fieldOrder): _*))
  }
}
