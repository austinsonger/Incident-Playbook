package org.thp.scalligraph.`macro`

import java.io.{PrintWriter, StringWriter}

import scala.annotation.StaticAnnotation
import scala.reflect.macros.blackbox

object LogLevel {
  type Value = Int
  val trace = 5
  val debug = 4
  val info  = 3
  val warn  = 2
  val error = 1
}

class TraceLogLevel extends StaticAnnotation

class DebugLogLevel extends StaticAnnotation

class InfoLogLevel extends StaticAnnotation

class WarnLogLevel extends StaticAnnotation

class ErrorLogLevel extends StaticAnnotation

class LogGeneratedCode extends StaticAnnotation

trait MacroLogger {
  val c: blackbox.Context

  import c.universe._

  var level: LogLevel.Value     = LogLevel.error
  var logGeneratedCode: Boolean = false

  def initLogger(s: Symbol): Unit = {
    level = s
      .annotations
      .map(_.tree)
      .collect {
        case a if a.tpe <:< typeOf[TraceLogLevel] => LogLevel.trace
        case a if a.tpe <:< typeOf[DebugLogLevel] => LogLevel.debug
        case a if a.tpe <:< typeOf[InfoLogLevel]  => LogLevel.info
        case a if a.tpe <:< typeOf[WarnLogLevel]  => LogLevel.warn
        case a if a.tpe <:< typeOf[ErrorLogLevel] => LogLevel.error
      }
      .reduceOption(Math.max)
      .getOrElse(LogLevel.error)
    logGeneratedCode = s.annotations.exists(_.tree.tpe <:< typeOf[LogGeneratedCode])
  }

  private def getCauseMessages(throwable: Throwable, causeMessages: Seq[String] = Nil): String =
    Option(throwable).fold(causeMessages.mkString("\n")) { e =>
      getCauseMessages(e.getCause, causeMessages :+ s"${e.getClass}: ${e.getMessage}")
    }

  private def printStackTrace(throwable: Throwable): String = {
    val writer = new StringWriter
    throwable.printStackTrace(new PrintWriter(writer))
    writer.toString
  }

  def isTraceEnabled: Boolean     = level >= LogLevel.trace
  def trace(msg: => String): Unit = if (isTraceEnabled) println(s"[TRACE] $msg")

  def isDebugEnabled: Boolean     = level >= LogLevel.debug
  def debug(msg: => String): Unit = if (isDebugEnabled) println(s"[DEBUG] $msg")

  def isInfoEnabled: Boolean     = level >= LogLevel.info
  def info(msg: => String): Unit = if (isInfoEnabled) println(s"[INFO]  $msg")

  def isWarnEnabled: Boolean                           = level >= LogLevel.warn
  def warn(msg: => String): Unit                       = if (isWarnEnabled) println(s"[WARN]  $msg")
  def warn(msg: => String, throwable: Throwable): Unit = if (isWarnEnabled) println(s"[WARN]  $msg\n${printStackTrace(throwable)}")

  def isErrorEnabled: Boolean     = level >= LogLevel.error
  def error(msg: => String): Unit = if (isErrorEnabled) println(s"[ERROR] $msg")

  def error(msg: => String, throwable: Throwable): Unit =
    if (isErrorEnabled) c.error(c.enclosingPosition, s"[ERROR] $msg\n${getCauseMessages(throwable)}")

  def fatal(msg: => String): Nothing                       = c.abort(c.enclosingPosition, s"[ERROR] $msg")
  def fatal(msg: => String, throwable: Throwable): Nothing = c.abort(c.enclosingPosition, s"[ERROR] $msg\n${printStackTrace(throwable)}")

  def cleanupCode(code: String): String =
    code
      .replaceAllLiterally("/" + "*{<null>}*/", "")
      .replaceAll(";\n", "\n")

  def ret(msg: => String, tree: Tree): Tree = {
    if (logGeneratedCode) println(s"[CODE]  $msg\n${cleanupCode(showCode(tree))}")
    tree
  }

  def ret[T](msg: => String, expr: Expr[T]): Expr[T] = {
    if (logGeneratedCode) println(s"[CODE]  $msg\n${cleanupCode(showCode(expr.tree, printOwners = false))}")
    expr
  }
}
