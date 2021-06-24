package org.thp.scalligraph.utils

import scala.concurrent.ExecutionContext

object UnthreadedExecutionContext extends ExecutionContext {
  override def execute(runnable: Runnable): Unit = runnable.run()
  override def reportFailure(t: Throwable): Unit =
    throw new IllegalStateException("exception in sameThreadExecutionContext", t)
}
