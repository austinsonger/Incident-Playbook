package org.thp.scalligraph

import java.util.{Set => JSet}

import com.google.inject.internal.{BindingImpl, Scoping}
import com.google.inject.spi._
import com.google.inject.util.{Modules => GuiceModules}
import com.google.inject.{Binder, Module => GuiceModule, _}
import javax.inject.Inject
import net.codingwell.scalaguice.{ScalaModule, ScalaMultibinder}
import org.thp.scalligraph.models.{GlobalSchema, Schema}
import play.api.inject.guice._
import play.api.routing.Router
import play.api.{ApplicationLoader, Configuration, Environment, Logger}

import scala.collection.JavaConverters._

class ScalligraphGuiceableModule(modules: Seq[GuiceableModule]) extends GuiceableModule {
  override def guiced(env: Environment, conf: Configuration, binderOptions: Set[BinderOption]): Seq[GuiceModule] = {
    val guiceModules = modules.flatMap(_.guiced(env, conf, binderOptions))
    val globalModule = guiceModules.tail.foldLeft(guiceModules.head) { (parentModule, childModule) =>
      GuiceModules.`override`(parentModule).`with`(addMultiBindings(childModule))
    }
    Seq(globalModule)
  }

  override def disable(classes: Seq[Class[_]]): GuiceableModule =
    new ScalligraphGuiceableModule(modules.filterNot(o => classes.exists(_.isAssignableFrom(o.getClass))))

  class InternalMultiBinding[T](binding: LinkedKeyBinding[T]) extends BindingImpl[T](null, binding.getKey, Scoping.UNSCOPED) {
    override def acceptTargetVisitor[V](visitor: BindingTargetVisitor[_ >: T, V]): V = visitor.visit(binding)
    override def applyTo(binder: Binder): Unit = {
      val multiBinder = ScalaMultibinder.newSetBinder[T](binder, binding.getKey.getTypeLiteral)
      multiBinder.addBinding.to(binding.getLinkedKey)
      ()
    }
  }

  class MultibindVisitor[T] extends DefaultBindingTargetVisitor[T, Seq[Element]] {
    def isMultiBind(key: Key[_]): Boolean = Option(key.getAnnotationType).map(_.getName).contains("com.google.inject.internal.Element")

    override def visit(linkedKeyBinding: LinkedKeyBinding[_ <: T]): Seq[Element] =
      if (isMultiBind(linkedKeyBinding.getKey)) Nil
      else Seq(new InternalMultiBinding(linkedKeyBinding))

    override def visitOther(binding: Binding[_ <: T]): Seq[Element] = Nil
  }

  def addMultiBindings(module: GuiceModule): GuiceModule = {
    val elements = Elements.getElements(module).asScala
    val cc = elements ++ elements.flatMap { e =>
      e.acceptVisitor(new DefaultElementVisitor[Seq[Element]] {
        override def visit[T](binding: Binding[T]): Seq[Element] = binding.acceptTargetVisitor(new MultibindVisitor[T])
        override def visitOther(element: Element): Seq[Element]  = Nil
      })
    }
    Elements.getModule(cc.asJava)
  }
}

object ScalligraphApplicationLoader {

  def loadModules(origLoadModules: (Environment, Configuration) => Seq[GuiceableModule]): (Environment, Configuration) => Seq[GuiceableModule] = {
    (env, conf) =>
      Seq(new ScalligraphGuiceableModule(origLoadModules(env, conf) :+ GuiceableModule.guiceable(new ScalligraphModule)))
  }
}

class ScalligraphApplicationLoader extends GuiceApplicationLoader {

  import ScalligraphApplicationLoader._

  lazy val logger: Logger = Logger("ScalligraphApplication")
  logger.info("Loading application ...")

  override protected def builder(context: ApplicationLoader.Context): GuiceApplicationBuilder = {
    val builder = initialBuilder
      .disableCircularProxies()
      .in(context.environment)
      .loadConfig(context.initialConfiguration)
      .overrides(overrides(context): _*)
    builder.load(loadModules(builder.loadModules))
  }
}

class ScalligraphModule extends ScalaModule {
  override def configure(): Unit = {
    Logger(getClass).info("Loading scalligraph module")
    bind(classOf[Router]).toProvider(classOf[ScalligraphRouter])
    bind(classOf[Schema]).toProvider(classOf[GlobalSchema])
    ()
  }
}

class ParentProvider[T] @Inject() (instances: Provider[JSet[T]]) extends Provider[Option[T]] {

  def get(): Option[T] = {
    val callerClassName = new Exception().getStackTrace.tail.head.getClassName
    instances
      .get
      .iterator()
      .asScala
      .toList
      .dropWhile(_.getClass.getName != callerClassName)
      .drop(1)
      .headOption
  }
}
