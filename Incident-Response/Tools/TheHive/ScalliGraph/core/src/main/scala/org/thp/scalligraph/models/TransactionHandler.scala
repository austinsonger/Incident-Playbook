package org.thp.scalligraph.models

import akka.stream.SubscriptionWithCancelException.NonFailureCancellation
import akka.stream._
import akka.stream.scaladsl.{Broadcast, Flow, GraphDSL, Source}
import akka.stream.stage.{GraphStage, GraphStageLogic, InHandler, OutHandler}

object TransactionHandler {
  def apply[TX, E, M](newTx: () => TX, commit: TX => Unit, rollback: TX => Unit, flow: Flow[TX, E, M]): Source[E, M] =
    Source.fromGraph(GraphDSL.create(flow) { implicit builder => flowShape =>
      import GraphDSL.Implicits._
      val tx        = Source.lazySingle(newTx)
      val bcast     = builder.add(Broadcast[TX](2))
      val txHandler = builder.add(new TransactionHandler[TX, E](commit, rollback))

      tx ~> bcast
      bcast.out(0) ~> txHandler.in0
      bcast.out(1) ~> flowShape ~> txHandler.in1

      SourceShape(txHandler.out)
    })
}

class TransactionHandler[TX, A](commit: TX => Unit, rollback: TX => Unit) extends GraphStage[FanInShape2[TX, A, A]] {
  val txIn: Inlet[TX]                       = Inlet[TX]("txIn")
  val elemIn: Inlet[A]                      = Inlet[A]("elemIn")
  val out: Outlet[A]                        = Outlet[A]("out")
  override val shape: FanInShape2[TX, A, A] = new FanInShape2(txIn, elemIn, out)

  override def createLogic(inheritedAttributes: Attributes): GraphStageLogic = new GraphStageLogic(shape) {
    var tx: Option[TX] = None
    def doCommit(): Unit = {
      tx.foreach(commit)
      tx = None
    }
    def doRollback(): Unit = {
      tx.foreach(rollback)
      tx = None
    }

    override def preStart(): Unit = pull(txIn)

    override def postStop(): Unit = {
      doCommit()
      super.postStop()
    }

    setHandler(txIn, new InHandler {
      override def onPush(): Unit = tx = Some(grab(txIn))

      override def onUpstreamFinish(): Unit = ()
    })

    setHandler(
      elemIn,
      new InHandler {
        override def onPush(): Unit = push(out, grab(elemIn))

        override def onUpstreamFinish(): Unit = {
          doCommit()
          completeStage()
        }

        override def onUpstreamFailure(ex: Throwable): Unit = {
          doRollback()
          failStage(ex)
        }
      }
    )

    setHandler(
      out,
      new OutHandler {
        override def onPull(): Unit = pull(elemIn)

        override def onDownstreamFinish(cause: Throwable): Unit = {
          cause match {
            case _: NonFailureCancellation => doCommit()
            case _                         => doRollback()
          }

          super.onDownstreamFinish(cause)
        }
      }
    )
  }
}
