package org.thp.scalligraph

import com.google.inject.Inject
import net.codingwell.scalaguice.{ScalaModule, ScalaMultibinder}
import org.specs2.mock.Mockito
import org.thp.scalligraph.auth.{AuthSrv, UserSrv}
import org.thp.scalligraph.models.{Database, Schema, UpdatableSchema}
import org.thp.scalligraph.query.QueryExecutor
import play.api.cache.caffeine.CaffeineCacheModule
import play.api.i18n.{I18nModule => PlayI18nModule}
import play.api.inject.guice.GuiceApplicationBuilder
import play.api.inject.{BuiltinModule => PlayBuiltinModule}
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.mvc.{CookiesModule => PlayCookiesModule}
import play.api.routing.{Router => PlayRouter}
import play.api.test.PlaySpecification
import play.api.{Configuration, Environment}

trait TestService {
  def id: String
}

class TestService1 @Inject() (parentTestService: ParentProvider[TestService]) extends TestService {
  lazy val parentServiceId: String = parentTestService.get().fold("**")(_.id)
  def id: String                   = s"<TestService1>$parentServiceId</TestService1>"
}

class TestService2 @Inject() (parentTestService: ParentProvider[TestService]) extends TestService {
  lazy val parentServiceId: String = parentTestService.get().fold("**")(_.id)
  def id: String                   = s"<TestService2>$parentServiceId</TestService2>"
}

class TestService3 @Inject() (parentTestService: ParentProvider[TestService]) extends TestService {
  lazy val parentServiceId: String = parentTestService.get().fold("**")(_.id)
  def id: String                   = s"<TestService3>$parentServiceId</TestService3>"
}

class TestServiceModule[TestServiceImpl <: TestService: Manifest] extends ScalaModule {
  override def configure(): Unit = {
    bind[TestService].to[TestServiceImpl]
    ()
  }
}

object TestModule extends ScalaModule with Mockito {
  override def configure(): Unit = {
    bind[AuthSrv].toInstance(mock[AuthSrv])
    bind[UserSrv].toInstance(mock[UserSrv])
    bind[Database].toInstance(mock[Database])
    ScalaMultibinder.newSetBinder[Schema](binder)
    ScalaMultibinder.newSetBinder[QueryExecutor](binder)
    ScalaMultibinder.newSetBinder[PlayRouter](binder)
    ScalaMultibinder.newSetBinder[UpdatableSchema](binder)
    ()
  }
}

class ScalligraphApplicationTest extends PlaySpecification {
  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)

  "create an application with overridden module" in {
    val applicationBuilder = GuiceApplicationBuilder()
      .load(
        new PlayBuiltinModule,
        new PlayI18nModule,
        new PlayCookiesModule,
        new CaffeineCacheModule,
        new TestServiceModule[TestService1],
        new TestServiceModule[TestService2],
        new TestServiceModule[TestService3],
        TestModule
      )

    val application = applicationBuilder
      .load(ScalligraphApplicationLoader.loadModules(applicationBuilder.loadModules))
      .build
    val injector = application.injector

    injector.instanceOf[TestService].id must_=== "<TestService3><TestService2><TestService1>**</TestService1></TestService2></TestService3>"
  }
}
