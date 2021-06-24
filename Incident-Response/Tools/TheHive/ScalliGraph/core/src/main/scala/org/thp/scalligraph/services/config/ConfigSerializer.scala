package org.thp.scalligraph.services.config

import java.io.NotSerializableException

import akka.serialization.Serializer

class ConfigSerializer extends Serializer {
  override def identifier: Int = 226591534

  override def includeManifest: Boolean = false

  /**
    * Serializes the given object into an Array of Byte
    */
  def toBinary(o: AnyRef): Array[Byte] =
    o match {
      case WaitNotification(path) => s"W$path".getBytes
      case Invalidate(path)       => s"I$path".getBytes
      case _                      => Array.empty[Byte] // Not serializable
    }

  /**
    * Produces an object from an array of bytes, with an optional type-hint;
    * the class should be loaded using ActorSystem.dynamicAccess.
    */
  @throws(classOf[NotSerializableException])
  def fromBinary(bytes: Array[Byte], manifest: Option[Class[_]]): AnyRef = {
    val s = new String(bytes)
    s(0) match {
      case 'W' => WaitNotification(s.tail)
      case 'I' => Invalidate(s.tail)
      case _   => throw new NotSerializableException
    }
  }
}
