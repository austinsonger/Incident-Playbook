package org.thp.scalligraph.query

import org.scalactic.Good
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers._
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph, IteratorOutput, Traversal}

import scala.language.existentials
import scala.reflect.runtime.{universe => ru}

// Use global lock because scala reflection subtype operator <:< is not thread safe (scala/bug#10766)
// https://stackoverflow.com/questions/56854716/inconsistent-result-when-checking-type-subtype
object SubType {
  def apply(t1: ru.Type, t2: ru.Type): Boolean = synchronized(t1 <:< t2)
}

abstract class ParamQuery[P: ru.TypeTag] { q =>
  val paramType: ru.Type = ru.typeOf[P]
  def paramParser(tpe: ru.Type): FieldsParser[P]
  val name: String
  def checkFrom(t: ru.Type): Boolean
  def toType(t: ru.Type): ru.Type

  def toQuery(param: P): Query =
    new Query {
      override val name: String                                                                        = q.name
      override def checkFrom(t: ru.Type): Boolean                                                      = q.checkFrom(t)
      override def toType(t: ru.Type): ru.Type                                                         = q.toType(t)
      override def apply(unitParam: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any = q(param, fromType, from, authContext)
    }
  def apply(param: P, fromType: ru.Type, from: Any, authContext: AuthContext): Any
}

abstract class Query extends ParamQuery[Unit] { q =>
  override def paramParser(tpe: ru.Type): FieldsParser[Unit] =
    FieldsParser[Unit]("unit") {
      case _ => Good(())
    }

  def andThen(query: Query): Query =
    new Query {
      override val name: String                   = q.name + "/" + query.name
      override def checkFrom(t: ru.Type): Boolean = q.checkFrom(t)
      override def toType(t: ru.Type): ru.Type    = query.toType(q.toType(t))
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
        query(param, q.toType(fromType), q(param, fromType, from, authContext), authContext)
    }
}

object Query {

  def init[T: ru.TypeTag](queryName: String, f: (Graph, AuthContext) => T): Query =
    new Query {
      override val name: String                                                                    = queryName
      override def checkFrom(t: ru.Type): Boolean                                                  = SubType(t, ru.typeOf[Graph])
      override def toType(t: ru.Type): ru.Type                                                     = ru.typeOf[T]
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any = f(from.asInstanceOf[Graph], authContext)
    }

  def initWithParam[P: ru.TypeTag, T: ru.TypeTag](queryName: String, f: (P, Graph, AuthContext) => T)(implicit
      parser: FieldsParser[P]
  ): ParamQuery[P] =
    new ParamQuery[P] {
      override def paramParser(tpe: ru.Type): FieldsParser[P]                                   = parser
      override val name: String                                                                 = queryName
      override def checkFrom(t: ru.Type): Boolean                                               = SubType(t, ru.typeOf[Graph])
      override def toType(t: ru.Type): ru.Type                                                  = ru.typeOf[T]
      override def apply(param: P, fromType: ru.Type, from: Any, authContext: AuthContext): Any = f(param, from.asInstanceOf[Graph], authContext)
    }

  def apply[F: ru.TypeTag, T: ru.TypeTag](queryName: String, f: (F, AuthContext) => T): Query =
    new Query {
      override val name: String                                                                    = queryName
      override def checkFrom(t: ru.Type): Boolean                                                  = SubType(t, ru.typeOf[F])
      override def toType(t: ru.Type): ru.Type                                                     = ru.typeOf[T]
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any = f(from.asInstanceOf[F], authContext)
    }

  def withParam[P: ru.TypeTag, F: ru.TypeTag, T: ru.TypeTag](queryName: String, f: (P, F, AuthContext) => T)(implicit
      parser: FieldsParser[P]
  ): ParamQuery[P] =
    new ParamQuery[P] {
      override def paramParser(tpe: ru.Type): FieldsParser[P]                                   = parser
      override val name: String                                                                 = queryName
      override def checkFrom(t: ru.Type): Boolean                                               = SubType(t, ru.typeOf[F])
      override def toType(t: ru.Type): ru.Type                                                  = ru.typeOf[T]
      override def apply(param: P, fromType: ru.Type, from: Any, authContext: AuthContext): Any = f(param, from.asInstanceOf[F], authContext)
    }

  def output[E: Renderer: ru.TypeTag]: Query =
    new Query {
      override val name: String                   = "output"
      override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[E])
      override def toType(t: ru.Type): ru.Type    = ru.typeOf[Output[_]]
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
        implicitly[Renderer[E]].toOutput(from.asInstanceOf[E])
    }

  def output[E: Renderer: ru.TypeTag, F <: Traversal[E, G, Converter[E, G]] forSome { type G }: ru.TypeTag]: Query = output(identity[F])

  def outputWithContext[E: ru.TypeTag, F: ru.TypeTag](transform: (F, AuthContext) => Traversal[E, G, Converter[E, G]] forSome { type G })(implicit
      renderer: Renderer[E]
  ): Query =
    new Query {
      override val name: String                   = "output"
      override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[F])
      override def toType(t: ru.Type): ru.Type    = ru.appliedType(ru.typeOf[IteratorOutput].typeConstructor, ru.typeOf[E])
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
        IteratorOutput(transform(from.asInstanceOf[F], authContext).domainMap(renderer.toJson), None)
    }
  def output[E: ru.TypeTag, F: ru.TypeTag](transform: F => Traversal[E, G, Converter[E, G]] forSome { type G })(implicit
      renderer: Renderer[E]
  ): Query =
    new Query {
      override val name: String                   = "output"
      override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[F])
      override def toType(t: ru.Type): ru.Type    = ru.appliedType(ru.typeOf[IteratorOutput].typeConstructor, ru.typeOf[E])
      override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
        IteratorOutput(transform(from.asInstanceOf[F]).domainMap(renderer.toJson), None)
    }
}

class SortQuery(publicProperties: PublicProperties) extends ParamQuery[InputSort] {
  override def paramParser(tpe: ru.Type): FieldsParser[InputSort] = InputSort.fieldsParser
  override val name: String                                       = "sort"
  override def checkFrom(t: ru.Type): Boolean                     = SubType(t, ru.typeOf[Traversal[_, _, _]])
  override def toType(t: ru.Type): ru.Type                        = t
  override def apply(inputSort: InputSort, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
    inputSort(
      publicProperties,
      fromType,
      from.asInstanceOf[Traversal.Unk],
      authContext
    )
}

object FilterQuery {
  def apply(publicProperties: PublicProperties)(
      fieldsParser: (
          ru.Type,
          ru.Type => FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]]
      ) => FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]]
  ): FilterQuery = new FilterQuery(publicProperties, fieldsParser :: Nil)
  def default(publicProperties: PublicProperties): FilterQuery =
    apply(publicProperties)(InputFilter.fieldsParser(_, publicProperties, _))
  def empty(publicProperties: PublicProperties) = new FilterQuery(publicProperties)
}

final class FilterQuery(
    publicProperties: PublicProperties,
    protected val fieldsParsers: List[
      (ru.Type, ru.Type => FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]]) => FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]]
    ] = Nil
) extends ParamQuery[InputQuery[Traversal.Unk, Traversal.Unk]] { filterQuery =>
  def paramParser(tpe: ru.Type): FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]] =
    fieldsParsers.foldLeft(FieldsParser.empty[InputQuery[Traversal.Unk, Traversal.Unk]])((fp, f) => fp orElse f(tpe, t => paramParser(t)))
  override val name: String                   = "filter"
  override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[Traversal[_, _, _]])
  override def toType(t: ru.Type): ru.Type    = t
  override def apply(inputFilter: InputQuery[Traversal.Unk, Traversal.Unk], fromType: ru.Type, from: Any, authContext: AuthContext): Any =
    inputFilter(
      publicProperties,
      fromType,
      from.asInstanceOf[Traversal.Unk], //.asInstanceOf[X forSome { type X <: Traversal.V[BaseVertex][_, X] }],
      authContext
    )
//  def addParser(parser: (ru.Type, () => FieldsParser[InputQuery[Traversal.Unk, Traversal.Unk]])): FilterQuery = new FilterQuery(db, publicProperties, parser :: fieldsParsers)
  def ++(other: FilterQuery): FilterQuery = new FilterQuery(publicProperties, filterQuery.fieldsParsers ::: other.fieldsParsers)
}

class AggregationQuery(publicProperties: PublicProperties, filterQuery: FilterQuery) extends ParamQuery[Aggregation] {
  override def paramParser(tpe: ru.Type): FieldsParser[Aggregation] = Aggregation.fieldsParser(filterQuery.paramParser(tpe))
  override val name: String                                         = "aggregation"
  override def checkFrom(t: ru.Type): Boolean                       = SubType(t, ru.typeOf[Traversal[_, _, _]])
  override def toType(t: ru.Type): ru.Type                          = ru.typeOf[Output[_]]
  override def apply(aggregation: Aggregation, fromType: ru.Type, from: Any, authContext: AuthContext): Any =
    aggregation(
      publicProperties,
      fromType,
      from.asInstanceOf[Traversal.Unk],
      authContext
    )
}

object CountQuery extends Query {
  override val name: String                   = "count"
  override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[Traversal[_, _, _]])
  override def toType(t: ru.Type): ru.Type    = ru.typeOf[Long]
  override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Long =
    from.asInstanceOf[Traversal[Any, Any, Converter[Any, Any]]].getCount
}

class LimitedCountQuery(threshold: Long) extends Query {
  override val name: String                   = "limitedCount"
  override def checkFrom(t: ru.Type): Boolean = SubType(t, ru.typeOf[Traversal[_, _, _]])
  override def toType(t: ru.Type): ru.Type    = ru.typeOf[Long]
  override def apply(param: Unit, fromType: ru.Type, from: Any, authContext: AuthContext): Long =
    from.asInstanceOf[Traversal[Any, Any, Converter[Any, Any]]].getLimitedCount(threshold)
}

trait InputQuery[FROM, TO] {
  def apply(
      publicProperties: PublicProperties,
      traversalType: ru.Type,
      traversal: FROM,
      authContext: AuthContext
  ): TO
}
