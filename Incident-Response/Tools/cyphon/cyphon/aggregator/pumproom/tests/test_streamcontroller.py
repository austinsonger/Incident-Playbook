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
Tests the StreamController class.
"""

# standard library
from unittest import skipUnless
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture

# local
from aggregator.pipes.models import Pipe
from aggregator.pumproom.faucet import Faucet
from aggregator.pumproom.streamcontroller import StreamController
from aggregator.pumproom.tests.test_pump import BKGD_SRCH, create_pumps
from aggregator.streams.models import Stream
from cyphon.transaction import close_old_connections
from platforms.twitter.handlers import  PublicStreamsAPI
from platforms.twitter.tests.mixins import (
    TWITTER_TESTS_ENABLED,
    TwitterPassportMixin
)
from tests.fixture_manager import get_fixtures
from .test_faucet import FaucetTransactionTestCase

User = get_user_model()

# pylint: disable=W0212
# allow use of protected members in tests


class StreamControllerTestCase(TestCase):
    """
    Base class for testing the StreamController class.
    """

    fixtures = get_fixtures(['plumbers', 'gateways', 'funnels',
                             'pipes', 'streams', 'searchterms'])

    def setUp(self):
        create_pumps(self)
        pipe = Pipe.objects.get_by_natural_key('twitter', 'SearchAPI')
        user = User.objects.get(pk=1)
        self.faucet = Faucet(endpoint=pipe, user=user, task=BKGD_SRCH)
        self.faucet.process_request = Mock()  # avoid NotImplementedError
        self.faucet.stop = Mock()
        self.controller = StreamController(
            faucet=self.faucet,
            query=self.query
        )
        self.stream = self.controller.stream


class GetStreamTestCase(StreamControllerTestCase):
    """
    Tests the _get_stream method of the StreamController class.
    """

    def setUp(self):
        super(GetStreamTestCase, self).setUp()
        self.auth = self.controller.faucet.emissary.passport
        self.pipe = self.controller.faucet.endpoint

    def test_when_no_stream(self):
        """
        Tests the _get_stream method when a Stream does not already exist.
        """
        Stream.objects.all().delete()
        self.assertEqual(Stream.objects.all().count(), 0)
        stream = self.controller.stream
        self.assertEqual(Stream.objects.all().count(), 1)
        saved_stream = Stream.objects.get(pk=stream.pk)
        self.assertEqual(saved_stream.auth, self.auth)
        self.assertEqual(saved_stream.pipe, self.pipe)

    def test_when_stream_exists(self):
        """
        Tests the _get_stream method when a Stream already exists.
        """
        Stream.objects.all().delete()
        new_stream = Stream(pipe=self.pipe, auth=self.auth)
        new_stream.save()
        saved_stream = self.controller.stream
        actual = saved_stream.pk
        expected = new_stream.pk
        self.assertEqual(actual, expected)


class StartThreadTestCase(StreamControllerTestCase):
    """
    Tests the _start_stream method of the StreamController class.
    """

    def test_start_thread(self):
        """
        Tests the _start_stream method.
        """
        self.controller.faucet.start = Mock()
        self.controller.faucet.stop = Mock()
        self.controller.stream.save_as_closed = Mock()
        with patch('threading.Thread.start') as mock_start:
            thread = self.controller._start_stream()
            self.assertIs(thread.daemon, True)
            self.assertEqual(mock_start.call_count, 1)


class QueryIsRunningTestCase(StreamControllerTestCase):
    """
    Tests the _query_is_running method of the StreamController class.
    """

    def test_streaming_and_query_same(self):
        """
        Tests the _query_is_running method when the stream is running and the
        query is unchanged.
        """
        self.stream = self.controller.stream
        self.stream.active = True
        self.stream.save()
        self.stream.record.query = self.controller.query.to_dict()
        self.stream.record.save()
        actual = self.controller._query_is_running()
        self.assertIs(actual, True)

    def test_streaming_but_query_diff(self):
        """
        Tests the _query_is_running method when the stream is running but the
        query has changed.
        """
        self.stream.active = True
        self.stream.save()
        actual = self.controller._query_is_running()
        self.assertIs(actual, False)

    def test_no_stream_and_query_same(self):
        """
        Tests the _query_is_running method when the query is unchanged but
        the stream is no longer running.
        """
        self.stream.active = False
        self.stream.save()
        self.controller.query = self.controller.stream.record.query
        actual = self.controller._query_is_running()
        self.assertIs(actual, False)

    def test_no_stream_and_query_diff(self):
        """
        Tests the _query_is_running method when the stream is no longer running
        and the query has changed.
        """
        self.stream.active = False
        self.stream.save()
        self.controller.query = {'new': 'query'}
        actual = self.controller._query_is_running()
        self.assertIs(actual, False)


class ProcessQueryTestCase(StreamControllerTestCase):
    """
    Tests the process_query method of the StreamController class.
    """

    def test_when_query_runnning(self):
        """
        Tests the process_query method when the query is already running.
        """
        self.controller._query_is_running = Mock(return_value=True)
        self.controller._start_thread = Mock()
        actual = self.controller.process_query()
        self.assertIs(actual, False)
        self.controller._start_thread.assert_not_called()

    def test_when_query_not_runnning(self):
        """
        Tests the process_query method when the query is not already running.
        """
        self.controller._query_is_running = Mock(return_value=False)
        self.controller._start_stream = Mock()

        # avoid exception in thread when test db destroyed
        self.controller.stream.save = Mock()

        actual = self.controller.process_query()
        self.assertIs(actual, True)
        self.assertEqual(self.controller._start_stream.call_count, 1)


@skipUnless(TWITTER_TESTS_ENABLED, 'Twitter API tests disabled')
@close_old_connections
class StreamingQueryTestCase(FaucetTransactionTestCase, TwitterPassportMixin):
    """
    Tests the process_query method of the StreamController class.
    """

    @patch('platforms.twitter.handlers.tweepy.Stream.filter',
           side_effect=Exception())
    @patch('aggregator.pumproom.streamcontroller.Stream.save_as_closed')
    def test_broken_stream(self, mock_stream_close, mock_stream_run):
        """
        Tests that a stream is restarted if an exception is encountered.
        """
        self._update_passport()
        stream_faucet = PublicStreamsAPI(
            endpoint=self.twitter_stream,
            user=self.user,
            task=BKGD_SRCH
        )
        stream_controller = StreamController(
            faucet=stream_faucet,
            query=self.query
        )

        self.assertEqual(Stream.objects.count(), 0)

        with LogCapture() as log_capture:
            stream_controller.process_query()

            self.assertEqual(Stream.objects.count(), 1)
            mock_stream_close.assert_called_once()

            expected = 'An error occurred in the stream'
            log_capture.check(
                ('aggregator.pumproom.streamcontroller', 'ERROR', expected),
            )
