package org.thp.scalligraph.models

import org.apache.tinkerpop.gremlin.structure.Vertex
import org.thp.scalligraph.InternalError
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{Converter, Traversal}
import play.api.Logger

import scala.reflect.{classTag, ClassTag}
import scala.util.{Failure, Success, Try}

sealed trait Operation

case class AddVertexModel(label: String)                                                                                     extends Operation
case class AddEdgeModel(label: String, mapping: Map[String, Mapping[_, _, _]])                                               extends Operation
case class AddProperty(model: String, propertyName: String, mapping: Mapping[_, _, _])                                       extends Operation
case class RemoveProperty(model: String, propertyName: String, usedOnlyByThisModel: Boolean)                                 extends Operation
case class UpdateGraph(model: String, update: Traversal.Identity[Vertex] => Try[Unit], comment: String, pageSize: Int = 100) extends Operation
case class AddIndex(model: String, indexType: IndexType.Value, properties: Seq[String])                                      extends Operation
object RebuildIndexes                                                                                                        extends Operation
object NoOperation                                                                                                           extends Operation
case class RemoveIndex(model: String, indexType: IndexType.Value, fields: Seq[String])                                       extends Operation
case class DBOperation[DB <: Database: ClassTag](comment: String, op: DB => Try[Unit]) extends Operation {
  def apply(db: Database): Try[Unit] =
    if (classTag[DB].runtimeClass.isAssignableFrom(db.getClass))
      op(db.asInstanceOf[DB])
    else
      Success(())
}

object Operations {
  def apply(schemaName: String): Operations = new Operations(schemaName, Nil)
}

case class Operations private (schemaName: String, operations: Seq[Operation]) {
  lazy val logger: Logger                               = Logger(getClass)
  val lastVersion: Int                                  = operations.length + 2
  private def addOperations(op: Operation*): Operations = copy(operations = operations ++ op)
  def addVertexModel[T](label: String): Operations =
    addOperations(AddVertexModel(label))
  def addEdgeModel[T](label: String, properties: Seq[String])(implicit mapping: UMapping[T]): Operations =
    addOperations(AddEdgeModel(label, properties.map(p => p -> mapping.toMapping).toMap))
  def addProperty[T](model: String, propertyName: String)(implicit mapping: UMapping[T]): Operations =
    addOperations(AddProperty(model, propertyName, mapping.toMapping))
  def removeProperty[T](model: String, propertyName: String, usedOnlyByThisModel: Boolean): Operations =
    addOperations(RemoveProperty(model, propertyName, usedOnlyByThisModel))
  def updateGraph(comment: String, model: String)(update: Traversal[Vertex, Vertex, Converter.Identity[Vertex]] => Try[Unit]): Operations =
    addOperations(UpdateGraph(model, update, comment))
  def addIndex(model: String, indexType: IndexType.Value, properties: String*): Operations =
    addOperations(AddIndex(model, indexType, properties))
  def dbOperation[DB <: Database: ClassTag](comment: String)(op: DB => Try[Unit]): Operations =
    addOperations(DBOperation[DB](comment, op))
  def noop: Operations                                                                    = addOperations(NoOperation)
  def rebuildIndexes: Operations                                                          = addOperations(RebuildIndexes)
  def removeIndex(model: String, indexType: IndexType.Value, fields: String*): Operations = addOperations(RemoveIndex(model, indexType, fields))

  def info(schemaName: String, version: Int, message: String): Unit = logger.info(s"*** UPDATE SCHEMA OF $schemaName (${version + 1}): $message")

  def execute(db: Database, schema: Schema)(implicit authContext: AuthContext): Try[Unit] =
    db.version(schemaName) match {
      case 0 =>
        info(schemaName, operations.length, "Create database schema")
        db.createSchemaFrom(schema)
          .flatMap(_ => db.setVersion(schemaName, operations.length + 1))
      case version =>
        operations.zipWithIndex.foldLeft[Try[Unit]](Success(())) {
          case (Success(_), (ops, v)) if v + 1 >= version =>
            (ops match {
              case AddVertexModel(label) =>
                info(schemaName, v, s"Add vertex model $label to schema")
                db.addVertexModel(label, Map.empty)
              case AddEdgeModel(label, mapping) =>
                info(schemaName, v, s"Add edge model $label to schema")
                db.addEdgeModel(label, mapping)
              case AddProperty(model, propertyName, mapping) =>
                info(schemaName, v, s"Add property $propertyName to $model")
                db.addProperty(model, propertyName, mapping)
              case RemoveProperty(model, propertyName, usedOnlyByThisModel) =>
                info(schemaName, v, s"Remove property $propertyName from $model")
                db.removeProperty(model, propertyName, usedOnlyByThisModel)
              case UpdateGraph(model, update, comment, pageSize) =>
                info(schemaName, v, s"Update graph: $comment")
                db
                  .roTransaction { roGraph =>
                    db
                      .V(model)(roGraph)
                      ._id
                      .toSeq
                  }
                  .toIterator
                  .grouped(pageSize)
                  .foldLeft[Try[Int]](Success(0)) {
                    case (Success(count), page) =>
                      info(schemaName, v, s"Update graph in progress ($count): $comment")
                      db.tryTransaction { rwGraph =>
                        update(db.V(model, page: _*)(rwGraph))
                      }.map(_ => count + pageSize)
                    case (failure, _) => failure
                  }
                  .map(_ => ())
                  .recoverWith { case error => Failure(InternalError(s"Unable to execute migration operation: $comment", error)) }
              case AddIndex(model, indexType, properties) =>
                info(schemaName, v, s"Add index in $model for properties: ${properties.mkString(", ")}")
                db.addIndex(model, Seq(indexType -> properties))
              case dbOperation: DBOperation[_] =>
                info(schemaName, v, s"Update database: ${dbOperation.comment}")
                dbOperation(db)
              case NoOperation =>
                info(schemaName, v, "No operation")
                Success(())
              case RebuildIndexes =>
                info(schemaName, v, "Rebuild all indexes")
                db.rebuildIndexes()
                Success(())
              case RemoveIndex(model, indexType, fields) =>
                info(schemaName, v, s"Remove index $model:${fields.mkString(",")}")
                db.removeIndex(model, indexType, fields)
            }).flatMap(_ => db.setVersion(schemaName, v + 2))
          case (acc, _) => acc
        }
    }
}
