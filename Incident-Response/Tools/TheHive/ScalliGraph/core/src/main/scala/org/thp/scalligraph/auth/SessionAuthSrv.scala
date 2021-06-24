package org.thp.scalligraph.auth

import org.thp.scalligraph.controllers.AuthenticatedRequest
import org.thp.scalligraph.{BadConfigurationError, EntityIdOrName}
import play.api.libs.json.Json
import play.api.mvc._
import play.api.{Configuration, Logger}

import javax.inject.{Inject, Singleton}
import scala.concurrent.duration.{DurationLong, FiniteDuration}
import scala.concurrent.{ExecutionContext, Future}
import scala.util.{Failure, Success, Try}

object ExpirationStatus {
  sealed abstract class Type
  case class Ok(duration: FiniteDuration)      extends Type
  case class Warning(duration: FiniteDuration) extends Type
  case object Error                            extends Type
}

object SessionAuthSrv {
  def now: Long = System.currentTimeMillis()
  private def readLong(request: RequestHeader, name: String): Option[Long] =
    request
      .session
      .get(name)
      .flatMap(expireStr => Try(expireStr.toLong).toOption)

  def isExpired(request: RequestHeader): Boolean = readLong(request, "expire").exists(_ < now)

  def isWarning(request: RequestHeader): Boolean = readLong(request, "warning").exists(_ < now)

  def expirationStatus(request: RequestHeader): Option[ExpirationStatus.Type] =
    readLong(request, "expire")
      .map {
        case expiration if expiration < now => ExpirationStatus.Error
        case expiration =>
          readLong(request, "warning") match {
            case Some(warning) if warning < now => ExpirationStatus.Warning((expiration - now).millis)
            case _                              => ExpirationStatus.Ok((expiration - now).millis)
          }
      }
}
class SessionAuthSrv(
    maxSessionInactivity: FiniteDuration,
    sessionWarning: FiniteDuration,
    userSrv: UserSrv,
    requestOrganisation: RequestOrganisation,
    val ec: ExecutionContext
) extends AuthSrv {
  import SessionAuthSrv._

  override val name: String = "session"
  lazy val logger: Logger   = Logger(getClass)

  /**
    * Insert or update session cookie containing user name and session expiration timestamp
    * Cookie is signed by Play framework (it cannot be modified by user)
    */
  override def setSessionUser(authContext: AuthContext): Result => Result = { result: Result =>
    if (result.header.status / 100 < 4) {
      val newAuthContext = result.header.headers.get("X-Organisation").fold(authContext) { newOrganisation =>
        authContext.changeOrganisation(
          EntityIdOrName(newOrganisation),
          Permission(result.header.headers.get("X-Permissions").fold(Set.empty[String])(_.split(',').toSet))
        )
      }
      val session = result.newSession.getOrElse(Session()) +
        ("authContext" -> Json.toJson(newAuthContext).toString) +
        ("expire"      -> (now + maxSessionInactivity.toMillis).toString) +
        ("warning"     -> (now + maxSessionInactivity.toMillis - sessionWarning.toMillis).toString)
      result.withSession(session)
    } else if (result.header.headers.contains("X-Logout"))
      result.withNewSession
    else
      result
  }

  def getAuthContext[A](request: Request[A]): Option[(AuthContext, AuthContext)] =
    for {
      authSession <-
        request
          .session
          .get("authContext")
      if !isExpired(request)
      authContext <- AuthContext.fromJson(request, authSession).toOption
      orgAuthContext <- requestOrganisation(request) match {
        case Some(organisation) if organisation != authContext.organisation =>
          userSrv.getAuthContext(request, authContext.userId, Some(organisation)).toOption
        case _ => Some(authContext)
      }
    } yield authContext -> orgAuthContext

  override def actionFunction(nextFunction: ActionFunction[Request, AuthenticatedRequest]): ActionFunction[Request, AuthenticatedRequest] =
    new ActionFunction[Request, AuthenticatedRequest] {
      override def invokeBlock[A](request: Request[A], block: AuthenticatedRequest[A] => Future[Result]): Future[Result] =
        getAuthContext(request)
          .fold(nextFunction.invokeBlock(request, block)) {
            case (originalAuthContext, authContext) =>
              block(new AuthenticatedRequest(authContext, request))
                .map(setSessionUser(originalAuthContext))(ec)
          }
      override protected def executionContext: ExecutionContext = ec
    }
}

@Singleton
class SessionAuthProvider @Inject() (userSrv: UserSrv, requestOrganisation: RequestOrganisation, ec: ExecutionContext) extends AuthSrvProvider {
  override val name: String = "session"
  override def apply(config: Configuration): Try[AuthSrv] =
    for {
      maxSessionInactivity <-
        config
          .getDeprecated[Option[FiniteDuration]]("timeout", "inactivity")
          .fold[Try[FiniteDuration]](Failure(BadConfigurationError(s"Configuration timeout is missing")))(Success(_))
      sessionWarning <- config.getOrFail[FiniteDuration]("warning")
    } yield new SessionAuthSrv(maxSessionInactivity, sessionWarning, userSrv, requestOrganisation, ec)
}
