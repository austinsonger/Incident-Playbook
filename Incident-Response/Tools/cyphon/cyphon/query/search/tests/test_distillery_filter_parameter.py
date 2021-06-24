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

# third party
from django.test import TestCase
from django.contrib.auth import get_user_model

# local
from query.search.search_parameter import SearchParameterType
from query.search.distillery_filter_parameter import DistilleryFilterParameter
from tests.fixture_manager import get_fixtures


class DistilleryFilterParameterTestCase(TestCase):
    """
    Test case for the DistilleryFilterParameter class.
    """
    fixtures = get_fixtures(['distilleries', 'users'])
    user_model = get_user_model()

    def setUp(self):
        self.user = self.user_model.objects.get(pk=1)

    def test_collection_filter(self):
        """
        Tests that the distilleries get filtered by collection name.
        """
        parameter = DistilleryFilterParameter(
            3, '@source="test_docs"', self.user)

        self.assertTrue(parameter.is_valid())
        self.assertEqual(len(parameter.distilleries), 2)
        self.assertEqual(
            str(parameter.distilleries[0]),
            'elasticsearch.test_index.test_docs',
        )
        self.assertEqual(
            str(parameter.distilleries[1]),
            'mongodb.test_database.test_docs',
        )

    def test_collection_picker(self):
        """
        Tests that only a single distillery is returned when selecting
        a particular distillery.
        """
        parameter = DistilleryFilterParameter(
            3, '@source="test_database.test_posts"', self.user)

        self.assertTrue(parameter.is_valid())
        self.assertEqual(len(parameter.distilleries), 1)
        self.assertEqual(
            str(parameter.distilleries[0]),
            'mongodb.test_database.test_posts',
        )

    def test_invalid_parameter(self):
        """
        Tests that an INVALID_PARAMETER is placed on the parameter errors
        if the string parameter cannot be parsed.
        """
        parameter = DistilleryFilterParameter(3, 'mah', self.user)

        self.assertFalse(parameter.is_valid())
        self.assertEqual(len(parameter.errors), 1)
        self.assertEqual(
            parameter.errors[0],
            DistilleryFilterParameter.INVALID_PARAMETER,
        )

    def test_empty_filter(self):
        """
        Tests that a FILTER_VALUE_IS_EMPTY error is placed on the
        parameter errors if the filter value is empty.
        """
        parameter = DistilleryFilterParameter(3, '@source=', self.user)

        self.assertFalse(parameter.is_valid())
        self.assertEqual(len(parameter.errors), 1)
        self.assertEqual(
            parameter.errors[0],
            DistilleryFilterParameter.INVALID_PARAMETER,
        )

    def test_parsed_properties(self):
        """
        Tests that the properties are parsed correctly from the
        parameter string.
        """
        parameter = DistilleryFilterParameter(
            3, '@source="test_do"', self.user)

        self.assertTrue(parameter.is_valid())
        self.assertEqual(parameter.filter, 'test_do')

    def test_invalid_collection(self):
        """
        Tests that a CANNOT_FIND_COLLECTION error is placed on the
        parameter errors when a collection is not found.
        """
        parameter = DistilleryFilterParameter(3, '@source="meh"', self.user)

        self.assertFalse(parameter.is_valid())
        self.assertEqual(len(parameter.errors), 1)
        self.assertEqual(
            parameter.errors[0],
            DistilleryFilterParameter.NO_MATCHING_DISTILLERIES.format('meh'),
        )

    def test_unknown_distillery(self):
        """
        Tests that a NO_MATCHING_DISTILLERIES error is placed on the
        parameter errors when no matching distilleries are found.
        """
        parameter = DistilleryFilterParameter(
            3, '@source="no_match"', self.user)

        self.assertFalse(parameter.is_valid())
        self.assertEqual(len(parameter.errors), 1)
        self.assertEqual(
            parameter.errors[0],
            DistilleryFilterParameter.NO_MATCHING_DISTILLERIES.format('no_match'),
        )

    def test_get_parameter_info_success(self):
        """
        Tests that .get_parameter_info() returns the correct dictionary
        for a valid parameter.
        """
        parameter = DistilleryFilterParameter(
            3, '@source="test_docs"', self.user)

        self.assertDictEqual(parameter.as_dict(), {
            'parameter': '@source="test_docs"',
            'type': SearchParameterType.DISTILLERY,
            'index': 3,
            'filter': 'test_docs',
            'distilleries': [
                'elasticsearch.test_index.test_docs',
                'mongodb.test_database.test_docs',
            ],
            'errors': [],
        })

    def test_limited_distilleries_per_user(self):
        restricted_user = self.user_model.objects.get(pk=3)
        parameter = DistilleryFilterParameter(
            3, '@source="_docs"', restricted_user)

        self.assertTrue(parameter.is_valid())
        self.assertEqual(len(parameter.distilleries), 1)

    def test_get_parameter_info_error(self):
        """
        Tests that .get_parameter_info() returns the correct dictionary
        for an invalid parameter.
        """
        parameter = DistilleryFilterParameter(3, '@source="bleh"', self.user)

        self.assertDictEqual(parameter.as_dict(), {
            'parameter': '@source="bleh"',
            'type': SearchParameterType.DISTILLERY,
            'index': 3,
            'filter': 'bleh',
            'distilleries': [],
            'errors': [
                DistilleryFilterParameter.NO_MATCHING_DISTILLERIES.format('bleh'),
            ],
        })
