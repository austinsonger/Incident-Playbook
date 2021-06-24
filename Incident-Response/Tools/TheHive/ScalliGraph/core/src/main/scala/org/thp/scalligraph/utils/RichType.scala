package org.thp.scalligraph.utils

import scala.reflect.runtime.universe._

object RichType {

  def getTypeArgs(t: Type, fromType: Type): List[Type] =
    t.baseType(fromType.typeSymbol).typeArgs
}

object CaseClassType {

  def unapplySeq(tpe: Type): Option[Seq[Symbol]] =
    unapplySeq(tpe.typeSymbol)

  def unapplySeq(s: Symbol): Option[Seq[Symbol]] =
    if (s.isClass) {
      val c = s.asClass
      if (c.isCaseClass)
        Some(c.primaryConstructor.typeSignature.paramLists.head)
      else None
    } else None
}
