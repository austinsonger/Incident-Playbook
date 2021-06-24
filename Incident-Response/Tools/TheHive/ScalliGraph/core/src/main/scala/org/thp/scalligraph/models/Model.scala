package org.thp.scalligraph.models

import org.apache.tinkerpop.gremlin.structure.{Edge, Element, Vertex}
import org.thp.scalligraph.`macro`.ModelMacro
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Graph}
import org.thp.scalligraph.{EntityId, NotFoundError}

import java.util.Date
import scala.annotation.StaticAnnotation
import scala.collection.JavaConverters._
import scala.language.experimental.macros

class Readonly extends StaticAnnotation

object IndexType extends Enumeration {
  val basic, standard, unique, fulltext, fulltextOnly = Value
}
class DefineIndex(indexType: IndexType.Value, fields: String*) extends StaticAnnotation

trait HasModel {
  val model: Model
}

trait Entity { _: Product =>
  def _id: EntityId
  def _label: String
  def _createdBy: String
  def _updatedBy: Option[String]
  def _createdAt: Date
  def _updatedAt: Option[Date]
}

object Model {
  type Base[E0 <: Product] = Model {
    type E = E0
  }

  type Vertex[E0 <: Product] = VertexModel {
    type E = E0
  }

  type Edge[E0 <: Product] = EdgeModel {
    type E = E0
  }

  def buildVertexModel[E <: Product]: Model.Vertex[E] =
    macro ModelMacro.mkVertexModel[E]

  def buildEdgeModel[E <: Product]: Model.Edge[E] =
    macro ModelMacro.mkEdgeModel[E]

  def printElement(e: Element): String =
    e + e
      .properties[Any]()
      .asScala
      .map(p => s"\n - ${p.key()} = ${p.orElse("<no value>")}")
      .mkString

  implicit def vertex[E <: Product]: Vertex[E] = macro ModelMacro.getModel[E]
  implicit def edge[E <: Product]: Edge[E] = macro ModelMacro.getModel[E]
}

abstract class Model {
  type E <: Product
  type EEntity = E with Entity
  type ElementType <: Element

  val label: String

  val indexes: Seq[(IndexType.Value, Seq[String])]

  def get(id: EntityId)(implicit graph: Graph): ElementType
  val fields: Map[String, Mapping[_, _, _]]
  def addEntity(e: E, entity: Entity): EEntity
  val converter: Converter[EEntity, ElementType]
}

abstract class VertexModel extends Model {
  override type ElementType = Vertex

  val initialValues: Seq[E]                  = Nil
  def getInitialValues: Seq[InitialValue[E]] = initialValues.map(iv => InitialValue(this.asInstanceOf[Model.Vertex[E]], iv))

  def create(e: E)(implicit graph: Graph): Vertex

  override def get(id: EntityId)(implicit graph: Graph): Vertex =
    graph.V(label, id).headOption.getOrElse(throw NotFoundError(s"Vertex $id not found"))
}

abstract class EdgeModel extends Model {
  override type ElementType = Edge

  def create(e: E, from: Vertex, to: Vertex)(implicit graph: Graph): Edge

  override def get(id: EntityId)(implicit graph: Graph): Edge =
    graph.E(label, id).headOption.getOrElse(throw NotFoundError(s"Edge $id not found"))
}
