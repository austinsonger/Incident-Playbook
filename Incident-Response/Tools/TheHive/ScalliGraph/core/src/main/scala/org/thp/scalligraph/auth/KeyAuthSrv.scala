package org.thp.scalligraph.auth

import javax.inject.Inject
import play.api.Configuration
import play.api.http.HeaderNames
import play.api.mvc.Request

import scala.concurrent.ExecutionContext
import scala.util.{Success, Try}

class KeyAuthSrv(authSrv: AuthSrv, requestOrganisation: RequestOrganisation, val ec: ExecutionContext) extends AuthSrvWithActionFunction {
  override val name: String = "key"

  override def getAuthContext[A](request: Request[A]): Option[AuthContext] =
    request
      .headers
      .get(HeaderNames.AUTHORIZATION)
      .collect {
        case h if h.startsWith("Bearer ") => h.substring(7)
      }
      .flatMap(key => authSrv.authenticate(key, requestOrganisation(request))(request).toOption)
}

class KeyAuthProvider @Inject() (authSrv: AuthSrv, requestOrganisation: RequestOrganisation, ec: ExecutionContext) extends AuthSrvProvider {
  override val name: String                               = "key"
  override def apply(config: Configuration): Try[AuthSrv] = Success(new KeyAuthSrv(authSrv, requestOrganisation, ec))
}
