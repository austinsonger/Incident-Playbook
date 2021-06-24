package org.thp.scalligraph.models

import org.apache.tinkerpop.gremlin.process.traversal.P
import org.thp.scalligraph.controllers.Renderer
import org.thp.scalligraph.query._
import org.thp.scalligraph.traversal.Traversal
import org.thp.scalligraph.traversal.TraversalOps._
import play.api.libs.json.{Json, OWrites}

case class OutputPerson(createdBy: String, label: String, name: String, age: Int)

object OutputPerson {
  implicit val writes: OWrites[OutputPerson] = Json.writes[OutputPerson]
}

case class OutputSoftware(createdBy: String, name: String, lang: String)

object OutputSoftware {
  implicit val writes: OWrites[OutputSoftware] = Json.writes[OutputSoftware]
}

object ModernOutputs {
  implicit val personOutput: Renderer[Person with Entity] =
    Renderer.toJson[Person with Entity, OutputPerson](person =>
      new OutputPerson(person._createdBy, s"Mister ${person.name}", person.name, person.age)
    )
  implicit val softwareOutput: Renderer[Software with Entity] =
    Renderer.toJson[Software with Entity, OutputSoftware](software => new OutputSoftware(software._createdBy, software.name, software.lang))
}

case class SeniorAgeThreshold(age: Int)
case class FriendLevel(level: Double)

class ModernQueryExecutor(implicit val db: Database) extends QueryExecutor {
  import ModernOps._
  import ModernOutputs._

  override val limitedCountThreshold: Long = 1000
  val personSrv                            = new PersonSrv
  val softwareSrv                          = new SoftwareSrv

  override val version: (Int, Int) = 1 -> 1

  override lazy val publicProperties: PublicProperties = {
    val labelMapping = SingleMapping[String, String](
      toGraph = {
        case d if d startsWith "Mister " => d.drop(7)
        case d                           => d
      },
      toDomain = (g: String) => "Mister " + g
    )
    PublicPropertyListBuilder[Person]
      .property("createdBy", UMapping.string)(_.rename("_createdBy").readonly)
      .property("label", labelMapping)(_.rename("name").updatable)
      .property("name", UMapping.string)(_.field.updatable)
      .property("age", UMapping.int)(_.field.updatable)
      .build ++
      PublicPropertyListBuilder[Software]
        .property("createdBy", UMapping.string)(_.rename("_createdBy").readonly)
        .property("name", UMapping.string)(_.field.updatable)
        .property("lang", UMapping.string)(_.field.updatable)
//        .property("any", UMapping.string)(
//          _.select(
//            _.property[String, String]("_createdBy", UMapping.string),
//            _.property("name", UMapping.string),
//            _.property("lang", UMapping.string)
//          ).readonly
//        )
        .build
  }

  override lazy val queries: Seq[ParamQuery[_]] = Seq(
    Query.init[Traversal.V[Person]]("allPeople", (graph, _) => personSrv.startTraversal(graph)),
    Query.init[Traversal.V[Software]]("allSoftware", (graph, _) => softwareSrv.startTraversal(graph)),
    Query.initWithParam[SeniorAgeThreshold, Traversal.V[Person]](
      "seniorPeople",
      (seniorAgeThreshold, graph, _) => personSrv.startTraversal(graph).has(_.age, P.gte(seniorAgeThreshold.age))
    ),
    Query[Traversal.V[Person], Traversal.V[Software]]("created", (personSteps, _) => personSteps.created),
    Query.withParam[FriendLevel, Traversal.V[Person], Traversal.V[Person]](
      "friends",
      (friendLevel, personSteps, _) => personSteps.friends(friendLevel.level)
    ),
    Query.output[Person with Entity, Traversal.V[Person]],
    Query.output[Software with Entity, Traversal.V[Software]]
  )
}
