package org.thp.scalligraph.auth

import org.thp.scalligraph.EntityIdOrName
import org.thp.scalligraph.utils.Instance
import play.api.libs.functional.syntax._
import play.api.libs.json._
import play.api.mvc.RequestHeader

import scala.util.Try

trait AuthContext {
  def userId: String
  def userName: String
  def organisation: EntityIdOrName
  def requestId: String
  def permissions: Set[Permission]
  def changeOrganisation(newOrganisation: EntityIdOrName, newPermissions: Set[Permission]): AuthContext
  def isPermitted(requiredPermission: Permission): Boolean = permissions.contains(requiredPermission)
}

case class AuthContextImpl(userId: String, userName: String, organisation: EntityIdOrName, requestId: String, permissions: Set[Permission])
    extends AuthContext {
  override def changeOrganisation(newOrganisation: EntityIdOrName, newPermissions: Set[Permission]): AuthContext =
    copy(organisation = newOrganisation, permissions = newPermissions)
}

object AuthContext {

  def fromJson(request: RequestHeader, json: String): Try[AuthContext] =
    Try {
      Json.parse(json).as(reads(Instance.getRequestId(request)))
    }

  def reads(requestId: String): Reads[AuthContext] =
    ((JsPath \ "userId").read[String] and
      (JsPath \ "userName").read[String] and
      (JsPath \ "organisation").read[String].map(EntityIdOrName.apply) and
      Reads.pure(requestId) and
      (JsPath \ "permissions").read[Set[String]].map(Permission.apply))(AuthContextImpl.apply _)

  implicit val writes: Writes[AuthContext] = Writes[AuthContext] { authContext =>
    Json.obj(
      "userId"       -> authContext.userId,
      "userName"     -> authContext.userName,
      "organisation" -> authContext.organisation.toString,
      "permissions"  -> authContext.permissions
    )
  }
}

trait UserSrv {
  def getAuthContext(request: RequestHeader, userId: String, organisationName: Option[EntityIdOrName]): Try[AuthContext]
  def getSystemAuthContext: AuthContext
  def createUser(userId: String, userInfo: JsObject): Try[User]
}

trait User {
  val id: String
  def getUserName: String
}
