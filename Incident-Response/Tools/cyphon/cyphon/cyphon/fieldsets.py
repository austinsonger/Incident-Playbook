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
Defines a |QueryFieldset| class. |QueryFieldsets| are used to construct
queries to data stores.
"""
import collections

# local
from cyphon.choices import FIELD_TYPE_CHOICES, OPERATOR_CHOICES


class QueryFieldset(object):
    """

    Attributes
    ----------
    field_name : str
        The name of the field being queried.

    field_type : str
        The type of field being queried. Corresponds to a value in
        |FIELD_TYPE_CHOICES|.

    operator : str
        The method used to evaluate the field being queried.
        Corresponds to a value in |OPERATOR_CHOICES|.

    value : str
        The value used to filter field being queried.

    Raises
    ------
    AssertionError
        If the :attr:`~cyphon.fieldsets.QueryFieldset.field_name` is not in
        |FIELD_TYPE_CHOICES| or the :attr:`~cyphon.fieldsets.QueryFieldset.field_type`
        is not in |OPERATOR_CHOICES|.

    """

    FIELD_TYPES = [choice[0] for choice in FIELD_TYPE_CHOICES]
    OPERATORS = [choice[0] for choice in OPERATOR_CHOICES]

    def __init__(self, field_name, field_type, operator, value):
        self.field_name = field_name
        self.field_type = field_type
        self.operator = operator
        self.value = value

        if self.field_type not in self.FIELD_TYPES:  # pragma: no cover
            raise ValueError('%s is not a valid field_type' % self.field_type)

        if self.operator not in self.OPERATORS:  # pragma: no cover
            raise ValueError('%s is not a valid operator' % self.operator)

    def __str__(self):
        items = collections.OrderedDict([
            ('field_name', self.field_name),
            ('field_type', self.field_type),
            ('operator', self.operator),
            ('value', self.value),
        ])
        items_str = '{' + ', '.join('%r: %r' % i for i in items.items()) + '}'
        return "%s: %s" % (self.__class__.__name__, items_str)
