package org.thp.scalligraph.models

import org.scalactic.{Good, Or}
import org.specs2.specification.core.{Fragment, Fragments}
import org.thp.scalligraph.AppBuilder
import org.thp.scalligraph.auth.UserSrv
import org.thp.scalligraph.controllers.Field
import play.api.libs.json.Json
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.test.PlaySpecification
import play.api.{Configuration, Environment}

import scala.util.Try

class QueryTest extends PlaySpecification {

  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)
  val userSrv: UserSrv = new DummyUserSrv

  Fragments.foreach(new DatabaseProviders().list) { dbProvider =>
    val app: AppBuilder = new AppBuilder()
      .bindToProvider(dbProvider)
      .addConfiguration("play.modules.disabled = [org.thp.scalligraph.ScalligraphModule]")
    step(setupDatabase(app)) ^ specs(dbProvider.name, app) ^ step(teardownDatabase(app))
  }

  def setupDatabase(app: AppBuilder): Try[Unit] =
    ModernDatabaseBuilder.build(app.apply[ModernSchema])(app.apply[Database], userSrv.getSystemAuthContext)

  def teardownDatabase(app: AppBuilder): Unit = app.apply[Database].drop()

  def specs(name: String, app: AppBuilder): Fragment = {

    implicit val db: Database = app.apply[Database]
    val queryExecutor         = new ModernQueryExecutor()

    s"[$name] Query executor" should {
      "execute simple query from Json" in {
        db.roTransaction { implicit graph =>
          val input =
            Field(
              Json.arr(
                Json.obj("_name" -> "allPeople"),
                Json.obj("_name" -> "sort", "_fields" -> Json.arr(Json.obj("age" -> "incr")))
              )
            )
          val result = queryExecutor.parser(input).flatMap { query =>
            Or.from(queryExecutor.execute(query, graph, userSrv.getSystemAuthContext).map(_.toJson))
          }
          result must_=== Good(
            Json.arr(
              Json.obj("createdBy" -> "admin", "label" -> "Mister vadas", "name"  -> "vadas", "age"  -> 27),
              Json.obj("createdBy" -> "admin", "label" -> "Mister franck", "name" -> "franck", "age" -> 28),
              Json.obj("createdBy" -> "admin", "label" -> "Mister marko", "name"  -> "marko", "age"  -> 29),
              Json.obj("createdBy" -> "admin", "label" -> "Mister josh", "name"   -> "josh", "age"   -> 32),
              Json.obj("createdBy" -> "admin", "label" -> "Mister marc", "name"   -> "marc", "age"   -> 34),
              Json.obj("createdBy" -> "admin", "label" -> "Mister peter", "name"  -> "peter", "age"  -> 35)
            )
          )
        }
      }

      "execute aggregation query" in {
        db.roTransaction { implicit graph =>
          val input = Field(
            Json.arr(
              Json.obj("_name" -> "allPeople"),
              Json.obj("_name" -> "aggregation", "_agg" -> "field", "_field" -> "age", "_select" -> Json.arr(Json.obj("_agg" -> "count")))
            )
          )
          val result = queryExecutor.parser(input).flatMap { query =>
            Or.from(queryExecutor.execute(query, graph, userSrv.getSystemAuthContext).map(_.toJson))
          }
          result must_== Good(
            Json.obj(
              "32" -> Json.obj("count" -> 1),
              "27" -> Json.obj("count" -> 1),
              "34" -> Json.obj("count" -> 1),
              "35" -> Json.obj("count" -> 1),
              "28" -> Json.obj("count" -> 1),
              "29" -> Json.obj("count" -> 1)
            )
          )
        }
      }

      "execute aggregation query 2" in {
        db.roTransaction { implicit graph =>
          val input = Field(
            Json.arr(
              Json.obj("_name" -> "allSoftware"),
              Json.obj("_name" -> "aggregation", "_agg" -> "field", "_field" -> "lang", "_select" -> Json.arr(Json.obj("_agg" -> "count")))
            )
          )
          val result = queryExecutor.parser(input).flatMap { query =>
            Or.from(queryExecutor.execute(query, graph, userSrv.getSystemAuthContext).map(_.toJson))
          }
          result must_== Good(
            Json.obj(
              "java" -> Json.obj("count" -> 2)
            )
          )
        }
      }
    }
  }
}
