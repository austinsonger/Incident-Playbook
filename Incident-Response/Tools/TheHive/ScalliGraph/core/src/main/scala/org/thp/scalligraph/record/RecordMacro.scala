package org.thp.scalligraph.record

import shapeless.labelled.KeyTag
import shapeless.tag.Tagged
import shapeless.{::, HList, HNil}

import scala.annotation.tailrec
import scala.reflect.macros.whitebox
import scala.tools.nsc.Global
import scala.{Symbol => ScalaSymbol}

class UnsafeSelector[L <: HList, K, O](i: Int) extends Selector[L, K] {
  type Out = O

  def apply(l: L): O = HList.unsafeGet(l, i).asInstanceOf[O]
}

class RecordMacro(val c: whitebox.Context) {
  import c.universe._

  def prefix(tpe: Type): Type = {
    val global = c.universe.asInstanceOf[Global]
    val gTpe   = tpe.asInstanceOf[global.Type]
    gTpe.prefix.asInstanceOf[Type]
  }

  object FieldType {

    import internal._

    val keyTagTpe: Type   = typeOf[KeyTag[_, _]]
    val keyTagSym: Symbol = keyTagTpe.typeSymbol

    def apply(kTpe: Type, vTpe: Type): Type =
      refinedType(List(vTpe, typeRef(prefix(keyTagTpe), keyTagTpe.typeSymbol, List(kTpe, vTpe))), NoSymbol)

    def unapply(fTpe: Type): Option[(Type, Type)] =
      fTpe.dealias match {
        case RefinedType(l, _) =>
          val rf = refinedType(l.init, NoSymbol)
          l.last match {
            case TypeRef(_, `keyTagSym`, List(k, v1)) if v1 =:= rf =>
              Some(k -> rf)
            case _ => None
          }
        case _ => None
      }
  }

  private lazy val hconsTpe  = typeOf[::[_, _]]
  private lazy val tagTpe    = typeOf[Tagged[_]]
  private lazy val hconsPre  = prefix(hconsTpe)
  private lazy val hnilTpe   = typeOf[HNil]
  private lazy val symbolTpe = typeOf[ScalaSymbol]
  private lazy val tagPre    = prefix(tagTpe)
  private lazy val tagSym    = tagTpe.typeSymbol

  object Record {

    /**
      * Extract shapeless record element type
      *
      * @param l type of the shapeless record
      * @return a tuple with key type (singleton), value type and the rest of the record
      */
    def unapply(l: Type): Option[(Type, Type, Type)] =
      if (l <:< typeOf[HNil]) None
      else
        l.baseType(hconsTpe.typeSymbol) match {
          case TypeRef(pre, _, List(FieldType(k, v), lTail)) if pre =:= hconsPre =>
            Some((k, v, lTail))
          case _ => None
        }
  }

  object KeyTag {

    def unapply(tTpe: Type): Option[String] =
      tTpe.dealias match {
        case RefinedType(List(`symbolTpe`, TypeRef(tPre, `tagSym`, List(ConstantType(Constant(name: String))))), _) if tPre =:= tagPre =>
          Some(name)
        case _ => None
      }
  }

  def extractHlistTypes(hl: Type): List[(String, Type)] = {
    @tailrec
    def unfold(l: Type, acc: List[(String, Type)]): List[(String, Type)] =
      if (l <:< hnilTpe) acc
      else
        l.baseType(hconsTpe.typeSymbol) match {
          case TypeRef(pre, _, List(FieldType(KeyTag(k), v), lTail)) if pre =:= hconsPre =>
            unfold(lTail, (k, v) :: acc)
          case _ => c.abort(c.enclosingPosition, s"$l is not an HList type")
        }

    unfold(hl, Nil)
  }

  def mkSelector[L <: HList, K](implicit lTag: WeakTypeTag[L], kTag: WeakTypeTag[K]): Tree = {
    def unfold(list: Type, key: Type): Option[(Type, Int)] =
      list match {
        case l if l <:< typeOf[HNil]      => None
        case Record(k, v, _) if k =:= key => Some(v -> 0)
        case Record(_, _, tail) =>
          unfold(tail, key).map { case (_v, i) => _v -> (i + 1) }
        case l => c.abort(c.enclosingPosition, s"$l is not an HList type")
      }

    val lTpe = lTag.tpe.dealias
    val kTpe = kTag.tpe.dealias
    unfold(lTpe, kTpe) match {
      case Some((v, i)) =>
        q" new org.thp.scalligraph.record.UnsafeSelector[$lTpe, $kTpe, $v]($i) "
      case _ =>
        c.echo(c.enclosingPosition, s"DEBUG: $lTag")
        c.echo(c.enclosingPosition, s"No field $kTpe in record [${extractHlistTypes(lTpe).map(_._1).mkString(",")}]")
        q" new org.thp.scalligraph.record.UnsafeSelector[$lTpe, $kTpe, Nothing](0) "
    }
  }
}
