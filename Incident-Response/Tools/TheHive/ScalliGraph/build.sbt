import Dependencies._

val scalligraphVersion     = "0.1.0-SNAPSHOT"
val scala212               = "2.12.13"
val scala213               = "2.13.1"
val supportedScalaVersions = List(scala212, scala213)

organization in ThisBuild := "org.thp"
scalaVersion in ThisBuild := scala212
crossScalaVersions in ThisBuild := supportedScalaVersions
resolvers in ThisBuild ++= Seq(
  Resolver.mavenLocal,
  "Oracle Released Java Packages" at "https://download.oracle.com/maven",
  "TheHive project repository" at "https://dl.bintray.com/thehive-project/maven/"
)
scalacOptions in ThisBuild ++= Seq(
  "-encoding",
  "UTF-8",
  "-deprecation", // Emit warning and location for usages of deprecated APIs.
  "-feature",     // Emit warning and location for usages of features that should be imported explicitly.
  "-unchecked",   // Enable additional warnings where generated code depends on assumptions.
  //"-Xfatal-warnings",      // Fail the compilation if there are any warnings.
  "-Xlint", // Enable recommended additional warnings.
//    "-Ywarn-adapted-args",     // Warn if an argument list is modified to match the receiver.
  //"-Ywarn-dead-code",      // Warn when dead code is identified.
//    "-Ywarn-inaccessible",     // Warn about inaccessible types in method signatures.
//    "-Ywarn-nullary-override", // Warn when non-nullary overrides nullary, e.g. def foo() over def foo.
  "-Ywarn-numeric-widen", // Warn when numerics are widened.
  "-Ywarn-value-discard", // Warn when non-Unit expression results are unused
  //"-Ylog-classpath",
  //"-Xlog-implicits",
  //"-Yshow-trees-compact",
  //"-Yshow-trees-stringified",
  //"-Ymacro-debug-lite",
  "-Xlog-free-types",
  "-Xlog-free-terms",
  "-Xprint-types"
)
fork in Test in ThisBuild := true
//        javaOptions += "-Xmx1G",
scalafmtConfig in ThisBuild := file(".scalafmt.conf")
scalacOptions in ThisBuild ++= {
  CrossVersion.partialVersion((Compile / scalaVersion).value) match {
    case Some((2, n)) if n >= 13 => "-Ymacro-annotations" :: Nil
    case _                       => Nil
  }
}
libraryDependencies in ThisBuild ++= {
  CrossVersion.partialVersion(scalaVersion.value) match {
    case Some((2, n)) if n >= 13 => Nil
    case _                       => compilerPlugin(macroParadise) :: Nil
  }
}

dependencyOverrides in ThisBuild += "io.netty" % "netty-all" % "4.0.56.Final"

lazy val scalligraph = (project in file("."))
  .dependsOn(core, /*graphql, */ janus /* , orientdb , neo4j, coreTest*/ )
  .dependsOn(coreTest % "test -> test")
  .aggregate(core, /*graphql, */ janus /* , orientdb, neo4j */, coreTest)
  .settings(
    name := "scalligraph",
    version := scalligraphVersion
  )

lazy val core = (project in file("core"))
  .settings(
    name := "scalligraph-core",
    version := scalligraphVersion,
    libraryDependencies ++= Seq(
      tinkerpop,
      scalactic,
      playGuice,
      scalaGuice,
      hadoopClient,
      alpakkaS3,
      akkaHttp,
      akkaHttpXml,
      playCore,
      apacheConfiguration,
      bouncyCastle,
      shapeless,
      caffeine,
      akkaCluster,
      akkaClusterTools,
      akkaClusterTyped,
      specs       % Test,
      playLogback % Test,
      scalaCompiler(scalaVersion.value),
      scalaReflect(scalaVersion.value),
      ws
    )
  )

lazy val coreTest = (project in file("core-test"))
  .dependsOn(core)
  .dependsOn(janus)
  //  .dependsOn(orientdb)
  //  .dependsOn(neo4j)
  .settings(
    name := "scalligraph-core-test",
    version := scalligraphVersion,
    libraryDependencies ++= Seq(
      janusGraphInMemory % Test,
      specs              % Test,
      playLogback        % Test
    )
  )

lazy val janus = (project in file("database/janusgraph"))
  .dependsOn(core)
  .settings(
    name := "scalligraph-janusgraph",
    version := scalligraphVersion,
    libraryDependencies ++= Seq(
      janusGraph,
      janusGraphBerkeleyDB,
//      janusGraphHBase,
      janusGraphLucene,
      janusGraphElasticSearch,
      janusGraphCassandra,
//      janusGraphDriver,
//      janusGraphCore,
      specs % Test
    )
  )

//lazy val orientdb = (project in file("database/orientdb"))
//  .dependsOn(core)
//  .settings(
//    name := "scalligraph-orientdb",
//    version := scalligraphVersion,
//    libraryDependencies ++= Seq(
//      gremlinScala,
//      gremlinOrientdb,
//      specs % Test
//    )
//  )
//
//lazy val neo4j = (project in file("database/neo4j"))
//  .dependsOn(core)
//  .settings(
//    name := "scalligraph-neo4j",
//    version := scalligraphVersion,
//    libraryDependencies ++= Seq(
//      gremlinScala,
//      neo4jGremlin,
//      neo4jTinkerpop,
//      specs % Test
//    )
//  )

//lazy val graphql = (project in file("graphql"))
//  .dependsOn(core)
//  .dependsOn(coreTest % "test->test")
//  .dependsOn(janus)
//  .settings(
//    name := "scalligraph-graphql",
//    version := scalligraphVersion,
//    libraryDependencies ++= Seq(
//      scalaGuice,
//      sangria,
//      sangriaPlay,
//      specs % Test
//    )
//  )
