package org.thp.scalligraph.models

import javax.inject.{Inject, Provider, Singleton}
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.traversal.Graph
import play.api.Logger

import scala.collection.immutable
import scala.util.{Success, Try}

case class InitialValue[V <: Product](model: Model.Vertex[V], value: V) {

  def create()(implicit graph: Graph, authContext: AuthContext): V with Entity =
    graph.db.createVertex[V](graph, authContext, model, value)
}

case class SchemaStatus(name: String, currentVersion: Int, expectedVersion: Int, error: Option[Throwable])

trait UpdatableSchema extends Schema {
  val authContext: AuthContext
  val operations: Operations
  lazy val name: String                           = operations.schemaName
  def schemaStatus: Option[SchemaStatus]          = _updateStatus
  private var _updateStatus: Option[SchemaStatus] = None
  def update(db: Database): Try[Unit] = {
    val result = operations.execute(db, this)(authContext)
    _updateStatus = Some(SchemaStatus(name, db.version(name), operations.operations.length + 1, result.fold(Some(_), _ => None)))
    result
  }
}

trait Schema { schema =>
  def modelList: Seq[Model]
  def initialValues: Seq[InitialValue[_]]                                            = Nil
  final def getModel(label: String): Option[Model]                                   = modelList.find(_.label == label)
  def init(db: Database)(implicit graph: Graph, authContext: AuthContext): Try[Unit] = Success(())

  def +(other: Schema): Schema =
    new Schema {
      override def modelList: Seq[Model]                                                          = schema.modelList ++ other.modelList
      override def initialValues: Seq[InitialValue[_]]                                            = schema.initialValues ++ other.initialValues
      override def init(db: Database)(implicit graph: Graph, authContext: AuthContext): Try[Unit] = schema.init(db).flatMap(_ => other.init(db))
    }
}

object Schema {

  def empty: Schema =
    new Schema {
      override def modelList: Seq[Model] = Nil
    }
}

@Singleton
class GlobalSchema @Inject() (schemas: immutable.Set[UpdatableSchema]) extends Provider[Schema] {
  lazy val logger: Logger = Logger(getClass)
  lazy val schema: Schema = {
    logger.debug(s"Build global schema from ${schemas.map(_.getClass.getSimpleName).mkString("+")}")
    schemas.reduceOption[Schema](_ + _).getOrElse(Schema.empty)
  }
  override def get(): Schema = schema
}
