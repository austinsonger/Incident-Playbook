package org.thp.scalligraph.models

import java.lang.{Boolean => JBoolean, Byte => JByte, Double => JDouble, Float => JFloat, Integer => JInt, Long => JLong, Short => JShort}
import java.util.{Base64, Date}

import org.apache.tinkerpop.gremlin.structure.VertexProperty.Cardinality
import org.apache.tinkerpop.gremlin.structure.{Element, Vertex, VertexProperty}
import org.thp.scalligraph.auth.Permission
import org.thp.scalligraph.controllers.Renderer
import org.thp.scalligraph.traversal.TraversalOps._
import org.thp.scalligraph.traversal.{BiConverter, Converter, IdentityConverter, Traversal}
import org.thp.scalligraph.utils.Hash
import org.thp.scalligraph.{EntityId, InternalError}
import play.api.libs.json._

import scala.collection.JavaConverters._
import scala.reflect.runtime.{universe => ru}
import scala.reflect.{classTag, ClassTag}

sealed trait MappingCardinality {
  val gremlinCardinality: VertexProperty.Cardinality
  override lazy val toString: String = getClass.getCanonicalName
}
object MappingCardinality {
  type Value = MappingCardinality
  object single extends MappingCardinality {
    override val gremlinCardinality: Cardinality = VertexProperty.Cardinality.single
  }
  object option extends MappingCardinality {
    override val gremlinCardinality: Cardinality = VertexProperty.Cardinality.single
  }
  object list extends MappingCardinality {
    override val gremlinCardinality: Cardinality = VertexProperty.Cardinality.list
  }
  object set extends MappingCardinality {
    override val gremlinCardinality: Cardinality = VertexProperty.Cardinality.set
  }

  def isCompatible(c1: Value, c2: Value): Boolean = c1.gremlinCardinality == c2.gremlinCardinality
}

trait UMapping[D] {
  _: Mapping[D, _, _] =>
  type SingleType
  type GraphType
  def toMapping: Mapping[D, _, _] = this
}

trait MappingLowestPrio {
//  implicit def build[T]: UMapping[T] = macro MappingMacro.getOrBuildMapping[T]
}

trait MappingLowerPrio extends MappingLowestPrio {
  implicit object json extends SingleMapping[JsValue, String](toGraph = j => j.toString, toDomain = s => Json.parse(s))
}

object UMapping extends MappingLowerPrio {
  def apply[T](implicit mapping: UMapping[T]): UMapping[T] = mapping
  implicit val permissionWrites: Writes[Permission]        = Writes.stringableWrites(Predef.identity)
  implicit object jsObject extends SingleMapping[JsObject, String](toGraph = j => j.toString, toDomain = s => Json.parse(s).as[JsObject])
  def identity[T: ClassTag: Renderer: NoValue]: IdentityMapping[T] = IdentityMapping[T]()
  implicit object entityId   extends SingleMapping[EntityId, String](_.value, EntityId.read)
  implicit object string     extends IdentityMapping[String]
  implicit object long       extends SingleMapping[Long, JLong](toGraph = Long.box, toDomain = Long.unbox)
  implicit object int        extends SingleMapping[Int, JInt](toGraph = Int.box, toDomain = Int.unbox)
  implicit object date       extends IdentityMapping[Date]
  implicit object boolean    extends SingleMapping[Boolean, JBoolean](toGraph = Boolean.box, toDomain = Boolean.unbox)
  implicit object double     extends SingleMapping[Double, JDouble](toGraph = Double.box, toDomain = Double.unbox)
  implicit object float      extends SingleMapping[Float, JFloat](toGraph = Float.box, toDomain = Float.unbox)
  implicit object permission extends SingleMapping[Permission, String](toGraph = _.asInstanceOf[String], toDomain = Permission.apply)
  implicit object hash       extends SingleMapping[Hash, String](toGraph = h => h.toString, toDomain = Hash(_))
  implicit object binary
      extends SingleMapping[Array[Byte], String](toGraph = b => Base64.getEncoder.encodeToString(b), toDomain = s => Base64.getDecoder.decode(s))
  implicit def option[D, G](implicit subMapping: SingleMapping[D, G]): OptionMapping[D, G] = OptionMapping(subMapping)
  implicit def seq[D, G](implicit subMapping: SingleMapping[D, G]): ListMapping[D, G]      = ListMapping(subMapping)
  implicit def set[D, G](implicit subMapping: SingleMapping[D, G]): SetMapping[D, G]       = SetMapping(subMapping)
  implicit def enum[E <: Enumeration: ClassTag]: SingleMapping[E#Value, String] =
    SingleMapping[E#Value, String](
      _.toString,
      { value =>
        val rm: ru.Mirror = ru.runtimeMirror(getClass.getClassLoader)
        val instance      = rm.reflectModule(rm.classSymbol(classTag[E].runtimeClass).asClass.module.asModule).instance
        instance.asInstanceOf[E].withName(value)
      }
    )

  def jsonNative: SingleMapping[JsValue, Any] = {
    implicit val noValue: NoValue[Any] = NoValue[Any]("")
    SingleMapping[JsValue, Any](
      toGraph = {
        case JsString(s)  => Some(s)
        case JsBoolean(b) => Some(b)
        case JsNumber(v)  => Some(v)
        case _            => None
      },
      toDomain = {
        case s: String  => JsString(s)
        case b: Boolean => JsBoolean(b)
        case d: Date    => JsNumber(d.getTime)
        case n: Number  => JsNumber(n.doubleValue())
        case _          => JsNull
      }
    )
  }

}

abstract class Mapping[M, D: ClassTag, G: ClassTag: NoValue](
    toGraph: D => G = (_: D).asInstanceOf[G],
    toDomain: G => D = (_: G).asInstanceOf[D]
)(implicit val getRenderer: Renderer[M], val selectRenderer: Renderer[D])
    extends UMapping[M]
    with BiConverter[D, G] {
  override type SingleType = D
  override type GraphType  = G
  val graphTypeClass: Class[_]  = Option(classTag[G]).fold[Class[_]](classOf[Any])(c => convertToJava(c.runtimeClass))
  val domainTypeClass: Class[_] = Option(classTag[D]).fold[Class[_]](classOf[Any])(c => convertToJava(c.runtimeClass))
  val cardinality: MappingCardinality.Value
  val noValue: G = implicitly[NoValue[G]].apply()

  override def apply(g: G): D           = toDomain(g)
  override val reverse: Converter[G, D] = toGraph(_)

  def isCompatibleWith(m: Mapping[_, _, _]): Boolean =
    graphTypeClass.equals(m.graphTypeClass) && MappingCardinality.isCompatible(cardinality, m.cardinality)

  def convertToJava(c: Class[_]): Class[_] =
    c match {
      case JByte.TYPE     => classOf[JByte]
      case JShort.TYPE    => classOf[Short]
      case Character.TYPE => classOf[Character]
      case Integer.TYPE   => classOf[Integer]
      case JLong.TYPE     => classOf[JLong]
      case JFloat.TYPE    => classOf[JFloat]
      case JDouble.TYPE   => classOf[JDouble]
      case JBoolean.TYPE  => classOf[JBoolean]
      case _              => c
    }

  def getProperty(element: Element, key: String): M
  def setProperty(element: Element, key: String, value: M): Unit
  def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](traversal: Traversal[TD, TG, TC], key: String, value: M): Traversal[TD, TG, TC]

  def wrap(us: Seq[D]): M
}

trait MultiValueMapping[D, G] { _: Mapping[_, D, G] =>
  def addValue(element: Element, key: String, value: D): Unit =
    element match {
      case vertex: Vertex => vertex.property(cardinality.gremlinCardinality, key, this.reverse(value)); ()
      case _              => throw InternalError("Edge doesn't support multi-valued properties")
    }
  def removeValue(element: Element, key: String, value: D): Unit = {
    val gValue = reverse(value)
    element match {
      case vertex: Vertex => vertex.properties[G](key).forEachRemaining(p => if (p.value() == gValue) p.remove())
      case _              => throw InternalError("Edge doesn't support multi-valued properties")
    }
  }

  def addValue[E <: Product](traversal: Traversal.V[E], key: String, value: D): Traversal.V[E] =
    traversal.onRaw(_.property(cardinality.gremlinCardinality, key, reverse(value)))

  def removeValue[E <: Product](traversal: Traversal.V[E], key: String, value: D): Traversal.V[E] = {
    val gValue = reverse(value)
    traversal.sideEffect(_.onRaw(t => t.properties[Any](key).hasValue(gValue).drop().asInstanceOf[t.type]))
  }
}

case class IdentityMapping[T: ClassTag: NoValue: Renderer]() extends SingleMapping[T, T](identity[T], identity[T]) with IdentityConverter[T]

class SingleMapping[D: ClassTag, G: ClassTag: NoValue](toGraph: D => G, toDomain: G => D)(implicit renderer: Renderer[D])
    extends Mapping[D, D, G](toGraph, toDomain) {
  override val cardinality: MappingCardinality.Value = MappingCardinality.single
  def optional: OptionMapping[D, G]                  = OptionMapping[D, G](this)
  def sequence: ListMapping[D, G]                    = ListMapping[D, G](this)
  def set: SetMapping[D, G]                          = SetMapping[D, G](this)

  def getProperty(element: Element, key: String): D = {
    val values = element.properties[G](key)
    if (values.hasNext) apply(values.next().value)
    else {
      logger.error(s"${element.label()} ${element.id} doesn't comply with its schema, field $key is missing:\n${Model.printElement(element)}")
      apply(noValue)
    }
  }

  def setProperty(element: Element, key: String, value: D): Unit = {
    element.property(key, reverse(value))
    ()
  }

  override def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](
      traversal: Traversal[TD, TG, TC],
      key: String,
      value: D
  ): Traversal[TD, TG, TC] = traversal.onRaw(_.property(key, reverse(value)))

  override def wrap(us: Seq[D]): D = us.head
}

object SingleMapping {
  def apply[D: ClassTag, G: ClassTag: NoValue](toGraph: D => G, toDomain: G => D)(implicit renderer: Renderer[D]) =
    new SingleMapping[D, G](toGraph, toDomain)
}

case class OptionMapping[D, G](singleMapping: SingleMapping[D, G])
    extends Mapping[Option[D], D, G](singleMapping.reverse, singleMapping.apply)(
      ClassTag(singleMapping.domainTypeClass),
      ClassTag(singleMapping.graphTypeClass),
      NoValue(singleMapping.noValue),
      singleMapping.getRenderer.opt,
      singleMapping.getRenderer
    ) {
  override val cardinality: MappingCardinality.Value = MappingCardinality.option
  override def getProperty(element: Element, key: String): Option[D] = {
    val values = element.properties[G](key)
    if (values.hasNext) Some(apply(values.next().value))
    else None
  }

  override def setProperty(element: Element, key: String, value: Option[D]): Unit = {
    value match {
      case Some(v) => element.property(key, reverse(v))
      case None    => element.properties(key).forEachRemaining(_.remove())
    }
    ()
  }

  override def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](
      traversal: Traversal[TD, TG, TC],
      key: String,
      value: Option[D]
  ): Traversal[TD, TG, TC] = value.fold(traversal.removeProperty(key))(v => traversal.onRaw(_.property(key, reverse(v))))

  override def wrap(us: Seq[D]): Option[D] = us.headOption
}

case class ListMapping[D, G](singleMapping: SingleMapping[D, G])
    extends Mapping[Seq[D], D, G](singleMapping.reverse, singleMapping.apply)(
      ClassTag(singleMapping.domainTypeClass),
      ClassTag(singleMapping.graphTypeClass),
      NoValue(singleMapping.noValue),
      singleMapping.getRenderer.list,
      singleMapping.getRenderer
    )
    with MultiValueMapping[D, G] {
  override val cardinality: MappingCardinality.Value = MappingCardinality.list

  override def getProperty(element: Element, key: String): Seq[D] =
    element
      .properties[G](key)
      .asScala
      .map(p => apply(p.value()))
      .toVector

  override def setProperty(element: Element, key: String, values: Seq[D]): Unit = {
    element.properties(key).forEachRemaining(_.remove())
    element match {
      case vertex: Vertex => values.map(reverse).foreach(vertex.property(Cardinality.list, key, _))
      case _              => throw InternalError("Edge doesn't support multi-valued properties")
    }
  }

  override def wrap(us: Seq[D]): Seq[D] = us

  override def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](
      traversal: Traversal[TD, TG, TC],
      key: String,
      value: Seq[D]
  ): Traversal[TD, TG, TC] =
    value.foldLeft(traversal.removeProperty(key))((t, v) => t.onRaw(_.property(Cardinality.list, key, reverse(v))))
}

case class SetMapping[D, G](singleMapping: SingleMapping[D, G])
    extends Mapping[Set[D], D, G](singleMapping.reverse, singleMapping.apply)(
      ClassTag(singleMapping.domainTypeClass),
      ClassTag(singleMapping.graphTypeClass),
      NoValue(singleMapping.noValue),
      singleMapping.getRenderer.set,
      singleMapping.getRenderer
    )
    with MultiValueMapping[D, G] {
  override val cardinality: MappingCardinality.Value = MappingCardinality.set

  override def getProperty(element: Element, key: String): Set[D] =
    element
      .properties[G](key)
      .asScala
      .map(p => apply(p.value()))
      .toSet

  override def setProperty(element: Element, key: String, values: Set[D]): Unit = {
    element.properties(key).forEachRemaining(_.remove())
    element match {
      case vertex: Vertex => values.map(reverse).foreach(vertex.property(Cardinality.set, key, _))
      case _              => throw InternalError("Edge doesn't support multi-valued properties")
    }
  }

  override def setProperty[TD, TG <: Element, TC <: Converter[TD, TG]](
      traversal: Traversal[TD, TG, TC],
      key: String,
      value: Set[D]
  ): Traversal[TD, TG, TC] = value.foldLeft(traversal.removeProperty(key))((t, v) => t.onRaw(_.property(Cardinality.set, key, reverse(v))))

  override def wrap(us: Seq[D]): Set[D] = us.toSet
}
