//package org.thp.scalligraph.models
//
//import akka.actor.ActorSystem
//import com.typesafe.config.ConfigFactory
//
//import org.specs2.specification.core.Fragments
//import org.thp.scalligraph.auth.{AuthContext, AuthContextImpl}
//import org.thp.scalligraph.janus.JanusDatabase
//import org.thp.scalligraph.{RichSeq, VertexEntity}
//import play.api.libs.logback.LogbackLoggerConfigurator
//import play.api.test.PlaySpecification
//import play.api.{Configuration, Environment}
//
//import scala.util.{Success, Try}
//
//class TimingStats {
//  private var iteration: List[Long] = Nil
//  def time[A](body: => A): A = {
//    val start = System.currentTimeMillis()
//    val a     = body
//    val end   = System.currentTimeMillis()
//    iteration = (end - start) :: iteration
//    a
//  }
//
//  override def toString: String = {
//    val count  = iteration.length
//    val sum    = iteration.sum
//    val mean   = sum.toDouble / count
//    val stddev = Math.sqrt(iteration.foldLeft(0d)((acc, i) => acc + Math.pow(i.toDouble - mean, 2)) / count)
//    s"Timing: $count iterations, mean: ${mean}ms, stddev: $stddev, min: ${iteration.min}ms, max: ${iteration.max}ms"
//  }
//}
//
//@DefineIndex(IndexType.basic, "name")
//@VertexEntity
//case class EntityWithName(name: String, value: Int)
//
//class PerformanceTest extends PlaySpecification {
//  (new LogbackLoggerConfigurator).configure(Environment.simple(), Configuration.empty, Map.empty)
//  val authContext: AuthContext = AuthContextImpl("me", "", "", "", Set.empty)
//  sequential
//
//  Fragments.foreach(
//    new DatabaseProviders(
//      Configuration(ConfigFactory.parseString("""
//                                                |db {
//                                                |  onConflict {
//                                                |    maxAttempts = 6
//                                                |    minBackoff = 100 milliseconds
//                                                |    maxBackoff = 1 seconds
//                                                |    randomFactor = 0.2
//                                                |  }
//                                                |  chunkSize = 32k
//                                                |  janusgraph {
//                                                |    storage {
//                                                |      backend: cql
//                                                |      hostname: ["172.17.0.2"]
//                                                |      cql {
//                                                |        cluster-name: Test Cluster
//                                                |        keyspace: thehive
//                                                |      }
//                                                |    }
//                                                |    ids {
//                                                |      block-size: 500000
//                                                |    }
//                                                |  }
//                                                |}
//                                                |""".stripMargin)),
////      num-partitions: 10
////        renew-percentage: 0.3
////      |    cache {
////        |      db-cache: true
////        |    }
//      //      |      db-cache-clean-wait: 1000
//      ActorSystem("DatabaseProviders")
//    ).list
//  ) { dbProvider =>
////    "unique index" in {
////      implicit val db: Database                     = dbProvider.get()
////      val model: Model.Vertex[EntityWithUniqueName] = Model.vertex[EntityWithUniqueName]
////
////      def getOrCreate(entity: EntityWithUniqueName)(implicit graph: Graph): EntityWithUniqueName with Entity =
////        db.labelFilter("EntityWithUniqueName")(graph.V)
////          .has(Key("name") -> entity.name)
////          .headOption
////          .fold(db.createVertex(graph, authContext, model, entity))(vertex => model.toDomain(vertex))
////
////      db.createSchema(model)
////      val createTiming = new TimingStats
////      (1 to 100000).toTry { i =>
////        if (i % 1000 == 0) println(s"creation: $i")
////        createTiming.time {
////          db.tryTransaction { implicit graph =>
////            Try(getOrCreate(EntityWithUniqueName(i.toString, i)))
////          }
////        }
////      }
////      val getTiming = new TimingStats
////      (1 to 100000).toTry { i =>
////        if (i % 1000 == 0) println(s"retrieve: $i")
////        getTiming.time {
////          db.tryTransaction { implicit graph =>
////            Success(getOrCreate(EntityWithUniqueName(i.toString, i + 1)).value must_== i)
////          }
////        }
////      }
////      println(s"[unique index] creation: $createTiming")
////      println(s"[unique index] retrieve: $getTiming")
////      ok
////    }
//
//    "basic index" in {
//      val iterations                          = 10000
//      val initDb: Database                    = dbProvider.get()
//      val model: Model.Vertex[EntityWithName] = Model.vertex[EntityWithName]
//      initDb.createSchema(model).get
//      val db = initDb match {
//        case j: JanusDatabase => j.batchMode
//        case other            => other
//      }
//
//      def getOrCreate(entity: EntityWithName)(implicit graph: Graph): EntityWithName with Entity =
//        db.labelFilter("EntityWithName")(graph.V)
//          .has(Key("name") -> entity.name)
//          .headOption
//          .fold(db.createVertex(graph, authContext, model, entity))(vertex => model.toDomain(vertex)(db))
//
//      db.createSchema(model)
//      val createTiming = new TimingStats
//      (1 to iterations).toTry { i =>
//        if (i % 1000 == 0) println(s"creation: $i")
//        createTiming.time {
//          db.tryTransaction { implicit graph =>
//            Try(getOrCreate(EntityWithName(i.toString, i)))
//          }
//        }
//      }.get
//      val getTiming = new TimingStats
//      (iterations * 9 / 10 + 1 to iterations * 11 / 10).toTry { i =>
//        if (i % 1000 == 0) println(s"retrieve: $i")
//        getTiming.time {
//          db.tryTransaction { implicit graph =>
//            Success(getOrCreate(EntityWithName(i.toString, i + 1)).value)
//          }
//        }
//      }.get
//      val findDuplicatedTiming = new TimingStats
//      findDuplicatedTiming.time {
//        db.tryTransaction { implicit graph =>
//          val x = db
//            .labelFilter("EntityWithName")(graph.V)
//            .groupCount(By(Key[String]("name")))
//            .unfold[java.util.Map.Entry[String, Long]]()
//            .where(x => x.selectValues.is(P.gt(1L)))
//            .toList
//
//          Success(x)
//        }
//      }
//      println(s"[basic index] creation: $createTiming")
//      println(s"[basic index] retrieve: $getTiming")
//      println(s"[basic index] find duplicated: $findDuplicatedTiming")
//      ok
//    }
//
//  }
//
//}
