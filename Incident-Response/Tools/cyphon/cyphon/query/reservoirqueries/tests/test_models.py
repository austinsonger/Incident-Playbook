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
Tests the ReservoirQueryHandler class. 
"""

# standard library
import datetime

# third party
from django.test import TestCase

# local
from query.reservoirqueries.models import ReservoirQueryParameters
from tests.fixture_manager import get_fixtures


class ReservoirQueryParametersTestCase(TestCase):
    """
    Base class for testing the ReservoirQueryParameters class and related classes.
    """
    fixtures = get_fixtures(['reservoirs', 'locations', 'searchterms',
                             'followees', 'parameters'])

    @staticmethod
    def _create_example_parameters():
        """
        Helper function that returns an example ReservoirQueryParameters object.
        """
        parameters = ReservoirQueryParameters.objects.get(pk=1)
        start_time = datetime.datetime.now()
        delta = datetime.timedelta(days=10)
        end_time = datetime.datetime.now() + delta
        parameters.start_time = start_time
        parameters.end_time = end_time
        return parameters


class ParseKeywordsTestCase(ReservoirQueryParametersTestCase):
    """
    Tests the _create_searchterms method.
    """

    def make_comparisons_for_words(self, terms):
        """
        Helper method that makes assertions for a standard set of expected
        results for an example query that includes only words.
        """
        self.assertEqual(terms[0].term, 'bear')
        self.assertEqual(terms[0].negate, False)
        self.assertEqual(terms[1].term, 'cat')
        self.assertEqual(terms[1].negate, False)
        self.assertEqual(terms[2].term, 'dog')
        self.assertEqual(terms[2].negate, False)
        self.assertEqual(terms[3].term, 'eagle')
        self.assertEqual(terms[3].negate, True)
        self.assertEqual(terms[4].term, 'fox')
        self.assertEqual(terms[4].negate, True)
        self.assertEqual(terms[5].term, 'gator')
        self.assertEqual(terms[5].negate, True)

    def make_comparisons_for_phrases(self, terms):
        """
        Helper method that makes assertions for a standard set of expected
        results for an example query that includes phrases.
        """
        self.assertEqual(terms[0].term, 'bear')
        self.assertEqual(terms[0].negate, False)
        self.assertEqual(terms[1].term, 'deer')
        self.assertEqual(terms[1].negate, False)
        self.assertEqual(terms[2].term, 'bird dog')
        self.assertEqual(terms[2].negate, False)
        self.assertEqual(terms[3].term, 'wild turkey')
        self.assertEqual(terms[3].negate, False)
        self.assertEqual(terms[4].term, 'fox')
        self.assertEqual(terms[4].negate, True)
        self.assertEqual(terms[5].term, 'gator')
        self.assertEqual(terms[5].negate, True)
        self.assertEqual(terms[6].term, 'eagle owl')
        self.assertEqual(terms[6].negate, True)
        self.assertEqual(terms[7].term, 'sparrow hawk')
        self.assertEqual(terms[7].negate, True)

    def test_comma_separated_values(self):
        """
        Tests the _create_searchterms method for comma-separated values.
        """
        handler = ReservoirQueryParameters(
            included_keywords='bear, cat, dog',
            excluded_keywords='eagle, fox, gator'
        )
        terms = handler._create_searchterms()
        self.make_comparisons_for_words(terms)

    def test_space_separated_values(self):
        """
        Tests the _create_searchterms method for space-separated values.
        """
        handler = ReservoirQueryParameters(
            included_keywords='bear cat dog',
            excluded_keywords='eagle fox gator'
        )
        terms = handler._create_searchterms()
        self.make_comparisons_for_words(terms)

    def test_phrases_with_commas(self):
        """
        Tests the _create_searchterms method for comma-separated values that
        include phrases.
        """
        handler = ReservoirQueryParameters(
            included_keywords='bear, "bird dog", deer, "wild turkey"',
            excluded_keywords='"eagle owl", "sparrow hawk", fox, gator'
        )
        terms = handler._create_searchterms()
        self.make_comparisons_for_phrases(terms)

    def test_phrases_with_spaces(self):
        """
        Tests the _create_searchterms method for space-separated values that
        include phrases.
        """
        handler = ReservoirQueryParameters(
            included_keywords='bear "bird dog" deer "wild turkey"',
            excluded_keywords='"eagle owl" "sparrow hawk" fox gator'
        )
        terms = handler._create_searchterms()
        self.make_comparisons_for_phrases(terms)

    def test_phrases_with_commas_spaces(self):
        """
        Tests the _create_searchterms method for both comma-separated and
        space-separated values that include phrases.
        """
        handler = ReservoirQueryParameters(
            included_keywords='bear, "bird dog", deer, "wild turkey"',
            excluded_keywords='"eagle owl" "sparrow hawk" fox gator'
        )
        terms = handler._create_searchterms()
        self.make_comparisons_for_phrases(terms)


class CreateReservoirQuery(ReservoirQueryParametersTestCase):
    """
    Tests the _create_reservoir_query method.
    """

    def test_create_reservoir_query(self):
        """
        Tests the _create_reservoir_query method.
        """
        parameters = self._create_example_parameters()
        query = parameters._create_reservoir_query()
        delta = query.timeframe.end - query.timeframe.start
        self.assertEqual(len(query.locations.all()), 2)
        self.assertEqual(len(query.searchterms), 3)
        self.assertEqual(delta.days, 10)
        self.assertEqual(query.trm_loc_logic, 'AND')

# TODO: test reservoirs parameter, including its default
# TODO: test locations parameter

