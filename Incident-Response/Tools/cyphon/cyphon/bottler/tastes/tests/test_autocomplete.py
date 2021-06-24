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
Tests Autocomplete classes for Tastes.
"""

# third party
from django.test import TestCase

# local
from bottler.datafields.models import DataField
from bottler.tastes.autocomplete_light_registry import \
    FilterFieldsAutocompleteBase


class FieldTypeIsMatchtestCase(TestCase):
    """
    Tests the _field_type_is_match method of the FilterFieldsAutocompleteBase
    class.
    """
    autocomplete = FilterFieldsAutocompleteBase()
    autocomplete.field_types = ['CharField', 'TextField']

    def test_field_type_and_query_match(self):
        """
        Tests the _field_type_is_match method when the field_name and
        field_type match.
        """
        query = 'cont'
        field = DataField(
            field_name='content',
            field_type='CharField'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, True)

    def test_field_type_only_is_match(self):
        """
        Tests the _field_type_is_match method when the field_type matches
        but not the field_name.
        """
        query = 'cont'
        field = DataField(
            field_name='text',
            field_type='CharField'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, False)

    def test_query_only_is_match(self):
        """
        Tests the _field_type_is_match method when the field_name matches
        but not the field_type.
        """
        query = 'cont'
        field = DataField(
            field_name='content',
            field_type='EmbeddedDocument'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, False)

    def test_no_match(self):
        """
        Tests the _field_type_is_match method when neither the field_name
        nor the field_type matches.
        """
        query = 'cont'
        field = DataField(
            field_name='location',
            field_type='PointField'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, False)

    def test_no_query_and_type_match(self):
        """
        Tests the _field_type_is_match method when both the field_type matches
        and no query is defined.
        """
        query = None
        field = DataField(
            field_name='content',
            field_type='CharField'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, True)

    def test_no_query_and_type_nonmatch(self):
        """
        Tests the _field_type_is_match method when the field_type doesn not
        match and no query is defined.
        """
        query = None
        field = DataField(
            field_name='content',
            field_type='PointField'
        )
        result = self.autocomplete._field_type_is_match(field, query)
        self.assertIs(result, False)

    def test_no_field_types_match(self):
        """
        Tests the _field_type_is_match method when the field_type doesn not
        match and no qno field_types are defined.
        """
        autocomplete = FilterFieldsAutocompleteBase()
        query = None
        field = DataField(
            field_name='content',
            field_type='CharField'
        )
        result = autocomplete._field_type_is_match(field, query)
        self.assertIs(result, True)

    def test_no_field_types_nonmatch(self):
        """
        Tests the _field_type_is_match method when the field_type doesn not
        match and no no field_types are defined.
        """
        autocomplete = FilterFieldsAutocompleteBase()
        query = 'cont'
        field = DataField(
            field_name='text',
            field_type='CharField'
        )
        result = autocomplete._field_type_is_match(field, query)
        self.assertIs(result, False)

