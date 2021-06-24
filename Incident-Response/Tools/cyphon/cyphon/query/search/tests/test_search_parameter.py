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
Tests for the SearchQueryParameter class.
"""

# third party
from django.test import TestCase

# local
from query.search.search_parameter import SearchParameterType


class SearchParameterTypeTestCase(TestCase):
    """
    Tests the SearchQueryParameterType class.
    """

    VALID_KEYWORDS = [
        '""',
        'keyword',
        '"keyword phrase"'
    ]
    """list of str

    Parameter strings that should match the KEYWORD type.
    """

    VALID_FIELDS = [
        'field_name=value',
        'field.name=value',
        '_field_._name_=value',
        'field_name="phrase of words"',
        'field_name=',
        '_field.name_=',
    ]
    """list of str

    Parameter strings that should match the FIELD type.
    """

    VALID_DISTILLERIES = [
        '@source=""',
        '@source="mail"',
        '@source="mail stuff"',
    ]
    """list of str

    Parameter strings that should match the DISTILLERY type.
    """

    INVALID_PARAMETERS = [
        'separated words',
        '',
        ' words with spaces '
        'field_name= ',
        ' blah',
    ]
    """list of str

    Parameter strings that shouldn't match any types.
    """

    def test_valid_keywords(self):
        """
        Tests that get_parameter_type returns KEYWORD for valid keywords
        search parameter strings.
        """
        for keyword in SearchParameterTypeTestCase.VALID_KEYWORDS:
            self.assertEquals(
                SearchParameterType.get_parameter_type(keyword),
                SearchParameterType.KEYWORD,
                '`{}` is not a keyword'.format(keyword)
            )

    def test_valid_fields(self):
        """
        Tests that get_parameter_type returns FIELD for valid field search
        parameter strings.
        """
        for field in SearchParameterTypeTestCase.VALID_FIELDS:
            self.assertEquals(
                SearchParameterType.get_parameter_type(field),
                SearchParameterType.FIELD,
                '`{}` is not a field'.format(field)
            )

    def test_valid_distillery_filter(self):
        """
        Tests that get_parameter_type returns DISTILLERY for a distillery
        filter parameter strings.
        """
        for distillery in SearchParameterTypeTestCase.VALID_DISTILLERIES:
            self.assertEquals(
                SearchParameterType.get_parameter_type(distillery),
                SearchParameterType.DISTILLERY,
                '`{}` is not a distillery filter'.format(distillery)
            )

    def test_invalid_parameters(self):
        """
        Tests that get_parameter_type returns None for an invalid parameters.
        """
        for parameter in SearchParameterTypeTestCase.INVALID_PARAMETERS:
            self.assertIsNone(
                SearchParameterType.get_parameter_type(parameter),
                '`{}` is not a distillery filter'.format(parameter)
            )
