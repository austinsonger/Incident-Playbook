package org.thp.scalligraph.controllers

import org.scalactic.{Bad, Good, One}
import org.specs2.matcher.Matcher
import org.specs2.mutable.Specification
import org.thp.scalligraph.InvalidFormatAttributeError
import org.thp.scalligraph.models.{MyEntity, UMapping}
import org.thp.scalligraph.query.{PropertyUpdater, PublicProperties, PublicPropertyListBuilder}
import play.api.libs.json.Json

import scala.util.Success

object TestEnumeration extends Enumeration {
  val a, b, c = Value
}

sealed trait TestSealedClassEnumeration
object EnumA extends TestSealedClassEnumeration
object EnumB extends TestSealedClassEnumeration
object EnumC extends TestSealedClassEnumeration

class FieldsParserMacroTest extends Specification with TestUtils {

  "FieldParser macro" should {

    "have a name" in {
      val fieldsParser = getFieldsParser[SimpleClassForFieldsParserMacroTest]
      fieldsParser.formatName must_=== "SimpleClassForFieldsParserMacroTest"
    }

    "parse a simple class" in {
      val fieldsParser = getFieldsParser[SimpleClassForFieldsParserMacroTest]
      val fields       = FObject("name" -> FString("simpleClass"), "value" -> FNumber(42))
      val simpleClass  = SimpleClassForFieldsParserMacroTest("simpleClass", 42)
      fieldsParser(fields) must_=== Good(simpleClass)
    }

    "parse complex class" in {
      val fieldsParser = getFieldsParser[ComplexClassForFieldsParserMacroTest]
      val fields = FObject(
        "name"       -> FString("complexClass"),
        "value"      -> FNumber(42),
        "subClasses" -> FSeq(FObject("name" -> FString("sc1"), "option" -> FNumber(12)), FObject("name" -> FString("sc2"), "option" -> FNull))
      )
      val complexClass = ComplexClassForFieldsParserMacroTest(
        "complexClass",
        42,
        Seq(SubClassForFieldsParserMacroTest("sc1", Some(12)), SubClassForFieldsParserMacroTest("sc2", None))
      )
      fieldsParser(fields) must_=== Good(complexClass)
    }

    "parse class with annotation" in {
      val fieldsParser        = getFieldsParser[ClassWithAnnotation]
      val fields              = FObject("name" -> FString("classWithAnnotation"), "valueFr" -> FString("un"), "valueEn" -> FString("three"))
      val classWithAnnotation = ClassWithAnnotation("classWithAnnotation", LocaleInt(1), LocaleInt(3))
      fieldsParser(fields) must_=== Good(classWithAnnotation)
    }

    "parse class with implicit" in {
      val subClassRegex = "(\\w+),(\\d+)".r
      implicit val subClassFieldsParser: FieldsParser[SubClassForFieldsParserMacroTest] = FieldsParser[SubClassForFieldsParserMacroTest]("SubClass") {
        case (_, FString(subClassRegex(name, value))) => Good(SubClassForFieldsParserMacroTest(name, Some(value.toInt)))
        case (_, FString(name))                       => Good(SubClassForFieldsParserMacroTest(name, None))
      }
      val fieldsParser = getFieldsParser[ComplexClassForFieldsParserMacroTest]
      val fields       = FObject("name" -> FString("complexClass"), "value" -> FNumber(42), "subClasses" -> FSeq(FString("sc1,12"), FString("sc2")))
      val complexClass = ComplexClassForFieldsParserMacroTest(
        "complexClass",
        42,
        Seq(SubClassForFieldsParserMacroTest("sc1", Some(12)), SubClassForFieldsParserMacroTest("sc2", None))
      )
      fieldsParser(fields) must_=== Good(complexClass)
    }

    "parse class with multi attachments in sub fields" in {
//      val fieldsParser = getFieldsParser[MultiAttachClassForFieldsParserMacroTest]
//      val fields = FObject(
//        "name" → FString("attachClass"),
//        "attachments" → FSeq(
//          FObject(
//            "name"       → FString("attach1"),
//            "mainAttach" → FFile("file1", Paths.get("/tmp/file1"), "text/plain"),
//            "otherAttach" → FSeq(
//              FFile("file2", Paths.get("/tmp/file2"), "text/plain"),
//              FFile("file3", Paths.get("/tmp/file3"), "text/plain")
//            )
//          ),
//          FObject(
//            "name"       → FString("attach2"),
//            "mainAttach" → FString("attach2"),
//            "mainAttach" → FFile("file4", Paths.get("/tmp/file4"), "text/plain"),
//          )
//        )
//      )
//      val multiAttachClass = MultiAttachClassForFieldsParserMacroTest(
//        "attachClass",
//        Seq(
//          SubMultiAttachClassForFieldsParserMacroTest(
//            "attach1",
//            FFile("file1", Paths.get("/tmp/file1"), "text/plain"),
//            Seq(FFile("file2", Paths.get("/tmp/file2"), "text/plain"), FFile("file3", Paths.get("/tmp/file3"), "text/plain"))
//          ),
//          SubMultiAttachClassForFieldsParserMacroTest("attach2", FFile("file4", Paths.get("/tmp/file4"), "text/plain"), Nil)
//        )
//      )
//
//      fieldsParser(fields) must_=== Good(multiAttachClass)
      pending
    }

    "parse a simple value" in {
      val fieldsParser = FieldsParser.string.on("myString")
      val fields       = FObject("myString" -> FString("stringValue"))

      fieldsParser(fields) must_=== Good("stringValue")
    }

    "parse an optional value from undefined field" in {
      val fieldsParser = FieldsParser.string.optional
      val fields       = FUndefined

      fieldsParser(fields) must_=== Good(None)
    }

    "parse an optional value from object" in {
      val fieldsParser = FieldsParser.string.optional.on("nonExistent")
      val fields       = FObject("name" -> FString("toom"))

      fieldsParser(fields) must_=== Good(None)
    }

    "parse a sequence of string" in {
      val fieldsParser = FieldsParser.string.sequence
      val fields       = FSeq(FString("value1"), FString("value2"), FString("value3"))

      fieldsParser(fields) must_=== Good(Seq("value1", "value2", "value3"))
    }

    "parse a sequence of object" in {
      val fieldsParser = getFieldsParser[SimpleClassForFieldsParserMacroTest].sequence
      val fields =
        FSeq(FObject("name" -> FString("simpleClass"), "value" -> FNumber(42)), FObject("name" -> FString("simpleClassBis"), "value" -> FNumber(43)))
      val simpleClass = Seq(SimpleClassForFieldsParserMacroTest("simpleClass", 42), SimpleClassForFieldsParserMacroTest("simpleClassBis", 43))

      fieldsParser(fields) must_=== Good(simpleClass)
    }

    "parse an enumeration" in {
      val fieldsParser = FieldsParser.build[TestEnumeration.Value]
      fieldsParser(FString("a")) must_=== Good(TestEnumeration.a)
      fieldsParser(FString("d")) must_=== Bad(
        One(InvalidFormatAttributeError("", "org.thp.scalligraph.controllers.TestEnumeration.Value", Set("a", "b", "c"), FString("d")))
      )
    }

    "parse an sealed type" in {
      val fieldsParser = FieldsParser.build[TestSealedClassEnumeration]
      fieldsParser(FString("EnumA")) must_=== Good(EnumA)
      fieldsParser(FString("d")) must_=== Bad(
        One(
          InvalidFormatAttributeError("", "org.thp.scalligraph.controllers.TestSealedClassEnumeration", Set("EnumA", "EnumB", "EnumC"), FString("d"))
        )
      )
    }
  }

  "Nothing to update" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.field.updatable)
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("yy" -> "plop", "xxx" -> "yop"))).toEither
    r must beRight.which(_.isEmpty)
  }

  "update one field" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.field.updatable)
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("yy" -> "plop", "p1" -> "yop"))).toEither
    r must beRight.which { updaters =>
      val p1Updater: Matcher[PropertyUpdater] = beLike {
        case PropertyUpdater(FPath("p1"), "yop", _) => ok
      }
      updaters must contain(exactly(p1Updater))
    }
  }

  "update using custom function" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.rename("p2").custom { (path, value, _, _, _) =>
        path must_=== FPath("p1.sp2")
        value must_== "yop"
        Success(Json.obj("p2" -> "yop"))
      })
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("yy" -> "plop", "p1.sp2" -> "yop"))).toEither
    r must beRight.which { updaters =>
      val p1Updater: Matcher[PropertyUpdater] = beLike {
        case PropertyUpdater(FPath("p1", "sp2"), "yop", f) =>
          f(null, null, null) must beSuccessfulTry
      }
      updaters must contain(exactly(p1Updater))
    }
  }

  "fail if contains an invalid field format" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.field.updatable)
      .property("p2", UMapping.string)(_.field.updatable)
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("yy" -> "plop", "p1" -> 10)))
    val expected           = Bad(One(InvalidFormatAttributeError("p1", "string", Set("string"), FNumber(10))))
    r must_=== expected
  }

  "update several fields" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.field.updatable)
      .property("p2", UMapping.string)(_.field.updatable)
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("p2" -> "plop", "p1" -> "a"))).toEither
    r must beRight.which { updaters =>
      val p1Updater: Matcher[PropertyUpdater] = beLike {
        case PropertyUpdater(FPath("p1"), "a", _) => ok
      }
      val p2Updater: Matcher[PropertyUpdater] = beLike {
        case PropertyUpdater(FPath("p2"), "plop", _) => ok
      }
      updaters must contain(exactly(p1Updater, p2Updater))
    }
  }

  "update subfield" in {
    val properties: PublicProperties = PublicPropertyListBuilder[MyEntity]
      .property("p1", UMapping.string)(_.field.updatable)
      .build
    val updateFieldsParser = FieldsParser.update("xxx", properties)
    val r                  = updateFieldsParser(Field(Json.obj("yy" -> "plop", "p1.sp1.sp2" -> "yop"))).toEither
    r must beRight.which { updaters =>
      val p1Updater: Matcher[PropertyUpdater] = beLike {
        case PropertyUpdater(FPath("p1", "sp1", "sp2"), "yop", _) => ok
      }
      updaters must contain(exactly(p1Updater))
    }
  }

}
