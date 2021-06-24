package org.thp.scalligraph.utils

import akka.actor.Scheduler
import akka.pattern.after
import play.api.Logger

import java.util.concurrent.ThreadLocalRandom
import scala.concurrent.duration.FiniteDuration
import scala.concurrent.{ExecutionContext, Future}
import scala.util.{Failure, Try}

object Retry {

  def exceptionCheck(exceptions: Seq[Class[_]])(t: Throwable): Boolean =
    exceptions.isEmpty || exceptions.contains(t.getClass) || Option(t.getCause).exists(exceptionCheck(exceptions))

  val logger: Logger = Logger(getClass)

  def apply[T](maxTries: Int) = new Retry(maxTries, Nil)
}

class Retry(maxTries: Int, exceptions: Seq[Class[_]]) {
  import Retry._

  def apply[T](fn: => T): T                              = run(1, fn)
  def withTry[T](fn: => Try[T]): Try[T]                  = runTry(1, fn)
  def on[E <: Throwable](implicit manifest: Manifest[E]) = new Retry(maxTries, exceptions :+ manifest.runtimeClass)

  def delayed(delay: Int => FiniteDuration)(implicit scheduler: Scheduler, ec: ExecutionContext) =
    new DelayRetry(maxTries, exceptions, scheduler, delay, ec)

  def withBackoff(minBackoff: FiniteDuration, maxBackoff: FiniteDuration, randomFactor: Double)(implicit
      scheduler: Scheduler,
      ec: ExecutionContext
  ): DelayRetry =
    delayed { n => // from akka.pattern.BackoffSupervisor.calculateDelay
      val rnd                = 1.0 + ThreadLocalRandom.current().nextDouble() * randomFactor
      val calculatedDuration = Try(maxBackoff.min(minBackoff * math.pow(2, n.toDouble)) * rnd).getOrElse(maxBackoff)
      calculatedDuration match {
        case f: FiniteDuration => f
        case _                 => maxBackoff
      }
    }

  def delayed(delay: FiniteDuration)(implicit scheduler: Scheduler, ec: ExecutionContext) =
    new DelayRetry(maxTries, exceptions, scheduler, _ => delay, ec)

  private def run[T](currentTry: Int, f: => T): T =
    try f
    catch {
      case e: Throwable if currentTry < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)")
        run(currentTry + 1, f)
      case e: Throwable if currentTry < maxTries =>
        logger.error("uncaught error, not retrying", e)
        throw e
    }

  private def runTry[T](currentTry: Int, fn: => Try[T]): Try[T] =
    Try(fn).flatten.recoverWith {
      case e: Throwable if currentTry < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)")
        runTry(currentTry + 1, fn)
      case e: Throwable if currentTry < maxTries =>
        logger.error("uncaught error, not retrying", e)
        Failure(e)
    }
}

class DelayRetry(maxTries: Int, exceptions: Seq[Class[_]], scheduler: Scheduler, delay: Int => FiniteDuration, implicit val ec: ExecutionContext) {
  import Retry._

  def apply[T](fn: => Future[T]): Future[T] = run(1, fn)

  def sync[T](fn: => T): T =
    try fn
    catch {
      case e: Throwable if 1 < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying (1)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying (1)")
        runSync(2, fn)
      case e: Throwable if 1 < maxTries =>
        logger.error("uncaught error, not retrying", e)
        throw e
      case e =>
        logger.error("An error occurs", e)
        throw e
    }

  def withTry[T](fn: => Try[T]): Try[T] =
    Try(fn).flatten.recoverWith {
      case e: Throwable if 1 < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying (1)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying (1)")
        Try(runSync(2, fn.get))
      case e: Throwable if 1 < maxTries =>
        logger.error("uncaught error, not retrying", e)
        Failure(e)
      case e =>
        logger.error("An error occurs", e)
        Failure(e)

    }

  def on[E <: Throwable](implicit manifest: Manifest[E]) = new DelayRetry(maxTries, exceptions :+ manifest.runtimeClass, scheduler, delay, ec)

  private def runSync[T](currentTry: Int, fn: => T): T =
    try fn
    catch {
      case e if currentTry < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)")
        Thread.sleep(delay(currentTry).toMillis)
        runSync(currentTry + 1, fn)
      case e: Throwable if currentTry < maxTries =>
        logger.error("uncaught error, not retrying", e)
        throw e
      case e =>
        logger.error("An error occurs", e)
        throw e
    }

  private def run[T](currentTry: Int, fn: => Future[T]): Future[T] =
    fn recoverWith {
      case e if currentTry < maxTries && exceptionCheck(exceptions)(e) =>
        if (logger.isDebugEnabled) logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)", e)
        else logger.warn(s"An error occurs (${e.getClass.getCanonicalName}: ${e.getMessage}), retrying ($currentTry)")
        after(delay(currentTry), scheduler)(run(currentTry + 1, fn))
      case e: Throwable if currentTry < maxTries =>
        logger.error("uncaught error, not retrying", e)
        Future.failed(e)
      case e =>
        logger.error("An error occurs", e)
        Future.failed(e)

    }
}
