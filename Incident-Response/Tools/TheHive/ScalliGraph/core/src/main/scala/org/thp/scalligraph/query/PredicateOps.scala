package org.thp.scalligraph.query

import org.apache.tinkerpop.gremlin.process.traversal.P
import org.apache.tinkerpop.gremlin.process.traversal.util.{AndP, OrP}

import java.util.function.BiPredicate
import java.util.stream.Collectors
import java.util.{List => JList}

object PredicateOps {

  implicit class PredicateOpsDefs[A](predicate: P[A]) {
    def mapValue[B](f: A => B): P[B] =
      predicate match {
        case or: OrP[_]   => new OrP[B](or.getPredicates.stream().map[P[B]](p => p.asInstanceOf[P[A]].mapValue(f)).collect(Collectors.toList()))
        case and: AndP[_] => new AndP[B](and.getPredicates.stream().map[P[B]](p => p.asInstanceOf[P[A]].mapValue(f)).collect(Collectors.toList()))
        case _ =>
          val biPredicate: BiPredicate[B, B] = predicate.getBiPredicate.asInstanceOf[BiPredicate[B, B]]
          predicate.getValue match {
            case l: JList[_] =>
              val x: JList[B] = l.stream().map[B](v => f(v.asInstanceOf[A])).collect(Collectors.toList())
              new P(biPredicate, x.asInstanceOf[B])
            case v =>
              try new P(biPredicate, f(v))
              catch { case _: ClassCastException => predicate.asInstanceOf[P[B]] }
          }
      }

    def mapPred[B](fv: A => B, fp: P[B] => P[B]): P[B] =
      predicate match {
        case or: OrP[_]   => new OrP[B](or.getPredicates.stream().map[P[B]](p => p.asInstanceOf[P[A]].mapPred(fv, fp)).collect(Collectors.toList()))
        case and: AndP[_] => new AndP[B](and.getPredicates.stream().map[P[B]](p => p.asInstanceOf[P[A]].mapPred(fv, fp)).collect(Collectors.toList()))
        case _ =>
          val biPredicate: BiPredicate[B, B] = predicate.getBiPredicate.asInstanceOf[BiPredicate[B, B]]
          predicate.getValue match {
            case l: JList[_] =>
              val x: JList[B] = l.stream().map[B](v => fv(v.asInstanceOf[A])).collect(Collectors.toList())
              fp(new P(biPredicate, x.asInstanceOf[B]))
            case v =>
              try fp(new P(biPredicate, fv(v)))
              catch { case _: ClassCastException => predicate.asInstanceOf[P[B]] }
          }
      }
  }
}
