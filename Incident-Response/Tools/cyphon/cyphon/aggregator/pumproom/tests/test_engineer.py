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
Tests the Engineer class.
"""

# third party
from django.test import TestCase
import six

# local
from aggregator.pipes.models import PipeSpecSheet
from aggregator.pumproom.engineer import Engineer
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Account
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from tests.fixture_manager import get_fixtures


class EngineerTestCase(TestCase):
    """
    Base class for testing the Engineer class.
    """
    fixtures = get_fixtures(['followees', 'searchterms', 'locations', 'pipes'])

    @staticmethod
    def _create_example_query():
        """
        Helper method that returns an example query.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        accounts = Account.objects.filter(pk__in=[1, 2])
        locations = Location.objects.filter(pk__in=[2, 3, 4, 5])
        return ReservoirQuery(
            searchterms=list(terms),
            accounts=list(accounts),
            locations=list(locations)
        )

    def setUp(self):
        self.query = self._create_example_query()


class GetQueryParametersTestCase(EngineerTestCase):
    """
    Tests methods for retrieving query parameters.
    """

    def setUp(self):
        super(GetQueryParametersTestCase, self).setUp()
        self.engineer = Engineer(query=self.query, specs=PipeSpecSheet())

    def test_get_accounts(self):
        """
        Tests the get_accounts method.
        """
        accounts = self.engineer.get_accounts()
        self.assertEqual(len(accounts), 2)

    def test_get_locations(self):
        """
        Tests the get_locations method.
        """
        locations = self.engineer.get_locations()
        self.assertEqual(len(locations), 4)

    def test_get_searchterms(self):
        """
        Tests the get_searchterms method.
        """
        searchterms = self.engineer.get_searchterms()
        self.assertEqual(len(searchterms), 3)


class FormatLocationsTestCase(EngineerTestCase):
    """
    Tests the format_locations method.
    """

    @classmethod
    def setUpClass(cls):
        super(FormatLocationsTestCase, cls).setUpClass()
        cls.locations = Location.objects.filter(pk__in=[2, 3, 5])

    def test_format_for_box(self):
        """
        Tests the format_locations method for a 'box' location_format.
        """
        query = ReservoirQuery(locations=self.locations)
        specs = PipeSpecSheet(location_format='box')
        engineer = Engineer(query=query, specs=specs)
        engineer._format_locations()

        all_boxes = False
        for new_location in engineer.get_locations():
            if new_location.shape == 'Rectangle':
                all_boxes = True
            else:
                all_boxes = False
                break

        self.assertTrue(all_boxes)

    def test_format_for_radius(self):
        """
        Tests the format_locations method for a 'radius' location_format.
        """
        query = ReservoirQuery(locations=self.locations)
        specs = PipeSpecSheet(location_format='radius', radius_limit_km=100)
        engineer = Engineer(query=query, specs=specs)
        engineer._format_locations()

        all_circles = False
        for new_location in engineer.get_locations():
            if new_location.shape == 'Circle':
                all_circles = True
            else:
                all_circles = False
                break

        self.assertTrue(all_circles)

    def test_invalid_location(self):
        """
        Tests the format_locations method for an invalid location_format.
        """
        query = ReservoirQuery(locations=self.locations)
        specs = PipeSpecSheet(location_format='bad_format')
        engineer = Engineer(query=query, specs=specs)
        with six.assertRaisesRegex(self, AttributeError,
                                    'Invalid location format "bad_format"'):
            engineer._format_locations()


class HandleNegationTestCase(EngineerTestCase):
    """
    Tests the _handle_negation method.
    """

    def test_for_negation_allowed(self):
        """
        Tests the _handle_negation method for an API that allows negation of
        search terms.
        """
        terms = [SearchTerm(term='police'), SearchTerm(term='car', negate=True)]
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet(NOT_operator='NOT')
        engineer = Engineer(query=query, specs=specs)
        engineer._handle_negation()
        searchterms = engineer.get_searchterms()
        self.assertEqual(len(searchterms), 2)

    def test_for_negation_not_allowed(self):
        """
        Tests the _handle_negation method for an API that doesn't allow
        negation of search terms.
        """
        terms = [SearchTerm(term='police'), SearchTerm(term='car', negate=True)]
        query = ReservoirQuery(searchterms=terms)
        engineer = Engineer(query=query, specs=PipeSpecSheet())
        engineer._handle_negation()
        searchterms = engineer.get_searchterms()
        self.assertEqual(len(searchterms), 1)


class HandlePhrasesTestCase(EngineerTestCase):
    """
    Tests the _handle_phrases method.
    """

    def test_for_not_accepts_phrases(self):
        """
        Tests the _handle_phrases method for an API that doesn't accept phrases.
        """
        terms = [SearchTerm(term='police officer')]
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet(accepts_phrases=False)
        engineer = Engineer(query=query, specs=specs)
        engineer._handle_phrases()
        searchterms = engineer.get_searchterms()
        self.assertEqual(len(searchterms), 3)
        self.assertEqual(searchterms[0].term, 'police')
        self.assertEqual(searchterms[1].term, 'officer')
        self.assertEqual(searchterms[2].term, 'policeofficer')

    def test_for_multiple_phrases(self):
        """
        Tests the _handle_phrases method for an API that accepts phrases.
        """
        # 'police', 'police oficeer', 'bank robbery'
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet(accepts_phrases=False)
        engineer = Engineer(query=query, specs=specs)
        engineer._handle_phrases()
        searchterms = engineer.get_searchterms()

        # 'police', 'officer', policeoficeer', 'bank', 'robbery', bankrobbery'
        self.assertEqual(len(searchterms), 6)

    def test_for_accepts_phrases(self):
        """
        Tests the _handle_phrases method for an API that accepts phrases.
        """
        terms = [SearchTerm(term='police officer')]
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet(accepts_phrases=True)
        engineer = Engineer(query=query, specs=specs)
        engineer._handle_phrases()
        searchterms = engineer.get_searchterms()
        self.assertEqual(len(searchterms), 1)
        self.assertEqual(searchterms[0].term, 'police officer')

    def test_dup_terms(self):
        """
        Tests the _handle_phrases method for terms with duplicate words.
        """
        terms = [SearchTerm(term='police'), SearchTerm(term='police officer')]
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet(accepts_phrases=False)
        engineer = Engineer(query=query, specs=specs)
        engineer._handle_phrases()
        searchterms = engineer.get_searchterms()
        self.assertEqual(len(searchterms), 3)


class GetNumSrchSearchTermsTestCase(EngineerTestCase):
    """
    Tests the get_num_searchterms method.
    """

    def test_do_not_count_operator(self):
        """
        Tests the get_num_searchterms method when operators are not counted
        as search terms. Uses the Twitter Public Streams API as an example.
        """
        terms = SearchTerm.objects.filter(pk=1)
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=query, specs=specs)

        # expect 1: 1 for SearchTerm
        self.assertEqual(engineer.get_num_searchterms(query), 1)

    def test_without_or(self):
        """
        Tests the get_num_searchterms method when the operators are counted as
        search terms and the default logic is "OR".
        """
        terms = SearchTerm.objects.filter(pk=1)
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet(
            combine_trm_fol=True,
            combine_trm_opr=True,
            trm_trm_logic='OR',
            OR_operator='OR'
        )
        engineer = Engineer(query=query, specs=specs)

        # expect 5: 1 for SearchTerm, 2 for Accounts
        self.assertEqual(engineer.get_num_searchterms(query), 3)

    def test_without_or_operator(self):
        """
        Tests the get_num_searchterms method when the operators are counted as
        search terms, the default logic is "AND", and an "OR" operator cannot
        be used to join terms.
        """
        terms = SearchTerm.objects.filter(pk=1)
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet(
            combine_trm_fol=True,
            combine_trm_opr=True,
            trm_trm_logic='AND',
            OR_operator='OR'
        )
        specs.combine_trm_opr = True
        specs.trm_trm_logic = 'AND'
        specs.OR_operator = None
        engineer = Engineer(query=query, specs=specs)

        # expect 5: 1 for SearchTerm, 2 for Accounts
        self.assertEqual(engineer.get_num_searchterms(query), 3)

    def test_with_or_operator(self):
        """
        Tests the get_num_searchterms method when operators are counted as
        search terms, the default logic is "AND", and an "OR" operator can
        be used to join terms. Uses the Twitter Search API as an example.
        """
        terms = SearchTerm.objects.filter(pk=1)
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)

        # expect 5: 1 for SearchTerm, 2 for Accounts, 2 for "OR" operators
        self.assertEqual(engineer.get_num_searchterms(query), 5)


class ExceedsSrchSearchTermsLimitTestCase(EngineerTestCase):
    """
    Tests the _exceeds_searchterms_limit method.
    """

    def test_exceeds_twitter_search_api(self):
        """
        Tests the _exceeds_searchterms_limit method for the Twitter Search API
        when the search terms exceed the limit.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3, 4])
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)

        # expect 10 terms: 4 for SearchTerms, 2 for Accounts, 5 for "OR" operators
        self.assertTrue(engineer._exceeds_searchterms_limit(query))

    def test_not_exceed_twitter_srchapi(self):
        """
        Test the _exceeds_searchterms_limit method for the Twitter Search API
        when the serach terms don't exceed the limit.
        """
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)

        # expect 9: 3 for SearchTerms, 2 for Accounts, 4 for "OR" operators
        self.assertFalse(engineer._exceeds_searchterms_limit(self.query))


class SeparateSearchTermsTestCase(EngineerTestCase):
    """
    Tests the _separate_terms method.
    """

    def test_multiple_terms(self):
        """
        Tests the _separate_terms method for multiple terms.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._separate_terms(query)

        self.assertEqual(len(queries), 3)

        # make sure Accounts are being copied to the child queries
        self.assertEqual(queries[2].accounts[0], accounts[0])

    def test_single_term(self):
        """
        Tests the _separate_terms method for a single term.
        """
        terms = SearchTerm.objects.filter(pk=1)
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._separate_terms(query)

        self.assertEqual(len(queries), 1)

        # make sure Accounts are being copied to the child queries
        self.assertEqual(queries[0].accounts[0], accounts[0])


class HandleTrmTrmLogicTestCase(EngineerTestCase):
    """
    Tests the _handle_trm_trm_logic method.
    """

    def test_default_or_logic(self):
        """
        Tests the _handle_trm_trm_logic method for API with default OR logic.
        """
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_trm_logic([self.query])
        self.assertEqual(len(queries), 1)

    def test_default_or_logic(self):
        """
        Tests the _handle_trm_trm_logic method for API with OR operator.
        """
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_trm_logic([self.query])
        self.assertEqual(len(queries), 1)

    def test_no_or_logic(self):
        """
        Tests the _handle_trm_trm_logic method for API without OR logic.
        """
        specs = PipeSpecSheet.objects.get(pipe=4)   # Instagram API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_trm_logic([self.query])
        self.assertEqual(len(queries), 3)


class SeparateLocationsAndSearchTermsTestCase(EngineerTestCase):
    """
    Tests the _separate_locations_and_terms method.
    """

    def test_separate_locations_and_terms(self):
        """
        Tests the _separate_locations_and_terms method.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        locations = Location.objects.filter(pk__in=[2, 3, 5])
        query = ReservoirQuery(searchterms=terms, locations=locations)
        specs = PipeSpecSheet.objects.get(pipe=4)
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._separate_locations_and_terms(query)

        self.assertEqual(len(queries), 2)
        self.assertEqual(len(queries[0].locations), 3)
        self.assertEqual(len(queries[0].searchterms), 0)
        self.assertEqual(len(queries[1].locations), 0)
        self.assertEqual(len(queries[1].searchterms), 3)


class HandleTrmLocLogicTestCase(EngineerTestCase):
    """
    Tests the _handle_trm_loc_logic method.
    """

    def test_default_and_logic(self):
        """
        Tests the _handle_trm_loc_logic method for an OR query with an
        API that joins SearchTerms and Locations using AND logic.
        """
        self.query.trm_loc_logic = 'OR'
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_loc_logic([self.query])
        self.assertEqual(len(queries), 2)

    def test_default_and_logic_multi_qs(self):
        """
        Tests the _handle_trm_loc_logic method for multiple OR queries with an
        API that joins SearchTerms and Locations using AND logic.
        """
        self.query.trm_loc_logic = 'OR'
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_loc_logic([self.query, self.query])
        self.assertEqual(len(queries), 4)

    def test_default_or_logic(self):
        """
        Tests the _handle_trm_loc_logic method for an API tha joins SearchTerms
        and Locations using OR logic.
        """
        self.query.trm_loc_logic = 'OR'
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_loc_logic([self.query])
        self.assertEqual(len(queries), 1)

    def test_query_and_logic(self):
        """
        Tests the _handle_trm_loc_logic method for a query that joins
        SearchTerms and Locations with AND logic.
        """
        self.query.trm_loc_logic = 'AND'
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_loc_logic([self.query])
        self.assertEqual(len(queries), 1)


class SeparateAccountsAndSearchTermsTestCase(EngineerTestCase):
    """
    Tests the _separate_accounts_and_terms method.
    """

    def test_separate_accounts_and_terms(self):
        """
        Tests the _separate_accounts_and_terms method.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        accounts = Account.objects.filter(pk__in=[1, 2])
        query = ReservoirQuery(searchterms=terms, accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=4)
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._separate_accounts_and_terms(query)

        self.assertEqual(len(queries), 2)
        self.assertEqual(len(queries[0].accounts), 2)
        self.assertEqual(len(queries[0].searchterms), 0)
        self.assertEqual(len(queries[1].accounts), 0)
        self.assertEqual(len(queries[1].searchterms), 3)


class HandleTrmFolLogicTestCase(EngineerTestCase):
    """
    Tests the _handle_trm_fol_logic method.
    """

    def test_can_use_or_logic(self):
        """
        Tests the _handle_trm_loc_logic method for an API that can join
        SearchTerms and Accounts using OR.
        """
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_fol_logic([self.query])
        self.assertEqual(len(queries), 1)

    def test_cannot_use_or_logic(self):
        """
        Tests the _handle_trm_loc_logic method for an API that cannot join
        SearchTerms and Accounts using OR.
        """
        specs = PipeSpecSheet.objects.get(pipe=5)   # YouTube Data API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_fol_logic([self.query])
        self.assertEqual(len(queries), 2)

    def test_can_use_or_logic_multi(self):
        """
        Tests the _handle_trm_loc_logic method for multiple queries with an API
        that can join SearchTerms and Accounts using OR.
        """
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_fol_logic([self.query, self.query])
        self.assertEqual(len(queries), 2)

    def test_default_or_logic(self):
        """
        Tests the _handle_trm_loc_logic method for an API that joins SearchTerms
        and Accounts using default OR logic.
        """
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_trm_fol_logic([self.query])
        self.assertEqual(len(queries), 1)


class SeparateComponentsTestCase(EngineerTestCase):
    """
    Tests the _separate_components method.
    """
    @staticmethod
    def _create_example_query():
        """
        Helper function to supply an example query.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3])
        accounts = Account.objects.filter(pk__in=[1, 2])
        locations = Location.objects.filter(pk__in=[2, 3, 5])
        return ReservoirQuery(searchterms=terms, accounts=accounts,
                                    locations=locations)

    def setUp(self):
        self.query = self._create_example_query()

    def test_and_specs_and_query(self):
        """
        Tests the _separate_components method for a query that joins SearchTerms
        and Locations with AND logic, with an API that can't join SearchTerms
        and Accounts using OR logic.
        """
        self.query.trm_loc_logic = 'AND'
        specs = PipeSpecSheet.objects.get(pipe=5)   # YouTube Data API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._separate_components()
        self.assertEqual(len(queries), 2)

    def test_or_specs_and_query(self):
        """
        Tests the _separate_components method for a query that joins SearchTerms
        and Locations with AND logic, with an API that joins SearchTerms and
        Accounts using OR logic.
        """
        self.query.trm_loc_logic = 'AND'
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._separate_components()
        self.assertEqual(len(queries), 1)

    def test_and_specs_or_query(self):
        """
        Tests the _separate_components method for a query that joins SearchTerms
        and Locations with OR logic, with an API that can't join SearchTerms and
        Accounts using OR logic.
        """
        self.query.trm_loc_logic = 'OR'
        specs = PipeSpecSheet.objects.get(pipe=5)   # YouTube Data API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._separate_components()
        self.assertEqual(len(queries), 4)

    def test_or_specs_or_query(self):
        """
        Tests the _separate_components method for a query that joins SearchTerms
        and Locations with OR logic, with an API that joins SearchTerms and
        Accounts using OR logic.
        """
        self.query.trm_loc_logic = 'OR'
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._separate_components()
        self.assertEqual(len(queries), 1)


class HandleCombinedTrmFolLimitTestCase(EngineerTestCase):
    """
    Tests the _handle_combined_trm_fol_limit method.
    """

    def test_not_handled_together(self):
        """
        Tests the _handle_combined_trm_fol_limit method for an API that doesn't
        count accounts as search terms.
        """
        specs = PipeSpecSheet.objects.get(pipe=2)   # Twitter Public Streams API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_combined_trm_fol_limit([self.query])
        self.assertEqual(len(queries), 1)

    def test_no_accounts(self):
        """
        Tests the _handle_combined_trm_fol_limit method for a query that doesn't
        include any accounts.
        """
        terms = SearchTerm.objects.all() # exceeds search terms limit
        query = ReservoirQuery(searchterms=terms)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._handle_combined_trm_fol_limit([query])
        self.assertEqual(len(queries), 1)

    def test_no_searchterms(self):
        """
        Tests the _handle_combined_trm_fol_limit method for a query that doesn't
        include any search terms.
        """
        accounts = Account.objects.filter(pk__in=[1, 2, 3])
        accounts = list(accounts).extend(accounts) # exceeds search terms limit
        query = ReservoirQuery(accounts=accounts)
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=query, specs=specs)
        queries = engineer._handle_combined_trm_fol_limit([query])
        self.assertEqual(len(queries), 1)

    def test_does_not_exceed_limit(self):
        """
        Tests the _handle_combined_trm_fol_limit method for a query that
        includes accounts and search terms, but that doesn't exceed the API
        limit.
        """
        specs = PipeSpecSheet.objects.get(pipe=1)   # Twitter Search API
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_combined_trm_fol_limit([self.query])
        self.assertEqual(len(queries), 1)    

    def test_needs_splitting(self):
        """
        Tests the _handle_combined_trm_fol_limit method for a query that
        includes accounts and search terms, but that doesn't exceed the API
        limit.
        """
        specs = PipeSpecSheet(
            searchterms_limit=8,
            combine_trm_fol=True,
            trm_trm_logic='AND',
            combine_trm_opr=True,
            OR_operator='OR'
        )
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._handle_combined_trm_fol_limit([self.query])

        self.assertEqual(len(queries), 2)


class FactorQueriesByComponentTestCase(EngineerTestCase):
    """
    Tests the _factor_queries_by_component method.
    """

    def test_factor_queries_by_component(self):
        """
        Tests the _factor_queries_by_component method for searchterms.
        """
        specs = PipeSpecSheet(searchterms_limit=1)
        engineer = Engineer(query=self.query, specs=specs)

        queries1 = engineer._factor_queries_by_component([self.query],
                                                         'locations', 1)
        self.assertEqual(len(queries1), 4)

        queries2 = engineer._factor_queries_by_component([self.query],
                                                         'accounts', 1)
        self.assertEqual(len(queries2), 2)


class FactorComponentsTestCase(EngineerTestCase):
    """
    Tests the _factor_components method.
    """

    def test_exceeds_accounts_limit(self):
        """
        Tests the _factor_components method for a query that exceeds the API
        limit on number of accounts.
        """
        specs = PipeSpecSheet(searchterms_limit=10, locations_limit=10,
                          followees_limit=1)
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._factor_components([self.query])
        self.assertEqual(len(queries), 2)

    def test_exceeds_locations_limit(self):
        """
        Tests the _factor_components method for a query that exceeds the API
        limit on number of locations.
        """
        specs = PipeSpecSheet(searchterms_limit=10, locations_limit=1,
                          followees_limit=10)
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._factor_components([self.query])
        self.assertEqual(len(queries), 4)

    def test_exceeds_searchterms_limit(self):
        """
        Tests the _factor_components method for a query that exceeds the API
        limit on number of terms.
        """
        specs = PipeSpecSheet(searchterms_limit=1, locations_limit=10,
                          followees_limit=10)
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._factor_components([self.query])
        self.assertEqual(len(queries), 3)

    def test_no_limits_exceeded(self):
        """
        Tests the _factor_components method for a query that doesn't exceed any
        API limits on number of arguments.
        """
        specs = PipeSpecSheet(searchterms_limit=10, locations_limit=10,
                          followees_limit=10)
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._factor_components([self.query])
        self.assertEqual(len(queries), 1)

    def test_exceeds_all_limits(self):
        """
        Tests the _factor_components method for a query that doesn't exceed any
        API limits on number of arguments.
        """
        specs = PipeSpecSheet(searchterms_limit=1, locations_limit=1,
                          followees_limit=1)
        engineer = Engineer(query=self.query, specs=specs)
        queries = engineer._factor_components([self.query])

        self.assertEqual(len(queries), 24)
        self.assertEqual(len(queries[12].accounts), 1)
        self.assertEqual(len(queries[12].locations), 1)
        self.assertEqual(len(queries[12].searchterms), 1)


class FactorQueryTestCase(EngineerTestCase):
    """
    Tests the factor_query method.
    """

    def test_for_small_circle(self):
        """
        Tests the factor_query method for a circular location smaller than
        the radius limit.
        """
        locations = Location.objects.filter(pk=2)
        query = ReservoirQuery(locations=locations)
        specs = PipeSpecSheet(location_format='radius', radius_limit_km=1)
        engineer = Engineer(query=query, specs=specs)
        queries = engineer.factor_query()
        self.assertTrue(len(queries[0].locations) == 1)

    def test_for_equal_circle(self):
        """
        Tests the factor_query method for a circular location equal to
        the radius limit.
        """
        locations = Location.objects.filter(pk=2)
        query = ReservoirQuery(locations=locations)
        specs = PipeSpecSheet(location_format='radius', radius_limit_km=0.1)
        engineer = Engineer(query=query, specs=specs)

        queries = engineer.factor_query()
        self.assertTrue(len(queries[0].locations) == 1)

    def test_for_large_circle(self):
        """
        Tests the factor_query method for a circular location larger than
        the radius limit.
        """
        locations = Location.objects.filter(pk=2)
        query = ReservoirQuery(locations=locations)
        specs = PipeSpecSheet(location_format='radius', radius_limit_km=0.05)
        engineer = Engineer(query=query, specs=specs)

        queries = engineer.factor_query()
        self.assertTrue(len(queries[0].locations) > 1)

    def test_complex_query(self):
        """
        Tests the factor_query method for an API that doens't accept phrases and
        for which the query exceeds the search term limit.
        """
        terms = SearchTerm.objects.filter(pk__in=[1, 2, 3]) # 6 terms when parsed
        accounts = Account.objects.filter(pk__in=[1, 2])
        locations = Location.objects.filter(pk=2)
        query = ReservoirQuery(
            searchterms=list(terms),
            accounts=list(accounts),
            locations=list(locations),
            trm_loc_logic='AND'
        )
        specs = PipeSpecSheet(
            searchterms_limit=10,
            followees_limit=1,
            accepts_phrases=False,
            combine_trm_fol=True,
            combine_trm_opr=True,
            trm_trm_logic='AND',
            trm_fol_logic='AND',
            trm_loc_logic='AND',
            OR_operator='OR',
            location_format='radius',
            radius_limit_km=0.1
        )
        engineer = Engineer(query=query, specs=specs)

        queries = engineer.factor_query()
        self.assertEqual(len(queries), 4)

# TODO(LH): tests for polygon, multipolygon
