package org.thp.scalligraph

import org.thp.scalligraph.controllers.FieldsParser
import play.api.libs.json.{Format, Reads, Writes}

sealed abstract class EntityIdOrName(val value: String) {
  def fold[A](ifIsId: EntityId => A, ifIsName: String => A): A
}
object EntityIdOrName {
  val prefixChar: Char                                                      = '~'
  def isId(value: String): Boolean                                          = value.nonEmpty && value.charAt(0) == prefixChar
  def fold[A](value: String)(ifIsId: String => A, ifIsName: String => A): A = if (isId(value)) ifIsId(value.substring(1)) else ifIsName(value)
  def apply(value: String): EntityIdOrName                                  = fold(value)(new EntityId(_), new EntityName(_))
  implicit val fieldsParser: FieldsParser[EntityIdOrName]                   = FieldsParser.string.on("idOrName").map("EntityIdOrName")(EntityIdOrName.apply)
}

case class EntityId(override val value: String) extends EntityIdOrName(value) {
  override def fold[A](ifIsId: EntityId => A, ifIsName: String => A): A = ifIsId(this)
  override def toString: String                                         = s"${EntityIdOrName.prefixChar}$value"
  def isDefined: Boolean                                                = value.nonEmpty
  def isEmpty: Boolean                                                  = value.isEmpty
}
object EntityId {
  def apply(id: AnyRef): EntityId                   = read(id.toString)
  def read(id: String): EntityId                    = EntityIdOrName.fold(id)(new EntityId(_), new EntityId(_))
  def empty                                         = EntityId("")
  implicit val format: Format[EntityId]             = Format(Reads.StringReads.map(EntityId.read), Writes.StringWrites.contramap(_.toString))
  implicit val fieldsParser: FieldsParser[EntityId] = FieldsParser.string.map("EntityId")(EntityId.read)
}

case class EntityName(override val value: String) extends EntityIdOrName(value) {
  override def fold[A](ifIsId: EntityId => A, ifIsName: String => A): A = ifIsName(value)
  override def toString: String                                         = value
}
object EntityName {
  implicit val format: Format[EntityName] = Format(Reads.StringReads.map(new EntityName(_)), Writes.StringWrites.contramap(_.toString))
}
