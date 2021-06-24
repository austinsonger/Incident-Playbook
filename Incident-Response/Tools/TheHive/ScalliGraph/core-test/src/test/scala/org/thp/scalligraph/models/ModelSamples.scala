package org.thp.scalligraph.models

import org.scalactic.Good
import org.thp.scalligraph.controllers.{FString, FieldsParser}
import play.api.libs.json.{JsString, Reads, Writes}

object ModelSamples {

  val hobbiesParser: FieldsParser[Seq[String]] = FieldsParser("hobbies") {
    case (_, FString(s)) => Good(s.split(",").toSeq)
  }
  val hobbiesDatabaseReads: Reads[Seq[String]]   = Reads[Seq[String]](json => json.validate[String].map(_.split(",").toSeq))
  val hobbiesDatabaseWrites: Writes[Seq[String]] = Writes[Seq[String]](h => JsString(h.mkString(",")))
  //val hobbiesDatabaseFormat: Format[Seq[String]] = Format[Seq[String]](hobbiesDatabaseReads, hobbiesDatabaseWrites)
}
