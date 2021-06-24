package org.thp.scalligraph.`macro`

case class MacroError(message: String, cause: Option[Throwable] = None) extends Exception(message, cause.orNull)
