package org.thp.scalligraph.controllers

import java.nio.file.Path
import org.scalactic.Good
import org.thp.scalligraph.InternalError
import play.api.Logger
import play.api.libs.json._
import play.api.mvc._

import scala.collection.immutable

sealed trait Field {
  def isDefined: Boolean = true

  def get(pathElement: String): Field = FUndefined

  def get(path: FPath): Field =
    path match {
      case FPathEmpty => this
      case _          => FUndefined
    }

  def set(path: FPath, field: Field): Field =
    if (path.isEmpty) field else throw InternalError(s"$this.set($path, $field)")
  def toJson: JsValue
}

object Field {
  private[Field] lazy val logger: Logger = Logger(getClass)

  def apply(json: JsValue): Field =
    json match {
      case JsString(s)  => FString(s)
      case JsNumber(n)  => FNumber(n.toDouble)
      case JsBoolean(b) => FBoolean(b)
      case JsObject(o)  => FObject(o.map { case (k, v) => k -> Field(v) }.toMap)
      case JsArray(a)   => FSeq(a.map(Field.apply).toList)
      case JsNull       => FNull
    }

  def apply(request: Request[AnyContent]): FObject =
    apply(request.body) ++ FObject(
      request
        .queryString
        .collect {
          case (k, v) if k.nonEmpty => k -> FAny(v)
        }
    )

  def apply(body: AnyContent): FObject =
    body match {
      case AnyContentAsFormUrlEncoded(data) =>
        FObject(data.map { case (k, v) => k -> FAny(v) })
      case AnyContentAsText(txt) =>
        logger.warn(s"Request body has unrecognized format (text), it is ignored:\n$txt")
        FObject()
      case AnyContentAsXml(xml) =>
        FObject("xml" -> FString(xml.toString()))
      case AnyContentAsJson(json: JsObject) =>
        Field(json).asInstanceOf[FObject]
      case AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, badParts)) =>
        if (badParts.nonEmpty)
          logger.warn("Request body contains invalid parts")

        val dataFields = dataParts.flatMap {
          case ("_json", Seq(s, _*)) =>
            Json
              .parse(s)
              .as[JsObject]
              .value
              .map {
                case (k, v) => k -> Field(v)
              }
              .toMap
          case (k, v) => Map(k -> FAny(v))
        }
        files.foldLeft(FObject(dataFields)) {
          case (obj, MultipartFormData.FilePart(key, filename, contentType, file, _, _)) =>
            obj.set(FPath(key), FFile(filename.split("[/\\\\]").last, file, contentType.getOrElse("application/octet-stream")))
        }
      case AnyContentAsRaw(raw) =>
        if (raw.size > 0)
          logger.warn(s"Request has unrecognized body format (raw), it is ignored:\n$raw")
        FObject()
      case AnyContentAsEmpty => FObject()
      case other =>
        logger.warn(s"Unknown request body type : $other (${other.getClass})")
        FObject()
    }

  implicit val fieldWrites: Writes[Field] = Writes[Field](field => JsString(field.toString)) // TODO need check if it is correct
  implicit val parser: FieldsParser[Field] = FieldsParser[Field]("Field") {
    case (_, field) => Good(field)
  }
}

case class FString(value: String) extends Field {
  override def toJson: JsValue = JsString(value)
}

object FString {
  implicit val parser: FieldsParser[FString] = FieldsParser[FString]("FString") {
    case (_, field: FString) => Good(field)
  }
  implicit val writes: Writes[FString] = Writes[FString](_.toJson)
}

case class FNumber(value: Double) extends Field {
  override def toJson: JsValue = JsNumber(value)
}

object FNumber {
  implicit val parser: FieldsParser[FNumber] = FieldsParser[FNumber]("FNumber") {
    case (_, field: FNumber) => Good(field)
  }
  implicit val writes: Writes[FNumber] = Writes[FNumber](_.toJson)
}

case class FBoolean(value: Boolean) extends Field {
  override def toJson: JsValue = JsBoolean(value)
}
object FBoolean {
  implicit val writes: Writes[FBoolean] = Writes[FBoolean](_.toJson)
}

case class FSeq(values: List[Field]) extends Field {
  override def set(path: FPath, field: Field): Field =
    path match {
      case FPathSeq(_, FPathEmpty) => FSeq(values :+ field)
      case FPathElemInSeq(_, index, tail) =>
        FSeq(values.patch(index, Seq(values.applyOrElse(index, (_: Int) => FUndefined).set(tail, field)), 1))
    }
  override def toJson: JsValue = JsArray(values.map(_.toJson))
}

object FSeq {
  def apply(value1: Field, values: Field*): FSeq = new FSeq(value1 :: values.toList)
  def apply()                                    = new FSeq(Nil)
  implicit val parser: FieldsParser[FSeq] = FieldsParser[FSeq]("FSeq") {
    case (_, field: FSeq) => Good(field)
  }
  implicit val writes: Writes[FSeq] = Writes[FSeq](_.toJson)
}
case object FNull extends Field {
  override def toJson: JsValue = JsNull
}

case object FUndefined extends Field {
  override def isDefined: Boolean = false
  override def toJson: JsValue    = JsNull
}

case class FAny(value: Seq[String]) extends Field {
  override def toJson: JsValue = JsArray(value.map(JsString.apply))
}

case class FFile(filename: String, filepath: Path, contentType: String) extends Field {
  override def toJson: JsValue = Json.obj("filename" -> filename, "filepath" -> filepath.toString, "contentType" -> contentType)
}
object FFile {
  implicit val writes: Writes[FFile] = Writes[FFile](_.toJson)
}

object FObject {
  def empty                                   = new FObject(Map.empty)
  def apply(elems: (String, Field)*): FObject = new FObject(Map(elems: _*))
  def apply(map: Map[String, Field]): FObject = new FObject(map)
  def apply(o: JsObject): FObject             = new FObject(o.value.mapValues(Field.apply).toMap)
  implicit val parser: FieldsParser[FObject] = FieldsParser[FObject]("FObject") {
    case (_, field: FObject) => Good(field)
  }
}
case class FObject(fields: immutable.Map[String, Field]) extends Field {
  lazy val pathFields: Seq[(FPath, Field)] = fields.toSeq.map { case (k, v) => FPath(k) -> v }

  def iterator: Iterator[(String, Field)] = fields.iterator

  def +(kv: (String, Field)): FObject = new FObject(fields + kv)

  def -(k: String) = new FObject(fields - k)

  def ++(other: FObject): FObject = new FObject(fields ++ other.fields)

  override def set(path: FPath, field: Field): FObject =
    path match {
      case FPathElem(p, tail) =>
        fields.get(p) match {
          case Some(FSeq(_))        => throw InternalError(s"$this.set($path, $field)")
          case Some(f)              => FObject(fields.updated(p, f.set(tail, field)))
          case None if tail.isEmpty => FObject(fields.updated(p, field))
          case None                 => FObject(fields.updated(p, FObject().set(tail, field)))
        }
      case FPathSeq(p, tail) if tail.isEmpty =>
        fields.get(p) match {
          case Some(FSeq(s)) => FObject(fields.updated(p, FSeq(s :+ field)))
          case None          => FObject(fields.updated(p, FSeq(List(field))))
          case _             => throw InternalError(s"$this.set($path, $field)")
        }
      case FPathElemInSeq(p, idx, tail) =>
        fields.get(p) match {
          case Some(FSeq(s)) if s.isDefinedAt(idx) =>
            FObject(fields.updated(p, FSeq(s.patch(idx, Seq(s(idx).set(tail, field)), 1))))
          case Some(FSeq(s)) if s.length == idx =>
            FObject(fields.updated(p, FSeq(s :+ field)))
          case _ => throw InternalError(s"$this.set($path, $field)")
        }
      case _ => throw InternalError(s"$this.set($path, $field)")
    }

  override def get(path: String): Field = fields.getOrElse(path, FUndefined)

  override def get(path: FPath): Field = {
    val selectedFields = pathFields
      .flatMap {
        case (p, f) => p.startsWith(path).map(_.toString -> f)
      }
    if (selectedFields.size == 1 && selectedFields.head._1.isEmpty) selectedFields.head._2
    else FObject(selectedFields.toMap)
  }

  def getString(path: String): Option[String] =
    fields.get(path).collect {
      case FString(s)     => s
      case FAny(s :: Nil) => s
    }

  def getNumber(path: String): Option[Double] =
    fields.get(path).collect {
      case FNumber(n) => n
    }

  override def toJson: JsValue = JsObject(fields.map { case (k, v) => k -> v.toJson })
}
