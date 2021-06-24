package org.thp.scalligraph.`macro`

import org.thp.scalligraph.models._

import scala.reflect.macros.blackbox

trait MappingMacroHelper extends MacroUtil with MacroLogger {
  val c: blackbox.Context

  import c.universe._

  case class MappingSymbol(name: String, valName: TermName, definition: Tree, tpe: Type)

  def getEnumMapping(eType: Type, symbol: Symbol): Option[Tree] =
    eType match {
      case EnumerationType(members @ _*) =>
        val valueCases = members.map {
          case (name, value) => cq"$name => $value"
        } :+
          cq"""other => throw org.thp.scalligraph.InternalError(
              "Wrong value " + other +
              " for numeration " + ${symbol.toString} +
              ". Possible values are " + ${members.map(_._1).mkString(",")})"""
        Some(q"""org.thp.scalligraph.models.SingleMapping[$eType, String]((_: $eType).toString, (_: String) match { case ..$valueCases })""")
      case _ => None
    }

  def getImplicitMapping(symbol: Symbol): Option[Tree] = {
    val mappingType = appliedType(typeOf[UMapping[_]].typeConstructor, symbol.typeSignature)
    val mapping     = c.inferImplicitValue(mappingType, silent = true, withMacrosDisabled = true)
    if (mapping.tpe =:= NoType) None
    else Some(mapping)
  }
  def getEntityMappings[E: WeakTypeTag]: Seq[MappingSymbol] = {
    val eType = weakTypeOf[E]
    eType match {
      case CaseClassType(symbols @ _*) =>
        symbols.map { s =>
          val mapping = getImplicitMapping(s)
            .orElse(getEnumMapping(s.typeSignature, s))
            .getOrElse(fatal(s"Fail to get mapping of $s (${s.typeSignature})"))
          MappingSymbol(s.name.decodedName.toString.trim, TermName(c.freshName(s.name + "Mapping")), mapping, s.typeSignature)
        }
    }
  }
}
