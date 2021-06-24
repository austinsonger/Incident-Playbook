package org.thp.scalligraph.models

import org.apache.tinkerpop.gremlin.structure.Transaction.Status
import org.specs2.specification.core.Fragments
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.test.PlaySpecification
import play.api.{Configuration, Environment}

class CallbackTest extends PlaySpecification {
  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)

  Fragments.foreach(new DatabaseProviders().list) { dbProvider =>
    val db: Database = dbProvider.get()

    s"[${dbProvider.name}] entity" should {
      "execute transaction callbacks when readonly transaction is committed" in {
        var commitFlag   = 0
        var rollbackFlag = 0
        db.roTransaction { implicit graph =>
          db.addTransactionListener({
            case Status.COMMIT   => commitFlag += 1
            case Status.ROLLBACK => rollbackFlag += 1
          })
        }
        (commitFlag, rollbackFlag) must beEqualTo((1, 0))
      }
    }
  }
}
