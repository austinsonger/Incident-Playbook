package org.thp.scalligraph.query

import org.apache.tinkerpop.gremlin.process.traversal.{Order, P}
import org.apache.tinkerpop.gremlin.structure.Vertex
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers.{FPath, FieldsParser, Renderer}
import org.thp.scalligraph.models.Mapping
import org.thp.scalligraph.query.PredicateOps.PredicateOpsDefs
import org.thp.scalligraph.traversal.TraversalOps.TraversalOpsDefs
import org.thp.scalligraph.traversal.{Converter, Graph, IdentityConverter, Traversal}
import play.api.libs.json.{JsObject, JsValue}

import scala.reflect.runtime.{universe => ru}
import scala.util.Try

///**
//  * A property that can be handled by API
//  * @param isApplicableFn indicate if this property exists in this type
//  * @param propertyName name of the property
//  * @param mapping used in aggregation to render this property
//  * @param definition query used to select the property value
//  * @param fieldsParser used to build filter, from input fields
//  * @param updateFieldsParser used to update the property
//  * @param filterSelect query used to apply filter
//  * @param filterConverter transform the input filter to match the filter select
//  * @tparam P
//  * @tparam U
//  */
case class PublicProperty(
    typeFilter: TypeFilter,
    propertyName: String,
    mapping: Mapping[_, _, _],
    select: TraversalSelect,
    updateFieldsParser: Option[FieldsParser[PropertyUpdater]],
    filter: PropertyFilter[_],
    sort: PropertyOrder
) {
  def toJson[A](value: A): JsValue = mapping.selectRenderer.asInstanceOf[Renderer[A]].toJson(value)
}

trait TypeFilter {
  def apply(tpe: ru.Type): Boolean
}

class TraversalTypeFilter[E <: Product: ru.TypeTag] extends TypeFilter {
  val refType: ru.Type                    = ru.typeOf[Traversal.V[E]]
  override def apply(t: ru.Type): Boolean = t <:< refType
}

trait TraversalSelect {
  def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext): Traversal.Unk
//  def widen: TraversalSelect = this.asInstanceOf[TraversalSelect[Any]]
}

class FieldSelect(fieldName: String) extends TraversalSelect {
  override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext): Traversal.Unk =
    traversal.onRawMap[Any, Any, IdentityConverter[Any]](_.values[Any](fieldName))(Converter.identity)
}

trait PropertyFilter[M] {
  val fieldsParser: FieldsParser[M]
  def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, predicate: P[_]): Traversal.Unk
  def existenceTest(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, exist: Boolean): Traversal.Unk
}

class FieldPropertyFilter[E <: Product, D](fieldName: String, mapping: Mapping[_, D, _])(implicit val fieldsParser: FieldsParser[D])
    extends PropertyFilter[D] {
  override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, predicate: P[_]): Traversal.Unk =
    traversal.onRaw(
      _.has(
        fieldName,
        predicate.mapPred(v => mapping.asInstanceOf[Mapping[Any, Any, Any]].reverse(v), traversal.graph.db.mapPredicate[Any])
      )
    )
  override def existenceTest(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, exist: Boolean): Traversal.Unk =
    if (exist) traversal.onRaw(_.has(fieldName))
    else traversal.onRaw(_.hasNot(fieldName))
}

class TraversalPropertyFilter[D](select: TraversalSelect, mapping: Mapping[_, D, _])(implicit val fieldsParser: FieldsParser[D])
    extends PropertyFilter[D] {
  override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, predicate: P[_]): Traversal.Unk =
    traversal.filter(t =>
      select(path, t, authContext).is(
        predicate.mapPred(v => mapping.asInstanceOf[Mapping[Any, Any, Any]].reverse(v), traversal.graph.db.mapPredicate)
      )
    )
  override def existenceTest(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, exist: Boolean): Traversal.Unk =
    if (exist) traversal.filter(t => select(path, t, authContext))
    else traversal.filterNot(t => select(path, t, authContext))
}

trait PropertyOrder {
  def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, order: Order): Traversal.Unk
}

class FieldPropertyOrder(fieldName: String) extends PropertyOrder {
  override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, order: Order): Traversal.Unk =
    traversal.onRaw(_.by(fieldName, order))
}

class TraversalPropertyOrder(select: TraversalSelect) extends PropertyOrder {
  override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, order: Order): Traversal.Unk =
    traversal.onRaw(_.by(select(path, traversal.start, authContext).raw, order))
}

object PropertyUpdater {

  def apply[D, V](fieldsParser: FieldsParser[V], propertyName: String)(
      f: (FPath, V, Vertex, Graph, AuthContext) => Try[JsObject]
  ): FieldsParser[PropertyUpdater] =
    new FieldsParser(
      fieldsParser.formatName,
      fieldsParser.acceptedInput.map(propertyName + "/" + _),
      {
        case (path, field) =>
          fieldsParser(path, field).map(fieldValue =>
            new PropertyUpdater(propertyName /: path, fieldValue) {

              override def apply(vertex: Vertex, graph: Graph, authContext: AuthContext): Try[JsObject] =
                f(path, fieldValue, vertex, graph, authContext)
            }
          )
      }
    )

  def apply(path: FPath, value: Any)(
      f: (Vertex, Graph, AuthContext) => Try[JsObject]
  ): PropertyUpdater =
    new PropertyUpdater(path, value) {
      override def apply(v: Vertex, graph: Graph, authContext: AuthContext): Try[JsObject] = f(v, graph, authContext)
    }

  def unapply(updater: PropertyUpdater): Option[(FPath, Any, (Vertex, Graph, AuthContext) => Try[JsObject])] =
    Some((updater.path, updater.value, updater.apply))
}

abstract class PropertyUpdater(val path: FPath, val value: Any) extends ((Vertex, Graph, AuthContext) => Try[JsObject]) {
  override def toString(): String =
    s"PropertyUpdater($path, $value)"
}

class PublicProperties(private val map: Map[String, Seq[PublicProperty]]) {
  def get[V, U](propertyName: String): Option[PublicProperty] =
    map.get(propertyName).flatMap(_.headOption)
  def get[V, U](propertyName: String, tpe: ru.Type): Option[PublicProperty] =
    map.get(propertyName).flatMap(_.find(_.typeFilter(tpe)))
  def get[V, U](propertyPath: FPath, tpe: ru.Type): Option[PublicProperty] =
    get[V, U](propertyPath.toString, tpe) orElse propertyPath.headOption.flatMap(get[V, U](_, tpe))

  def list: Seq[PublicProperty] = map.flatMap(_._2.headOption).toSeq
  def :+[V, U](property: PublicProperty): PublicProperties =
    new PublicProperties(map + (property.propertyName -> (map.getOrElse(property.propertyName, Nil) :+ property)))
  def ++(properties: PublicProperties): PublicProperties = {
    val newMap = (map.keySet ++ properties.map.keySet).map(k => k -> (map.getOrElse(k, Nil) ++ properties.map.getOrElse(k, Nil))).toMap
    new PublicProperties(newMap)
  }
}

object PublicProperties {
  def empty: PublicProperties = new PublicProperties(Map.empty)
}
