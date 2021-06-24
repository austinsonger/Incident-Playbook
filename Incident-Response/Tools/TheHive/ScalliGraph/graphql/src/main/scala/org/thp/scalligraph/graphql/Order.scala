package org.thp.scalligraph.graphql


import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.query.PublicProperty

import scala.reflect.{ClassTag, classTag}
import scala.util.Try

object Order {

  lazy val orderEnumeration = EnumType(
    "Order",
    values = List(
      EnumValue("decr", value = org.apache.tinkerpop.gremlin.process.traversal.Order.desc),
      EnumValue("incr", value = org.apache.tinkerpop.gremlin.process.traversal.Order.asc),
      EnumValue("shuffle", value = org.apache.tinkerpop.gremlin.process.traversal.Order.shuffle)
    )
  )

  def getField[S <: Traversal.V[Scalli][_, E, S]: ClassTag, E <: Element](
      properties: List[PublicProperty[_ <: Element, _, _]],
      traversalType: OutputType[S]
  ): Option[Field[AuthGraph, S]] = {

    case class FieldOrder[A <: Element](property: PublicProperty[A, _, _], order: org.apache.tinkerpop.gremlin.process.traversal.Order) {
      def orderBy(authContext: AuthContext): OrderBy[_] = By(property.select(__[A], authContext), order)
    }

    val fields = properties.map(p => InputField(p.propertyName, OptionInputType(orderEnumeration)))
    val inputType: InputObjectType[Seq[FieldOrder[_]]] =
      InputObjectType[Seq[FieldOrder[_]]](classTag[S].runtimeClass.getSimpleName + "Order", fields)

    val fromInput: FromInput[Seq[FieldOrder[_]]] = new FromInput[Seq[FieldOrder[_]]] {
      override val marshaller: ResultMarshaller = CoercedScalaResultMarshaller.default

      override def fromResult(node: marshaller.Node): Seq[FieldOrder[_]] = {
        val input = node.asInstanceOf[Map[String, Option[Any]]]
        for {
          (key, valueMaybe) <- input.toSeq
          value             <- valueMaybe
          order             <- Try(org.apache.tinkerpop.gremlin.process.traversal.Order.valueOf(value.toString)).toOption
          property          <- properties.find(_.propertyName == key)
        } yield FieldOrder(property, order)
      }
    }
    val arg = Argument("order", inputType)(
      fromInput.asInstanceOf[FromInput[Seq[FieldOrder[_]] @@ FromInput.InputObjectResult]],
      WithoutInputTypeTags.ioArgTpe[Seq[FieldOrder[_]]]
    )
    Some(
      Field[AuthGraph, S, S, S](
        "order",
        traversalType,
        arguments = List(arg),
        resolve = ctx => ctx.value.sort(ctx.arg(arg).map(_.orderBy(ctx.ctx.auth)): _*)
      )
    )
  }
}
