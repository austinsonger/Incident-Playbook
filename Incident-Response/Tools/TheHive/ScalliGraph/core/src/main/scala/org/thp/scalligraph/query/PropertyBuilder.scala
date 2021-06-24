package org.thp.scalligraph.query

import org.apache.tinkerpop.gremlin.process.traversal.P
import org.apache.tinkerpop.gremlin.structure.Vertex
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.controllers.{FPath, FieldsParser}
import org.thp.scalligraph.models.Mapping
import org.thp.scalligraph.traversal.{Graph, Traversal}
import play.api.libs.json.{JsObject, Json}

import scala.reflect.runtime.{universe => ru}
import scala.util.{Success, Try}

class PropertyBuilder[E <: Product, M, D](typeFilter: TypeFilter, propertyName: String, mapping: Mapping[M, D, Traversal.UnkG]) {

  def field(implicit fieldsParser: FieldsParser[D]) =
    new FieldBasedProperty(typeFilter, propertyName, mapping, propertyName, new FieldPropertyFilter[E, D](propertyName, mapping))

  def rename(newName: String)(implicit fieldsParser: FieldsParser[D]) =
    new FieldBasedProperty(typeFilter, propertyName, mapping, newName, new FieldPropertyFilter[E, D](newName, mapping))

  def select(definition: Traversal.V[E] => Traversal[D, _, _])(implicit fieldsParser: FieldsParser[D]): TraversalBasedProperty = {
    val select: TraversalSelect = (_: FPath, t: Traversal.Unk, _: AuthContext) =>
      definition(t.asInstanceOf[Traversal.V[E]]).asInstanceOf[Traversal.Unk]
    new TraversalBasedProperty(
      typeFilter,
      propertyName,
      mapping,
      select,
      new TraversalPropertyFilter[D](select, mapping)
    )
  }

  def authSelect(definition: (Traversal.V[E], AuthContext) => Traversal[D, _, _])(implicit fieldsParser: FieldsParser[D]): TraversalBasedProperty = {
    val select: TraversalSelect = (_: FPath, t: Traversal.Unk, a: AuthContext) =>
      definition(t.asInstanceOf[Traversal.V[E]], a).asInstanceOf[Traversal.Unk]
    new TraversalBasedProperty(
      typeFilter,
      propertyName,
      mapping,
      select,
      new TraversalPropertyFilter[D](select, mapping)
    )
  }

  def subSelect(definition: (FPath, Traversal.V[E]) => Traversal[D, _, _])(implicit fieldsParser: FieldsParser[D]): TraversalBasedProperty = {
    val select: TraversalSelect = (p: FPath, t: Traversal.Unk, _: AuthContext) =>
      definition(p, t.asInstanceOf[Traversal.V[E]]).asInstanceOf[Traversal.Unk]
    new TraversalBasedProperty(
      typeFilter,
      propertyName,
      mapping,
      select,
      new TraversalPropertyFilter[D](select, mapping)
    )
  }

  class FieldBasedProperty(typeFilter: TypeFilter, propertyName: String, mapping: Mapping[M, D, _], fieldName: String, filter: PropertyFilter[D]) {
    def readonly: PublicProperty =
      PublicProperty(typeFilter, propertyName, mapping, new FieldSelect(fieldName), None, filter, new FieldPropertyOrder(fieldName))
    def updatable(implicit updateFieldsParser: FieldsParser[M]): PublicProperty =
      PublicProperty(
        typeFilter,
        propertyName,
        mapping,
        new FieldSelect(fieldName),
        Some(PropertyUpdater(updateFieldsParser, propertyName) { (_: FPath, value: M, vertex: Vertex, _: Graph, _: AuthContext) =>
          mapping.setProperty(vertex, fieldName, value)
          Success(Json.obj(fieldName -> mapping.getRenderer.toJson(value)))
        }),
        filter,
        new FieldPropertyOrder(fieldName)
      )
    def custom(
        f: (FPath, M, Vertex, Graph, AuthContext) => Try[JsObject]
    )(implicit updateFieldsParser: FieldsParser[M]): PublicProperty =
      PublicProperty(
        typeFilter,
        propertyName,
        mapping,
        new FieldSelect(fieldName),
        Some(PropertyUpdater(updateFieldsParser, propertyName)(f)),
        filter,
        new FieldPropertyOrder(fieldName)
      )
  }

  class TraversalBasedProperty(
      typeFilter: TypeFilter,
      propertyName: String,
      mapping: Mapping[M, D, _],
      select: TraversalSelect,
      filter: PropertyFilter[_]
  ) {
    def filter[A](f: (FPath, Traversal.V[E], AuthContext, Either[Boolean, P[A]]) => Traversal.V[E])(implicit fp: FieldsParser[A]) =
      new TraversalBasedProperty(
        typeFilter,
        propertyName,
        mapping,
        select,
        new PropertyFilter[A] {
          override val fieldsParser: FieldsParser[A] = fp
          override def apply(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, predicate: P[_]): Traversal.Unk =
            f(
              path,
              traversal.asInstanceOf[Traversal.V[E]],
              authContext,
              Right(predicate.asInstanceOf[P[A]])
            ).asInstanceOf[Traversal.Unk]

          override def existenceTest(path: FPath, traversal: Traversal.Unk, authContext: AuthContext, exist: Boolean): Traversal.Unk =
            f(path, traversal.asInstanceOf[Traversal.V[E]], authContext, Left(exist)).asInstanceOf[Traversal.Unk]

        }
      )

    def readonly: PublicProperty =
      PublicProperty(typeFilter, propertyName, mapping, select, None, filter, new TraversalPropertyOrder(select))
    def custom(
        f: (FPath, M, Vertex, Graph, AuthContext) => Try[JsObject]
    )(implicit updateFieldsParser: FieldsParser[M]): PublicProperty =
      PublicProperty(
        typeFilter,
        propertyName,
        mapping,
        select,
        Some(PropertyUpdater(updateFieldsParser, propertyName)(f)),
        filter,
        new TraversalPropertyOrder(select)
      )
  }
}

class PublicPropertyListBuilder[E <: Product](typeFilter: TypeFilter, properties: PublicProperties) {
  def build: PublicProperties = properties

  def property[M, D](
      name: String,
      mapping: Mapping[M, D, _]
  )(prop: PropertyBuilder[E, M, D] => PublicProperty): PublicPropertyListBuilder[E] =
    new PublicPropertyListBuilder[E](
      typeFilter,
      properties :+ prop(new PropertyBuilder[E, M, D](typeFilter, name, mapping.asInstanceOf[Mapping[M, D, Traversal.UnkG]]))
    )
}

object PublicPropertyListBuilder {
  def apply[E <: Product: ru.TypeTag]: PublicPropertyListBuilder[E] =
    forType[E](new TraversalTypeFilter[E])
  def forType[E <: Product](typeFilter: TypeFilter): PublicPropertyListBuilder[E] =
    new PublicPropertyListBuilder[E](typeFilter, PublicProperties.empty)
}
