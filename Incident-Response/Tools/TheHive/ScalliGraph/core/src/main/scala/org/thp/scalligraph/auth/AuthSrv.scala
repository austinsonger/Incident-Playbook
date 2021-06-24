package org.thp.scalligraph.auth

import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.controllers.AuthenticatedRequest
import org.thp.scalligraph.{AuthenticationError, AuthorizationError, BadConfigurationError, EntityIdOrName}
import play.api.mvc.{ActionFunction, Request, RequestHeader, Result}
import play.api.{ConfigLoader, Configuration}

import scala.concurrent.{ExecutionContext, Future}
import scala.util.matching.Regex
import scala.util.{Failure, Success, Try}

object AuthCapability extends Enumeration {
  val changePassword, setPassword, authByKey, sso, mfa = Value
}

@Singleton
class RequestOrganisation(header: Option[String], parameter: Option[String], pathSegment: Option[Regex], cookie: Option[String])
    extends (Request[_] => Option[EntityIdOrName]) {
  @Inject() def this(configuration: Configuration) =
    this(
      configuration.getOptional[String]("auth.organisationHeader"),
      configuration.getOptional[String]("auth.organisationParameter"),
      configuration.getOptional[String]("auth.organisationPathExtractor").map(_.r),
      configuration.getOptional[String]("auth.organisationCookieName")
    )
  override def apply(request: Request[_]): Option[EntityIdOrName] =
    (header.flatMap(request.headers.get(_)) orElse
      parameter.flatMap(request.queryString.getOrElse(_, Nil).headOption) orElse
      pathSegment.flatMap(r => r.findFirstMatchIn(request.path).flatMap(m => Option(m.group(0)))) orElse
      cookie.flatMap(request.cookies.get).map(_.value)).map(EntityIdOrName.apply)
}

trait AuthSrvProvider extends (Configuration => Try[AuthSrv]) {
  val name: String
  implicit class RichConfig(configuration: Configuration) {

    def getOrFail[A: ConfigLoader](path: String): Try[A] =
      configuration
        .getOptional[A](path)
        .fold[Try[A]](Failure(BadConfigurationError(s"Configuration $path is missing")))(Success(_))
  }
}

trait AuthSrv {
  val name: String
  def capabilities = Set.empty[AuthCapability.Value]

  def actionFunction(nextFunction: ActionFunction[Request, AuthenticatedRequest]): ActionFunction[Request, AuthenticatedRequest] =
    nextFunction

  def authenticate(username: String, password: String, organisation: Option[EntityIdOrName], code: Option[String])(implicit
      request: RequestHeader
  ): Try[AuthContext] =
    Failure(AuthenticationError("Operation not supported"))

  def authenticate(key: String, organisation: Option[EntityIdOrName])(implicit request: RequestHeader): Try[AuthContext] =
    Failure(AuthenticationError("Operation not supported"))

  def setSessionUser(authContext: AuthContext): Result => Result = identity

  def changePassword(username: String, oldPassword: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] =
    Failure(AuthorizationError("Operation not supported"))

  def setPassword(username: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] =
    Failure(AuthorizationError("Operation not supported"))

  def renewKey(username: String)(implicit authContext: AuthContext): Try[String] =
    Failure(AuthorizationError("Operation not supported"))

  def getKey(username: String)(implicit authContext: AuthContext): Try[String] =
    Failure(AuthorizationError("Operation not supported"))

  def removeKey(username: String)(implicit authContext: AuthContext): Try[Unit] =
    Failure(AuthorizationError("Operation not supported"))
}

trait AuthSrvWithActionFunction extends AuthSrv {

  protected def ec: ExecutionContext

  def getAuthContext[A](request: Request[A]): Option[AuthContext]

  def transformResult[A](request: Request[A], authContext: AuthContext): Result => Result = identity

  override def actionFunction(nextFunction: ActionFunction[Request, AuthenticatedRequest]): ActionFunction[Request, AuthenticatedRequest] =
    new ActionFunction[Request, AuthenticatedRequest] {
      override def invokeBlock[A](request: Request[A], block: AuthenticatedRequest[A] => Future[Result]): Future[Result] =
        getAuthContext(request)
          .fold(nextFunction.invokeBlock(request, block)) { authContext =>
            block(new AuthenticatedRequest(authContext, request))
              .map(transformResult(request, authContext))(ec)
          }

      override protected def executionContext: ExecutionContext = ec
    }
}
