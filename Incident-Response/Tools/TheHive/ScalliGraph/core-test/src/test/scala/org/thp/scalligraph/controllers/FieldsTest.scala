package org.thp.scalligraph.controllers

import java.io.File
import java.nio.file.Path

import play.api.libs.Files
import play.api.libs.Files.TemporaryFileCreator
import play.api.mvc.MultipartFormData.FilePart
import play.api.mvc.{AnyContentAsMultipartFormData, Headers, MultipartFormData}
import play.api.test.{FakeRequest, NoTemporaryFileCreator, PlaySpecification}

case class FakeTemporaryFile(file: File) extends Files.TemporaryFile {
  def path: Path                                 = file.toPath
  def temporaryFileCreator: TemporaryFileCreator = NoTemporaryFileCreator
}

object FakeTemporaryFile {
  def apply(): Files.TemporaryFile                    = FakeTemporaryFile.fromFile("temporaryFileName")
  def fromFile(name: String): Files.TemporaryFile     = FakeTemporaryFile(new File(name))
  def fromResource(name: String): Files.TemporaryFile = FakeTemporaryFile(new File(getClass.getResource(name).toURI))
}

class FieldsTest extends PlaySpecification {
  "Field" should {
    "be built from HTTP request with file" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":"v1"}"""))
      val files     = Seq(FilePart("attachment", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"         -> FString("v1"),
        "attachment" -> FFile("myfile.txt", file.path, "text/plain"),
        "notIgnore"  -> FAny(Seq("x", "xx"))
      )
    }

    "be built from HTTP request with file in sub field" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":{"a":"v1"}}"""))
      val files     = Seq(FilePart("f1.b", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"        -> FObject("a" -> FString("v1"), "b" -> FFile("myfile.txt", file.path, "text/plain")),
        "notIgnore" -> FAny(Seq("x", "xx"))
      )
    }

    "be built from HTTP request with file in sub field 2" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":{"a":"v1"}}"""))
      val files     = Seq(FilePart("f2.b", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"        -> FObject("a" -> FString("v1")),
        "f2"        -> FObject("b" -> FFile("myfile.txt", file.path, "text/plain")),
        "notIgnore" -> FAny(Seq("x", "xx"))
      )
    }

    "be built from HTTP request with file in seq field" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":{"a":"v1", "b": []}}"""))
      val files     = Seq(FilePart("f1.b[]", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"        -> FObject("a" -> FString("v1"), "b" -> FSeq(List(FFile("myfile.txt", file.path, "text/plain")))),
        "notIgnore" -> FAny(Seq("x", "xx"))
      )
    }

    "be built from HTTP request with file in seq field 2" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":{"a":"v1", "b": ["a", "b"]}}"""))
      val files     = Seq(FilePart("f1.b[]", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"        -> FObject("a" -> FString("v1"), "b" -> FSeq(List(FString("a"), FString("b"), FFile("myfile.txt", file.path, "text/plain")))),
        "notIgnore" -> FAny(Seq("x", "xx"))
      )
    }

    "be built from HTTP request with file in seq field 3" in {
      val file      = FakeTemporaryFile()
      val dataParts = Map("notIgnore" -> Seq("x", "xx"), "_json" -> Seq("""{"f1":{"a":"v1", "b": ["a", "b", "c"]}}"""))
      val files     = Seq(FilePart("f1.b[1]", "myfile.txt", Some("text/plain"), file))
      val request   = FakeRequest("GET", "/", Headers.create(), body = AnyContentAsMultipartFormData(MultipartFormData(dataParts, files, Nil)))

      Field(request) must_=== FObject(
        "f1"        -> FObject("a" -> FString("v1"), "b" -> FSeq(List(FString("a"), FFile("myfile.txt", file.path, "text/plain"), FString("c")))),
        "notIgnore" -> FAny(Seq("x", "xx"))
      )
    }

    "extract subfields in an object" in {
      val obj = FObject("a" -> FString("a"))
      obj.get(FPath("a")) must_=== FString("a")
    }

    "extract subfields in an object of path" in {
      val obj = FObject("c" -> FString("c"), "a.b" -> FSeq(FString("b"), FNumber(3)))
      obj.get(FPath("a.b")) must_=== FSeq(FString("b"), FNumber(3))
    }

    "extract subfields in an object of path" in {
      val obj = FObject("c" -> FString("c"), "a.b.c" -> FSeq(FString("b"), FNumber(3)))
      obj.get(FPath("a.b")) must_=== FObject("c" -> FSeq(FString("b"), FNumber(3)))
    }
  }
}
