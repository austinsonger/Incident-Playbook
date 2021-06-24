package org.thp.scalligraph.auth

import javax.inject.{Inject, Provider, Singleton}
import org.thp.scalligraph.controllers.AuthenticatedRequest
import org.thp.scalligraph.services.config.ApplicationConfig.configurationFormat
import org.thp.scalligraph.services.config.{ApplicationConfig, ConfigItem}
import org.thp.scalligraph.{AuthenticationError, AuthorizationError, BadConfigurationError, EntityIdOrName, RichSeq}
import play.api.mvc.{ActionFunction, Request, RequestHeader, Result}
import play.api.{Configuration, Logger}

import scala.collection.immutable
import scala.util.{Failure, Success, Try}

class MultiAuthSrv(configuration: Configuration, appConfig: ApplicationConfig, availableAuthProviders: immutable.Set[AuthSrvProvider])
    extends AuthSrv {
  val name: String        = "multi"
  lazy val logger: Logger = Logger(getClass)

  val authSrvProviderConfigsConfig: ConfigItem[Seq[Configuration], Seq[Configuration]] =
    appConfig.validatedItem[Seq[Configuration]](
      "auth.providers",
      "List of authentication provider",
      (cfg: Seq[Configuration]) => parseConfiguration(cfg).map(_ => cfg)
    )
  authSrvProviderConfigsConfig.onUpdate((_, cfg) => internalAuthProviders = parseConfiguration(cfg).get)
  /* this is a lazy var implementation to prevent circular dependency with Guice (some authSrv requires global authSrv) at class init */
  private var internalAuthProviders: Seq[AuthSrv]          = Nil
  @volatile private var internalAuthProvidersFlag: Boolean = false

  def authProviders: Seq[AuthSrv] = {
    if (!internalAuthProvidersFlag)
      authSrvProviderConfigsConfig.synchronized {
        if (!internalAuthProvidersFlag)
          internalAuthProviders = parseConfiguration(authSrvProviderConfigsConfig.get).get
        internalAuthProvidersFlag = true
      }
    internalAuthProviders
  }

  def parseConfiguration(providerConfig: Seq[Configuration]): Try[Seq[AuthSrv]] =
    providerConfig
      .toTry { config =>
        for {
          name     <- config.getOptional[String]("name").toRight(BadConfigurationError("Name missing in authentication provider configuration")).toTry
          provider <- availableAuthProviders.find(_.name == name).toRight(BadConfigurationError(s"Authentication provider $name not found")).toTry
          defaultConfig = configuration.getOptional[Configuration](s"auth.defaults.$name").getOrElse(Configuration.empty)
          authSrv <- provider(config withFallback defaultConfig)
        } yield authSrv
      }

  def providerNames: Seq[String] = authProviders.map(_.name)

  override def capabilities: Set[AuthCapability.Value] = authProviders.flatMap(_.capabilities).toSet

  private def forAllAuthProviders[A](providers: Seq[AuthSrv])(body: AuthSrv => Try[A]): Try[A] =
    providers.foldLeft[Either[Seq[(String, Throwable)], A]](Left(Seq())) {
      case (right: Right[_, _], _) => right
      case (Left(errors), auth) =>
        body(auth).fold(
          error => Left(errors :+ ((auth.name, error))),
          success => Right(success)
        )
    } match {
      case Right(auth) => Success(auth)
      case Left(Seq()) => Failure(AuthorizationError("no authentication provider found"))
      case Left(errors) =>
        errors.foreach {
          case (authName, AuthenticationError(_, cause)) if cause != null => logAuthError(authName, cause)
          case (authName, AuthorizationError(_, cause)) if cause != null  => logAuthError(authName, cause)
          case (authName, error)                                          => logAuthError(authName, error)
        }
        if (errors.exists(_._2.isInstanceOf[AuthorizationError]))
          Failure(AuthorizationError("Operation not permitted"))
        else
          Failure(AuthenticationError("Authentication failure"))
    }

  private def logAuthError(authName: String, error: Throwable): Unit = {
    logger.warn(s"$authName fails: $error")
    logger.debug(s"$authName fails: $error", error)
  }

  override def actionFunction(nextFunction: ActionFunction[Request, AuthenticatedRequest]): ActionFunction[Request, AuthenticatedRequest] =
    authProviders.foldRight(nextFunction)((authSrv, af) => authSrv.actionFunction(af))

  override def authenticate(username: String, password: String, organisation: Option[EntityIdOrName], code: Option[String])(implicit
      request: RequestHeader
  ): Try[AuthContext] =
    forAllAuthProviders(authProviders)(_.authenticate(username, password, organisation, code))
      .recoverWith(authErrorHandler)

  override def authenticate(key: String, organisation: Option[EntityIdOrName])(implicit request: RequestHeader): Try[AuthContext] =
    forAllAuthProviders(authProviders)(_.authenticate(key, organisation))
      .recoverWith(authErrorHandler)

  val authErrorHandler: PartialFunction[Throwable, Try[AuthContext]] = {
    case _ => Failure(AuthenticationError("Authentication failure"))
  }

  override def setSessionUser(authContext: AuthContext): Result => Result =
    authProviders.map(_.setSessionUser(authContext)).reduceLeft(_ andThen _)

  override def changePassword(username: String, oldPassword: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] =
    forAllAuthProviders(authProviders)(_.changePassword(username, oldPassword, newPassword))

  override def setPassword(username: String, newPassword: String)(implicit authContext: AuthContext): Try[Unit] =
    forAllAuthProviders(authProviders)(_.setPassword(username, newPassword))

  override def renewKey(username: String)(implicit authContext: AuthContext): Try[String] =
    forAllAuthProviders(authProviders)(_.renewKey(username))

  override def getKey(username: String)(implicit authContext: AuthContext): Try[String] =
    forAllAuthProviders(authProviders)(_.getKey(username))

  override def removeKey(username: String)(implicit authContext: AuthContext): Try[Unit] =
    forAllAuthProviders(authProviders)(_.removeKey(username))
}

@Singleton
class MultiAuthSrvProvider @Inject() (configuration: Configuration, appConfig: ApplicationConfig, authProviders: immutable.Set[AuthSrvProvider])
    extends Provider[AuthSrv] {
  override def get(): AuthSrv = new MultiAuthSrv(configuration, appConfig, authProviders)
}
