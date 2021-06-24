package org.thp.scalligraph

import java.util.Date

package object graphql {
  val DateType: ScalarAlias[Date, Long] = ScalarAlias[Date, Long](LongType, _.getTime, ts => Right(new Date(ts)))
}
