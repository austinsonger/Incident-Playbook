package org.thp.scalligraph.controllers

import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.auth.{AuthSrv, Permission}
import org.thp.scalligraph.models.Database
import org.thp.scalligraph.record.Record
import org.thp.scalligraph.traversal.Graph
import org.thp.scalligraph.{AttributeCheckingError, AuthenticationError, AuthorizationError, DiagnosticContext}
import play.api.Logger
import play.api.http.HttpErrorHandler
import play.api.mvc._
import shapeless.labelled.FieldType
import shapeless.{::, labelled, HList, HNil, Witness}

import scala.concurrent.{ExecutionContext, Future}
import scala.util.{Failure, Try}

/**
  * API entry point. This class create a controller action which parse request and check authentication
  *
  * @param authSrv method that check user authentication
  * @param actionBuilder ActionBuilder
  * @param ec            ExecutionContext
  */
@Singleton
class Entrypoint @Inject() (
    authSrv: AuthSrv,
    actionBuilder: DefaultActionBuilder,
    errorHandler: HttpErrorHandler,
    implicit val ec: ExecutionContext
) {

  lazy val logger: Logger = Logger(getClass)

  /**
    * Create a named entry point
    *
    * @param name name of entry point
    * @return empty entry point
    */
  def apply(name: String): EntryPointBuilder[HNil] =
    EntryPointBuilder[HNil](name, FieldsParser.good(HNil))

  /**
    * An entry point is defined by its name, a fields parser which transform request into a record V and the type of request (
    * authenticated or not)
    *
    * @param name         name of the entry point
    * @param fieldsParser fields parser that transform request into a record of type V
    * @tparam V type of record
    */
  case class EntryPointBuilder[V <: HList](
      name: String,
      fieldsParser: FieldsParser[V]
  ) {

    val AuthenticationFailureActionFunction: ActionFunction[Request, AuthenticatedRequest] =
      new ActionFunction[Request, AuthenticatedRequest] {
        override def invokeBlock[A](request: Request[A], block: AuthenticatedRequest[A] => Future[Result]): Future[Result] =
          Future.failed(AuthenticationError("Authentication failure"))
        override protected def executionContext: ExecutionContext = ec
      }

    /**
      * Extract a field from request.
      *
      * @param fp field parser to use to extract value from request
      * @tparam T type of extracted field
      * @return a new entry point with added fields parser
      */
    def extract[T](fieldName: Witness, fp: FieldsParser[T]): EntryPointBuilder[FieldType[fieldName.T, T] :: V] =
      EntryPointBuilder(name, fieldsParser.andThen(fieldName.toString)(fp)(labelled.field[fieldName.T](_) :: _))

    def authTransaction(
        db: Database
    )(block: AuthenticatedRequest[Record[V]] => Graph => Try[Result]): Action[AnyContent] =
      auth(request => db.tryTransaction(graph => block(request)(graph)))

    /**
      * Add an authentication check to this entry point.
      *
      * @return a new entry point with added authentication check
      */
    def auth(block: AuthenticatedRequest[Record[V]] => Try[Result]): Action[AnyContent] =
      asyncAuth { request =>
        block(request).fold(errorHandler.onServerError(request, _), Future.successful)
      }

    def authPermitted(permission: Permission)(block: AuthenticatedRequest[Record[V]] => Try[Result]): Action[AnyContent] =
      auth { request =>
        if (request.isPermitted(permission)) block(request)
        else Failure(AuthorizationError(s"Your are not authorized to $name, you haven't the permission $permission"))
      }

    /**
      * Add async auth check to this entry point
      *
      * @param block the action body block returning a future
      * @return
      */
    def asyncAuth(block: AuthenticatedRequest[Record[V]] => Future[Result]): Action[AnyContent] =
      actionBuilder
        .andThen(authSrv.actionFunction(AuthenticationFailureActionFunction))
        .async { request =>
          DiagnosticContext.withRequest(request) {
            fieldsParser(Field(request))
              .fold(v => block(request.map(_ => Record(v))), e => errorHandler.onServerError(request, AttributeCheckingError(e.toSeq)))
          }
        }

    def asyncAuthPermitted(permission: Permission)(block: AuthenticatedRequest[Record[V]] => Future[Result]): Action[AnyContent] =
      asyncAuth { request =>
        if (request.isPermitted(permission)) block(request)
        else Future.failed(AuthorizationError(s"Your are not authorized to $name, you haven't the permission $permission"))
      }

    /**
      * @param db necessary db instance for transaction
      * @param permission permission to check
      * @param block business login function that transforms request into response
      * @return
      */
    def authPermittedTransaction(
        db: Database,
        permission: Permission
    )(block: AuthenticatedRequest[Record[V]] => Graph => Try[Result]): Action[AnyContent] =
      auth { request =>
        if (request.isPermitted(permission)) db.tryTransaction(graph => block(request)(graph))
        else Failure(AuthorizationError(s"Your are not authorized to $name, you haven't the permission $permission"))
      }

    def authPermittedRoTransaction(
        db: Database,
        permission: Permission
    )(block: AuthenticatedRequest[Record[V]] => Graph => Try[Result]): Action[AnyContent] =
      auth { request =>
        if (request.isPermitted(permission)) db.roTransaction(graph => block(request)(graph))
        else Failure(AuthorizationError(s"Your are not authorized to $name, you haven't the permission $permission"))
      }

    def authRoTransaction(
        db: Database
    )(block: AuthenticatedRequest[Record[V]] => Graph => Try[Result]): Action[AnyContent] =
      auth(request => db.roTransaction(graph => block(request)(graph)))

    /**
      * Materialize action using a function that transform request into response
      *
      * @param block business login function that transform request into response
      * @return Action
      */
    def apply(block: Request[Record[V]] => Try[Result]): Action[AnyContent] =
      async { request =>
        DiagnosticContext.withRequest(request) {
          block(request).fold(errorHandler.onServerError(request, _), Future.successful)
        }
      }

    /**
      * Materialize action using a function that transform request into future response
      *
      * @param block business login function that transform request into future response
      * @return Action
      */
    def async(block: Request[Record[V]] => Future[Result]): Action[AnyContent] =
      actionBuilder.async { request =>
        DiagnosticContext.withRequest(request) {
          fieldsParser(Field(request))
            .fold(v => block(request.map(_ => Record(v))), e => errorHandler.onServerError(request, AttributeCheckingError(e.toSeq)))
        }
      }
  }
}
