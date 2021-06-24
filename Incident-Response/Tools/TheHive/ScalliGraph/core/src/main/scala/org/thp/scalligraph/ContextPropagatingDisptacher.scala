package org.thp.scalligraph

import java.util.concurrent.TimeUnit
import java.util.{Map => JMap}

import akka.dispatch._
import com.typesafe.config.Config
import org.slf4j.MDC
import play.api.mvc.RequestHeader

import scala.concurrent.ExecutionContext
import scala.concurrent.duration.{Duration, FiniteDuration}

/**
  * Configurator for a context propagating dispatcher.
  */
class ContextPropagatingDispatcherConfigurator(config: Config, prerequisites: DispatcherPrerequisites)
    extends MessageDispatcherConfigurator(config, prerequisites) {

  private val instance = new ContextPropagatingDispatcher(
    this,
    config.getString("id"),
    config.getInt("throughput"),
    FiniteDuration(config.getDuration("throughput-deadline-time", TimeUnit.NANOSECONDS), TimeUnit.NANOSECONDS),
    configureExecutor(),
    FiniteDuration(config.getDuration("shutdown-timeout", TimeUnit.MILLISECONDS), TimeUnit.MILLISECONDS)
  )

  override def dispatcher(): MessageDispatcher = instance
}

/**
  * A context propagating dispatcher.
  *
  * This dispatcher propagates the current diagnostic context if it's set when it's executed.
  */
class ContextPropagatingDispatcher(
    _configurator: MessageDispatcherConfigurator,
    id: String,
    throughput: Int,
    throughputDeadlineTime: Duration,
    executorServiceFactoryProvider: ExecutorServiceFactoryProvider,
    shutdownTimeout: FiniteDuration
) extends Dispatcher(
      _configurator,
      id,
      throughput,
      throughputDeadlineTime,
      executorServiceFactoryProvider,
      shutdownTimeout
    ) { self =>

  override def prepare(): ExecutionContext =
    new ExecutionContext {
      // capture the context
      val context: CapturedDiagnosticContext = DiagnosticContext.capture()
      def execute(r: Runnable): Unit         = self.execute(() => context.withContext(r.run()))
      def reportFailure(t: Throwable): Unit  = self.reportFailure(t)
    }
}

/**
  * The current diagnostic context.
  */
object DiagnosticContext {

  /**
    * Capture the current diagnostic context.
    */
  def capture(): CapturedDiagnosticContext =
    new CapturedDiagnosticContext {
      val maybeMDC: Option[JMap[String, String]] = getDiagnosticContext

      def withContext[T](block: => T): T =
        maybeMDC match {
          case Some(mdc) => withDiagnosticContext(mdc)(block)
          case None      => block
        }
    }

  /**
    * Get the current diagnostic context.
    */
  def getDiagnosticContext: Option[JMap[String, String]] = Option(MDC.getCopyOfContextMap)

  /**
    * Execute the given block with the given diagnostic context.
    */
  def withDiagnosticContext[T](mdc: JMap[String, String])(block: => T): T = {
    assert(mdc != null, "MDC must not be null")
    saveDiagnosticContext {
      MDC.setContextMap(mdc)
      block
    }
  }

  def withRequest[T](requestHeader: RequestHeader)(block: => T): T = {
    assert(requestHeader != null, "RequestHeader must not be null")
    saveDiagnosticContext {
      MDC.put("request", f"${requestHeader.id}%08x")
      MDC.remove("tx")
      block
    }
  }

  def saveDiagnosticContext[T](block: => T): T = {
    val maybeOld = getDiagnosticContext
    try block
    finally maybeOld match {
      case Some(old) => MDC.setContextMap(old)
      case None      => MDC.clear()
    }
  }
}

/**
  * A captured context
  */
trait CapturedDiagnosticContext {

  /**
    * Execute the given block with the captured context.
    */
  def withContext[T](block: => T): T
}
