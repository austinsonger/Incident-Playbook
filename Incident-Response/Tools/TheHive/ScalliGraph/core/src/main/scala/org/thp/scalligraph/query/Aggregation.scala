package org.thp.scalligraph.query

import org.apache.tinkerpop.gremlin.process.traversal.Order
import org.scalactic.Accumulation._
import org.scalactic._
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers._
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal._
import org.thp.scalligraph.{BadRequestError, InvalidFormatAttributeError}
import play.api.Logger
import play.api.libs.json.{JsNull, JsNumber, JsObject, Json}

import java.lang.{Long => JLong}
import java.time.temporal.ChronoUnit
import java.util.{Calendar, Date, List => JList}
import scala.reflect.runtime.{universe => ru}
import scala.util.Try
import scala.util.matching.Regex

object Aggregation {

  object AggObj {
    def unapply(field: Field): Option[(String, FObject)] =
      field match {
        case f: FObject =>
          f.get("_agg") match {
            case FString(name) => Some(name -> (f - "_agg"))
            case _             => None
          }
        case _ => None
      }
  }

  val intervalParser: FieldsParser[(Long, ChronoUnit)] = FieldsParser[(Long, ChronoUnit)]("interval") {
    case (_, f) =>
      withGood(
        FieldsParser.long.optional.on("_interval")(f),
        FieldsParser[ChronoUnit]("chronoUnit") {
          case (_, f @ FString(value)) =>
            Or.from(
              Try(ChronoUnit.valueOf(value)).toOption,
              One(InvalidFormatAttributeError("_unit", "chronoUnit", ChronoUnit.values.toSet.map((_: ChronoUnit).toString), f))
            )
        }.on("_unit")(f)
      )((i, u) => i.getOrElse(0L) -> u)
  }

  val intervalRegex: Regex = "(\\d+)([smhdwMy])".r

  val mergedIntervalParser: FieldsParser[(Long, ChronoUnit)] = FieldsParser[(Long, ChronoUnit)]("interval") {
    case (_, FString(intervalRegex(interval, unit))) =>
      Good(unit match {
        case "s" => interval.toLong -> ChronoUnit.SECONDS
        case "m" => interval.toLong -> ChronoUnit.MINUTES
        case "h" => interval.toLong -> ChronoUnit.HOURS
        case "d" => interval.toLong -> ChronoUnit.DAYS
        case "w" => interval.toLong -> ChronoUnit.WEEKS
        case "M" => interval.toLong -> ChronoUnit.MONTHS
        case "y" => interval.toLong -> ChronoUnit.YEARS
      })
  }

//  def aggregationFieldParser(add[String, FieldsParser[Aggregation]] = {
//    case "field" =>
//      FieldsParser("FieldAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser.string.on("_field")(field),
//            FieldsParser.string.sequence.on("_order")(field).orElse(FieldsParser.string.on("_order").map("order")(Seq(_))(field)),
//            FieldsParser.long.optional.on("_size")(field),
//            fieldsParser.sequence.on("_select")(field)
//          )((aggName, fieldName, order, size, subAgg) => FieldAggregation(aggName, fieldName, order, size, subAgg))
//      }
//    case "count" =>
//      FieldsParser("CountAggregation") {
//        case (_, field) => FieldsParser.string.optional.on("_name")(field).map(aggName => AggCount(aggName))
//      }
//    case "time" =>
//      FieldsParser("TimeAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser
//              .string
//              .sequence
//              .on("_fields")(field)
//              .orElse(FieldsParser.string.on("_fields")(field).map(Seq(_))), //.map("toSeq")(f => Good(Seq(f)))),
//            mergedIntervalParser.on("_interval").orElse(intervalParser)(field),
//            fieldsParser.sequence.on("_select")(field)
//          ) { (aggName, fieldNames, intervalUnit, subAgg) =>
//            if (fieldNames.lengthCompare(1) > 0)
//              logger.warn(s"Only one field is supported for time aggregation (aggregation $aggName, ${fieldNames.tail.mkString(",")} are ignored)")
//            TimeAggregation(aggName, fieldNames.head, intervalUnit._1, intervalUnit._2, subAgg)
//          }
//      }
//    case "avg" =>
//      FieldsParser("AvgAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser.string.on("_field")(field)
//          )((aggName, fieldName) => AggAvg(aggName, fieldName))
//      }
//    case "min" =>
//      FieldsParser("MinAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser.string.on("_field")(field)
//          )((aggName, fieldName) => AggMin(aggName, fieldName))
//      }
//    case "max" =>
//      FieldsParser("MaxAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser.string.on("_field")(field)
//          )((aggName, fieldName) => AggMax(aggName, fieldName))
//      }
//    case "sum" =>
//      FieldsParser("SumAggregation") {
//        case (_, field) =>
//          withGood(
//            FieldsParser.string.optional.on("_name")(field),
//            FieldsParser.string.on("_field")(field)
//          )((aggName, fieldName) => AggSum(aggName, fieldName))
//      }
//    case other =>
//      new FieldsParser[Aggregation](
//        "unknownAttribute",
//        Set.empty,
//        {
//          case (path, _) =>
//            Bad(One(InvalidFormatAttributeError(path.toString, "string", Set("field", "time", "count", "avg", "min", "max", "sum"), FString(other))))
//        }
//      )
//  }

  def fieldsParser(filterParser: FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]]): FieldsParser[Aggregation] =
    FieldsParser("aggregation") {
//      case (_, AggObj(name, field)) => aggregationFieldParser(name)(field)
      case (_, AggObj("field", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser.string.on("_field")(field),
          FieldsParser.string.sequence.on("_order")(field).orElse(FieldsParser.string.on("_order").map("order")(Seq(_))(field)),
          FieldsParser.long.optional.on("_size")(field),
          fieldsParser(filterParser).sequence.on("_select")(field),
          filterParser.optional.on("_query")(field)
        )((aggName, fieldName, order, size, subAgg, filter) => FieldAggregation(aggName, fieldName, order, size, subAgg, filter))
      case (_, AggObj("count", field)) =>
        withGood(FieldsParser.string.optional.on("_name")(field), filterParser.optional.on("_query")(field))((aggName, filter) =>
          AggCount(aggName, filter)
        )
      case (_, AggObj("time", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser
            .string
            .sequence
            .on("_fields")(field)
            .orElse(FieldsParser.string.on("_fields")(field).map(Seq(_))), //.map("toSeq")(f => Good(Seq(f)))),
          mergedIntervalParser.on("_interval").orElse(intervalParser)(field),
          fieldsParser(filterParser).sequence.on("_select")(field),
          filterParser.optional.on("_query")(field)
        ) { (aggName, fieldNames, intervalUnit, subAgg, filter) =>
          if (fieldNames.lengthCompare(1) > 0)
            logger.warn(s"Only one field is supported for time aggregation (aggregation $aggName, ${fieldNames.tail.mkString(",")} are ignored)")
          TimeAggregation(aggName, fieldNames.head, intervalUnit._1, intervalUnit._2, subAgg, filter)
        }
      case (_, AggObj("avg", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser.string.on("_field")(field),
          filterParser.optional.on("_query")(field)
        )((aggName, fieldName, filter) => AggAvg(aggName, fieldName, filter))
      case (_, AggObj("min", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser.string.on("_field")(field),
          filterParser.optional.on("_query")(field)
        )((aggName, fieldName, filter) => AggMin(aggName, fieldName, filter))
      case (_, AggObj("max", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser.string.on("_field")(field),
          filterParser.optional.on("_query")(field)
        )((aggName, fieldName, filter) => AggMax(aggName, fieldName, filter))
      case (_, AggObj("sum", field)) =>
        withGood(
          FieldsParser.string.optional.on("_name")(field),
          FieldsParser.string.on("_field")(field),
          filterParser.optional.on("_query")(field)
        )((aggName, fieldName, filter) => AggSum(aggName, fieldName, filter))
    }
}

abstract class Aggregation(val name: String) extends InputQuery[Traversal.Unk, Output[_]] {

  override def apply(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Output[_] = getTraversal(publicProperties, traversalType, traversal, authContext).headOption.getOrElse(Output(null, JsNull))

  def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]]
}

case class AggSum(aggName: Option[String], fieldName: String, filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]])
    extends Aggregation(s"sum_$fieldName") {
  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    filter
      .fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
      .coalesce(
        t =>
          property
            .select(FPath(fieldName), t, authContext)
            .sum
            .domainMap(sum => Output(sum, Json.obj(name -> JsNumber(BigDecimal(sum.toString)))))
            .castDomain[Output[_]],
        Output(null, JsNull)
      )
  }
}
case class AggAvg(aggName: Option[String], fieldName: String, filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]])
    extends Aggregation(s"sum_$fieldName") {
  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    filter
      .fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
      .coalesce(
        t =>
          property
            .select(FPath(fieldName), t, authContext)
            .mean
            .domainMap(avg => Output(Json.obj(name -> avg)))
            .asInstanceOf[Traversal.Domain[Output[_]]],
        Output(null, JsNull)
      )
  }
}

case class AggMin(aggName: Option[String], fieldName: String, filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]])
    extends Aggregation(s"min_$fieldName") {
  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    filter
      .fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
      .coalesce(
        t =>
          property
            .select(FPath(fieldName), t, authContext)
            .min
            .domainMap(min => Output(min, Json.obj(name -> property.toJson(min)))),
        Output(null, JsNull)
      )
  }
}

case class AggMax(aggName: Option[String], fieldName: String, filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]])
    extends Aggregation(s"max_$fieldName") {
  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    filter
      .fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
      .coalesce(
        t =>
          property
            .select(FPath(fieldName), t, authContext)
            .max
            .domainMap(max => Output(max, Json.obj(name -> property.toJson(max)))),
        Output(null, JsNull)
      )
  }
}

case class AggCount(aggName: Option[String], filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]])
    extends Aggregation(aggName.getOrElse("count")) {
  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] =
    filter
      .fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
      .count
      .domainMap(count => Output(count.longValue(), Json.obj(name -> count)))
      .castDomain[Output[_]]
}

//case class AggTop[T](fieldName: String) extends AggFunction[T](s"top_$fieldName")

case class FieldAggregation(
    aggName: Option[String],
    fieldName: String,
    orders: Seq[String],
    size: Option[Long],
    subAggs: Seq[Aggregation],
    filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]]
) extends Aggregation(aggName.getOrElse(s"field_$fieldName")) {
  lazy val logger: Logger = Logger(getClass)

  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val label = StepLabel[Traversal.UnkD, Traversal.UnkG, Converter[Traversal.UnkD, Traversal.UnkG]]
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    val filteredTraversal = filter.fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
    val groupedVertices   = property.select(FPath(fieldName), filteredTraversal.as(label), authContext).group(_.by, _.by(_.select(label).fold)).unfold
//    val groupedVertices = traversal.group(_.by(t => property.select(FPath(fieldName), t).cast[Any, Any])).unfold
    val sortedAndGroupedVertex = orders
      .map {
        case order if order.headOption.contains('-') => order.tail -> Order.desc
        case order if order.headOption.contains('+') => order.tail -> Order.asc
        case order                                   => order      -> Order.asc
      }
      .foldLeft(groupedVertices) {
        case (acc, (field, order)) if field == fieldName => acc.sort(_.by(_.selectKeys, order))
        case (acc, (field, order)) if field == "count"   => acc.sort(_.by(_.selectValues.localCount, order))
        case (acc, (field, _)) =>
          logger.warn(s"In field aggregation you can only sort by the field ($fieldName) or by count, not by $field")
          acc
      }
    val sizedSortedAndGroupedVertex = size.fold(sortedAndGroupedVertex)(sortedAndGroupedVertex.limit)
    val subAggProjection = subAggs.map {
      agg => (s: GenericBySelector[Seq[Traversal.UnkD], JList[Traversal.UnkG], Converter.CList[Traversal.UnkD, Traversal.UnkG, Converter[
        Traversal.UnkD,
        Traversal.UnkG
      ]]]) =>
        s.by(t => agg.getTraversal(publicProperties, traversalType, t.unfold, authContext).castDomain[Output[_]])
    }

    sizedSortedAndGroupedVertex
      .project(
        _.by(_.selectKeys)
          .by(
            _.selectValues
              .flatProject(subAggProjection: _*)
              .domainMap { aggResult =>
                val outputs = aggResult.asInstanceOf[Seq[Output[_]]]
                val json = outputs.map(_.toJson).foldLeft(JsObject.empty) {
                  case (acc, jsObject: JsObject) => acc ++ jsObject
                  case (acc, r) =>
                    logger.warn(s"Invalid stats result: $r")
                    acc
                }
                Output(outputs.map(_.toValue), json)
              }
          )
      )
      .fold
      .domainMap(x => Output(x.map(kv => kv._1 -> kv._2.toValue).toMap, JsObject(x.map(kv => kv._1.toString -> kv._2.toJson))))
      .castDomain[Output[_]]
  }
}

case class TimeAggregation(
    aggName: Option[String],
    fieldName: String,
    interval: Long,
    unit: ChronoUnit,
    subAggs: Seq[Aggregation],
    filter: Option[InputQuery[Traversal.Unk, Traversal.Unk]]
) extends Aggregation(aggName.getOrElse(s"time_$fieldName")) {
  val calendar: Calendar = Calendar.getInstance()

  def dateToKey(date: Date): Long =
    unit match {
      case ChronoUnit.WEEKS =>
        calendar.setTime(date)
        val year = calendar.get(Calendar.YEAR)
        val week = (calendar.get(Calendar.WEEK_OF_YEAR) / interval) * interval
        calendar.setTimeInMillis(0)
        calendar.set(Calendar.YEAR, year)
        calendar.set(Calendar.WEEK_OF_YEAR, week.toInt)
        calendar.getTimeInMillis

      case ChronoUnit.MONTHS =>
        calendar.setTime(date)
        val year  = calendar.get(Calendar.YEAR)
        val month = (calendar.get(Calendar.MONTH) / interval) * interval
        calendar.setTimeInMillis(0)
        calendar.set(Calendar.YEAR, year)
        calendar.set(Calendar.MONTH, month.toInt)
        calendar.getTimeInMillis

      case ChronoUnit.YEARS =>
        calendar.setTime(date)
        val year = (calendar.get(Calendar.YEAR) / interval) * interval
        calendar.setTimeInMillis(0)
        calendar.set(Calendar.YEAR, year.toInt)
        calendar.getTimeInMillis

      case other =>
        val duration = other.getDuration.toMillis * interval
        (date.getTime / duration) * duration
    }

  def keyToDate(key: Long): Date = new Date(key)

  override def getTraversal(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: Traversal.Unk,
      authContext: AuthContext
  ): Traversal.Domain[Output[_]] = {
    val property = publicProperties
      .get[Traversal.UnkD, Traversal.UnkDU](fieldName, traversalType)
      .getOrElse(throw BadRequestError(s"Property $fieldName for type $traversalType not found"))
    val label             = StepLabel[Traversal.UnkD, Traversal.UnkG, Converter[Traversal.UnkD, Traversal.UnkG]]
    val filteredTraversal = filter.fold(traversal)(_(publicProperties, traversalType, traversal, authContext))
    val groupedVertex = property
      .select(FPath(fieldName), filteredTraversal.as(label), authContext)
      .cast[Date, Date]
      .graphMap[Long, JLong, Converter[Long, JLong]](dateToKey, Converter.long)
      .group(_.by, _.by(_.select(label).fold))
      .unfold

    val subAggProjection = subAggs.map {
      agg => (s: GenericBySelector[Seq[Traversal.UnkD], JList[Traversal.UnkG], Converter.CList[Traversal.UnkD, Traversal.UnkG, Converter[
        Traversal.UnkD,
        Traversal.UnkG
      ]]]) =>
        s.by(t => agg.getTraversal(publicProperties, traversalType, t.unfold, authContext).castDomain[Output[_]])
    }

    groupedVertex
      .project(
        _.by(_.selectKeys)
          .by(
            _.selectValues
              .flatProject(subAggProjection: _*)
              .domainMap { aggResult =>
                val outputs = aggResult.asInstanceOf[Seq[Output[_]]]
                val json = outputs.map(_.toJson).foldLeft(JsObject.empty) {
                  case (acc, jsObject: JsObject) => acc ++ jsObject
                  case (acc, r) =>
                    logger.warn(s"Invalid stats result: $r")
                    acc
                }
                Output(outputs.map(_.toValue), json)
              }
          )
      )
      .fold
      .domainMap(x => Output(x.map(kv => kv._1 -> kv._2.toValue).toMap, JsObject(x.map(kv => kv._1.toString -> kv._2.toJson))))
      .castDomain[Output[_]]
  }
}
