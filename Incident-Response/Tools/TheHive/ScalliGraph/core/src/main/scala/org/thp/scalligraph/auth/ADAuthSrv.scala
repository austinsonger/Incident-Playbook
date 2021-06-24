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

case class ADConfig(dnsDomain: String, winDomain: String, hosts: Seq[String], useSSL: Boolean)

class ADAuthSrv(adConfig: ADConfig, userSrv: UserSrv) extends AuthSrv {
  lazy val logger: Logger                              = Logger(getClass)
  val name: String                                     = "ad"
  override val capabilities: Set[AuthCapability.Value] = Set(AuthCapability.changePassword)

  override def authenticate(username: String, password: String, organisation: Option[EntityIdOrName], code: Option[String])(implicit
      request: RequestHeader
  ): Try[AuthContext] =
    connect(adConfig.winDomain + "\\" + username, password)(_ => Success(()))
      .flatMap(_ => userSrv.getAuthContext(request, username, organisation))
      .recoverWith { case t => Failure(AuthenticationError("Authentication failure", t)) }

  override def changePassword(username: String, oldPassword: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] = {
    val unicodeOldPassword = ("\"" + oldPassword + "\"").getBytes("UTF-16LE")
    val unicodeNewPassword = ("\"" + newPassword + "\"").getBytes("UTF-16LE")
    connect(adConfig.winDomain + "\\" + username, oldPassword) { ctx =>
      getUserDN(ctx, username).map { userDN =>
        val mods = Array(
          new ModificationItem(DirContext.REMOVE_ATTRIBUTE, new BasicAttribute("unicodePwd", unicodeOldPassword)),
          new ModificationItem(DirContext.ADD_ATTRIBUTE, new BasicAttribute("unicodePwd", unicodeNewPassword))
        )
        ctx.modifyAttributes(userDN, mods)
      }
    }.recoverWith {
      case t => Failure(AuthorizationError("Change password failure", t))
    }
  }

  private val noADServerAvailableException = AuthenticationError("No AD server found")

  @scala.annotation.tailrec
  private def isFatal(t: Throwable): Boolean =
    t match {
      case null                           => true
      case `noADServerAvailableException` => false
      case _: ConnectException            => false
      case _                              => isFatal(t.getCause)
    }

  private def connect[A](username: String, password: String)(f: InitialDirContext => Try[A]): Try[A] =
    adConfig.hosts.foldLeft[Try[A]](Failure(noADServerAvailableException)) {
      case (Failure(e), serverName) if !isFatal(e) =>
        val protocol = if (adConfig.useSSL) "ldaps://" else "ldap://"
        val env      = new util.Hashtable[Any, Any]
        env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory")
        env.put(Context.PROVIDER_URL, protocol + serverName)
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

  def getUserDN(ctx: InitialDirContext, username: String): Try[String] =
    Try {
      val controls = new SearchControls()
      controls.setSearchScope(SearchControls.SUBTREE_SCOPE)
      controls.setCountLimit(1)
      val domainDN     = adConfig.dnsDomain.split("\\.").mkString("dc=", ",dc=", "")
      val searchResult = ctx.search(domainDN, "(sAMAccountName={0})", Array[Object](username), controls)
      if (searchResult.hasMore) searchResult.next().getNameInNamespace
      else throw AuthenticationError("User not found in Active Directory")
    }
}

@Singleton
class ADAuthProvider @Inject() (userSrv: UserSrv) extends AuthSrvProvider {
  override val name: String = "ad"
  override def apply(config: Configuration): Try[AuthSrv] =
    for {
      dnsDomain <- config.getOrFail[String]("dnsDomain")
      winDomain <- config.getOrFail[String]("winDomain")
      useSSL    <- config.getOrFail[Boolean]("useSSL")
      hosts    = config.getOptional[Seq[String]]("hosts").getOrElse(Seq(dnsDomain))
      adConfig = ADConfig(dnsDomain, winDomain, hosts, useSSL)
    } yield new ADAuthSrv(adConfig, userSrv)
}
