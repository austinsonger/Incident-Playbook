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
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe
from platforms.tests.test_apihandler import (
    ApiHandlerTestCase,
    ApiHandlerTransactionTestCase,
)
from platforms.twitter.handlers import PublicStreamsAPI
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Account
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame
from .mixins import TWITTER_TESTS_ENABLED, TwitterPassportMixin


class TwitterPublicStreamsMixin(object):
    """
    Mixin for tests of the PublicStreamsAPI class.
    """

    @staticmethod
    def _create_stream_handler():
        """
        Helper method that returns an example PublicStreamsAPI handler.
        """
        endpoint = Pipe.objects.get(pk=2)
        return PublicStreamsAPI(endpoint=endpoint, user=None, task='BKGD_SRCH')


class TwitterPublicStreamsTestCase(ApiHandlerTestCase, TwitterPublicStreamsMixin):
    """
    Tests the PublicStreamsAPI class.
    """

    def setUp(self):
        super(TwitterPublicStreamsTestCase, self).setUp()
        self.stream_handler = self._create_stream_handler()


class FormatFolloweesTestCase(TwitterPublicStreamsTestCase):
    """
    Tests the _format_followees_param method.
    """

    def test_two_accounts(self):
        """
        Tests the _format_followees_param method for two accounts.
        """
        actual = self.stream_handler._format_followees_param(self.query.accounts)
        expected = ['73987', '89632']
        self.assertEqual(actual, expected)

    def test_one_account(self):
        """
        Tests the _format_followees_param method for one account.
        """
        self.query.accounts = Account.objects.filter(pk=1)
        actual = self.stream_handler._format_followees_param(self.query.accounts)
        expected = ['73987']
        self.assertEqual(actual, expected)

    def test_no_accounts(self):
        """
        Tests the _format_followees_param method for no accounts.
        """
        self.query.accounts = []
        actual = self.stream_handler._format_followees_param(self.query.accounts)
        expected = []
        self.assertEqual(actual, expected)


class FormatLocationsTestCase(TwitterPublicStreamsTestCase):
    """
    Tests the _format_locations_param method.
    """

    def test_one_location(self):
        """
        Tests the _format_locations_param method for one location.
        """
        locations = Location.objects.filter(pk__in=[5])
        actual = self.stream_handler._format_locations_param(locations)
        expected = [0.0, 0.0, 2.0, 2.0]
        self.assertEqual(actual, expected)

    def test_two_locations(self):
        """
        Tests the _format_locations_param method for two locations.
        """
        locations = Location.objects.filter(pk__in=[5, 8])
        actual = self.stream_handler._format_locations_param(locations)
        expected = [0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 50.0, 20.0]
        self.assertEqual(actual, expected)

    def test_no_location(self):
        """
        Tests the _format_locations_param method for no locations.
        """
        locations = []
        actual = self.stream_handler._format_locations_param(locations)
        self.assertEqual(actual, [])


class FormatSearchTermsTestCase(TwitterPublicStreamsTestCase):
    """
    Tests the _format_searchterms_param method.
    """

    def test_format_searchterms_param(self):
        """
        Tests the _format_searchterms_param method.
        """
        searchterms = [SearchTerm(term='photos'), SearchTerm(term='social media')]
        actual = self.stream_handler._format_searchterms_param(searchterms)
        expected = ['photos', '"social media"']
        self.assertEqual(actual, expected)


class FormatStreamQueryTestCase(TwitterPublicStreamsTestCase):
    """
    Tests the _format_query method.
    """

    def test_for_three_parameters(self):
        """
        Tests the _format_query method for all three parameters.
        """
        actual = self.stream_handler._format_query(self.query)
        expected = {
            'follow': ['73987', '89632'],
            'locations': [1.0, 0.0, 50.5, 50.5, 0.0, 0.0, 1.0, 1.0],
            'track': ['"lion cub"', 'tiger']
        }
        self.assertEqual(actual['follow'], expected['follow'])
        self.assertEqual(actual['locations'], expected['locations'])
        self.assertEqual(actual['track'], expected['track'])

    def test_for_no_parameters(self):
        """
        Tests the _format_query method for no parameters.
        """
        self.stream_handler._format_query(ReservoirQuery())
        self.assertFalse(hasattr(self.stream_handler, 'follow'))
        self.assertFalse(hasattr(self.stream_handler, 'locations'))
        self.assertFalse(hasattr(self.stream_handler, 'track'))


class SubmitStreamQueryTestCase(ApiHandlerTransactionTestCase,
                                TwitterPublicStreamsMixin,
                                TwitterPassportMixin):
    """
    Tests the PublicStreamsAPI class.
    """

    def setUp(self):
        super(SubmitStreamQueryTestCase, self).setUp()
        self.stream_handler = self._create_stream_handler()

    @staticmethod
    def _create_test_query():
        """
        Returns a ReservoirQuery for @twitter.
        """
        accounts = [Account(user_id=783214), Account(user_id=6253282)]
        locations = Location.objects.filter(pk__in=[9, 10])
        searchterms = SearchTerm.objects.filter(pk__in=[1, 4])
        timeframe = TimeFrame.objects.get(pk=1)
        return ReservoirQuery(
            accounts=accounts,
            locations=locations,
            searchterms=searchterms,
            timeframe=timeframe
        )

    @skipUnless(TWITTER_TESTS_ENABLED, 'Twitter API tests disabled')
    def test_submit_query(self):
        """
        Tests the _submit_query method.
        """
        self._update_passport()
        query = self._create_test_query()

        with LogCapture('platforms.twitter.handlers') as log_capture:
            self.stream_handler.process_request(query)
            expected = 'Received 10 objects from Twitter and saved 10 of them'
            log_capture.check(
                ('platforms.twitter.handlers', 'INFO', expected),
            )
