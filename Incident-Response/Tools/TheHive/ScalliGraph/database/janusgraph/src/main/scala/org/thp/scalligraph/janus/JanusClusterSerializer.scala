package org.thp.scalligraph.janus

import akka.actor.ExtendedActorSystem
import akka.actor.typed.{ActorRef, ActorRefResolver}
import akka.actor.typed.scaladsl.adapter.ClassicActorSystemOps
import akka.serialization.Serializer
import play.api.libs.json.{Json, OFormat, Reads, Writes}

import java.io.NotSerializableException

class JanusClusterSerializer(system: ExtendedActorSystem) extends Serializer {
  import JanusClusterManagerActor._

  private val actorRefResolver = ActorRefResolver(system.toTyped)

  implicit def actorRefReads[T]: Reads[ActorRef[T]]    = Reads.StringReads.map(actorRefResolver.resolveActorRef)
  implicit def actorRefWrites[T]: Writes[ActorRef[T]]  = Writes.StringWrites.contramap[ActorRef[T]](actorRefResolver.toSerializationFormat)
  implicit val joinClusterFormat: OFormat[JoinCluster] = Json.format[JoinCluster]

  override def identifier: Int = 775347820

  override def toBinary(o: AnyRef): Array[Byte] =
    o match {
      case joinCluster: JoinCluster                         => 0.toByte +: Json.toJson(joinCluster).toString.getBytes
      case ClusterRequestInit                               => Array(1)
      case ClusterInitSuccess                               => Array(2)
      case ClusterInitFailure                               => Array(3)
      case ClusterSuccessConfigurationIgnored(indexBackend) => 4.toByte +: indexBackend.getBytes
      case ClusterSuccess                                   => Array(5)
      case ClusterFailure                                   => Array(6)
      case GetStatus(replyTo)                               => 7.toByte +: actorRefResolver.toSerializationFormat(replyTo).getBytes
      case StatusInit                                       => Array(8)
      case StatusSuccess                                    => Array(9)
      case StatusFailure                                    => Array(10)
      case _                                                => throw new NotSerializableException
    }

  override def includeManifest: Boolean = false

  override def fromBinary(bytes: Array[Byte], manifest: Option[Class[_]]): AnyRef =
    bytes(0) match {
      case 0  => Json.parse(bytes.tail).as[JoinCluster]
      case 1  => ClusterRequestInit
      case 2  => ClusterInitSuccess
      case 3  => ClusterInitFailure
      case 4  => ClusterSuccessConfigurationIgnored(new String(bytes.tail))
      case 5  => ClusterSuccess
      case 6  => ClusterFailure
      case 7  => GetStatus(actorRefResolver.resolveActorRef(new String(bytes.tail)))
      case 8  => StatusInit
      case 9  => StatusSuccess
      case 10 => StatusFailure
      case _  => throw new NotSerializableException
    }
}
