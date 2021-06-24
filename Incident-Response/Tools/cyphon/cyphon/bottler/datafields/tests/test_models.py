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
Tests the Bottle class.
"""

# third party
from django.test import TestCase

# local
from bottler.datafields.models import DataField


class DateFieldTestCase(TestCase):
    """
    Tests the DateField class.
    """

    datafield = DataField(
        field_name='title',
        field_type='CharField',
        target_type='Keyword'
    )

    def test_to_dict_no_parent(self):
        """
        Tests the to_dict method when no parent_name is provided.
        """
        actual = self.datafield.to_dict()
        expected = {
            'field_name': 'title',
            'field_type': 'CharField',
            'target_type': 'Keyword'
        }
        self.assertEqual(actual, expected)

    def test_to_dict_with_parent(self):
        """
        Tests the to_dict method when no parent_name is provided.
        """
        actual = self.datafield.to_dict('post')
        expected = {
            'field_name': 'post.title',
            'field_type': 'CharField',
            'target_type': 'Keyword'
        }
        self.assertEqual(actual, expected)

    def test_to_key_val_w_target_type(self):
        """
        Tests the to_key_val method for a field with a defined target_type.
        """
        actual = self.datafield.to_key_val()
        expected = {'title': 'CharField (Keyword)'}
        self.assertEqual(actual, expected)

    def test_to_key_val_wo_target_type(self):
        """
        Tests the to_key_val method for a field without a defined target_type.
        """
        datafield = DataField(
            field_name='name',
            field_type='CharField',
        )
        actual = datafield.to_key_val()
        expected = {'name': 'CharField'}
        self.assertEqual(actual, expected)

