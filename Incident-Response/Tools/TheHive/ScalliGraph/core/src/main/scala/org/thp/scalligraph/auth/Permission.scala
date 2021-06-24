package org.thp.scalligraph.auth

import play.api.Logger

import scala.language.implicitConversions

trait PermissionTag

object Permission {
  def apply(name: String): Permission            = shapeless.tag[PermissionTag][String](name)
  def apply(names: Set[String]): Set[Permission] = names.map(apply)
}

case class PermissionDesc(name: String, label: String, scope: String*) {
  val permission: Permission = Permission(name)
}

object PermissionDesc {
  implicit def PermissionDescToPermission(pd: PermissionDesc): Permission = pd.permission
}

trait Permissions {
  lazy val logger: Logger = Logger(getClass)

  val defaultScopes: Seq[String]
  val list: Set[PermissionDesc]

  lazy val all: Set[Permission] = list.map(_.permission)

  def forScope(scope: String): Set[Permission] = list.collect {
    case p if p.scope.contains(scope) => p.permission
  }

  def desc(permission: Permission): PermissionDesc = list.find(_.permission == permission).getOrElse {
    logger.error(s"Unknown permission: $permission")
    PermissionDesc(permission, permission, defaultScopes: _*)
  }
}
