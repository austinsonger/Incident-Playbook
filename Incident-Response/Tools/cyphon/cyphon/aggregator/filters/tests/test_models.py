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
Tests the Filter class.
"""

# third party
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# local
from aggregator.filters.models import Filter
from target.followees.models import Followee
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from tests.fixture_manager import get_fixtures


class FilterModelsTestCase(TestCase):
    """
    Base class for testing Filter class and related classes.
    """
    fixtures = get_fixtures(['followees', 'filters', 'reservoirs'])


class FilterManagerTestCase(FilterModelsTestCase):
    """
    Tests the FilterManager class.
    """

    def test_enabled_filters_by_type(self):
        """
        Tests the _find_enabled_filters_by_type method.
        """
        followee_type = ContentType.objects.get_for_model(Followee)
        followees = Filter.objects._find_enabled_filters_by_type(followee_type)
        self.assertEqual(len(followees), 2)

        location_type = ContentType.objects.get_for_model(Location)
        locations = Filter.objects._find_enabled_filters_by_type(location_type)
        self.assertEqual(len(locations), 3)

        term_type = ContentType.objects.get_for_model(SearchTerm)
        terms = Filter.objects._find_enabled_filters_by_type(term_type)
        self.assertEqual(len(terms), 1)

    def test_get_oldest_time_last_used(self):
        """
        Tests the _get_oldest_time_last_used method.
        """
        oldest_time = Filter.objects._get_oldest_time_last_used()
        self.assertEqual(str(oldest_time), "2000-01-01 05:00:00+00:00")

    def test_create_timeframe(self):
        """
        Tests the _get_timeframe method.
        """
        timeframe = Filter.objects._create_timeframe()
        self.assertEqual(str(timeframe.start), "2000-01-01 05:00:00+00:00")

    def test_create_reservoir_query(self):
        """
        Tests the create_reservoir_query method.
        """
        query = Filter.objects.create_reservoir_query()
        self.assertEqual(len(query.accounts), 4)
        self.assertEqual(len(query.locations), 3)
        self.assertEqual(len(query.searchterms), 1)


class FilterTestCase(FilterModelsTestCase):
    """
    Tests the Filter class.
    """

    def setUp(self):
        followee_type = ContentType.objects.get_for_model(Followee)
        location_type = ContentType.objects.get_for_model(Location)
        srchterm_type = ContentType.objects.get_for_model(SearchTerm)

        self.followee_filter = Filter(
            content_type=followee_type,
            object_id=1,
            last_used="2015-01-01T12:00:00+05:00"
        )

        self.location_filter = Filter(
            content_type=location_type,
            object_id=1,
            last_used="2015-01-01T12:00:00+05:00"
        )

        self.srchterm_filter = Filter(
            content_type=srchterm_type,
            object_id=1,
            last_used="2015-01-01T12:00:00+05:00"
        )

    def test_str(self):
        """
        Tests the __str__ method.
        """
        actual = str(self.location_filter)
        expected = 'Point <Point> (location)'
        self.assertEqual(actual, expected)

    def test_filter_type(self):
        """
        Tests the filter_type method.
        """
        actual = self.followee_filter.filter_type
        expected = 'followee'
        self.assertEqual(actual, expected)

    def test_create_followee_filter(self):
        """
        Test case for a Followee Filter.
        """
        try:
            self.followee_filter.full_clean()
        except ValidationError:
            self.fail("Followee filter raised ValidationError unexpectedly")

    def test_create_location_filter(self):
        """
        Test case for a Location Filter.
        """
        try:
            self.location_filter.full_clean()
        except ValidationError:
            self.fail("Location filter raised ValidationError unexpectedly")

    def test_create_searchterm_filter(self):
        """
        Test case for a SearchTerm Filter.
        """
        try:
            self.srchterm_filter.full_clean()
        except ValidationError:
            self.fail("SearchTerm filter raised ValidationError unexpectedly")

    def test_create_invalid_filter(self):
        """
        Test case for an invalid Filter.
        """
        user_type = ContentType.objects.get_for_model(User)
        new_filter = Filter(
            content_type=user_type,
            object_id=1,
            last_used="2015-01-01T12:00:00+05:00"
        )
        with self.assertRaises(ValidationError):
            new_filter.full_clean()
