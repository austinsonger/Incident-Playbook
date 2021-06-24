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

# standard library
from unittest import TestCase

# local
from cyphon.fieldsets import QueryFieldset


class QueryFieldsetTestCase(TestCase):
    """
    Tests the QueryFieldset class.
    """

    fieldset = QueryFieldset(
        field_name='foo',
        field_type='CharField',
        operator='eq',
        value='foobar'
    )

    def test_str(self):
        """
        Tests the __str__ method on a QueryFieldset.
        """
        actual = str(self.fieldset)
        expected = ("QueryFieldset: {'field_name': 'foo', 'field_type': "
                    "'CharField', 'operator': 'eq', 'value': 'foobar'}")
        self.assertEqual(actual, expected)

    def test_vars(self):
        """
        Tests the outcome of the vars() function on a QueryFieldset.
        """
        actual = vars(self.fieldset)
        expected = {
            'field_name': 'foo',
            'field_type': 'CharField',
            'operator': 'eq',
            'value': 'foobar'
        }
        self.assertEqual(actual, expected)
