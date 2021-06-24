package org.thp.scalligraph.`macro`

import scala.reflect.macros.whitebox

class AnnotationMacro(val c: whitebox.Context) extends MacroUtil with MappingMacroHelper with MacroLogger {

  import c.universe._

  def buildVertexModel(annottees: Tree*): Tree =
    annottees.toList match {
      case (modelClass @ ClassDef(classMods, className, Nil, _)) :: tail if classMods.hasFlag(Flag.CASE) =>
        val modelDef = Seq(
          q"val model: org.thp.scalligraph.models.Model.Vertex[$className] = org.thp.scalligraph.models.Model.buildVertexModel[$className]"
        )

        val modelModule = tail match {
          case ModuleDef(moduleMods, moduleName, moduleTemplate) :: Nil =>
            val parents = tq"org.thp.scalligraph.models.HasModel" :: moduleTemplate.parents.filterNot {
              case Select(_, TypeName("AnyRef")) => true
              case _                             => false
            }

            ModuleDef(
              moduleMods,
              moduleName,
              Template(parents = parents, self = moduleTemplate.self, body = moduleTemplate.body ++ modelDef)
            )
          case Nil =>
            val moduleName = className.toTermName
            q"object $moduleName extends org.thp.scalligraph.models.HasModel { ..$modelDef }"
        }

        Block(modelClass :: modelModule :: Nil, Literal(Constant(())))
    }

  def buildEdgeModel(annottees: Tree*): Tree =
    annottees.toList match {
      case (modelClass @ ClassDef(classMods, className, Nil, _)) :: tail if classMods.hasFlag(Flag.CASE) =>
        val modelDef = Seq(
          q"val model = org.thp.scalligraph.models.Model.buildEdgeModel[$className]"
        )
        val modelModule = tail match {
          case ModuleDef(moduleMods, moduleName, moduleTemplate) :: Nil =>
            val parents = tq"org.thp.scalligraph.models.HasModel" :: moduleTemplate.parents.filterNot {
              case Select(_, TypeName("AnyRef")) => true
              case _                             => false
            }
            ModuleDef(
              moduleMods,
              moduleName,
              Template(
                parents = parents,
                self = moduleTemplate.self,
                body = moduleTemplate.body ++ modelDef
              )
            )
          case Nil =>
            val moduleName = className.toTermName
            q"object $moduleName extends org.thp.scalligraph.models.HasModel { ..$modelDef }"
        }

        Block(modelClass :: modelModule :: Nil, Literal(Constant(())))
    }
}
