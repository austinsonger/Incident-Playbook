package org.thp.scalligraph

import com.google.inject.Provider
import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.auth.AuthSrv
import org.thp.scalligraph.controllers.{AuthenticatedRequest, Entrypoint}
import org.thp.scalligraph.query.{Query, QueryExecutor}
import play.api.Logger
import play.api.cache.AsyncCacheApi
import play.api.http.HttpConfiguration
import play.api.mvc._
import play.api.routing.Router.Routes
import play.api.routing.sird._
import play.api.routing.{Router, SimpleRouter}

import scala.collection.immutable
import scala.concurrent.{ExecutionContext, Future}

object DebugRouter {
  lazy val logger: Logger = Logger(getClass)

  def apply(name: String, router: Router): Router = new Router {
    override def routes: Routes = new Routes {
      override def isDefinedAt(x: RequestHeader): Boolean = {
        val result = router.routes.isDefinedAt(x)
        logger.info(s"ROUTER $name $x => $result")
        result
      }
      override def apply(v1: RequestHeader): Handler = router.routes.apply(v1)
    }
    override def documentation: Seq[(String, String, String)] = router.documentation
    override def withPrefix(prefix: String): Router           = DebugRouter(s"$name.in($prefix)", router.withPrefix(prefix))
    override def toString: String                             = s"router($name)@$hashCode"
  }
}

@Singleton
class GlobalQueryExecutor @Inject() (queryExecutors: immutable.Set[QueryExecutor], cache: AsyncCacheApi) {

  def get(version: Int): QueryExecutor =
    cache.sync.getOrElseUpdate(s"QueryExecutor.$version") {
      queryExecutors
        .filter(_.versionCheck(version))
        .reduceOption(_ ++ _)
        .getOrElse(throw BadRequestError(s"No available query executor for version $version"))
    }

  def get: QueryExecutor = queryExecutors.reduce(_ ++ _)
}

@Singleton
class ScalligraphRouter @Inject() (
    httpConfig: HttpConfiguration,
    routers: immutable.Set[Router],
    entrypoint: Entrypoint,
    globalQueryExecutor: GlobalQueryExecutor,
    actionBuilder: DefaultActionBuilder,
    authSrv: AuthSrv,
    implicit val ec: ExecutionContext
) extends Provider[Router] {
  lazy val logger: Logger           = Logger(getClass)
  lazy val routerList: List[Router] = routers.toList
  val prefix: String                = httpConfig.context
  override lazy val get: Router = {

    routerList
      .reduceOption(_ orElse _)
      .getOrElse(Router.empty)
      .orElse(SimpleRouter(queryRoutes))
      .orElse(SimpleRouter(authRoutes))
      .withPrefix(prefix)
  }

  val queryRoutes: Routes = {
    case POST(p"/api/v${int(version)}/query") =>
      val queryExecutor = globalQueryExecutor.get(version)
      entrypoint("query")
        .extract("query", queryExecutor.parser.on("query"))
        .auth { request =>
          // macro can't be used because it is in the same module
          // val query: Query = request.body("query"
          val query: Query = request.body.list.head
          queryExecutor.execute(query, request)
        }
  }

  val defaultAction: ActionFunction[Request, AuthenticatedRequest] = new ActionFunction[Request, AuthenticatedRequest] {
    override def invokeBlock[A](request: Request[A], block: AuthenticatedRequest[A] => Future[Result]): Future[Result] =
      Future.failed(NotFoundError(request.path))
    override protected def executionContext: ExecutionContext = ec
  }

  val authRoutes: Routes = {
    case _ =>
      actionBuilder.async { request =>
        authSrv
          .actionFunction(defaultAction)
          .invokeBlock(
            request,
            (_: AuthenticatedRequest[AnyContent]) =>
              if (request.path.endsWith("/ssoLogin"))
                Future.successful(Results.Redirect(prefix))
              else
                Future.failed(NotFoundError(request.path))
          )
      }
  }
}
