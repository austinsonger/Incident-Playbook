package org.thp.scalligraph.janus

import akka.actor.ActorSystem
import akka.actor.typed.receptionist.{Receptionist, ServiceKey}
import akka.actor.typed.scaladsl.adapter._
import akka.actor.typed.scaladsl.{ActorContext, Behaviors, StashBuffer, TimerScheduler}
import akka.actor.typed.{ActorRef, Behavior, SupervisorStrategy}
import akka.cluster.typed.{ClusterSingleton, SingletonActor}

import scala.concurrent.duration.DurationInt

object JanusClusterManagerActor {
  sealed trait Message
  sealed trait Command extends Message
  sealed trait Result  extends Message

  case class JoinCluster(replyTo: ActorRef[Result], indexBackend: String, indexLocation: String) extends Command
  case object ClusterRequestInit                                                                 extends Result
  case object ClusterInitSuccess                                                                 extends Command
  case object ClusterInitFailure                                                                 extends Command
  case object ClusterFailure                                                                     extends Result
  case class ClusterSuccessConfigurationIgnored(indexBackend: String)                            extends Result
  case object ClusterSuccess                                                                     extends Result

  /* internal messages */
  case class PeerList(listing: Receptionist.Listing) extends Message
  case class GetStatus(replyTo: ActorRef[Message])   extends Message
  case object StatusInit                             extends Message
  case object StatusSuccess                          extends Message
  case object StatusFailure                          extends Message

  private case object TimerKey
  private case object Timeout extends Message

  private val JanusGraphManagerServiceKey: ServiceKey[Message] = ServiceKey[Message]("JanusGraphClusterManagerService")

  def getClusterManagerActor(system: ActorSystem): ActorRef[Command] = {
    val leader =
      ClusterSingleton(system.toTyped)
        .init(SingletonActor(Behaviors.supervise(waitFirstJoin).onFailure[Exception](SupervisorStrategy.stop), "JanusGraphClusterLeader"))

    val behavior =
      Behaviors.setup[Message] { context =>
        Behaviors.withTimers { timers =>
          Behaviors.withStash(10) { buffer =>
            registerPeer(context, timers, buffer, leader)
          }
        }
      }
    system.spawn(behavior, "JanusGraphManagerProxy").narrow[Command]
  }

  def registerPeer(
      context: ActorContext[Message],
      timers: TimerScheduler[Message],
      buffer: StashBuffer[Message],
      leader: ActorRef[Command]
  ): Behavior[Message] = {
    val listingResponseAdapter = context.messageAdapter[Receptionist.Listing](PeerList)
    context.system.receptionist ! Receptionist.Register(JanusGraphManagerServiceKey, context.self)
    context.system.receptionist ! Receptionist.Find(JanusGraphManagerServiceKey, listingResponseAdapter)
    waitPeerList(context, timers, buffer, leader)
  }

  def waitPeerList(
      context: ActorContext[Message],
      timers: TimerScheduler[Message],
      buffer: StashBuffer[Message],
      leader: ActorRef[Command]
  ): Behavior[Message] =
    Behaviors.receiveMessagePartial {
      case PeerList(JanusGraphManagerServiceKey.Listing(peers)) if peers.nonEmpty =>
        timers.startSingleTimer(TimerKey, Timeout, 1.second)
        peers.foreach(_ ! GetStatus(context.self))
        waitForPeerStatus(context, timers, buffer, leader, peers.size)
      case _: PeerList => // no peers found
        registerPeer(context, timers, buffer, leader)
      case GetStatus(replyTo) =>
        replyTo ! StatusInit
        Behaviors.same
      case joinCluster: JoinCluster =>
        buffer.stash(joinCluster)
        Behaviors.same
    }

  def waitForPeerStatus(
      context: ActorContext[Message],
      timers: TimerScheduler[Message],
      buffer: StashBuffer[Message],
      leader: ActorRef[Command],
      waitingPeerCount: Int
  ): Behavior[Message] =
    Behaviors.receiveMessagePartial {
      case StatusSuccess =>
        timers.cancel(TimerKey)
        buffer.unstashAll(clusterAlreadyInitialised)
      case StatusInit if waitingPeerCount == 1 =>
        timers.cancel(TimerKey)
        buffer.unstashAll(proxyToLeader(context, leader))
      case StatusInit =>
        waitForPeerStatus(context, timers, buffer, leader, waitingPeerCount - 1)
      case StatusFailure =>
        clusterFailure
      case GetStatus(replyTo) =>
        replyTo ! StatusInit
        Behaviors.same
      case joinCluster: JoinCluster =>
        buffer.stash(joinCluster)
        Behaviors.same
      case Timeout =>
        buffer.unstashAll(proxyToLeader(context, leader))
    }

  def clusterAlreadyInitialised: Behavior[Message] =
    Behaviors.receiveMessagePartial {
      case joinCluster: JoinCluster =>
        joinCluster.replyTo ! ClusterSuccess
        Behaviors.same
      case GetStatus(replyTo) =>
        replyTo ! StatusSuccess
        Behaviors.same
    }

  def proxyToLeader(context: ActorContext[Message], leader: ActorRef[Command]): Behavior[Message] =
    Behaviors.receiveMessagePartial {
      case joinCluster: JoinCluster =>
        leader ! joinCluster
        leader ! joinCluster.copy(replyTo = context.self)
        Behaviors.same
      case GetStatus(replyTo) =>
        replyTo ! StatusInit
        Behaviors.same
      case ClusterInitSuccess =>
        leader ! ClusterInitSuccess
        clusterAlreadyInitialised
      case ClusterSuccess =>
        clusterAlreadyInitialised
      case _: ClusterSuccessConfigurationIgnored =>
        clusterAlreadyInitialised
      case ClusterFailure =>
        clusterFailure
      case ClusterInitFailure =>
        leader ! ClusterInitFailure
        clusterFailure
    }

  def clusterFailure: Behavior[Message] =
    Behaviors.receiveMessagePartial {
      case joinCluster: JoinCluster =>
        joinCluster.replyTo ! ClusterFailure
        Behaviors.same
      case GetStatus(replyTo) =>
        replyTo ! StatusFailure
        Behaviors.same
    }

  def waitFirstJoin: Behavior[Command] =
    Behaviors.receiveMessage {
      case JoinCluster(replyTo, indexBackend, parameter) =>
        replyTo ! ClusterRequestInit
        leaderInitialising(indexBackend, parameter)
      case ClusterInitFailure => leaderFailed
      case ClusterInitSuccess => leaderInitialised("", "")
    }

  def leaderInitialising(
      installedIndexBackend: String,
      installedIndexLocation: String,
      goodConfMembers: Seq[ActorRef[Result]] = Nil,
      badConfMembers: Seq[ActorRef[Result]] = Nil
  ): Behavior[Command] =
    Behaviors.receiveMessage {
      case JoinCluster(replyTo, indexBackend, indexLocation) if indexBackend == installedIndexBackend && indexLocation == installedIndexLocation =>
        leaderInitialising(installedIndexBackend, installedIndexLocation, goodConfMembers :+ replyTo, badConfMembers)
      case JoinCluster(replyTo, _, _) =>
        leaderInitialising(installedIndexBackend, installedIndexLocation, goodConfMembers, badConfMembers :+ replyTo)
      case ClusterInitSuccess =>
        goodConfMembers.foreach(_ ! ClusterSuccess)
        badConfMembers.foreach(_ ! ClusterSuccessConfigurationIgnored(installedIndexBackend))
        leaderInitialised(installedIndexBackend, installedIndexLocation)
      case ClusterInitFailure =>
        goodConfMembers.foreach(_ ! ClusterFailure)
        badConfMembers.foreach(_ ! ClusterFailure)
        leaderFailed
    }

  def leaderInitialised(installedIndexBackend: String, installedIndexLocation: String): Behavior[Command] =
    Behaviors.receiveMessage {
      case JoinCluster(replyTo, indexBackend, indexLocation) if indexBackend == installedIndexBackend && indexLocation == installedIndexLocation =>
        replyTo ! ClusterSuccess
        Behaviors.same
      case JoinCluster(replyTo, _, _) =>
        replyTo ! ClusterSuccessConfigurationIgnored(installedIndexBackend)
        Behaviors.same
      case ClusterInitSuccess =>
        Behaviors.same
    }

  def leaderFailed: Behavior[Command] =
    Behaviors.receiveMessage {
      case joinCluster: JoinCluster =>
        joinCluster.replyTo ! ClusterFailure
        Behaviors.same
      case _ => Behaviors.same
    }
}
