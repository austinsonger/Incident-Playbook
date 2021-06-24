package org.thp.scalligraph.models

import org.specs2.specification.core.{Fragment, Fragments}
import org.thp.scalligraph.{AppBuilder, EntityName}
import org.thp.scalligraph.auth.{AuthContext, AuthContextImpl}
import org.thp.scalligraph.traversal.TraversalOps._
import play.api.test.PlaySpecification

import scala.util.Try

class ModernTest extends PlaySpecification {

  implicit val authContext: AuthContext = AuthContextImpl("me", "", EntityName(""), "", Set.empty)

  Fragments.foreach(new DatabaseProviders().list) { dbProvider =>
    val app: AppBuilder = new AppBuilder()
      .bindToProvider(dbProvider)
    step(setupDatabase(app)) ^ specs(dbProvider.name, app) ^ step(teardownDatabase(app))
  }

  def setupDatabase(app: AppBuilder): Try[Unit] =
    ModernDatabaseBuilder.build(app.apply[ModernSchema])(app.apply[Database], authContext)

  def teardownDatabase(app: AppBuilder): Unit = app.apply[Database].drop()

  def specs(name: String, app: AppBuilder): Fragment = {
    implicit val db: Database = app.apply[Database]
    val personSrv             = app.apply[PersonSrv]

    s"[$name] graph" should {
//      "remove connected edge when a vertex is removed" in db.transaction { implicit graph =>
//        // Check that marko is connected to two other people, with known level 0.5 and 1.0
//        personSrv.get("marko").knownLevels must contain(exactly(0.5, 1.0))
//        // Remove vadas who is connected to marko
//        personSrv.get("vadas").remove()
//        // Check that marko is connected to only one person
//        personSrv.get("marko").knownLevels must contain(exactly(1.0))
//      }

      "create initial values" in db.roTransaction { implicit graph =>
        personSrv.startTraversal.toSeq.map(_.name) must contain(exactly("marko", "vadas", "franck", "marc", "josh", "peter"))
      }
    }
  }
}
