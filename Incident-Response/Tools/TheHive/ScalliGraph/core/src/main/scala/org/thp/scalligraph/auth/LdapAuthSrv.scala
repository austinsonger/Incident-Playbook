package org.thp.scalligraph.auth

import java.net.ConnectException
import java.util

import javax.inject.{Inject, Singleton}
import javax.naming.Context
import javax.naming.directory._
import org.thp.scalligraph.{AuthenticationError, AuthorizationError, EntityIdOrName}
import play.api.mvc.RequestHeader
import play.api.{Configuration, Logger}

import scala.util.{Failure, Success, Try}

case class LdapConfig(hosts: Seq[String], useSSL: Boolean, bindDN: String, bindPW: String, baseDN: String, filter: String)

class LdapAuthSrv(ldapConfig: LdapConfig, userSrv: UserSrv) extends AuthSrv {
  lazy val logger: Logger                              = Logger(getClass)
  val name                                             = "ldap"
  override val capabilities: Set[AuthCapability.Value] = Set(AuthCapability.changePassword)

  override def authenticate(username: String, password: String, organisation: Option[EntityIdOrName], code: Option[String])(implicit
      request: RequestHeader
  ): Try[AuthContext] =
    connect(ldapConfig.bindDN, ldapConfig.bindPW)(ctx => getUserDN(ctx, username))
      .flatMap(userDN => connect(userDN, password)(_ => Success(())))
      .flatMap(_ => userSrv.getAuthContext(request, username, organisation))
      .recoverWith { case t => Failure(AuthenticationError("Authentication failure", t)) }

  override def changePassword(username: String, oldPassword: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] =
    connect(ldapConfig.bindDN, ldapConfig.bindPW)(ctx => getUserDN(ctx, username))
      .flatMap { userDN =>
        connect(userDN, oldPassword) { ctx =>
          val mods = Array(new ModificationItem(DirContext.REPLACE_ATTRIBUTE, new BasicAttribute("userPassword", newPassword)))
          Try(ctx.modifyAttributes(userDN, mods))
        }
      }
      .recoverWith {
        case t => Failure(AuthorizationError("Change password failure", t))
      }

  private val noLdapServerAvailableException = AuthenticationError("No LDAP server found")

  @scala.annotation.tailrec
  private def isFatal(t: Throwable): Boolean =
    t match {
      case null                             => true
      case `noLdapServerAvailableException` => false
      case _: ConnectException              => false
      case _                                => isFatal(t.getCause)
    }

  private def connect[A](username: String, password: String)(f: InitialDirContext => Try[A]): Try[A] =
    ldapConfig.hosts.foldLeft[Try[A]](Failure(noLdapServerAvailableException)) {
      case (Failure(e), host) if !isFatal(e) =>
        val protocol = if (ldapConfig.useSSL) "ldaps://" else "ldap://"
        val env      = new util.Hashtable[Any, Any]
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory")
        env.put(Context.PROVIDER_URL, protocol + host)
        env.put(Context.SECURITY_AUTHENTICATION, "simple")
        env.put(Context.SECURITY_PRINCIPAL, username)
        env.put(Context.SECURITY_CREDENTIALS, password)
        Try {
          val ctx = new InitialDirContext(env)
          try f(ctx)
          finally ctx.close()
        }.flatten
      case (failure @ Failure(e), _) =>
        logger.debug("LDAP connect error", e)
        failure
      case (r, _) => r
    }

  private def getUserDN(ctx: InitialDirContext, username: String): Try[String] =
    Try {
      val controls = new SearchControls()
      controls.setSearchScope(SearchControls.SUBTREE_SCOPE)
      controls.setCountLimit(1)
      val searchResult = ctx.search(ldapConfig.baseDN, ldapConfig.filter, Array[Object](username), controls)
      if (searchResult.hasMore) searchResult.next().getNameInNamespace
      else throw AuthenticationError("User not found in LDAP server")
    }
}

@Singleton
class LdapAuthProvider @Inject() (userSrv: UserSrv) extends AuthSrvProvider {
  override val name: String = "ldap"
  override def apply(config: Configuration): Try[AuthSrv] =
    for {
      bindDN <- config.getOrFail[String]("bindDN")
      bindPW <- config.getOrFail[String]("bindPW")
      baseDN <- config.getOrFail[String]("baseDN")
      filter <- config.getOrFail[String]("filter")
      hosts  <- config.getOrFail[Seq[String]]("hosts")
      useSSL <- config.getOrFail[Boolean]("useSSL")
      ldapConfig = LdapConfig(hosts, useSSL, bindDN, bindPW, baseDN, filter)
    } yield new LdapAuthSrv(ldapConfig, userSrv)
}
