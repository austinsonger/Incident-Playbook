package org.thp.scalligraph.graphql

import java.io.FileNotFoundException

import org.thp.scalligraph.auth.{AuthContext, AuthContextImpl}
import org.thp.scalligraph.models._
import org.thp.scalligraph.utils.UnthreadedExecutionContext
import play.api.libs.json.{JsObject, JsValue, Json}
import play.api.{Configuration, Environment}

import scala.concurrent.duration._
import scala.concurrent.{Await, ExecutionContext}
import scala.io.Source
import scala.util.control.NonFatal
import scala.util.{Failure, Try}

class SangriaTest extends PlaySpecification {
  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)
  implicit val authContext: AuthContext = AuthContextImpl("me", "", "", "", Set.empty)

  def executeQuery(query: Document, expected: JsValue, variables: JsValue = JsObject.empty)(
      implicit graph: Graph,
      schema: SangriaSchema[AuthGraph, Unit]
  ): MatchResult[_] = {
    implicit val ec: ExecutionContext = UnthreadedExecutionContext

    val futureResult = Executor.execute(schema, query, AuthGraph(authContext, graph), variables = variables)
    val result       = Await.result(futureResult, 10.seconds)
    result must_=== expected
  }

  def readResource(resource: String): Try[String] =
    Try(Source.fromResource(resource).mkString)
      .recoverWith { case NonFatal(_) => Failure(new FileNotFoundException(resource)) }

  def executeQueryFile(
      testName: String,
      variables: JsObject = JsObject.empty
  )(implicit graph: Graph, schema: SangriaSchema[AuthGraph, Unit]): MatchResult[_] = {
    val query    = QueryParser.parse(readResource(s"graphql/$testName.graphql").get).get
    val expected = Json.parse(readResource(s"graphql/$testName.expected.json").get)
    val vars     = readResource(s"graphql/$testName.vars.json").fold(_ => variables, Json.parse)
    executeQuery(query = query, expected = expected, variables = vars)
  }

  Fragments.foreach(new DatabaseProviders().list) { dbProvider =>
    val app: AppBuilder = AppBuilder()
      .bindToProvider(dbProvider)
    step(setupDatabase(app)) ^ specs(dbProvider.name, app) ^ step(teardownDatabase(app))
  }

  def setupDatabase(app: AppBuilder): Try[Unit] =
    DatabaseBuilder.build(app.instanceOf[ModernSchema])(app.instanceOf[Database], authContext)

  def teardownDatabase(app: AppBuilder): Unit = () //app.instanceOf[Database].drop()

  def specs(name: String, app: AppBuilder): Fragment = {
    val db: Database                                    = app.instanceOf[Database]
    val executor                                        = new ModernQueryExecutor()(db)
    implicit val schema: SangriaSchema[AuthGraph, Unit] = SchemaGenerator(executor)

    s"[$name] Modern graph" should {
      "finds all persons" in db.transaction { implicit graph =>
        val personSteps = app.instanceOf[PersonSrv].initSteps
        val r           = personSteps.toSet.map(_.name)
        r must_=== Set("marko", "vadas", "josh", "peter", "marc", "franck")
      }

      "have GraphQL schema" in db.transaction { _ =>
        val schemaStr = SchemaRenderer.renderSchema(schema)
//      println(s"new modern graphql schema is:\n$schemaStr")

        schemaStr must_!== ""
      }

      "execute simple query" in db.transaction { implicit graph =>
        executeQueryFile("simpleQuery")
      }

      "filter entity using query object" in db.transaction { implicit graph =>
        executeQueryFile("queryWithFilterObject")
      }

      "filter entity using query object with boolean operator" in db.transaction { implicit graph =>
        executeQueryFile("queryWithBooleanOperators")
      }

      "return several attributes" in db.transaction { implicit graph =>
        executeQueryFile("queryWithSeveralAttributes")
      }

      "execute complex query" in db.transaction { implicit graph =>
        executeQueryFile("complexQuery")
      }
    }
  }
}
