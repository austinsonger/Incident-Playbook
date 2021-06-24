package org.thp.scalligraph.auth

import java.util.Base64

import javax.inject.{Inject, Provider, Singleton}
import org.thp.scalligraph.AuthenticationError
import org.thp.scalligraph.controllers.AuthenticatedRequest
import play.api.Configuration
import play.api.http.{HeaderNames, Status}
import play.api.mvc.{ActionFunction, Request, Result, Results}

import scala.concurrent.{ExecutionContext, Future}
import scala.util.{Failure, Success, Try}

class BasicAuthSrv(realm: Option[String], authSrv: AuthSrv, requestOrganisation: RequestOrganisation, implicit val ec: ExecutionContext)
    extends AuthSrv {

  private val authHeader = realm.map(r => "WWW-Authenticate" -> s"""Basic realm="$r"""")

  override val name: String = "basic"

  def getAuthContext[A](request: Request[A]): Option[AuthContext] =
    request
      .headers
      .get(HeaderNames.AUTHORIZATION)
      .collect {
        case h if h.startsWith("Basic ") =>
          val authWithoutBasic = h.substring(6)
          val decodedAuth      = new String(Base64.getDecoder.decode(authWithoutBasic), "UTF-8")
          decodedAuth.split(":")
      }
      .flatMap {
        case Array(username, password) =>
          authSrv.authenticate(username, password, requestOrganisation(request), None)(request).toOption
        case Array(username, password, code) =>
          authSrv.authenticate(username, password, requestOrganisation(request), Some(code))(request).toOption
        case _ => None
      }

  def addAuthenticateHeader[A](request: Request[A], result: Future[Result]): Future[Result] =
    authHeader match {
      case Some(h) if !request.headers.hasHeader("Referer") =>
        result.transform {
          case Success(result) if result.header.status == Status.UNAUTHORIZED => Success(result.withHeaders(h))
          case Failure(error: AuthenticationError)                            => Success(Results.Unauthorized(error.toJson).withHeaders(h))
          case other                                                          => other
        }
      case _ => result
    }

  override def actionFunction(nextFunction: ActionFunction[Request, AuthenticatedRequest]): ActionFunction[Request, AuthenticatedRequest] =
    new ActionFunction[Request, AuthenticatedRequest] {
      override def invokeBlock[A](request: Request[A], block: AuthenticatedRequest[A] => Future[Result]): Future[Result] =
        getAuthContext(request).fold(addAuthenticateHeader(request, nextFunction.invokeBlock(request, block))) { authContext =>
          block(new AuthenticatedRequest(authContext, request))
        }

      override protected def executionContext: ExecutionContext = ec
    }
}

@Singleton
class BasicAuthProvider @Inject() (authSrvProvider: Provider[AuthSrv], requestOrganisation: RequestOrganisation, ec: ExecutionContext)
    extends AuthSrvProvider {
  lazy val authSrv: AuthSrv = authSrvProvider.get
  override val name: String = "basic"
  override def apply(config: Configuration): Try[AuthSrv] = {
    val realm = config.getOptional[String]("realm")
    Success(new BasicAuthSrv(realm, authSrv, requestOrganisation, ec))
  }
}
