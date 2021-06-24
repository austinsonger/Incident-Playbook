package org.thp.scalligraph.models

import org.thp.scalligraph.{EntityIdOrName, EntityName}
import org.thp.scalligraph.auth._
import play.api.libs.json.JsObject
import play.api.mvc.RequestHeader

import scala.util.{Success, Try}

case class DummyUserSrv(
    userId: String = "admin",
    userName: String = "default admin user",
    organisation: String = "admin",
    permissions: Set[Permission] = Set.empty,
    requestId: String = "testRequest"
) extends UserSrv { userSrv =>

  val authContext: AuthContext =
    AuthContextImpl(userSrv.userId, userSrv.userName, EntityName(userSrv.organisation), userSrv.requestId, userSrv.permissions)
  override def getAuthContext(request: RequestHeader, userId: String, organisationName: Option[EntityIdOrName]): Try[AuthContext] =
    Success(authContext)

  override def getSystemAuthContext: AuthContext = authContext

  override def createUser(userId: String, userInfo: JsObject): Try[User] = ???
}
