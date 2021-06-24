package org.thp.scalligraph

import shapeless.tag.@@

package object auth {
  type Permission = String @@ PermissionTag
}
