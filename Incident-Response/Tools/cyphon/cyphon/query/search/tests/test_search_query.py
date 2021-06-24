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
Tests for the SearchQuery class.
"""

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase

# local
from query.search.search_query import SearchQuery, UnknownParameter
from query.search.field_search_parameter import FieldSearchParameter
from query.search.distillery_filter_parameter import DistilleryFilterParameter
from tests.fixture_manager import get_fixtures


class SearchQueryTestCase(TestCase):
    """
    Tests the SearchQuery class.
    """
    user_model = get_user_model()
    fixtures = get_fixtures(['distilleries', 'users', 'alerts', 'comments'])

    def setUp(self):
        self.user = self.user_model.objects.get(pk=1)

    def test_empty_search_query_error(self):
        """
        Tests that an empty error is thrown if the query is empty.
        """
        query = SearchQuery('', self.user)

        self.assertFalse(query.is_valid())
        self.assertEqual(len(query.errors), 1)
        self.assertEqual(query.errors[0], SearchQuery.EMPTY_SEARCH_QUERY)

    def test_parsing_error(self):
        """
        Tests that a parsing error is thrown if the query cannot be parsed.
        """
        query = SearchQuery(' ', self.user)

        self.assertFalse(query.is_valid())
        self.assertEqual(len(query.errors), 1)
        self.assertEqual(query.errors[0], SearchQuery.PARSING_ERROR.format(' '))

    def test_unknown_parameters(self):
        """
        Tests that unknown parameter types are correctly identified.
        """
        unknown_parameter_string_1 = 'fjlk#!!.!@#$'
        unknown_parameter_string_2 = 'fieoh$%@.!@98'
        unknown_parameter_1 = UnknownParameter(0, unknown_parameter_string_1)
        unknown_parameter_2 = UnknownParameter(1, unknown_parameter_string_2)
        query = SearchQuery(
            '{} {}'.format(
                unknown_parameter_string_1,
                unknown_parameter_string_2,
            ),
            self.user,
        )

        self.assertFalse(query.is_valid())
        self.assertEqual(len(query.unknown_parameters), 2)
        self.assertEqual(len(query.invalid_parameters), 2)
        self.assertEqual(
            query.invalid_parameters[0].as_dict(),
            unknown_parameter_1.as_dict(),
        )
        self.assertEqual(
            query.invalid_parameters[1].as_dict(),
            unknown_parameter_2.as_dict(),
        )

    def test_parameter_index(self):
        """
        Tests that the parameter index is correct for each search
        parameter.
        """
        query = SearchQuery('ip_address=34.25.12.32 "search phrase"', self.user)

        self.assertTrue(query.is_valid())
        self.assertEqual(len(query.keyword_parameters), 1)
        self.assertEqual(query.keyword_parameters[0].index, 1)
        self.assertEqual(len(query.field_parameters), 1)
        self.assertEqual(query.field_parameters[0].index, 0)

    def test_distillery_parameter(self):
        """
        Tests that a distillery filter string is correctly identified.
        """
        query = SearchQuery('@source="test_logs"', self.user)

        self.assertTrue(query.is_valid())
        self.assertIsNotNone(query.distillery_filter_parameter)
        self.assertIsInstance(
            query.distillery_filter_parameter, DistilleryFilterParameter,
        )

    def test_distillery_hyphen(self):
        """
        Tests that a distillery with a hyphen is correctly identified.
        """
        query = SearchQuery('@source="test-logs"', self.user)

        self.assertFalse(query.is_valid())
        self.assertIsNotNone(query.distillery_filter_parameter)
        self.assertIsInstance(query.distillery_filter_parameter,
                              DistilleryFilterParameter)

    def test_parameter_errors(self):
        """
        Tests that the parameter errors are passed onto the search
        query object.
        """
        field_parameter_string = 'field_name=blah'
        field_parameter = FieldSearchParameter(0, field_parameter_string)
        query = SearchQuery(field_parameter_string, self.user)

        self.assertFalse(query.is_valid())
        self.assertEqual(len(query.invalid_parameters), 1)
        self.assertEqual(
            query.invalid_parameters[0].as_dict(),
            field_parameter.as_dict(),
        )

    def test_multiple_distillery_filters_error(self):
        """
        Tests that the query invalidates when multiple distillery filters are
        used.
        """
        query = SearchQuery(
            '@source="test_logs" @source="test_logs"', self.user)

        self.assertFalse(query.is_valid())
        self.assertEqual(len(query.errors), 1)
        self.assertEqual(
            query.errors[0],
            SearchQuery.MULTIPLE_DISTILLERY_FILTERS.format(
                '@source="test_logs"', 1,
            ),
        )
