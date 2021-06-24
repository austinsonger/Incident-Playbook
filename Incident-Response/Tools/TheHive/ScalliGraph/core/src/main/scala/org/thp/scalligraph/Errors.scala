package org.thp.scalligraph

import org.thp.scalligraph.controllers.Field
import play.api.libs.json._

abstract class GenericError(val `type`: String, message: String, cause: Throwable) extends Exception(message, cause) {

  def toJson: JsObject = {
    val json = Json.obj("type" -> `type`, "message" -> message)
    if (cause == null) json
    else json + ("cause" -> JsString(cause.getMessage))
  }
}

case class AuthenticationError(message: String, cause: Throwable = null)     extends GenericError("AuthenticationError", message, cause)
case class AuthorizationError(message: String, cause: Throwable = null)      extends GenericError("AuthorizationError", message, cause)
case class MultiFactorCodeRequired(message: String, cause: Throwable = null) extends GenericError("MultiFactorCodeRequired", message, cause)
case class CreateError(message: String, cause: Throwable = null)             extends GenericError("CreateError", message, cause)
case class GetError(message: String, cause: Throwable = null)                extends GenericError("GetError", message, cause)
case class SearchError(message: String, cause: Throwable = null)             extends GenericError("SearchError", message, cause)
case class UpdateError(status: Option[String], message: String, attributes: JsObject, cause: Throwable = null)
    extends GenericError("UpdateError", message, cause) {
  override def toJson: JsObject = super.toJson + ("object" -> attributes)
}
case class NotFoundError(message: String, cause: Throwable = null)   extends GenericError("NotFoundError", message, cause)
case class BadRequestError(message: String, cause: Throwable = null) extends GenericError("BadRequest", message, cause)
case class MultiError(message: String, exceptions: Seq[GenericError], cause: Throwable = null)
    extends GenericError("MultiError", message + exceptions.map(_.getMessage).mkString(" :\n\t- ", "\n\t- ", ""), cause) {
  override def toJson: JsObject = super.toJson + ("suberrors" -> JsArray(exceptions.map(_.toJson)))
}
case class InternalError(message: String, cause: Throwable = null)                                        extends GenericError("InternalError", message, cause)
case class BadConfigurationError(message: String, cause: Throwable = null)                                extends GenericError("BadConfigurationError", message, cause)
case class OAuth2Redirect(redirectUrl: String, params: Map[String, Seq[String]], cause: Throwable = null) extends Exception(redirectUrl, cause)
case class AttributeCheckingError(errors: Seq[AttributeError] = Nil, cause: Throwable = null)
    extends GenericError("AttributeCheckingError", errors.mkString("[", "][", "]"), cause) {
  override def toJson: JsObject = super.toJson + ("errors" -> Json.toJson(errors))
}

object AttributeError {
  implicit val invalidFormatAttributeErrorWrites: OWrites[InvalidFormatAttributeError] =
    Json.writes[InvalidFormatAttributeError]
  implicit val unknownAttributeErrorWrites: OWrites[UnknownAttributeError] = Json.writes[UnknownAttributeError]
  implicit val updateReadOnlyAttributeErrorWrites: OWrites[UpdateReadOnlyAttributeError] =
    Json.writes[UpdateReadOnlyAttributeError]
  implicit val missingAttributeErrorWrites: OWrites[MissingAttributeError] = Json.writes[MissingAttributeError]
  implicit val unsupportedAttributeErrorWrites: OWrites[UnsupportedAttributeError] =
    Json.writes[UnsupportedAttributeError]

  implicit val attributeErrorWrites: Writes[AttributeError] = Writes[AttributeError] {
    case ifae: InvalidFormatAttributeError =>
      invalidFormatAttributeErrorWrites.writes(ifae) + ("type" -> JsString("InvalidFormatAttributeError"))
    case uae: UnknownAttributeError =>
      unknownAttributeErrorWrites.writes(uae) + ("type" -> JsString("UnknownAttributeError"))
    case uroae: UpdateReadOnlyAttributeError =>
      updateReadOnlyAttributeErrorWrites.writes(uroae) + ("type" -> JsString("UpdateReadOnlyAttributeError"))
    case mae: MissingAttributeError =>
      missingAttributeErrorWrites.writes(mae) + ("type" -> JsString("MissingAttributeError"))
    case uae: UnsupportedAttributeError =>
      unsupportedAttributeErrorWrites.writes(uae) + ("type" -> JsString("UnsupportedAttributeError"))
  }
}

sealed trait AttributeError extends Throwable {
  val name: String
  def withName(name: String): AttributeError

  override def getMessage: String = toString
}

case class InvalidFormatAttributeError(name: String, format: String, acceptedInput: Set[String], field: Field) extends AttributeError {
  override def toString = s"Invalid format for $name: $field, expected $format ${acceptedInput.mkString("(", ",", ")")}"
  override def withName(newName: String): InvalidFormatAttributeError =
    copy(name = newName)
}
case class UnknownAttributeError(name: String, field: Field) extends AttributeError {
  override def toString = s"Unknown attribute $name: $field"
  override def withName(newName: String): UnknownAttributeError =
    copy(name = newName)
}
case class UpdateReadOnlyAttributeError(name: String) extends AttributeError {
  override def toString = s"Attribute $name is read-only"
  override def withName(newName: String): UpdateReadOnlyAttributeError =
    copy(name = newName)
}
case class MissingAttributeError(name: String) extends AttributeError {
  override def toString = s"Attribute $name is missing"
  override def withName(newName: String): MissingAttributeError =
    copy(name = newName)
}
case class UnsupportedAttributeError(name: String) extends AttributeError {
  override def toString = s"Attribute $name is not supported"
  override def withName(newName: String): UnsupportedAttributeError =
    copy(name = newName)
}
