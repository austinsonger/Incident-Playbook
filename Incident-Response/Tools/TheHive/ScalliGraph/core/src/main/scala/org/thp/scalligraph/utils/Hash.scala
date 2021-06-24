package org.thp.scalligraph.utils

import java.io.InputStream
import java.nio.charset.Charset
import java.nio.file.{Files, Path, Paths}
import java.security.MessageDigest

import akka.stream.Materializer
import akka.stream.scaladsl.{FileIO, Source}
import akka.util.ByteString
import play.api.libs.json.{Format, JsString, Reads, Writes}

import scala.concurrent.duration.DurationInt
import scala.concurrent.{Await, ExecutionContext, Future}

case class Hasher(algorithms: String*) {

  val bufferSize = 4096

  def fromPath(path: Path): Seq[Hash] =
    fromInputStream(Files.newInputStream(path))

  def fromInputStream(is: InputStream): Seq[Hash] = {
    val mds = algorithms.map(algo => MessageDigest.getInstance(algo))
    def readNextBuffer: Array[Byte] = {
      val buffer = Array.ofDim[Byte](bufferSize)
      val len    = is.read(buffer)
      if (len == bufferSize) buffer else buffer.take(len)
    }

    Iterator
      .continually(readNextBuffer)
      .takeWhile(_.nonEmpty)
      .foreach(buffer => mds.foreach(md => md.update(buffer)))
    mds.map(md => Hash(md.digest()))
  }

  def fromString(data: String): Seq[Hash] = fromBinary(data.getBytes(Charset.forName("UTF8")))

  def fromBinary(data: Array[Byte]): Seq[Hash] = {
    val mds = algorithms.map(algo => MessageDigest.getInstance(algo))
    mds.map(md => Hash(md.digest(data)))
  }

  def fromBinary(data: Source[ByteString, _])(implicit mat: Materializer): Seq[Hash] = {
    val mds = algorithms.map(algo => MessageDigest.getInstance(algo))
    Await.ready(data.runForeach(bs => mds.foreach(_.update(bs.toByteBuffer))), 5.minutes)
    mds.map(md => Hash(md.digest()))
  }
}

class MultiHash(algorithms: String)(implicit mat: Materializer, ec: ExecutionContext) {
  private val md = MessageDigest.getInstance(algorithms)

  def addValue(value: String): Unit = {
    md.update(0.asInstanceOf[Byte])
    md.update(value.getBytes)
  }
  def addFile(filename: String): Future[Unit] = addFile(Paths.get(filename))

  def addFile(file: Path): Future[Unit] = {
    md.update(0.asInstanceOf[Byte])
    FileIO
      .fromPath(file)
      .runForeach(bs => md.update(bs.toByteBuffer))
      .map(_ => ())
  }

  def addSource(source: Source[ByteString, _]): Future[Unit] =
    source
      .runForeach(bs => md.update(bs.toByteBuffer))
      .map(_ => ())
  def digest: Hash = Hash(md.digest())
}

case class Hash(data: Array[Byte]) {
  override def toString: String = data.map(b => f"$b%02x").mkString

  override def equals(obj: scala.Any): Boolean = obj match {
    case Hash(d) => d.sameElements(data)
    case _       => false
  }
}

object Hash {

  def apply(s: String): Hash = Hash {
    s.grouped(2)
      .map { cc =>
        (Character.digit(cc(0), 16) << 4 | Character.digit(cc(1), 16)).toByte
      }
      .toArray
  }

  val hashReads: Reads[Hash]            = Reads(json => json.validate[String].map(h => Hash(h)))
  val hashWrites: Writes[Hash]          = Writes[Hash](h => JsString(h.toString()))
  implicit val hashFormat: Format[Hash] = Format(hashReads, hashWrites)
}
