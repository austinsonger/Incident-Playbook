package org.thp.scalligraph

class SingleInstance(val value: Boolean) {
  override lazy val toString: String = if (value) "single node" else "cluster"
}
