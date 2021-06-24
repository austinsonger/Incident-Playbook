package org.thp.scalligraph.utils

import java.lang.{Boolean => JBoolean, Byte => JByte, Double => JDouble, Float => JFloat, Long => JLong, Short => JShort}
import java.math.{BigInteger, BigDecimal => JBigDecimal}
import java.util.{Properties, Iterator => JIterator, List => JList}

import org.apache.commons.configuration.{Configuration => ApacheConfig}
import play.api.{Configuration => PlayConfig}

import scala.collection.JavaConverters._

class Config(config: PlayConfig) extends ApacheConfig {
  override def subset(prefix: String): ApacheConfig                               = new Config(config.getOptional[PlayConfig](prefix).getOrElse(PlayConfig.empty))
  override def isEmpty: Boolean                                                   = config.underlying.isEmpty
  override def containsKey(key: String): Boolean                                  = config.keys.contains(key)
  override def addProperty(key: String, value: scala.Any): Unit                   = ???
  override def setProperty(key: String, value: scala.Any): Unit                   = ???
  override def clearProperty(key: String): Unit                                   = ???
  override def clear(): Unit                                                      = ???
  override def getProperty(key: String): AnyRef                                   = config.underlying.getAnyRef(key)
  override def getKeys(prefix: String): JIterator[String]                         = config.keys.filter(_.startsWith(prefix)).toIterator.asJava
  override def getKeys: JIterator[String]                                         = config.keys.toIterator.asJava
  override def getProperties(key: String): Properties                             = ???
  override def getBoolean(key: String): Boolean                                   = config.get[Boolean](key)
  override def getBoolean(key: String, defaultValue: Boolean): Boolean            = config.getOptional[Boolean](key).getOrElse(defaultValue)
  override def getBoolean(key: String, defaultValue: JBoolean): JBoolean          = config.getOptional[Boolean](key).fold(defaultValue)(Boolean.box)
  override def getByte(key: String): Byte                                         = config.get[Int](key).toByte
  override def getByte(key: String, defaultValue: Byte): Byte                     = config.getOptional[Int](key).fold(defaultValue)(_.toByte)
  override def getByte(key: String, defaultValue: JByte): JByte                   = config.getOptional[Int](key).fold(defaultValue)(_.toByte)
  override def getDouble(key: String): Double                                     = config.get[Double](key)
  override def getDouble(key: String, defaultValue: Double): Double               = config.getOptional[Double](key).getOrElse(defaultValue)
  override def getDouble(key: String, defaultValue: JDouble): JDouble             = config.getOptional[Double](key).fold(defaultValue)(Double.box)
  override def getFloat(key: String): Float                                       = config.get[Double](key).toFloat
  override def getFloat(key: String, defaultValue: Float): Float                  = config.getOptional[Double](key).fold(defaultValue)(_.toFloat)
  override def getFloat(key: String, defaultValue: JFloat): JFloat                = config.getOptional[Double](key).fold(defaultValue)(_.toFloat)
  override def getInt(key: String): Int                                           = config.get[Int](key)
  override def getInt(key: String, defaultValue: Int): Int                        = config.getOptional[Int](key).getOrElse(defaultValue)
  override def getInteger(key: String, defaultValue: Integer): Integer            = config.getOptional[Int](key).fold(defaultValue)(Int.box)
  override def getLong(key: String): Long                                         = config.get[Long](key)
  override def getLong(key: String, defaultValue: Long): Long                     = config.getOptional[Long](key).getOrElse(defaultValue)
  override def getLong(key: String, defaultValue: JLong): JLong                   = config.getOptional[Long](key).fold(defaultValue)(_.asInstanceOf[JLong])
  override def getShort(key: String): Short                                       = config.get[Int](key).toShort
  override def getShort(key: String, defaultValue: Short): Short                  = config.getOptional[Int](key).fold(defaultValue)(_.toShort)
  override def getShort(key: String, defaultValue: JShort): JShort                = config.getOptional[Int](key).fold(defaultValue)(_.toShort.asInstanceOf[JShort])
  override def getBigDecimal(key: String): JBigDecimal                            = ???
  override def getBigDecimal(key: String, defaultValue: JBigDecimal): JBigDecimal = ???
  override def getBigInteger(key: String): BigInteger                             = ???
  override def getBigInteger(key: String, defaultValue: BigInteger): BigInteger   = ???
  override def getString(key: String): String                                     = config.get[String](key)
  override def getString(key: String, defaultValue: String): String               = config.getOptional[String](key).getOrElse(defaultValue)
  override def getStringArray(key: String): Array[String]                         = config.get[Seq[String]](key).toArray
  override def getList(key: String): JList[AnyRef] =
    config.underlying.getAnyRef(key) match {
      case l: JList[_] => l.asInstanceOf[JList[AnyRef]]
      case v           => Seq(v).asJava
    }
  override def getList(key: String, defaultValue: JList[_]): JList[AnyRef] = ???
}
