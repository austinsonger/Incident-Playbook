package org.thp.scalligraph.services

import javax.inject.{Inject, Provider, Singleton}
import org.thp.scalligraph.models.Model
import play.api.Logger

import scala.collection.immutable

@Singleton
class ModelSrv @Inject() (modelsProvider: Provider[immutable.Set[Model]]) {
  private[ModelSrv] lazy val logger: Logger = Logger(getClass)

  lazy val models: Set[Model]                 = modelsProvider.get
  private[ModelSrv] lazy val modelMap         = models.map(m => m.label -> m).toMap
  def apply(modelName: String): Option[Model] = modelMap.get(modelName)
  val list: Set[Model]                        = models
}
