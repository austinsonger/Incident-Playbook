package org.thp.scalligraph.graphql

import java.util.Date

import org.thp.scalligraph._
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers.Output
import org.thp.scalligraph.models.{Schema => _, _}
import org.thp.scalligraph.query._
import org.thp.scalligraph.utils.{CaseClassType, RichType}
import play.api.Logger

import scala.reflect.runtime.{currentMirror => rm, universe => ru}

object SchemaGenerator {
  lazy val logger : Logger = Logger(getClass)

  lazy val orderEnumeration = EnumType(
    "Order",
    values = List(
      EnumValue("decr", value = org.apache.tinkerpop.gremlin.process.traversal.Order.desc),
      EnumValue("incr", value = org.apache.tinkerpop.gremlin.process.traversal.Order.asc),
      EnumValue("shuffle", value = org.apache.tinkerpop.gremlin.process.traversal.Order.shuffle)
    )
  )

  val outputType: ru.Type = ru.typeOf[Output[_]]

  case class FieldFilter[V](
      property: PublicProperty[Element, _, _],
      fieldSuffix: String,
      inputType: InputType[V],
      filter: V => GremlinScala[_] => GremlinScala[_]
  ) {
    lazy val fieldName: String = property.propertyName + fieldSuffix

    def inputField: InputField[Option[V]] = InputField(fieldName, OptionInputType(inputType))

    def getEntityFilter(value: V): EntityFilter = {
      val f: GremlinScala[_] => GremlinScala[_] = filter(value)
      new EntityFilter {
        override def apply[G](authContext: AuthContext)(raw: GremlinScala[G]): GremlinScala[G] = {
          val x: Seq[GremlinScala[G] => GremlinScala[_]] = property.definition.map(_.andThen(f)).asInstanceOf[Seq[GremlinScala[G] => GremlinScala[_]]]
          raw.or(x: _*)
        }
      }
    }
  }

  def stringFilters(p: PublicProperty[Element, _, _]) =
    List(
      FieldFilter[String](p, "", StringType, value => _.is(P.eq[String](value))),
      FieldFilter[String](p, "_not", StringType, value => _.is(P.neq(value))),
      FieldFilter[Seq[String]](p, "_in", ListInputType(StringType), value => _.is(P.within(value))),
      FieldFilter[Seq[String]](p, "_not_in", ListInputType(StringType), value => _.is(P.without(value))),
      FieldFilter[String](p, "_lt", StringType, value => _.is(P.lt(value))),
      FieldFilter[String](p, "_lte", StringType, value => _.is(P.lte(value))),
      FieldFilter[String](p, "_gt", StringType, value => _.is(P.gt(value))),
      FieldFilter[String](p, "_gte", StringType, value => _.is(P.gte(value))),
      FieldFilter[String](p, "_contains", StringType, value => _.is(InputFilter.stringContains(value))),
      FieldFilter[String](p, "_starts_with", StringType, value => _.is(InputFilter.stringStartsWith(value))),
      FieldFilter[String](p, "_ends_with", StringType, value => _.is(InputFilter.stringEndsWith(value).negate)),
      FieldFilter[String](p, "_not_starts_with", StringType, value => _.is(InputFilter.stringStartsWith(value))),
      FieldFilter[String](p, "_no_ends_with", StringType, value => _.is(InputFilter.stringEndsWith(value).negate))
    )

  def intFilters(p: PublicProperty[Element, _, _]) =
    List(
      FieldFilter[Int](p, "", IntType, value => _.is(P.eq[Int](value))),
      FieldFilter[Int](p, s"_not", IntType, value => _.is(P.neq(value))),
      FieldFilter[Seq[Int]](p, s"_in", ListInputType(IntType), value => _.is(P.within(value))),
      FieldFilter[Seq[Int]](p, s"_not_in", ListInputType(IntType), value => _.is(P.without(value))),
      FieldFilter[Int](p, s"_lt", IntType, value => _.is(P.lt(value))),
      FieldFilter[Int](p, s"_lte", IntType, value => _.is(P.lte(value))),
      FieldFilter[Int](p, s"_gt", IntType, value => _.is(P.gt(value))),
      FieldFilter[Int](p, s"_gte", IntType, value => _.is(P.gte(value)))
    )

  abstract class CacheFunction[T] extends (() => T) { lf =>
    def fn: T
    private lazy val value                      = fn
    override def apply(): T                     = value
    def andThen[U](f: T => U): CacheFunction[U] = CacheFunction[U](f(lf.value))
  }

  object CacheFunction {

    def sequence[T](s: Seq[CacheFunction[T]]): CacheFunction[Seq[T]] = new CacheFunction[Seq[T]] {
      override def fn: Seq[T] = s.map(_.apply())
    }

    def apply[T](f: => T): CacheFunction[T] = new CacheFunction[T] {
      override def fn: T = f
    }
  }

  class TypeCatalog[T] {
    private var content: List[(ru.Type, T)] = Nil

    def getOrElseUpdate(tpe: ru.Type)(value: T): T =
      content
        .find(_._1 =:= tpe)
        .map(_._2)
        .getOrElse {
          content ::= tpe -> value
          value
        }

    def +(entry: (ru.Type, T)): TypeCatalog[T] = {
      content ::= entry
      this
    }
  }

  def duplicate[A](value: A): A = value match {
    case step: Traversal => step.clone().asInstanceOf[A]
    case _               => value
  }

  def getScalarField(name: String, tpe: ru.Type): InputField[_] =
    if (tpe =:= ru.typeOf[String]) InputField(name, StringType)
    else if (tpe =:= ru.typeOf[Int]) InputField(name, IntType)
    else if (tpe =:= ru.typeOf[Long]) InputField(name, LongType)
    else if (tpe =:= ru.typeOf[Float]) InputField(name, FloatType)
    else if (tpe =:= ru.typeOf[Double]) InputField(name, FloatType) // TODO add DoubleType ?
    else if (tpe =:= ru.typeOf[Boolean]) InputField(name, BooleanType)
    else if (tpe =:= ru.typeOf[Date]) InputField(name, DateType)
    else throw InternalError(s"Type of $name ($tpe) is not scalar")

  def getField(tpe: ru.Type, query: ParamQuery[_])(
      implicit executor: QueryExecutor,
      objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]
  ): CacheFunction[Option[Field[AuthGraph, Any]]] = {
    val pq = query.asInstanceOf[ParamQuery[Any]]
    logger.debug(s"$tpe : query ${query.name} found, no param")
    getObject(query.toType(tpe)).andThen(_.map { o =>
      if (tpe =:= ru.typeOf[Graph])
        Field[AuthGraph, Any, Any, Any](query.name, o, resolve = ctx => pq((), ctx.ctx.graph, ctx.ctx.auth))
      else
        Field[AuthGraph, Any, Any, Any](query.name, o, resolve = ctx => pq((), duplicate(ctx.value), ctx.ctx.auth))
    })
  }

  def getParamField(tpe: ru.Type, query: ParamQuery[_], symbols: Seq[ru.Symbol])(
      implicit executor: QueryExecutor,
      objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]
  ): CacheFunction[Option[Field[AuthGraph, Any]]] = {
    val pq = query.asInstanceOf[ParamQuery[Any]]
    logger.debug(s"$tpe : query ${query.name} found, with param ${query.paramType}")
    val inputFields = symbols.map(s => getScalarField(s.name.decodedName.toString.trim, s.typeSignature)).toList
    val argName     = query.paramType.typeSymbol.name.decodedName.toString.trim
    val arg         = Argument(argName, InputObjectType(argName, inputFields)) // FIXME must build a case class of type tpe
    getObject(query.toType(tpe)).andThen(_.map({ o =>
      if (tpe =:= ru.typeOf[Graph])
        Field[AuthGraph, Any, Any, Any](query.name, o, arguments = List(arg), resolve = ctx => pq(ctx.arg(arg), ctx.ctx.graph, ctx.ctx.auth))
      else
        Field[AuthGraph, Any, Any, Any](query.name, o, arguments = List(arg), resolve = ctx => pq(ctx.arg(arg), duplicate(ctx.value), ctx.ctx.auth))
    }))
  }

  def getOutputFields(tpe: ru.Type)(
      implicit executor: QueryExecutor,
      objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]
  ): Seq[CacheFunction[Option[Field[AuthGraph, Any]]]] =
    executor
      .queries
      .find(_.checkFrom(tpe))
      .collectFirst {
        case q if q.toType(tpe) <:< outputType =>
          RichType.getTypeArgs(q.toType(tpe), outputType).head match {
            case CaseClassType(symbols @ _*) =>
              symbols.map { s =>
                getObject(s.typeSignature)
                  .andThen(
                    _.map(
                      o =>
                        Field[AuthGraph, Any, Any, Any](
                          s.name.toString,
                          o,
                          resolve = { ctx =>
                            val output = q
                              .asInstanceOf[Query]((), duplicate(ctx.value), ctx.ctx.auth) // TODO check if q requires param
                              .asInstanceOf[Output[_]]
                              .toOutput
                            output.getClass.getMethod(s.name.toString).invoke(output)
                          }
                        )
                    )
                  )
              }
          }
      }
      .getOrElse(Nil)

  def getObject(
      tpe: ru.Type
  )(implicit executor: QueryExecutor, objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]): CacheFunction[Option[OutputType[_]]] = {
    logger.debug(s"getObject($tpe)")
    objectCatalog.getOrElseUpdate(tpe) {
      if (tpe <:< ru.typeOf[Seq[_]]) // TODO add Set type ?
        getObject(RichType.getTypeArgs(tpe, ru.typeOf[Seq[_]]).head).andThen(_.map(ListType(_)))
      else if (tpe <:< ru.typeOf[Option[_]])
        getObject(RichType.getTypeArgs(tpe, ru.typeOf[Option[_]]).head).andThen(_.map(OptionType(_)))
      else {
        new CacheFunction[Option[OutputType[_]]] { current =>
          override def fn: Some[ObjectType[AuthGraph, Any]] = {
            val fields: Seq[CacheFunction[Option[Field[AuthGraph, Any]]]] = getQueryFields(tpe, current) ++
              executor.publicProperties.filter(_.traversalType =:= tpe).map(getPropertyFields(_)) ++
              getOutputFields(tpe) :+
              CacheFunction[Option[Field[AuthGraph, Any]]](Some(Field("_", OptionType(StringType), resolve = _ => None)))

            val objectName = tpe.typeArgs.map(typeName).mkString + typeName(tpe)
            Some(
              ObjectType(
                objectName,
                fieldsFn = CacheFunction.sequence(fields).andThen { l =>
                  val x = l.flatten.toList.groupBy(_.name).map(_._2.head)
                  logger.debug(s"fields of $objectName are: ${x.map(_.name).mkString(",")}")
                  x
                }
              )
            )
          }
        }
      }
    }
  }

  def getSortField(tpe: ru.Type, stepObjectType: OutputType[_])(implicit executor: QueryExecutor): Option[Field[AuthGraph, Any]] = {
    val objectName = tpe.typeSymbol.name.decodedName.toString.trim
    val inputFields = executor
      .publicProperties
      .filter(_.traversalType =:= tpe)
      .map(prop => InputField(prop.propertyName, OptionInputType(orderEnumeration)))
    if (inputFields.isEmpty) None
    else {
      val fromInput: FromInput[InputSort] = new FromInput[InputSort] {
        override val marshaller: ResultMarshaller = CoercedScalaResultMarshaller.default
        override def fromResult(node: marshaller.Node): InputSort = {
          val input = node
            .asInstanceOf[Map[String, Option[Any]]]
            .collect {
              case (name, Some(order)) => name -> org.apache.tinkerpop.gremlin.process.traversal.Order.valueOf(order.toString)
            }
            .toSeq
          InputSort(input: _*)
        }
      }
      val arg = Argument("sort", InputObjectType[InputSort](s"${objectName}Sort", inputFields))(
        fromInput.asInstanceOf[FromInput[InputSort @@ FromInput.InputObjectResult]],
        WithoutInputTypeTags.ioArgTpe[InputSort]
      )
      Some(
        Field[AuthGraph, Any, Any, Any](
          "sort",
          stepObjectType,
          arguments = List(arg),
          resolve = ctx =>
            Value(
              ctx
                .arg(arg)
                .apply(
                  executor.publicProperties,
                  rm.classSymbol(ctx.value.getClass).toType,
                  duplicate(ctx.value).asInstanceOf[ScalliSteps[_, _, _ <: AnyRef]],
                  ctx.ctx.auth
                )
            )
        )
      )
    }
  }

  def getFilterField(tpe: ru.Type, stepObjectType: OutputType[_])(implicit executor: QueryExecutor): Option[Field[AuthGraph, Any]] = {
    val objectName = tpe.typeSymbol.name.decodedName.toString.trim
    val fieldFilters: List[FieldFilter[_]] = executor
      .publicProperties
      .filter(_.traversalType =:= tpe)
      .flatMap {
        case prop if prop.mapping.domainTypeClass == classOf[String] => stringFilters(prop.asInstanceOf[PublicProperty[Element, _, _]])
        case prop if prop.mapping.domainTypeClass == classOf[Int]    => intFilters(prop.asInstanceOf[PublicProperty[Element, _, _]])
        case _                                                       => Nil
      }
    if (fieldFilters.isEmpty) None
    else {
      val inputFields = fieldFilters.map(_.inputField)

      val fromInput: FromInput[EntityFilter] = new FromInput[EntityFilter] {
        override val marshaller: ResultMarshaller = CoercedScalaResultMarshaller.default
        override def fromResult(node: marshaller.Node): EntityFilter =
          node
            .asInstanceOf[Map[String, Option[Any]]]
            .flatMap {
              case (name, Some(value)) =>
                fieldFilters.find(_.fieldName == name).map {
                  case ff: FieldFilter[v] => ff.getEntityFilter(value.asInstanceOf[v])
                }
              case _ => None
            }
            .toSeq
            .reduce(_ and _)
      }
      val arg = Argument("filter", InputObjectType[EntityFilter](s"${objectName}Filter", inputFields))(
        fromInput.asInstanceOf[FromInput[EntityFilter @@ FromInput.InputObjectResult]],
        WithoutInputTypeTags.ioArgTpe[EntityFilter]
      )
      Some(
        Field[AuthGraph, Any, Any, Any](
          "filter",
          stepObjectType,
          arguments = List(arg),
          resolve = ctx =>
            Value(
              ctx
                .arg(arg)
                .apply(ctx.ctx.auth, duplicate(ctx.value).asInstanceOf[ScalliSteps[_, _, _ <: AnyRef]])
            )
        )
      )
    }
  }

  def getQueryFields(tpe: ru.Type, currentObject: CacheFunction[Option[OutputType[_]]])(
      implicit executor: QueryExecutor,
      objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]
  ): Seq[CacheFunction[Option[Field[AuthGraph, Any]]]] =
    executor
      .allQueries
      .filter(_.checkFrom(tpe))
      .flatMap {
        case q if q.toType(tpe) <:< outputType => Seq.empty
        case _: SortQuery =>
          logger.debug(s"$tpe : add field sort")
          Seq(currentObject.andThen(_.flatMap(o => getSortField(tpe, o))))
        case _: FilterQuery =>
          logger.debug(s"$tpe : add field filter")
          Seq(currentObject.andThen(_.flatMap(o => getFilterField(tpe, o))))
        case _: AggregationQuery => // TODO add support of aggregation query
          Seq.empty
        case q =>
          logger.debug(s"$tpe : add field ${q.name}")
          q.paramType match {
            case t if t =:= ru.typeOf[Unit]  => Seq(getField(tpe, q))
            case CaseClassType(symbols @ _*) => Seq(getParamField(tpe, q, symbols))
          }
      }

  def getPropertyFields[A <: Element, B](property: PublicProperty[A, _, B])(
      implicit executor: QueryExecutor,
      objectCatalog: TypeCatalog[CacheFunction[Option[OutputType[_]]]]
  ): CacheFunction[Option[Field[AuthGraph, Any]]] = {
    val t          = rm.classSymbol(property.mapping.domainTypeClass).toType // FIXME domainType or graphType ?
    val optionType = ru.typeOf[Option[_]].typeConstructor
    val seqType    = ru.typeOf[Seq[_]].typeConstructor
    val propertyType = property.mapping.cardinality match {
      case MappingCardinality.single => t
      case MappingCardinality.option => ru.appliedType(optionType, t)
      case MappingCardinality.list   => ru.appliedType(seqType, t)
      case MappingCardinality.set    => ru.appliedType(seqType, t)
    }
    val traversalType   = ru.appliedType(ru.typeOf[Traversal[Any]].typeConstructor, propertyType)
    val objectType = getObject(traversalType).apply().get
    CacheFunction(
      Some(
        Field[AuthGraph, ScalliSteps[A, _, _ <: AnyRef], Traversal[B], Any]( // FIXME should be ElementStep instead of ScalliSteps. Property can be applied only on element step.
          property.propertyName,
          objectType,
          resolve = ctx =>
            Value(
              duplicate(ctx.value)                       // ScalliSteps[EndDomain, EndGraph => B, ThisStep <: AnyRef]
                .asInstanceOf[BaseElementSteps[_, A, _]] // ElementSteps[E <: Product: ru.TypeTag, EndGraph <: Element, ThisStep <: Traversal.V[Element][E, EndGraph, ThisStep]] ScalliSteps[E with Entity, EndGraph, ThisStep]
                .getByIds[B](ctx.ctx.auth, property)
            )
        ) // def get[A](authContext: AuthContext, property: PublicProperty[EndGraph, _, A]): Traversal[A] = {
          .asInstanceOf[Field[AuthGraph, Any]]
      )
    )
  }

  def typeName(tpe: ru.Type): String = {
    import ru._
    tpe match {
      case RefinedType(cl :: _, _) => symbolName(cl.typeSymbol)
      case cl                      => symbolName(cl.typeSymbol)
    }
  }

  def symbolName(s: ru.Symbol): String = s.name.decodedName.toString.trim

  def apply(executor: QueryExecutor): Schema[AuthGraph, Unit] = {
    logger.info(s"Generate GraphQL schema from ${executor.getClass}")

    val objectCatalog = new TypeCatalog[CacheFunction[Option[OutputType[_]]]] +
      (ru.typeOf[String]  -> CacheFunction(Some(StringType))) +
      (ru.typeOf[Int]     -> CacheFunction(Some(IntType))) +
      (ru.typeOf[Long]    -> CacheFunction(Some(LongType))) +
      (ru.typeOf[Float]   -> CacheFunction(Some(FloatType))) +
      (ru.typeOf[Double]  -> CacheFunction(Some(FloatType))) +
      (ru.typeOf[Boolean] -> CacheFunction(Some(BooleanType))) +
      (ru.typeOf[Date]    -> CacheFunction(Some(DateType)))
    val schemaObjectType = getObject(ru.typeOf[Graph])(executor, objectCatalog).apply().get.asInstanceOf[ObjectType[AuthGraph, Unit]]
    Schema(schemaObjectType)
  }
}
