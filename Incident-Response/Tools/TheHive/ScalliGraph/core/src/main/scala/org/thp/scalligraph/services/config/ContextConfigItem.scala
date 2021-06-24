package org.thp.scalligraph.services.config

import javax.inject.{Inject, Singleton}
import org.thp.scalligraph.BadConfigurationError
import org.thp.scalligraph.auth.AuthContext
import org.thp.scalligraph.models.Database
import org.thp.scalligraph.services.EventSrv
import play.api.libs.json.{Format, JsObject, JsValue, Json}

import scala.compat.java8.OptionConverters._
import scala.concurrent.ExecutionContext
import scala.util.{Failure, Try}

trait ConfigContext[C] {
  def defaultPath(path: String): String
  def getValue(context: C, path: String): Option[JsValue]
  def setValue(context: C, path: String, value: JsValue): Try[String]
}

@Singleton
class GlobalConfigContext @Inject() (db: Database) extends ConfigContext[Unit] {
  override def defaultPath(path: String): String = path

  override def getValue(context: Unit, path: String): Option[JsValue] =
    db.roTransaction { implicit graph =>
      graph
        .variables
        .get[String](s"config.$path")
    }.asScala
      .map(Json.parse)

  override def setValue(context: Unit, path: String, value: JsValue): Try[String] =
    db.tryTransaction { implicit graph =>
      Try(
        graph
          .variables
          .set(s"config.$path", value.toString)
      )
    }.map(_ => path)
}

trait ContextConfigItem[T, C] {
  val context: ConfigContext[C]
  val path: String
  val description: String
  val defaultValue: T
  val jsonFormat: Format[T]
  def get(context: C): T
  def set(context: C, v: T)(implicit authContext: AuthContext): Try[Unit]
  def validation(v: T): Try[T]
  def getDefaultValueJson: JsValue = jsonFormat.writes(defaultValue)
  def getJson(context: C): JsValue = jsonFormat.writes(get(context))

  def setJson(context: C, v: JsValue)(implicit authContext: AuthContext): Try[Unit] =
    jsonFormat
      .reads(v)
      .map(set(context, _))
      .fold(
        error => {
          val message = JsObject(error.map {
            case (path, es) => path.toString -> Json.toJson(es.flatMap(_.messages))
          })
          Failure(BadConfigurationError(message.toString))
        },
        identity
      )
}

class ContextConfigItemImpl[T, C](
    val context: ConfigContext[C],
    val path: String,
    val description: String,
    val defaultValue: T,
    val jsonFormat: Format[T],
    val validationFunction: T => Try[T],
    eventSrv: EventSrv,
    implicit val ec: ExecutionContext
) extends ContextConfigItem[T, C] {

  private var value: T       = _
  @volatile private var flag = false

  override def get(ctx: C): T = {
    if (!flag)
      synchronized {
        if (!flag)
          value = context
            .getValue(ctx, path)
            .flatMap(s => jsonFormat.reads(s).asOpt)
            .getOrElse(defaultValue)
        flag = true
      }
    value
  }

  override def set(ctx: C, v: T)(implicit authContext: AuthContext): Try[Unit] =
    validation(v).flatMap { value =>
      val valueJson = jsonFormat.writes(value)
      context
        .setValue(ctx, path, valueJson)
        .map(p => eventSrv.publish(ConfigTopic.topicName)(Invalidate(p)))
    }
  override def validation(v: T): Try[T] = validationFunction(v)
}
