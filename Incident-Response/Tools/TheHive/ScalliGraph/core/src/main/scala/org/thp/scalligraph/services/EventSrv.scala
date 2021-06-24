package org.thp.scalligraph.services

import akka.actor.{ActorRef, ActorSystem}
import akka.cluster.pubsub.DistributedPubSub
import akka.cluster.pubsub.DistributedPubSubMediator.{Publish, Subscribe, Unsubscribe}
import akka.pattern.{ask => akkaAsk}
import akka.util.Timeout
import javax.inject.{Inject, Singleton}
import play.api.Logger

import scala.concurrent.Future

@Singleton
class EventSrv @Inject() (system: ActorSystem) {
  lazy val logger: Logger = Logger(getClass)
  private val mediator    = DistributedPubSub(system).mediator

  def publish(topicName: String)(message: Any): Unit = {
    logger.debug(s"publish $topicName $message")
    mediator ! Publish(topicName, message)
  }

  def publishAsk(topicName: String)(message: Any)(implicit timeout: Timeout): Future[Any] = {
    logger.debug(s"publish $topicName $message")
    mediator ? Publish(topicName, message)
  }

  def subscribe(topicName: String, actor: ActorRef): Unit = mediator ! Subscribe(topicName, actor)

  def unsubscribe(topicName: String, actor: ActorRef): Unit = mediator ! Unsubscribe(topicName, actor)
}
