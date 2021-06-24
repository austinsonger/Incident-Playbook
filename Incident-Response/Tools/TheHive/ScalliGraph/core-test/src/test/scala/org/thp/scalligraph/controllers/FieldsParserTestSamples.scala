package org.thp.scalligraph.controllers

import org.scalactic.Good

case class SimpleClassForFieldsParserMacroTest(name: String, value: Int)

case class SubClassForFieldsParserMacroTest(name: String, option: Option[Int])

case class ComplexClassForFieldsParserMacroTest(name: String, value: Int, subClasses: Seq[SubClassForFieldsParserMacroTest])

//case class SubMultiAttachClassForFieldsParserMacroTest(name: String, mainAttach: Attachment, otherAttach: Seq[Attachment])
//case class MultiAttachClassForFieldsParserMacroTest(name: String, attachments: Seq[SubMultiAttachClassForFieldsParserMacroTest])

@WithParser(CustomFieldsParsers.englishIntFieldsParser)
@WithUpdateParser(CustomFieldsParsers.englishUpdateFieldsParser)
case class LocaleInt(value: Int)

object CustomFieldsParsers {

  val englishIntFieldsParser: FieldsParser[LocaleInt] = FieldsParser[LocaleInt]("englishInt", Set("one", "two", "three")) {
    case (_, FString("one"))   => Good(LocaleInt(1))
    case (_, FString("two"))   => Good(LocaleInt(2))
    case (_, FString("three")) => Good(LocaleInt(3))
  }

  val frenchIntFieldsParser: FieldsParser[LocaleInt] = FieldsParser[LocaleInt]("frenchInt", Set("un", "deux", "trois")) {
    case (_, FString("un"))    => Good(LocaleInt(1))
    case (_, FString("deux"))  => Good(LocaleInt(2))
    case (_, FString("trois")) => Good(LocaleInt(3))
  }

  val englishUpdateFieldsParser: UpdateFieldsParser[LocaleInt] =
    UpdateFieldsParser[LocaleInt]("englishLocalInt", Seq(FPath.empty -> englishIntFieldsParser))

  val frenchUpdateFieldsParser: UpdateFieldsParser[LocaleInt] =
    UpdateFieldsParser[LocaleInt]("frenchLocalInt", Seq(FPath.empty -> frenchIntFieldsParser))
}

case class ClassWithAnnotation(
    name: String,
    @WithParser(CustomFieldsParsers.frenchIntFieldsParser)
    @WithUpdateParser(CustomFieldsParsers.frenchUpdateFieldsParser)
    valueFr: LocaleInt,
    valueEn: LocaleInt
)
