package org.thp.scalligraph

import play.api.Logger
import play.api.http.Status.{BAD_REQUEST, FORBIDDEN, NOT_FOUND}
import play.api.http.{HttpErrorHandler, Status, Writeable}
import play.api.libs.json.{JsObject, JsString, Json}
import play.api.mvc.{RequestHeader, ResponseHeader, Result}

import scala.concurrent.Future

/**
  * This class handles errors. It traverses all causes of exception to find known error and shows the appropriate message
  */
class ErrorHandler extends HttpErrorHandler {
  lazy val logger: Logger = Logger(getClass)

  def onClientError(request: RequestHeader, statusCode: Int, message: String): Future[Result] = {
    val tpe = statusCode match {
      case BAD_REQUEST => "BadRequest"
      case FORBIDDEN   => "Forbidden"
      case NOT_FOUND   => "NotFound"
      case _           => "Unknown"
    }
    Future.successful(toResult(statusCode, Json.obj("type" -> tpe, "message" -> message)))
  }

  def toErrorResult(ex: Throwable): (Int, JsObject) =
    ex match {
      case e: AuthenticationError     => Status.UNAUTHORIZED          -> e.toJson
      case e: AuthorizationError      => Status.FORBIDDEN             -> e.toJson
      case e: MultiFactorCodeRequired => Status.PAYMENT_REQUIRED      -> e.toJson
      case e: CreateError             => Status.BAD_REQUEST           -> e.toJson
      case e: GetError                => Status.INTERNAL_SERVER_ERROR -> e.toJson
      case e: SearchError             => Status.BAD_REQUEST           -> e.toJson
      case e: UpdateError             => Status.INTERNAL_SERVER_ERROR -> e.toJson
      case e: NotFoundError           => Status.NOT_FOUND             -> e.toJson
      case e: BadRequestError         => Status.BAD_REQUEST           -> e.toJson
      case e: MultiError              => Status.MULTI_STATUS          -> e.toJson
      case e: AttributeCheckingError  => Status.BAD_REQUEST           -> e.toJson
      case e: InternalError           => Status.INTERNAL_SERVER_ERROR -> e.toJson
      case e: BadConfigurationError   => Status.BAD_REQUEST           -> e.toJson
      case nfe: NumberFormatException =>
        Status.BAD_REQUEST -> Json.obj("type" -> "NumberFormatException", "message" -> ("Invalid format " + nfe.getMessage))
      case iae: IllegalArgumentException      => Status.BAD_REQUEST -> Json.obj("type" -> "IllegalArgument", "message" -> iae.getMessage)
      case _ if Option(ex.getCause).isDefined => toErrorResult(ex.getCause)
      case _ =>
        logger.error("Internal error", ex)
        val json = Json.obj("type" -> ex.getClass.getName, "message" -> ex.getMessage)
        Status.INTERNAL_SERVER_ERROR -> (if (ex.getCause == null) json else json + ("cause" -> JsString(ex.getCause.getMessage)))
    }

  def toResult[C](status: Int, c: C)(implicit writeable: Writeable[C]): Result =
    Result(header = ResponseHeader(status), body = writeable.toEntity(c))

  def onServerError(request: RequestHeader, exception: Throwable): Future[Result] = {
    val (status, body) = toErrorResult(exception)
    if (!exception.isInstanceOf[AuthenticationError])
      if (logger.isDebugEnabled) logger.warn(s"${request.method} ${request.uri} returned $status", exception)
      else logger.warn(s"${request.method} ${request.uri} returned $status")
    Future.successful(toResult(status, body))
  }
}
