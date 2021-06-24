package org.thp.scalligraph.`macro`

import org.thp.scalligraph.models.Model

import scala.reflect.macros.blackbox

class ModelMacro(val c: blackbox.Context) extends MappingMacroHelper with IndexMacro with MacroLogger {

  import c.universe._

  def getModel[E <: Product: WeakTypeTag]: Tree = {
    val companion = weakTypeOf[E].typeSymbol.companion
    q"$companion.model"
  }

  /**
    * Create a model from entity type e
    */
  def mkVertexModel[E <: Product: WeakTypeTag]: Expr[Model.Vertex[E]] = {
    val entityType: Type = weakTypeOf[E]
    initLogger(entityType.typeSymbol)
    debug(s"Building vertex model for $entityType")
    val label: String      = entityType.toString.split("\\.").last
    val mappings           = getEntityMappings[E]
    val mappingDefinitions = mappings.map(m => q"val ${m.valName} = ${m.definition}")
    val fieldMap           = mappings.map(m => q"${m.name} -> ${m.valName}")
    val setProperties      = mappings.map(m => q"${m.valName}.setProperty(vertex, ${m.name}, e.${TermName(m.name)})")
    val initialValues =
      try {
        val entityTypeModule = entityType.typeSymbol.companion
        if (entityTypeModule.typeSignature.members.exists(_.name.toString == "initialValues"))
          q"$entityTypeModule.initialValues"
        else q"Nil"
      } catch {
        case e: Throwable =>
          error(s"Unable to get initialValues from $label: $e")
          q"Nil"
      }
    val domainBuilder = mappings.map(m => q"${m.valName}.getProperty(element, ${m.name})")

    val model = c.Expr[Model.Vertex[E]](q"""
      import java.util.Date
      import scala.concurrent.{ExecutionContext, Future}

      import scala.util.{Failure, Try}
      import org.apache.tinkerpop.gremlin.structure.Vertex
      import org.thp.scalligraph.{EntityId, InternalError}
      import org.thp.scalligraph.controllers.FPath
      import org.thp.scalligraph.models.{Database, Entity, IndexType, Mapping, Model, UMapping, VertexModel}
      import org.thp.scalligraph.traversal.{Converter, Graph}

      new VertexModel {
        override type E = $entityType

        override val label: String = $label

        override val initialValues: Seq[E] = $initialValues
        override val indexes: Seq[(IndexType.Value, Seq[String])] = ${getIndexes[E]}

        ..$mappingDefinitions

        override def create(e: E)(implicit graph: Graph): Vertex = {
          val vertex = graph.addVertex(label)
          ..$setProperties
          vertex
        }

        override val fields: Map[String, Mapping[_, _, _]] = Map(..$fieldMap)

        override val converter: Converter[EEntity, ElementType] = (element: ElementType) => new $entityType(..$domainBuilder) with Entity {
          val _id        = EntityId(element.id())
          val _label     = $label
          val _createdAt = UMapping.date.getProperty(element, "_createdAt")
          val _createdBy = UMapping.string.getProperty(element, "_createdBy")
          val _updatedAt = UMapping.date.optional.getProperty(element, "_updatedAt")
          val _updatedBy = UMapping.string.optional.getProperty(element, "_updatedBy")
        }

        override def addEntity(e: $entityType, entity: Entity): EEntity = new $entityType(..${mappings
      .map(m => q"e.${TermName(m.name)}")}) with Entity {
          override def _id: EntityId              = entity._id
          override def _label: String             = entity._label
          override def _createdBy: String         = entity._createdBy
          override def _updatedBy: Option[String] = entity._updatedBy
          override def _createdAt: Date           = entity._createdAt
          override def _updatedAt: Option[Date]   = entity._updatedAt
        }
      }
      """)
    ret(s"Vertex model $entityType", model)
  }

  def mkEdgeModel[E <: Product: WeakTypeTag]: Expr[Model.Edge[E]] = {
    val entityType: Type = weakTypeOf[E]
    initLogger(entityType.typeSymbol)
    debug(s"Building vertex model for $entityType")
    val label: String      = entityType.toString.split("\\.").last
    val mappings           = getEntityMappings[E]
    val mappingDefinitions = mappings.map(m => q"val ${m.valName} = ${m.definition}")
    val fieldMap           = mappings.map(m => q"${m.name} -> ${m.valName}")
    val setProperties      = mappings.map(m => q"${m.valName}.setProperty(edge, ${m.name}, e.${TermName(m.name)})")
    val getProperties      = mappings.map(m => q"${m.valName}.getProperty(edge, ${m.name})")
    val model              = c.Expr[Model.Edge[E]](q"""
      import java.util.Date
      import scala.concurrent.{ExecutionContext, Future}
      import scala.util.Try
      import org.apache.tinkerpop.gremlin.structure.{Edge, Vertex}
      import org.thp.scalligraph.traversal.Graph

      import org.thp.scalligraph.{EntityId, InternalError}
      import org.thp.scalligraph.controllers.FPath
      import org.thp.scalligraph.models.{Database, EdgeModel, Entity, IndexType, Mapping, MappingCardinality, Model, UMapping}
      import org.thp.scalligraph.traversal.Converter

      new EdgeModel {
        override type E = $entityType

        override val label: String = $label

        override val indexes: Seq[(IndexType.Value, Seq[String])] = ${getIndexes[E]}

        ..$mappingDefinitions

        override def create(e: E, from: Vertex, to: Vertex)(implicit graph: Graph): Edge = {
          val edge = from.addEdge(label, to)
          ..$setProperties
          edge
        }

        override val fields: Map[String, Mapping[_, _, _]] = Map(..$fieldMap)

        override val converter: Converter[EEntity, ElementType] = (edge: ElementType) => new $entityType(..$getProperties) with Entity {
          val _id        = EntityId(edge.id())
          val _label     = $label
          val _createdAt = UMapping.date.getProperty(edge, "_createdAt")
          val _createdBy = UMapping.string.getProperty(edge, "_createdBy")
          val _updatedAt = UMapping.date.optional.getProperty(edge, "_updatedAt")
          val _updatedBy = UMapping.string.optional.getProperty(edge, "_updatedBy")
        }

        override def addEntity(e: $entityType, entity: Entity): EEntity =
          new $entityType(..${mappings.map(m => q"e.${TermName(m.name)}")}) with Entity {
            override def _id: EntityId              = entity._id
            override def _label: String             = entity._label
            override def _createdBy: String         = entity._createdBy
            override def _updatedBy: Option[String] = entity._updatedBy
            override def _createdAt: Date           = entity._createdAt
            override def _updatedAt: Option[Date]   = entity._updatedAt
          }
      }
      """)
    ret(s"Edge model $entityType", model)
  }
}
