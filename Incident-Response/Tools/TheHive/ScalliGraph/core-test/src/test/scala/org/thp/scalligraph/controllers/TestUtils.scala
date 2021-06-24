package org.thp.scalligraph.controllers

import org.thp.scalligraph.`macro`.FieldsParserMacro

import scala.language.experimental.macros

trait TestUtils {
  def getFieldsParser[T]: FieldsParser[T] = macro FieldsParserMacro.getOrBuildFieldsParser[T]
  def getUpdateFieldsParser[T]: UpdateFieldsParser[T] = macro FieldsParserMacro.getOrBuildUpdateFieldsParser[T]
}
