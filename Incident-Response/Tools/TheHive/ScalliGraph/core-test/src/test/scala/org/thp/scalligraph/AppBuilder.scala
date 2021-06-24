package org.thp.scalligraph

import akka.actor.{Actor, ActorRef, Props}
import com.google.inject.name.Names
import com.google.inject.util.Providers
import com.typesafe.config.ConfigFactory
import javax.inject.Provider
import net.codingwell.scalaguice.{ScalaModule, ScalaMultibinder}
import play.api.inject.guice.{GuiceApplicationBuilder, GuiceableModule}
import play.api.libs.concurrent.Akka
import play.api.{Application, Configuration}

import scala.reflect.ClassTag

class AppBuilder extends ScalaModule {

  private var initialized                            = false
  private var init: Function[Unit, _]                = identity[Unit]
  private var configuration: Configuration           = Configuration.empty
  private var overrideModules: List[GuiceableModule] = Nil

  override def configure(): Unit = {
    init(())
    ()
  }

  def addConfiguration(config: Configuration): AppBuilder = {
    configuration = config withFallback configuration
    this
  }

  def addConfiguration(config: String): AppBuilder =
    addConfiguration(Configuration(ConfigFactory.parseString(config)))

  def bind[T: Manifest, TImpl <: T: Manifest]: AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].to[TImpl])
    this
  }

  def bindNamed[T: Manifest, TImpl <: T: Manifest](name: String): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].annotatedWithName(name).to[TImpl])
    this
  }

  def multiBind[T: Manifest](implementations: Class[_ <: T]*): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen { _ =>
      val multiBindings = ScalaMultibinder.newSetBinder[T](binder)
      implementations.foreach(i => multiBindings.addBinding.to(i))
    }
    this
  }

  def multiBindInstance[T: Manifest](implementations: T*): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen { _ =>
      val multiBindings = ScalaMultibinder.newSetBinder[T](binder)
      implementations.foreach(i => multiBindings.addBinding.toInstance(i))
    }
    this
  }

  def bindInstance[T: Manifest](instance: T): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].toInstance(instance))
    this
  }

  def bindNamedInstance[T: Manifest](name: String, instance: T): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].annotatedWith(Names.named(name)).toInstance(instance))
    this
  }

  def bindEagerly[T: Manifest]: AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].asEagerSingleton())
    this
  }

  def bindToProvider[T: Manifest](provider: Provider[T]): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].toProvider(provider))
    this
  }

  def bindToProvider[T: Manifest, TImpl <: Provider[T]: Manifest]: AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].toProvider[TImpl])
    this
  }

  def bindNamedToProvider[T: Manifest](name: String, provider: Provider[T]): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].annotatedWithName(name).toProvider(provider))
    this
  }

  def bindNamedToProvider[T: Manifest, TImpl <: Provider[T]: Manifest](name: String): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen(_ => bind[T].annotatedWithName(name).toProvider[TImpl])
    this
  }

  def bindActor[T <: Actor: ClassTag](name: String, props: Props => Props = identity): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    init = init.andThen { _ =>
      bind(classOf[ActorRef])
        .annotatedWith(Names.named(name))
        .toProvider(Providers.guicify(Akka.providerOf[T](name, props)))
        .asEagerSingleton()
    }
    this
  }

  def `override`(m: AppBuilder => AppBuilder): AppBuilder = {
    if (initialized) throw InternalError("Bind is not permitted after app use")
    overrideModules = m(new AppBuilder()) :: overrideModules
    this
  }

  lazy val app: Application = {
    initialized = true
    GuiceApplicationBuilder(modules = Seq(this), overrides = overrideModules, configuration = configuration).build()
  }

  def apply[T: ClassTag]: T = app.injector.instanceOf[T]

}
