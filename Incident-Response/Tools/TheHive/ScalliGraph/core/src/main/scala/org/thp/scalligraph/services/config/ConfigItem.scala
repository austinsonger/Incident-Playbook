package org.thp.scalligraph.services.config

import akka.actor.ActorRef
import akka.pattern.ask
import org.thp.scalligraph.BadConfigurationError
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models.Database
import org.thp.scalligraph.services.EventSrv
import play.api.Logger
import play.api.libs.json.{Format, JsObject, JsValue, Json}

import scala.compat.java8.OptionConverters._
import scala.concurrent.ExecutionContext
import scala.concurrent.duration.DurationInt
import scala.util.{Failure, Success, Try}

trait ConfigItem[B, F] {
  val path: String
  val description: String
  val defaultValue: B
  val jsonFormat: Format[B]
  def get: F
  def set(v: B)(implicit authContext: AuthContext): Try[Unit]
  def validation(v: B): Try[B]
  def getDefaultValueJson: JsValue = jsonFormat.writes(defaultValue)
  def getJson: JsValue

  def setJson(v: JsValue)(implicit authContext: AuthContext): Try[Unit] =
    jsonFormat
      .reads(v)
      .map(b => set(b))
      .fold(
        error => {
          val message = JsObject(error.map {
            case (path, es) => path.toString -> Json.toJson(es.flatMap(_.messages))
          })
          Failure(BadConfigurationError(message.toString))
        },
        identity
      )
  def onUpdate(f: (B, B) => Unit): Unit
}

class ConfigItemImpl[B, F](
    val path: String,
    val description: String,
    val defaultValue: B,
    val jsonFormat: Format[B],
    val validationFunction: B => Try[B],
    mapFunction: B => F,
    db: Database,
    eventSrv: EventSrv,
    configActor: ActorRef,
    implicit val ec: ExecutionContext
) extends ConfigItem[B, F] {
  lazy val logger: Logger                           = Logger(getClass)
  private var fValue: F                             = _
  private var bValue: B                             = _
  @volatile private var flag                        = false
  private var updateCallbacks: List[(B, B) => Unit] = Nil

  invalidateCache(Success(()))

  private def invalidateCache(msg: Try[Any]): Unit = {
    msg.foreach {
      case Invalidate(_) =>
        val oldValue = bValue
        bValue = getValue.getOrElse(defaultValue)
        fValue = mapFunction(bValue)
        updateCallbacks.foreach(_.apply(oldValue, bValue))
      case _ =>
    }
    configActor
      .ask(WaitNotification(path))(1.hour)
      .onComplete { msg =>
        logger.debug(s"Receive message from config actor: $msg")
        invalidateCache(msg)
      }
  }

  protected def getValue: Option[B] =
    db.roTransaction { implicit graph =>
      graph
        .variables
        .get[String](s"config.$path")
    }.asScala
      .flatMap(s => Try(Json.parse(s)).toOption)
      .flatMap(jsonFormat.reads(_).asOpt)

  private def retrieveValues(): Unit =
    synchronized {
      if (!flag) {
        bValue = getValue.getOrElse(defaultValue)
        fValue = mapFunction(bValue)
        flag = true
      }
    }

  override def get: F = {
    if (!flag) retrieveValues()
    fValue
  }

  override def getJson: JsValue = {
    if (!flag) retrieveValues()
    jsonFormat.writes(bValue)
  }

  override def set(v: B)(implicit authContext: AuthContext): Try[Unit] =
    validation(v).flatMap { value =>
      val valueJson = jsonFormat.writes(value)
      db.tryTransaction { implicit graph =>
        Try(
          graph
            .variables
            .set(s"config.$path", valueJson.toString)
        )
      }.map(_ => eventSrv.publish(ConfigTopic.topicName)(Invalidate(path)))
    }

  override def validation(v: B): Try[B] = validationFunction(v)

  override def onUpdate(f: (B, B) => Unit): Unit =
    synchronized {
      updateCallbacks = f :: updateCallbacks
    }
}
