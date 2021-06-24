package org.thp.scalligraph.models

import akka.actor.ActorSystem
import akka.stream.Materializer
import akka.stream.scaladsl.{Flow, Keep, Sink, Source}
import play.api.libs.logback.LogbackLoggerConfigurator
import play.api.test.PlaySpecification
import play.api.{Configuration, Environment}

import scala.concurrent.duration.DurationInt
import scala.util.Try

class StreamTransactionTest extends PlaySpecification {
  val system: ActorSystem        = ActorSystem("test")
  implicit val mat: Materializer = Materializer(system)

  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)
  class Tx {
    var isCommitted = false
    var isRollback  = false

    def commit(): Unit =
      if (isCommitted || isRollback) throw new IllegalStateException("Transaction can't be committed, it is already closed")
      else
        isCommitted = true

    def rollback(): Unit =
      if (isCommitted || isRollback) throw new IllegalStateException("Transaction can't be rolled back, it is already closed")
      else isRollback = true
  }

  object Tx {
    def apply[E, M](flow: Flow[Tx, E, M]): (Tx, Source[E, M]) = {
      val tx = new Tx
      tx -> TransactionHandler[Tx, E, M](() => tx, _.commit(), _.rollback(), flow)
    }
  }

  "transactional stream" should {
    "commit the transaction if sink consume all elements" in {
      val flow      = Flow[Tx].mapConcat(_ => 1 to 10)
      val (tx, src) = Tx(flow)
      await(src.runWith(Sink.seq)) must beEqualTo(Seq(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
      tx.isCommitted must beTrue.setMessage(s"$tx is not committed").eventually(5, 10.milliseconds)
    }

    "commit the transaction if sink consume part of elements" in {
      val flow      = Flow[Tx].mapConcat(_ => 1 to 10)
      val (tx, src) = Tx(flow)
      await(src.runWith(Sink.head)) must beEqualTo(1)
      println(s"$tx ${tx.isCommitted}")
      tx.isCommitted must beTrue.setMessage(s"$tx is not committed").eventually(5, 10.milliseconds)
    }

    "rollback the transaction if flow fails" in {
      val flow      = Flow[Tx].mapConcat(_ => 1 to 10).map(v => 1 / (v - 3))
      val (tx, src) = Tx(flow)
      Try(await(src.runWith(Sink.seq))) must beAFailedTry
      tx.isRollback must beTrue.setMessage(s"$tx is not rolled back").eventually(5, 10.milliseconds)
    }

    "rollback the transaction if sink fails" in {
      val flow      = Flow[Tx].mapConcat(_ => 1 to 10)
      val (tx, src) = Tx(flow)
      Try(await(src.runWith(Flow[Int].map(v => 1 / (v - 3)).toMat(Sink.ignore)(Keep.right)))) must beAFailedTry
      tx.isRollback must beTrue.setMessage(s"$tx is not rolled back").eventually(5, 10.milliseconds)
    }
  }
}
