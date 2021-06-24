package org.thp.scalligraph.`macro`

import org.thp.scalligraph.controllers._

import scala.reflect.macros.blackbox

class FieldsParserMacro(val c: blackbox.Context) extends MacroLogger with UpdateFieldsParserUtil {

  import c.universe._

  def getOrBuildFieldsParser[E: WeakTypeTag]: Tree = {
    val eType = weakTypeOf[E]
    if (eType <:< typeOf[Enumeration#Value]) initLogger(eType.asInstanceOf[TypeRef].pre.typeSymbol)
    else initLogger(eType.typeSymbol)
    ret(
      s"FieldParser of $eType",
      getParserFromAnnotation(eType.typeSymbol, eType)
        .orElse(getParserFromImplicit(eType, withMacrosDisabled = true))
        .orElse(buildParser(eType))
        .getOrElse(c.abort(c.enclosingPosition, s"Build FieldsParser of $eType fails"))
    )
  }

  def getOrBuildUpdateFieldsParser[E: WeakTypeTag]: Tree = {
    val eType             = weakTypeOf[E]
    val className: String = eType.toString.split("\\.").last
    initLogger(eType.typeSymbol)

    val parser = getUpdateParserFromAnnotation(eType.typeSymbol, eType)
      .orElse(getUpdateParserFromImplicit(eType))
      .orElse(buildUpdateParser(eType.typeSymbol, eType))
      .getOrElse(c.abort(c.enclosingPosition, s"Build FieldsParser of $eType fails"))

    ret(s"UpdateFieldParser of $eType", q"$parser.forType[$eType]($className)")
  }
}

trait FieldsParserUtil extends MacroLogger with MacroUtil {
  val c: blackbox.Context

  import c.universe._

  protected def getOrBuildParser(symbol: Symbol, eType: Type): Option[Tree] = {
    debug(s"getOrBuildParser($symbol, $eType)")
    getParserFromAnnotation(symbol, eType)
      .orElse(getParserFromImplicit(eType, withMacrosDisabled = false))
      .orElse(buildParser(eType))
  }

  protected def getParserFromAnnotation(symbol: Symbol, eType: Type): Option[Tree] = {
    val withParserType = appliedType(typeOf[WithParser[_]], eType)
    (symbol.annotations ::: eType.typeSymbol.annotations)
      .find(_.tree.tpe <:< withParserType)
      .map(annotation => annotation.tree.children.tail.head)
  }

  protected def getParserFromImplicit(eType: Type, withMacrosDisabled: Boolean): Option[Tree] = {
    val fieldsParserType =
      appliedType(typeOf[FieldsParser[_]].typeConstructor, eType)
    val fieldsParser = c.inferImplicitValue(fieldsParserType, silent = true, withMacrosDisabled)
    trace(s"getParserFromImplicit($eType): search implicit of $fieldsParserType => $fieldsParser")
    if (fieldsParser.tpe =:= NoType) None
    else Some(fieldsParser)
  }

  protected def buildParser(eType: Type): Option[Tree] =
    eType match {
      case CaseClassType(paramSymbols @ _*) =>
        trace(s"build FieldsParser case class $eType")
        val companion = eType.typeSymbol.companion
        val initialBuilder = paramSymbols.length match {
          case 0 => q"$companion.apply()"
          case 1 => q"($companion.apply _)"
          case _ => q"($companion.apply _).curried"
        }
        val entityBuilder = paramSymbols
          .foldLeft[Option[Tree]](Some(q"org.scalactic.Good($initialBuilder).orBad[org.scalactic.Every[org.thp.scalligraph.AttributeError]]")) {
            case (maybeBuilder, s) =>
              val symbolName = s.name.toString
              for {
                builder <- maybeBuilder
                parser  <- getOrBuildParser(s, s.typeSignature)
              } yield {
                val builderName = TermName(c.freshName())
                q"""
                  import org.scalactic.{Bad, Every}
                  import org.thp.scalligraph.AttributeError

                  val $builderName = $builder
                  $parser.apply(path :/ $symbolName, field.get($symbolName)).fold(
                    param => $builderName.map(_.apply(param)),
                    error => $builderName match {
                      case Bad(errors: Every[_]) => Bad(errors.asInstanceOf[Every[AttributeError]] ++ error)
                      case _ => Bad(error)
                    })
                """
              }
          }

        entityBuilder.map { builder =>
          val className: String = eType.toString.split("\\.").last
          q"""
            import org.thp.scalligraph.controllers.FieldsParser

            FieldsParser[$eType]($className) { case (path, field) => $builder }
          """
        }
      case EnumerationType(values @ _*) =>
        trace(s"build FieldsParser enumeration of ${values.map(_._1).mkString("[", ",", "]")}")
        val caseValues = values
          .map {
            case (name, value) => cq"(_, org.thp.scalligraph.controllers.FString($name)) => org.scalactic.Good($value)"
          }
        Some(q"org.thp.scalligraph.controllers.FieldsParser(${eType.toString}, Set(..${values.map(_._1)})) { case ..$caseValues }")
      case _ =>
        None
    }
}

trait UpdateFieldsParserUtil extends FieldsParserUtil {
  val c: blackbox.Context

  import c.universe._

  protected def getOrBuildUpdateParser(symbol: Symbol, eType: Type): Tree = {
    debug(s"getOrBuildUpdateParser($symbol, $eType")
    getUpdateParserFromAnnotation(symbol, eType)
      .orElse(getUpdateParserFromImplicit(eType))
      .orElse(buildUpdateParser(symbol, eType))
      .getOrElse {
        warn(s"$eType is not updatable")
        val className: String = eType.toString.split("\\.").last
        q"org.thp.scalligraph.controllers.UpdateFieldsParser.empty[$eType]($className)"
      }

  }

  protected def getUpdateParserFromAnnotation(symbol: Symbol, eType: Type): Option[Tree] = {
    val withUpdateParserType =
      appliedType(weakTypeOf[WithUpdateParser[_]], eType)
    val parser = (symbol.annotations ::: eType.typeSymbol.annotations)
      .find(_.tree.tpe <:< withUpdateParserType)
      .map(annotation => annotation.tree.children.tail.head)
    trace(s"getUpdateParserFromAnnotation($symbol, $eType) => $parser")
    parser
  }

  protected def getUpdateParserFromImplicit(eType: Type): Option[Tree] = {
    val fieldsParserType =
      appliedType(typeOf[UpdateFieldsParser[_]].typeConstructor, eType)
    val fieldsParser = c.inferImplicitValue(fieldsParserType, silent = true)
    trace(s"getParserFromImplicit($eType): search implicit of $fieldsParserType => $fieldsParser")
    if (fieldsParser.tpe =:= NoType) None
    else Some(fieldsParser)
  }

  def buildUpdateParser(symbol: Symbol, eType: Type): Option[Tree] = {
    val updateParser = eType match {
      case CaseClassType(symbols @ _*) =>
        symbols
          .map { s =>
            val sName = s.name.toString
            s.typeSignature match {
              case SeqType(subType) =>
                val parser = getOrBuildUpdateParser(subType.typeSymbol, subType)
                q"$parser.seq($sName)"
              case t =>
                val parser = getOrBuildUpdateParser(s, t)
                q"$parser.on($sName)"
            }
          }
          .reduceOption((p1, p2) => q"$p1 ++ $p2")
      case _ => None
    }
    val parser = getOrBuildParser(symbol, eType).map(p => q"$p.toUpdate")
    val combinedParser = for {
      p1 <- updateParser
      p2 <- parser
    } yield q"$p1 ++ $p2"
    combinedParser.orElse(updateParser).orElse(parser)
  }
}
