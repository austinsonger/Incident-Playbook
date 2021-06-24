package org.thp.scalligraph.services

import java.io.InputStream
import java.nio.file.{Files, Path, Paths}

import akka.actor.ActorSystem
import org.specs2.mock.Mockito
import org.specs2.mutable.Specification
import org.specs2.specification.core.{Fragment, Fragments}
import org.thp.scalligraph.EntityName
import org.thp.scalligraph.auth.{AuthContextImpl, UserSrv}
import org.thp.scalligraph.models.{Database, DatabaseProvider, DatabaseProviders}
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.{Configuration, Environment}

import scala.annotation.tailrec
//import org.thp.scalligraph.orientdb.{OrientDatabase, OrientDatabaseStorageSrv}

class StorageSrvTest extends Specification with Mockito {
  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)

  @tailrec
  private def streamCompare(is1: InputStream, is2: InputStream): Boolean = {
    val n1 = is1.read()
    val n2 = is2.read()
    // println(s"$n1 -- $n2")
    if (n1 == -1 || n2 == -1) n1 == n2
    else (n1 == n2) && streamCompare(is1, is2)
  }

  val storageDirectory: Path = Paths.get(s"target/AttachmentTest-${math.random()}")
  Files.createDirectory(storageDirectory)
  val actorSystem: ActorSystem = ActorSystem("AttachmentTest")
  val dbProviders              = new DatabaseProviders(actorSystem)
  val userSrv: UserSrv         = mock[UserSrv]
  userSrv.getSystemAuthContext returns AuthContextImpl("test", "Test user", EntityName("test"), "test-request-id", Set.empty)

  val dbProvStorageSrv: Seq[(DatabaseProvider, StorageSrv)] = dbProviders.list.map { db =>
    db -> new DatabaseStorageSrv(32 * 1024, userSrv, db.get())
//    case db if db.name == "orientdb" => db -> new OrientDatabaseStorageSrv(db.get().asInstanceOf[OrientDatabase], 32 * 1024)
  } // :+ (new DatabaseProvider("janus", new JanusDatabase(actorSystem)) -> new LocalFileSystemStorageSrv(storageDirectory))

  Fragments.foreach(dbProvStorageSrv) {
    case (dbProvider, storageSrv) =>
      val db = dbProvider.get()
      step(db.createSchema(Nil)) ^ specs(dbProvider.name, db, storageSrv) ^ step(db.drop())
  }

  def specs(dbName: String, db: Database, storageSrv: StorageSrv): Fragment =
    s"[$dbName] attachment" should {

      "save and read stored data" in {
        val f1       = Paths.get("../build.sbt")
        lazy val f2  = Paths.get("build.sbt")
        val filePath = if (Files.exists(f1)) f1 else f2
        val is       = Files.newInputStream(filePath)
        val fId      = "build.sbt-custom-id"
        db.tryTransaction { implicit graph =>
          storageSrv.saveBinary("test", fId, is)
        } must beSuccessfulTry(())
        is.close()

        val is1 = storageSrv.loadBinary("test", fId)
        val is2 = Files.newInputStream(filePath)
        try {
          streamCompare(is1, is2) must beTrue
          storageSrv.exists("test", fId) must beTrue
        } finally {
          is1.close()
          is2.close()
        }
      }
    }
}
