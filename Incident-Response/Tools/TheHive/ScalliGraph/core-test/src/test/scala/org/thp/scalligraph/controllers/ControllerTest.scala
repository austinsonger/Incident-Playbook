package org.thp.scalligraph.controllers

import org.specs2.concurrent.ExecutionEnv
import org.specs2.mock.Mockito
import org.thp.scalligraph.ErrorHandler
import org.thp.scalligraph.auth.AuthSrv
import play.api.inject.guice.GuiceApplicationBuilder
import play.api.libs.json.Json
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.mvc.{AnyContentAsJson, DefaultActionBuilder, Results}
import play.api.test.{FakeRequest, Helpers, PlaySpecification}
import play.api.{Application, Configuration, Environment}

import scala.util.Success

class ControllerTest(implicit executionEnv: ExecutionEnv) extends PlaySpecification with Mockito {
  lazy val app: Application = new GuiceApplicationBuilder().build()

  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)

  "controller" should {

    "extract simple class from HTTP request" in {

      val actionBuilder = DefaultActionBuilder(Helpers.stubBodyParser())
      val entrypoint    = new Entrypoint(mock[AuthSrv], actionBuilder, new ErrorHandler, executionEnv.ec)

      val action = entrypoint("model extraction")
        .extract("simpleClass", FieldsParser[SimpleClassForFieldsParserMacroTest]) { req =>
          val simpleClass = req.body("simpleClass")
          simpleClass must_=== SimpleClassForFieldsParserMacroTest("myName", 44)
          Success(Results.Ok("ok"))
        }

      val request  = FakeRequest("POST", "/api/simple_class").withBody(AnyContentAsJson(Json.obj("name" -> "myName", "value" -> 44)))
      val result   = action(request)
      val bodyText = contentAsString(result)
      bodyText must be equalTo "ok"
    }

//    "render stream with total number of element in header" in {
//
//      val actionBuilder = DefaultActionBuilder(Helpers.stubBodyParser())
//      val entrypoint    = new EntryPoint(mock[AuthenticateSrv], actionBuilder, new ErrorHandler, ee.ec, mat)
//
//      val action = entrypoint("find entity")
//        .chunked(_ => Source(0 to 3).mapMaterializedValue(_ => 10))
//      val request = FakeRequest("GET", "/")
//      val result  = Await.result(action(request), 1.second)
//      result.header.headers("X-Total") must_=== "10"
//      result.body.contentType must beSome("application/json")
//      Await.result(result.body.consumeData.map(_.decodeString("utf-8")), 1.second) must_=== Json.arr(0, 1, 2, 3).toString
//    }
  }
}
