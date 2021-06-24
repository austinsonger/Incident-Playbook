package org.thp.scalligraph.controllers

import scala.annotation.StaticAnnotation

class WithParser[A](fieldsParser: FieldsParser[A]) extends StaticAnnotation

class WithUpdateParser[A](fieldsParsers: UpdateFieldsParser[A]) extends StaticAnnotation
