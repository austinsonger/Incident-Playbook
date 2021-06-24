package org.thp.scalligraph.services.config

import akka.actor.{Actor, ActorRef}
import javax.inject.Inject
import org.thp.scalligraph.services.EventSrv

class ConfigActor @Inject() (eventSrv: EventSrv) extends Actor {

  override def preStart(): Unit = {
    eventSrv.subscribe(ConfigTopic.topicName, self)
    super.preStart()
  }

  override def receive: Receive = receive(Nil)

  def receive(clients: List[(String, ActorRef)]): Receive = {
    case WaitNotification(path) => context.become(receive((path -> sender()) :: clients))
    case msg @ Invalidate(path) =>
      val (clientsToBeNotified, otherClients) = clients.partition(_._1 == path)
      clientsToBeNotified.foreach(_._2 ! msg)
      context.become(receive(otherClients))
  }
}

object ConfigTopic {
  val topicName: String = "config"
}
sealed trait ConfigMessage
case class WaitNotification(path: String) extends ConfigMessage
case class Invalidate(path: String)       extends ConfigMessage
