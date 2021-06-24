package org.thp.scalligraph.`macro`

import org.thp.scalligraph.models.DefineIndex

import scala.reflect.macros.blackbox

trait IndexMacro {
  val c: blackbox.Context

  import c.universe._

  def getIndexes[E: WeakTypeTag]: Tree = {
    val eType = weakTypeOf[E]
    val indexes = eType.typeSymbol.annotations.collect {
      case annotation if annotation.tree.tpe <:< typeOf[DefineIndex] =>
        val args      = annotation.tree.children.tail
        val indexType = args.head
        val fields    = args.tail
        q"$indexType -> $fields"
    }
    q"Seq(..$indexes)"
  }
}
