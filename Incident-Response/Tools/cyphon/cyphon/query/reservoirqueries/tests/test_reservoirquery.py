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
Tests the MediaQuery class used for keywords and phrases.
"""

# standard library
from datetime import datetime

# third party
from django.test import TestCase

# local
from aggregator.reservoirs.models import Reservoir
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Account
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame
from tests.fixture_manager import get_fixtures


class ReservoirQueryTestCase(TestCase):
    """
    Tests the ReservoirQuery class.
    """
    fixtures = get_fixtures(['reservoirs', 'locations', 'searchterms',
                             'followees'])

    start_date = datetime(2015, 1, 1, 12, 0, 0, 0)
    end_date = datetime(2015, 2, 1, 12, 0, 0, 0)

    def _create_example_query(self):
        """
        Helper function to supply an example query.
        """
        accounts = Account.objects.filter(pk__in=[1, 2, 3])
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        locations = Location.objects.filter(pk__in=[2, 3, 4, 5])
        timeframe = TimeFrame(start=self.start_date, end=self.end_date)

        return ReservoirQuery(
            accounts=list(accounts),
            searchterms=list(terms),
            locations=list(locations),
            timeframe=timeframe,
            trm_loc_logic='AND'
        )

    @staticmethod
    def _create_query_2_included_terms():
        """
        Helper method that returns a ReservoirQuery with two included terms.
        """
        term1 = SearchTerm(term='cops', negate=False)
        term2 = SearchTerm(term='robbers', negate=False)
        terms = [term1, term2]
        return ReservoirQuery(searchterms=terms)

    @staticmethod
    def _create_query_2_excluded_terms():
        """
        Helper method that returns a ReservoirQuery with two excluded terms.
        """
        term1 = SearchTerm(term='cops', negate=True)
        term2 = SearchTerm(term='robbers', negate=True)
        terms = [term1, term2]
        return ReservoirQuery(searchterms=terms)

    @staticmethod
    def _create_query_2_mixed_terms():
        """
        Helper method that returns a ReservoirQuery with one included term and
        one excluded term.
        """
        term1 = SearchTerm(term='cops', negate=False)
        term2 = SearchTerm(term='robbers', negate=True)
        terms = [term1, term2]
        return ReservoirQuery(searchterms=terms)

    def setUp(self):
        self.query = self._create_example_query()
        self.query_with_2_included_terms = self._create_query_2_included_terms()
        self.query_with_2_excluded_terms = self._create_query_2_excluded_terms()
        self.query_with_2_mixed_terms = self._create_query_2_mixed_terms()


class QueryConversionTestCase(ReservoirQueryTestCase):
    """
    Tests the to_dict and to_json methods.
    """

    def _create_complete_query(self):
        """
        Helper function to supply an example query using all avaiable parameters.
        """
        accounts = Account.objects.filter(pk__in=[1, 2])
        terms = SearchTerm.objects.filter(pk__in=[1, 2])
        locations = Location.objects.filter(pk__in=[2, 3])
        timeframe = TimeFrame(start=self.start_date, end=self.end_date)

        return ReservoirQuery(
            accounts=list(accounts),
            searchterms=list(terms),
            locations=list(locations),
            timeframe=timeframe,
            trm_loc_logic='AND'
        )

    @staticmethod
    def _create_empty_query():
        """
        Helper function to supply an empty query.
        """
        return ReservoirQuery()

    def setUp(self):
        super(QueryConversionTestCase, self).setUp()
        self.complete_query = self._create_complete_query()
        self.empty_query = self._create_empty_query()

    def test_to_dict_for_complete_query(self):
        """
        Tests the to_dict method for a ReservoirQuery using all available
        parameters.
        """
        self.maxDiff = None
        actual = self.complete_query.to_dict()
        expected = {
            'accounts': [
                {
                    'followee': 1,
                    'platform': 1,
                    'user_id': '73987',
                    'username': 'jad'
                },
                {
                    'followee': 1,
                    'platform': 1,
                    'user_id': '89632',
                    'username': 'jad2'
                }
            ],
            'locations': [
                {
                    'buffer_m': 100,
                    'created_by': 1,
                    'editable': True,
                    'geom': 'SRID=4326;POINT (-78.2 36.4)',
                    'name': 'Circle'
                },
                {
                    'buffer_m': 0,
                    'created_by': 1,
                    'editable': True,
                    'geom': 'SRID=4326;POLYGON ((1 0, 1 50.5, 50.5 50.5, 50.5 0, 1 0))',
                    'name': 'Big Polygon'
                }
            ],
            'searchterms': [
                {
                    'negate': False,
                    'term': 'police'
                },
                {
                    'negate': False,
                    'term': 'police officer'
                }
            ],
            'timeframe': {
                'end': '2015-02-01T12:00:00',
                'start': '2015-01-01T12:00:00'
            },
            'trm_loc_logic': 'AND'
        }
        self.assertEqual(actual, expected)

    def test_to_dict_for_empty_query(self):
        """
        Tests the to_dict method for a ReservoirQuery using none of the
        available parameters.
        """
        self.maxDiff = None
        actual = self.empty_query.to_dict()
        expected = {
            'accounts': [],
            'locations': [],
            'searchterms': [],
            'timeframe': {},
            'trm_loc_logic': 'OR'
        }
        self.assertEqual(actual, expected)

    def test_to_json_for_complete_query(self):
        """
        Tests the to_json method for a ReservoirQuery using all available
        parameters.
        """
        self.maxDiff = None
        actual = self.complete_query.to_json()
        expected = \
'''{
    "accounts": [
        {
            "followee": 1,
            "platform": 1,
            "user_id": "73987",
            "username": "jad"
        },
        {
            "followee": 1,
            "platform": 1,
            "user_id": "89632",
            "username": "jad2"
        }
    ],
    "locations": [
        {
            "buffer_m": 100,
            "created_by": 1,
            "editable": true,
            "geom": "SRID=4326;POINT (-78.2 36.4)",
            "name": "Circle"
        },
        {
            "buffer_m": 0,
            "created_by": 1,
            "editable": true,
            "geom": "SRID=4326;POLYGON ((1 0, 1 50.5, 50.5 50.5, 50.5 0, 1 0))",
            "name": "Big Polygon"
        }
    ],
    "searchterms": [
        {
            "negate": false,
            "term": "police"
        },
        {
            "negate": false,
            "term": "police officer"
        }
    ],
    "timeframe": {
        "end": "2015-02-01T12:00:00",
        "start": "2015-01-01T12:00:00"
    },
    "trm_loc_logic": "AND"
}'''
        self.assertEqual(actual, expected)

    def test_to_json_for_empty_query(self):
        """
        Tests the to_josn method for a ReservoirQuery using none of the
        available parameters.
        """
        self.maxDiff = None
        actual = self.empty_query.to_json()
        expected = \
'''{
    "accounts": [],
    "locations": [],
    "searchterms": [],
    "timeframe": {},
    "trm_loc_logic": "OR"
}'''
        self.assertEqual(actual, expected)


class IncludedSearchTermsTestCase(ReservoirQueryTestCase):
    """
    Tests the included_terms property.
    """

    def test_included_for_no_terms(self):
        """
        Tests the included_terms property for no search terms.
        """
        query = ReservoirQuery(searchterms=[])
        self.assertEqual(query.included_terms, [])

    def test_no_included_terms(self):
        """
        Tests the included_terms property for no included terms.
        """
        query = self.query_with_2_excluded_terms
        self.assertEqual(len(query.included_terms), 0)

    def test_one_included_term(self):
        """
        Tests the included_terms property for one included term.
        """
        query = self.query_with_2_mixed_terms
        self.assertEqual(len(query.included_terms), 1)

    def test_multiple_included_terms(self):
        """
        Tests the included_terms property for multiple included terms.
        """
        query = self.query_with_2_included_terms
        self.assertEqual(len(query.included_terms), 2)


class ExcludedSearchTermsTestCase(ReservoirQueryTestCase):
    """
    Tests the excluded_terms property.
    """

    def test_excluded_for_no_terms(self):
        """
        Tests the excluded_terms property for no search terms.
        """
        query = ReservoirQuery(searchterms=[])
        self.assertEqual(query.excluded_terms, [])

    def test_no_excluded_terms(self):
        """
        Tests the excluded_terms property for no excluded terms.
        """
        query = self.query_with_2_included_terms
        self.assertEqual(len(query.excluded_terms), 0)

    def test_one_excluded_term(self):
        """
        Tests the excluded_terms property for one excluded term.
        """
        query = self.query_with_2_mixed_terms
        self.assertEqual(len(query.excluded_terms), 1)

    def test_multiple_excluded_terms(self):
        """
        Tests the excluded_terms property for multiple excluded terms.
        """
        query = self.query_with_2_excluded_terms
        self.assertEqual(len(query.excluded_terms), 2)


class RemoveNegatedTermsTestCase(ReservoirQueryTestCase):
    """
    Tests the excluded_terms property.
    """

    def test_excluded_for_no_terms(self):
        """
        Tests the remove_negated_terms method for no search terms.
        """
        query = ReservoirQuery(searchterms=[])
        query.remove_negated_terms()
        self.assertEqual(query.searchterms, [])

    def test_no_excluded_terms(self):
        """
        Tests the remove_negated_terms method for no excluded terms.
        """
        query = self.query_with_2_included_terms
        query.remove_negated_terms()
        self.assertEqual(len(query.searchterms), 2)

    def test_one_excluded_term(self):
        """
        Tests the remove_negated_terms method for one excluded term.
        """
        query = self.query_with_2_mixed_terms
        query.remove_negated_terms()
        self.assertEqual(len(query.searchterms), 1)

    def test_multiple_excluded_terms(self):
        """
        Tests the remove_negated_terms method for multiple excluded terms.
        """
        query = self.query_with_2_excluded_terms
        query.remove_negated_terms()
        self.assertEqual(len(query.searchterms), 0)


class FilterAccountsTestCase(ReservoirQueryTestCase):
    """
    Tests the filter_accounts method.
    """

    def test_no_followees(self):
        """
        Tests the filter_accounts method for a Reservoir with no
        Followees associated with it.
        """
        query = self._create_example_query()
        reservoir = Reservoir.objects.get_by_natural_key('youtube')
        query.filter_accounts(reservoir)

        # check that all the data was copied over
        self.assertEqual(len(query.accounts), 0)
        self.assertEqual(len(query.locations), 4)
        self.assertEqual(len(query.searchterms), 3)
        self.assertEqual(query.timeframe.start, self.start_date)
        self.assertEqual(query.trm_loc_logic, 'AND')

    def test_single_followee(self):
        """
        Tests the filter_accounts method for a Reservoir with one
        Followee associated with it.
        """
        query = self._create_example_query()
        reservoir = Reservoir.objects.get_by_natural_key('facebook')
        query.filter_accounts(reservoir)
        self.assertEqual(len(query.accounts), 1)

    def test_multiple_followees(self):
        """
        Tests the filter_accounts method for a Reservoir with multiple
        Followees associated with it.
        """
        query = self._create_example_query()
        reservoir = Reservoir.objects.get_by_natural_key('twitter')
        query.filter_accounts(reservoir)
        self.assertEqual(len(query.accounts), 2)


class ConvertToBoxesTestCase(ReservoirQueryTestCase):
    """
    Tests the convert_all_shapes_to_boxes method.
    """

    def test_for_no_locations(self):
        """
        Tests the convert_all_shapes_to_boxes method for no locations.
        """
        query = ReservoirQuery(locations=[])
        query.convert_all_shapes_to_boxes()
        self.assertEqual(query.locations, [])

    def test_for_multiple_locations(self):
        """
        Tests the convert_all_shapes_to_boxes method for multiple locations.
        """
        locations = Location.objects.filter(pk__in=[2, 3, 5])
        query = ReservoirQuery(locations=locations)
        query.convert_all_shapes_to_boxes()

        all_boxes = False
        for new_location in query.locations:
            if new_location.shape == 'Rectangle':
                all_boxes = True
            else:
                all_boxes = False
                break

        self.assertTrue(all_boxes)


class FactorLocationsByRadiusTestCase(ReservoirQueryTestCase):
    """
    Tests the factor_locations_by_radius method.
    """

    def test_for_no_locations(self):
        """
        Tests the factor_locations_by_radius method for no locations.
        """
        query = ReservoirQuery(locations=[])
        query.factor_locations_by_radius(radius_km=100)
        self.assertEqual(query.locations, [])

    def test_for_multiple_locations(self):
        """
        Tests the factor_locations_by_radius method for multiple locations.
        """
        locations = Location.objects.filter(pk__in=[2, 3, 5])
        query = ReservoirQuery(locations=locations)
        query.factor_locations_by_radius(radius_km=100)

        all_circles = False
        for new_location in query.locations:
            if new_location.shape == 'Circle':
                all_circles = True
            else:
                all_circles = False
                break

        self.assertTrue(all_circles)


class AddSrchtermTestCase(ReservoirQueryTestCase):
    """
    Tests the add_searchterm method.
    """

    def test_for_unique_term(self):
        """
        Tests the add_searchterm method for a non-duplicate term.
        """
        terms = [SearchTerm(term='police'), SearchTerm(term='car')]
        query = ReservoirQuery(searchterms=terms)
        query.add_searchterm(SearchTerm(term='arrest'))
        self.assertEqual(len(query.searchterms), 3)

    def test_for_duplicate_term(self):
        """
        Tests the add_searchterm method for a duplicate term.
        """
        terms = [SearchTerm(term='police'), SearchTerm(term='car')]
        query = ReservoirQuery(searchterms=terms)
        query.add_searchterm(SearchTerm(term='police'))
        self.assertEqual(len(query.searchterms), 2)


class TransformPhrasesTestCase(ReservoirQueryTestCase):
    """
    Tests the transform_phrases method.
    """

    def test_for_no_terms(self):
        """
        Tests the transform_phrases method for no terms.
        """
        query = ReservoirQuery(searchterms=[])
        query.transform_phrases()
        self.assertEqual(query.searchterms, [])

    def test_for_mixed_terms(self):
        """
        Tests the transform_phrases method for a mix of phrases and non-phrases.
        """
        terms = [SearchTerm(term='robbery'), SearchTerm(term='police car')]
        query = ReservoirQuery(searchterms=terms)
        query.transform_phrases()

        self.assertEqual(len(query.searchterms), 4)
        self.assertEqual(query.searchterms[0].term, 'robbery')
        self.assertEqual(query.searchterms[1].term, 'police')
        self.assertEqual(query.searchterms[2].term, 'car')
        self.assertEqual(query.searchterms[3].term, 'policecar')


class WrapPhrasesInQuotesTestCase(ReservoirQueryTestCase):
    """
    Tests the wrap_phrases_in_quotes method.
    """

    def test_for_mixed_terms(self):
        """
        Tests the transform_phrases method for a mix of phrases and non-phrases.
        """
        terms = [SearchTerm(term='robbery'), SearchTerm(term='police car')]
        query = ReservoirQuery(searchterms=terms)
        query.wrap_phrases_in_quotes()

        self.assertEqual(len(query.searchterms), 2)
        self.assertEqual(query.searchterms[0].term, 'robbery')
        self.assertEqual(query.searchterms[1].term, '"police car"')
