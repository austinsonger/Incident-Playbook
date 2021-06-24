package org.thp.scalligraph

import org.specs2.mutable.Specification
import org.thp.scalligraph.controllers._

class FPathTest extends Specification {

  "path" should {
    "parse elements" in {
      FPath("a__.b__.c__") must_=== FPathElem("a__", FPathElem("b__", FPathElem("c__", FPathEmpty)))
    }

    "parse indexed seq elements" in {
      FPath("a[3].b.c[2]") must_=== FPathElemInSeq("a", 3, FPathElem("b", FPathElemInSeq("c", 2, FPathEmpty)))
    }

    "parse seq elements" in {
      FPath("a[].b.c[]") must_=== FPathSeq("a", FPathElem("b", FPathSeq("c", FPathEmpty)))
    }
  }
}
