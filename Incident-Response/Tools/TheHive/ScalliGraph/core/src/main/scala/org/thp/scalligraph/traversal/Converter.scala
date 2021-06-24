package org.thp.scalligraph.traversal

import java.lang.{Double => JDouble, Long => JLong}
import java.util.{Collection => JCollection, List => JList, Map => JMap}

import org.apache.tinkerpop.gremlin.process.traversal.P
import org.apache.tinkerpop.gremlin.process.traversal.dsl.graph.__

import scala.collection.JavaConverters._

trait BiConverter[D, G] extends Converter[D, G] {
  val reverse: Converter[G, D]
}

trait Converter[+D, G] extends (G => D) {
  def startTraversal: Traversal[D, G, this.type] = new Traversal[D, G, this.type](AnonymousGraph, __.start[G](), this)
  def apply(predicate: P[G]): P[_] =
    Option(predicate.getValue).fold(predicate.asInstanceOf[P[D]]) {
      case c: JCollection[_] =>
        if (c.isEmpty) predicate.asInstanceOf[P[D]]
        else {
          val p = predicate.clone().asInstanceOf[P[D]]
          p.setValue(c.asScala.map(v => apply(v.asInstanceOf[G])).asJavaCollection.asInstanceOf[D])
          p
        }
      case v =>
        val p = predicate.clone().asInstanceOf[P[D]]
        p.setValue(apply(v))
        p
    }
}

object Converter {
  type any         = Converter[Nothing, Any]
  type Identity[A] = IdentityConverter[A]
  def identity[A]: IdentityConverter[A]  = new IdentityConverter[A] {}
  val long: Converter[Long, JLong]       = _.toLong
  val double: Converter[Double, JDouble] = _.toDouble
  type CCollection[D, G, C <: Converter[D, G]] = Poly1Converter[Seq[D], JCollection[G], D, G, C]
  type CList[D, G, C <: Converter[D, G]]       = Poly1Converter[Seq[D], JList[G], D, G, C]
  def clist[D, G, C <: Converter[D, G]](converter: C): CList[D, G, C] =
    new Poly1Converter[Seq[D], JList[G], D, G, C] {
      override val subConverter: C = converter
      override def apply(l: JList[G]): Seq[D] =
        converter match {
          case _: IdentityConverter[_] => l.asScala.asInstanceOf[Seq[D]]
          case c                       => l.asScala.map(c)
        }
    }
  def ccollection[D, G, C <: Converter[D, G]](converter: C): CCollection[D, G, C] = new CollectionConverter[D, G, C](converter)
  val cid: Converter[String, AnyRef]                                              = _.toString
  type CGroupMap[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]] =
    CMap[DK, Seq[DV], GK, JCollection[GV], CK, CCollection[DV, GV, CV]]

  type CMapEntry[DK, GK, DV, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]] =
    Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV] with Converter[(DK, DV), JMap.Entry[GK, GV]]
  type CGroupMapEntry[DK, GK, DV, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]] =
    CMapEntry[DK, GK, Seq[DV], JCollection[GV], CK, CCollection[DV, GV, CV]]
  def cmap[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](kConverter: CK, vConverter: CV): CMap[DK, DV, GK, GV, CK, CV] =
    new MapConverter[DK, DV, GK, GV, CK, CV](kConverter, vConverter)

  def cgroupMap[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](kConverter: CK, vConverter: CV): CGroupMap[DK, DV, GK, GV, CK, CV] =
    new GroupMapConverter[DK, DV, GK, GV, CK, CV](kConverter, vConverter)

  type CMap[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]] =
    Poly1Converter[
      Map[DK, DV],
      JMap[GK, GV],
      (DK, DV),
      JMap.Entry[GK, GV],
      Converter[(DK, DV), JMap.Entry[GK, GV]] with Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV]
    ] with Poly2Converter[Map[DK, DV], JMap[GK, GV], DK, DV, GK, GV, CK, CV]
}
class MapConverter[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](
    override val subConverterKey: CK,
    override val subConverterValue: CV
) extends Poly1Converter[
      Map[DK, DV],
      JMap[GK, GV],
      (DK, DV),
      JMap.Entry[GK, GV],
      Converter[(DK, DV), JMap.Entry[GK, GV]] with Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV]
    ]
    with Poly2Converter[Map[DK, DV], JMap[GK, GV], DK, DV, GK, GV, CK, CV] {
  override val subConverter: Converter[(DK, DV), JMap.Entry[GK, GV]] with Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV] =
    new MapEntryConverter[DK, DV, GK, GV, CK, CV](subConverterKey, subConverterValue)

  override def apply(jmap: JMap[GK, GV]): Map[DK, DV] =
    jmap
      .asScala
      .map { case (gk, gv) => subConverterKey(gk) -> subConverterValue(gv) }
      .toMap
}

/*
Error:(80, 5) type arguments [Map[DK,DV],java.util.Map[GK,GV],(DK, DV),java.util.Map.Entry[GK,GV],org.thp.scalligraph.traversal.Poly2Converter[(DK, DV),java.util.Map.Entry[GK,GV],DK,DV,GK,GV,CK,CV]]
do not conform to trait Poly1Converter's type parameter bounds [+SD,SG,D,G,C <: org.thp.scalligraph.traversal.Converter[D,G]]
    Poly1Converter[Map[DK, DV], JMap[GK, GV], (DK, DV), JMap.Entry[GK, GV], Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV]]
 */
class GroupMapConverter[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](override val subConverterKey: CK, vConverter: CV)
    extends Poly1Converter[
      Map[DK, Seq[DV]],
      JMap[GK, JCollection[GV]],
      (DK, Seq[DV]),
      JMap.Entry[GK, JCollection[GV]],
      Converter[(DK, Seq[DV]), JMap.Entry[GK, JCollection[GV]]] with Poly2Converter[
        (DK, Seq[DV]),
        JMap.Entry[GK, JCollection[GV]],
        DK,
        Seq[DV],
        GK,
        JCollection[GV],
        CK,
        Poly1Converter[Seq[DV], JCollection[GV], DV, GV, CV]
      ]
    ]
    with Poly2Converter[Map[DK, Seq[DV]], JMap[GK, JCollection[GV]], DK, Seq[DV], GK, JCollection[GV], CK, Poly1Converter[
      Seq[DV],
      JCollection[GV],
      DV,
      GV,
      CV
    ]] {
  override val subConverter: Converter[(DK, Seq[DV]), JMap.Entry[GK, JCollection[GV]]]
    with Poly2Converter[(DK, Seq[DV]), JMap.Entry[GK, JCollection[GV]], DK, Seq[DV], GK, JCollection[GV], CK, Poly1Converter[Seq[
      DV
    ], JCollection[GV], DV, GV, CV]] =
    new GroupMapEntryConverter[DK, DV, GK, GV, CK, CV](subConverterKey, vConverter)
  //    new MapEntryConverter[DK, Seq[DV], GK, JCollection[GV], CK, CollectionConverter[DV, GV, CV]](
  //      subConverterKey,
  //      new CollectionConverter[DV, GV, CV](vConverter)
  //    )
  override val subConverterValue: Poly1Converter[Seq[DV], JCollection[GV], DV, GV, CV] = new CollectionConverter[DV, GV, CV](vConverter)

  override def apply(jmap: JMap[GK, JCollection[GV]]): Map[DK, Seq[DV]] =
    jmap.asScala.map { case (k, v) => subConverterKey(k) -> subConverterValue(v) }.toMap
}

class GroupMapEntryConverter[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](override val subConverterKey: CK, vConverter: CV)
    extends Converter[(DK, Seq[DV]), JMap.Entry[GK, JCollection[GV]]]
    with Poly2Converter[(DK, Seq[DV]), JMap.Entry[GK, JCollection[GV]], DK, Seq[DV], GK, JCollection[GV], CK, Poly1Converter[
      Seq[DV],
      JCollection[GV],
      DV,
      GV,
      CV
    ]] {
  //  override def apply(jmapEntry: JMap.Entry[GK, GV]): (DK, DV) = subConverterKey(jmapEntry.getKey) -> subConverterValue(jmapEntry.getValue)
  override val subConverterValue: Poly1Converter[Seq[DV], JCollection[GV], DV, GV, CV] = new CollectionConverter[DV, GV, CV](vConverter)

  override def apply(jmapEntry: JMap.Entry[GK, JCollection[GV]]): (DK, Seq[DV]) =
    subConverterKey(jmapEntry.getKey) -> subConverterValue(jmapEntry.getValue)
}

class MapEntryConverter[DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]](
    override val subConverterKey: CK,
    override val subConverterValue: CV
) extends Converter[(DK, DV), JMap.Entry[GK, GV]]
    with Poly2Converter[(DK, DV), JMap.Entry[GK, GV], DK, DV, GK, GV, CK, CV] {
  override def apply(jmapEntry: JMap.Entry[GK, GV]): (DK, DV) = subConverterKey(jmapEntry.getKey) -> subConverterValue(jmapEntry.getValue)
}

trait IdentityConverter[A] extends BiConverter[A, A] {
  override def apply(a: A): A           = a
  override val reverse: Converter[A, A] = this
}
trait Poly1Converter[+SD, SG, D, G, C <: Converter[D, G]] extends Converter[SD, SG] {
  val subConverter: C
}

class CollectionConverter[D, G, C <: Converter[D, G]](override val subConverter: C) extends Poly1Converter[Seq[D], JCollection[G], D, G, C] {
  override def apply(jcoll: JCollection[G]): Seq[D] = jcoll.asScala.map(subConverter).toSeq
}

trait Poly2Converter[+SD, SG, DK, DV, GK, GV, CK <: Converter[DK, GK], CV <: Converter[DV, GV]] {
  val subConverterKey: CK
  val subConverterValue: CV
}
