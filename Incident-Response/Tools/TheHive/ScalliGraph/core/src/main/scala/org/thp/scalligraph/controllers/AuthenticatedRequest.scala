package org.thp.scalligraph.controllers

import org.thp.scalligraph.EntityIdOrName
import org.thp.scalligraph.auth.{AuthContext, Permission}
import org.thp.scalligraph.utils.Instance
import play.api.mvc.{Request, WrappedRequest}

/**
  * A request with authentication information
  *
  * @param authContext authentication information (which contains user name, permissions, ...)
  * @param request the request
  * @tparam A the body content type.
  */
class AuthenticatedRequest[A](val authContext: AuthContext, request: Request[A]) extends WrappedRequest[A](request) with AuthContext with Request[A] {
  override def userId: String                             = authContext.userId
  override def userName: String                           = authContext.userName
  override def organisation: EntityIdOrName               = authContext.organisation
  override def requestId: String                          = Instance.getRequestId(request)
  override def permissions: Set[Permission]               = authContext.permissions
  override def map[B](f: A => B): AuthenticatedRequest[B] = new AuthenticatedRequest(authContext, request.map(f))
  override def changeOrganisation(newOrganisation: EntityIdOrName, newPermissions: Set[Permission]): AuthContext =
    authContext.changeOrganisation(newOrganisation, newPermissions)
}
