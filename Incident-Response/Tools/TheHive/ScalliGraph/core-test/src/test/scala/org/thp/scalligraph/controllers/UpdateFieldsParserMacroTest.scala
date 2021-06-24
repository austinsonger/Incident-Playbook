package org.thp.scalligraph.controllers

import org.scalactic.{Bad, Good, One}
import org.specs2.mutable.Specification
import org.thp.scalligraph.InvalidFormatAttributeError

class UpdateFieldsParserMacroTest extends Specification with TestUtils {

  "UpdateFieldParser macro" should {

    "parse a simple class" in {
      val fieldsParser = getUpdateFieldsParser[SimpleClassForFieldsParserMacroTest]
      val fields       = FObject("name" -> FString("simpleClass"))
      val updates      = Seq(FPath("name") -> "simpleClass")
      fieldsParser(fields) must_=== Good(updates)
    }

    "make all fields of complex class updatable" in {
      val fieldsParser = getUpdateFieldsParser[ComplexClassForFieldsParserMacroTest]
      fieldsParser.parsers.map(_._1.toString) must contain(exactly("", "name", "value", "subClasses[]", "subClasses[].name", "subClasses[].option"))
    }

    "parse complex class" in {
      val fieldsParser = getUpdateFieldsParser[ComplexClassForFieldsParserMacroTest]
      val fields       = FObject("subClasses[0].name" -> FString("sc1"), "subClasses[1].option" -> FNull)
      val updates      = Seq(FPath("subClasses[0].name") -> "sc1", FPath("subClasses[1].option") -> None)
      fieldsParser(fields) must_=== Good(updates)
    }

    "parse class with annotation" in {
      val fieldsParser = getUpdateFieldsParser[ClassWithAnnotation]
      val fields       = FObject("valueFr" -> FString("un"), "valueEn" -> FString("three"))
      val updates      = Seq(FPath("valueFr") -> LocaleInt(1), FPath("valueEn") -> LocaleInt(3))
      fieldsParser(fields) must_=== Good(updates)
    }

    "parse class with implicit" in {
      implicit val subClassFieldsParser: UpdateFieldsParser[SubClassForFieldsParserMacroTest] =
        UpdateFieldsParser[SubClassForFieldsParserMacroTest](
          "SubClassForFieldsParserMacroTest",
          Seq(FPath("option") -> FieldsParser.build[Option[Int]], FPath("name") -> FieldsParser.build[String])
        )
      val fieldsParser = getUpdateFieldsParser[ComplexClassForFieldsParserMacroTest]

      val fields  = FObject("subClasses[0].option"    -> FNumber(3), "subClasses[1].option"     -> FNull)
      val updates = Seq(FPath("subClasses[0].option") -> Some(3), FPath("subClasses[1].option") -> None)
      fieldsParser(fields) must_=== Good(updates)
    }

    "return an error if provided fields is not correct" in {
      val fieldsParser = getUpdateFieldsParser[SimpleClassForFieldsParserMacroTest]
      val fields       = FObject("name" -> FNumber(12)) // invalid format

      fieldsParser(fields) must_=== Bad(One(InvalidFormatAttributeError("name", "string", Set("string"), FNumber(12))))
    }
  }
}
