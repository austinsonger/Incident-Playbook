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
Tests the TwitterSearch class.
"""

# standard library
from unittest import skipUnless

# third party
from django.contrib.gis.geos import Point

# local
from aggregator.pipes.models import Pipe
from platforms.tests.test_apihandler import ApiHandlerTestCase
from platforms.twitter.handlers import SearchAPI
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Account
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame
from .mixins import TWITTER_TESTS_ENABLED, TwitterPassportMixin


class TwitterSearchTestCase(ApiHandlerTestCase):
    """
    Tests the SearchAPI class.
    """

    @staticmethod
    def _create_search_handler():
        """
        Helper method that returns an example SearchAPI handler.
        """
        endpoint = Pipe.objects.get(pk=1)
        return SearchAPI(endpoint=endpoint, user=None, task='AD_HOC_SRCH')

    def setUp(self):
        super(TwitterSearchTestCase, self).setUp()
        self.search_handler = self._create_search_handler()


class FormatTimeFrameTestCase(TwitterSearchTestCase):
    """
    Tests the platform_name property for the Twitter SearchAPI class.
    """

    def test_platform_name(self):
        """
        Tests the platform_name property for the Twitter SearchAPI class.
        """
        actual = self.search_handler.data_source_label
        self.assertEqual(actual, 'twitter')

    def test_pipe_natural_key(self):
        """
        Tests the pipe_natural_key property for the Twitter SearchAPI class.
        """
        actual = self.search_handler.pipe_natural_key
        expected = ('twitter', 'SearchAPI')
        self.assertEqual(actual, expected)

        # make sure the natural key can really be used to get a Pipe
        pipe = Pipe.objects.get_by_natural_key(*expected)
        self.assertEqual(pipe.id, 1)


class FormatTimeFrameTestCase(TwitterSearchTestCase):
    """
    Tests the _format_timeframe method.
    """

    def test_start_and_end(self):
        """
        Tests the _format_timeframe method.
        """
        self.query.timeframe = TimeFrame.objects.get(pk=1)
        actual = self.search_handler._format_timeframe(self.query.timeframe)
        expected = 'since:2015-01-01 until:2015-01-04'
        self.assertEqual(actual, expected)

    def test_start_only(self):
        """
        Tests the _format_timeframe method.
        """
        self.query.timeframe = TimeFrame.objects.get(pk=3)
        actual = self.search_handler._format_timeframe(self.query.timeframe)
        expected = 'since:2015-01-01'
        self.assertEqual(actual, expected)

    def test_end_only(self):
        """
        Tests the _format_timeframe method.
        """
        self.query.timeframe = TimeFrame.objects.get(pk=4)
        actual = self.search_handler._format_timeframe(self.query.timeframe)
        expected = 'until:2015-01-04'
        self.assertEqual(actual, expected)


class FormatSearchTermsTestCase(TwitterSearchTestCase):
    """
    Tests the _format_searchterms method.
    """

    def test_one_included_term(self):
        """
        Tests the _format_searchterms method for one included term.
        """
        self.query.searchterms = SearchTerm.objects.filter(pk=10)
        actual = self.search_handler._format_searchterms(self.query.searchterms)
        expected = '"lion cub"'
        self.assertEqual(actual, expected)

    def test_three_included_terms(self):
        """
        Tests the _format_searchterms method for three included terms.
        """
        self.query.searchterms = SearchTerm.objects.filter(pk__in=[9, 10, 11])
        actual = self.search_handler._format_searchterms(self.query.searchterms)
        expected = '(dove OR "lion cub" OR tiger)'
        self.assertEqual(actual, expected)

    def test_one_excluded_term(self):
        """
        Tests the _format_searchterms method for one excluded term.
        """
        self.query.searchterms = SearchTerm.objects.filter(pk=12)
        actual = self.search_handler._format_searchterms(self.query.searchterms)
        expected = '-bear'
        self.assertEqual(actual, expected)

    def test_two_excluded_terms(self):
        """
        Tests the _format_searchterms method for two excluded terms.
        """
        self.query.searchterms = SearchTerm.objects.filter(pk__in=[12, 13])
        actual = self.search_handler._format_searchterms(self.query.searchterms)
        expected = '-bear -deer'
        self.assertEqual(actual, expected)

    def test_three_mixed_terms(self):
        """
        Tests the _format_searchterms method for two included terms and one
        excluded term.
        """
        actual = self.search_handler._format_searchterms(self.query.searchterms)
        expected = '("lion cub" OR tiger) -bear'
        self.assertEqual(actual, expected)


class FormatAccountsTestCase(TwitterSearchTestCase):
    """
    Tests the _format_accounts method.
    """

    def test_two_accounts(self):
        """
        Tests the _format_accounts method for two accounts.
        """
        actual = self.search_handler._format_accounts(self.query.accounts)
        expected = '(@jad OR @jad2)'
        self.assertEqual(actual, expected)

    def test_one_account(self):
        """
        Tests the _format_accounts method for one account.
        """
        self.query.accounts = Account.objects.filter(pk=1)
        actual = self.search_handler._format_accounts(self.query.accounts)
        expected = '@jad'
        self.assertEqual(actual, expected)

    def test_no_accounts(self):
        """
        Tests the _format_accounts method for no accounts.
        """
        self.query.accounts = []
        actual = self.search_handler._format_accounts(self.query.accounts)
        expected = ''
        self.assertEqual(actual, expected)


class FormatQParamTestCase(TwitterSearchTestCase):
    """
    Tests the _format_q_param method.
    """

    def test_format_q_param(self):
        """
        Tests the _format_q_param method.
        """
        actual = self.search_handler._format_q_param(self.query)
        expected = '("lion cub" OR tiger) -bear (@jad OR @jad2) since:2015-01-01 until:2015-01-04'
        self.assertEqual(actual, expected)


class FormatGeocodeParamTestCase(TwitterSearchTestCase):
    """
    Tests the _format_geocode_param method.
    """

    def test_format_geocode_param(self):
        """
        Tests the _format_geocode_param method.
        """
        location = Location.objects.get(pk=2)
        actual = self.search_handler._format_geocode_param(location)
        expected = '36.4,-78.2,0.1km'
        self.assertEqual(actual, expected)


class FormatSearchQueryTestCase(TwitterSearchTestCase):
    """
    Tests the _format_query method.
    """

    def test_with_location(self):
        """
        Tests the _format_query method when the query contains a location.
        """
        self.query.locations = [Location.objects.get(pk=2)]
        actual = self.search_handler._format_query(self.query)
        expected = {
            'q': '("lion cub" OR tiger) -bear (@jad OR @jad2) since:2015-01-01 until:2015-01-04',
            'geocode_param': '36.4,-78.2,0.1km',
            'result_type': 'recent'
        }
        self.assertEqual(actual['q'], expected['q'])
        self.assertEqual(actual['geocode_param'], expected['geocode_param'])
        self.assertEqual(actual['result_type'], expected['result_type'])

    def test_no_location(self):
        """
        Tests the _format_query method when the query contains a location.
        """
        self.query.locations = []
        actual = self.search_handler._format_query(self.query)
        expected = {
            'q': '("lion cub" OR tiger) -bear (@jad OR @jad2) since:2015-01-01 until:2015-01-04',
            'result_type': 'recent'
        }
        self.assertEqual(actual['q'], expected['q'])
        self.assertEqual(actual['result_type'], expected['result_type'])
        self.assertFalse(hasattr(actual, 'geocode_param'))


class ProcessSearchQueryTestCase(TwitterSearchTestCase, TwitterPassportMixin):
    """
    Tests the process_query method.
    """

    def _create_test_query(self):
        """
        Helper method that returns an example ReservoirQuery.
        """
        accounts = [Account(username='twitter')]
        locations = [Location(geom=Point(-76.6653729, 39.4904058), buffer_m=1000)]
        searchterms = [
            SearchTerm(term='photos'),
            SearchTerm(term='media')
        ]
        timeframe = self._create_example_timeframe()

        return ReservoirQuery(
            accounts=accounts,
            locations=locations,
            searchterms=searchterms,
            timeframe=timeframe
        )

    @skipUnless(TWITTER_TESTS_ENABLED, 'Twitter API tests disabled')
    def test_process_request(self):
        """
        Tests the process_request method.
        """
        self._update_passport()
        query = self._create_test_query()
        results = self.search_handler.process_request(query)

        # ensure that we're getting multiple tweets back
        self.assertTrue(len(results.data) > 2)
