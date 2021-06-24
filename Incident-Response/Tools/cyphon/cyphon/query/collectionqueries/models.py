# -*- coding: utf-8 -*-
# Copyright 2017-2019 ControlScan, Inc.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# Cyphon Engine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cyphon Engine. If not, see <http://www.gnu.org/licenses/>.
"""

"""

# third party
from django.db import models
from django.conf import settings

# local
from cyphon.choices import FIELD_TYPE_CHOICES, LOGIC_CHOICES, OPERATOR_CHOICES
from warehouses.models import Collection


class CollectionQuery(models.Model):
    """

    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                   null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    collections = models.ManyToManyField(Collection, related_name='+')
    joiner = models.CharField(max_length=40, choices=LOGIC_CHOICES)

    class meta:
        verbose_name_plural = 'field queries'

    def __str__(self):
        return '%s %s' % (self.created_date, self.created_by)


class Fieldset(models.Model):
    """
    Defines a fieldset.

    Attributes:
        field_name:
        field_type:
        operator:
        value:

    """
    query = models.ForeignKey(CollectionQuery, related_name='fieldsets',
                              related_query_name='fieldset')
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=255, choices=FIELD_TYPE_CHOICES)
    operator = models.CharField(max_length=40, choices=OPERATOR_CHOICES)
    value = models.TextField()  # this could be a string, number, etc.

    def __str__(self):
        return '%s %s %s' % (self.field, self.operator, self.value)
