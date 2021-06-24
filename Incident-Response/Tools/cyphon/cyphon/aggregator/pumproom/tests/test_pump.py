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
Tests the Pump class.
"""

# standard library
try:
    from unittest.mock import Mock, call, patch
except ImportError:
    from mock import Mock, call, patch

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture
import six

# local
from aggregator.pumproom.exceptions import (
    PipeDoesNotExist,
    SpecsheetDoesNotExist,
)
from aggregator.pipes.models import Pipe
from aggregator.plumbers.models import Plumber
from aggregator.pumproom.pump import Pump
from aggregator.reservoirs.models import Reservoir
from ambassador.exceptions import EmissaryDoesNotExist
from cyphon.transaction import close_old_connections
from query.reservoirqueries.models import ReservoirQuery
from target.searchterms.models import SearchTerm
from tests.fixture_manager import get_fixtures

User = get_user_model()

# pylint: disable=W0212
# allow use of protected members in tests

BKGD_SRCH = 'BKGD_SRCH'
ADHOC_SRCH = 'ADHOC_SRCH'
FAKE_TASK = 'FAKE_TASK'


def create_pumps(obj):
    """

    """
    term = SearchTerm.objects.get(pk=1)
    obj.query = ReservoirQuery(searchterms=[term])
    reservoir = Reservoir.objects.get(name='twitter')
    obj.stream_pump = Pump(reservoir=reservoir, task=BKGD_SRCH)
    obj.nonstream_pump = Pump(reservoir=reservoir, task=ADHOC_SRCH)


class PumpBaseTestCase(TestCase):
    """
    Base class for testing the Pump class.
    """
    fixtures = get_fixtures(['plumbers', 'gateways', 'funnels',
                             'pipes', 'streams', 'searchterms'])

    def setUp(self):
        self.subquery1 = Mock()
        self.subquery2 = Mock()
        self.query_list = [self.subquery1, self.subquery2]
        create_pumps(self)


class PumpTestCase(PumpBaseTestCase):
    """
    Tests basic methods of the Pump class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the Pump class.
        """
        self.assertEqual(str(self.nonstream_pump), 'Twitter SearchAPI')
        self.assertEqual(str(self.stream_pump), 'Twitter PublicStreamsAPI')

    def test_get_time_requirements(self):
        """
        Tests the get_time_requirements method.
        """
        with patch('aggregator.pumproom.pump.Pump._plumber') as mock_plumber:
            mock_plumber.calculate_query_time_in_minutes = Mock(return_value=60)
            self.nonstream_pump.get_time_requirements(query_cnt=5)
            mock_plumber.calculate_query_time_in_minutes.assert_called_once_with(5)


class FindPipeTestCase(PumpBaseTestCase):
    """
    Tests the _pipe property.
    """

    def test_with_existing_pipe(self):
        """
        Tests the _pipe property for a Pipe that exists.
        """
        actual = self.stream_pump._pipe
        expected = Pipe.objects.get_by_natural_key('twitter',
                                                   'PublicStreamsAPI')
        self.assertEqual(actual, expected)

    def test_with_missing_pipe(self):
        """
        Tests the _pipe property for a Pipe doesn't exist.
        """
        reservoir = Reservoir.objects.get(name='twitter')
        pump = Pump(reservoir=reservoir, task=FAKE_TASK)
        msg = 'The Reservoir "twitter" has no Pipe for the Task "FAKE_TASK"'
        with six.assertRaisesRegex(self, PipeDoesNotExist, msg):
            pump._pipe


class FindSpecsheetTestCase(PumpBaseTestCase):
    """
    Tests the _specsheet property.
    """

    def test_with_missing_specsheet(self):
        """
        Tests the _pipe property for a Pipe doesn't exist.
        """
        reservoir = Reservoir.objects.get(name='facebook')
        pump = Pump(reservoir=reservoir, task=ADHOC_SRCH)
        msg = 'The Pipe "Facebook GraphAPI" has no Specsheet'
        with six.assertRaisesRegex(self, SpecsheetDoesNotExist, msg):
            pump._specsheet


class FindPlumberTestCase(PumpBaseTestCase):
    """
    Tests the _plumber property.
    """

    def test_with_multiple_plumbers(self):
        """
        Tests the _plumber property when multiple Plumbers exist.
        """
        plumbers = Plumber.objects.filter(pk__in=[1, 3])
        with patch('ambassador.emissaries.models.EmissaryManager.find_any',
                   return_value=plumbers):
            actual = self.stream_pump._plumber
            expected = Plumber.objects.get(pk=1)
            self.assertEqual(actual, expected)

    def test_w_missing_plumber(self):
        """
        Tests the _plumber property when the Plumber is missing.
        """
        plumbers = Plumber.objects.filter(name='fake_plumber')
        self.stream_pump.user = User.objects.get(pk=1)
        with patch('ambassador.emissaries.models.EmissaryManager.find_any',
                   return_value=plumbers):
            msg = 'No Plumber exists to handle the request to Twitter '\
                  'PublicStreamsAPI by testuser1@testdomain.com'
            with six.assertRaisesRegex(self, EmissaryDoesNotExist, msg):
                self.stream_pump._plumber

    def test_w_missing_plumber_and_user(self):
        """
        Tests the _plumber property when the Plumber is missing and the
        AppUser is not defined.
        """
        plumbers = Plumber.objects.filter(name='fake_plumber')
        with patch('ambassador.emissaries.models.EmissaryManager.find_any',
                   return_value=plumbers):
            msg = 'No Plumber exists to handle the request to Twitter '\
                  'PublicStreamsAPI by an anonymous user'
            with six.assertRaisesRegex(self, EmissaryDoesNotExist, msg):
                self.stream_pump._plumber


class FactorQueryTestCase(PumpBaseTestCase):
    """
    Tests the _factor_query method.
    """

    def test_factor_query(self):
        """
        Tests the _factor_query method.
        """
        mock_engineer = Mock()
        mock_engineer.factor_query = Mock(return_value=self.query_list)

        with patch('aggregator.pumproom.pump.Engineer',
                   return_value=mock_engineer) as engineer:
            queries = self.nonstream_pump._factor_query(self.query)
            engineer.assert_called_once_with(
                query=self.query, specs=self.nonstream_pump._specsheet)
            self.assertEqual(queries, self.query_list)


class CreateRequestHandlerTestCase(PumpBaseTestCase):
    """
    Tests the _create_request_handler method.
    """

    def test_faucet(self):
        """
        Tests the _faucet property.
        """
        mock_faucet = Mock()
        self.stream_pump._pipe.create_request_handler = Mock(return_value=mock_faucet)
        faucet = self.stream_pump._faucet
        self.stream_pump._pipe.create_request_handler.assert_called_once_with(
            user=self.stream_pump.user,
            params={'task': 'BKGD_SRCH'})
        self.assertEqual(faucet, mock_faucet)


class CreateStreamControllerTestCase(PumpBaseTestCase):
    """
    Tests the _create_stream_controller method.
    """

    def test_create_stream_controller(self):
        """
        Tests the _create_stream_controller method.
        """
        with patch('aggregator.pumproom.pump.StreamController',
                   return_value=True) as stream_manager:
            result = self.stream_pump._create_stream_controller(self.query)
            stream_manager.assert_called_once_with(
                faucet=self.stream_pump._faucet, query=self.query)
            self.assertIs(result, True)


class ProcessStreamingQueryTestCase(PumpBaseTestCase):
    """
    Tests the _process_streaming_query method.
    """

    def test_process_streaming_query(self):
        """
        Tests the _process_streaming_query method.
        """
        mock_controller = Mock()
        mock_result = Mock()
        mock_controller.process_query = Mock(return_value=mock_result)
        self.stream_pump._create_stream_controller = Mock(return_value=mock_controller)
        result = self.stream_pump._process_streaming_query(self.query)
        self.assertEqual(mock_controller.process_query.call_count, 1)
        self.assertIs(result, mock_result)


class ProcessNonstreamingQueryTestCase(PumpBaseTestCase):
    """
    Tests the _process_nonstreaming_query method.
    """

    def test_process_nonstreaming_query(self):
        """
        Tests the _process_nonstreaming_query method.
        """
        mock_faucet = Mock()
        mock_result = Mock()
        mock_faucet.run = Mock()
        mock_faucet.process_results = Mock(return_value=mock_result)
        self.nonstream_pump._faucet = mock_faucet
        result = self.nonstream_pump._process_nonstreaming_query(self.query)
        mock_faucet.run.assert_called_once_with(self.query)
        self.assertEqual(mock_faucet.process_results.call_count, 1)
        self.assertIs(result, mock_result)


class ProcessNonstreamingQueriesTestCase(PumpBaseTestCase):
    """
    Tests the _process_nonstreaming_queries method.
    """

    def test_multipart_query_list(self):
        """
        Tests the _process_nonstreaming_queries method for a multi-part query
        when each query returns a list.
        """
        mock_faucet = Mock()
        mock_result1 = Mock()
        mock_result2 = Mock()
        self.nonstream_pump._faucet = mock_faucet
        self.nonstream_pump._process_nonstreaming_query = Mock(
            side_effect=[[mock_result1], [mock_result2]])
        result = self.nonstream_pump._process_nonstreaming_queries(self.query_list)

        # check that each element of the query list was processed
        self.nonstream_pump._process_nonstreaming_query.has_calls(
            [call(mock_faucet, self.query_list[0]),
             call(mock_faucet, self.query_list[1])])

        # check that combined results were returned
        self.assertEqual(result, [mock_result1, mock_result2])

    def test_multipart_query_nonlist(self):
        """
        Tests the _process_nonstreaming_queries method for a multi-part query
        when each query returns a nonlist.
        """
        mock_faucet = Mock()
        mock_result1 = Mock()
        mock_result2 = Mock()
        self.nonstream_pump._faucet = mock_faucet
        self.nonstream_pump._process_nonstreaming_query = Mock(
            side_effect=[mock_result1, mock_result2])
        result = self.nonstream_pump._process_nonstreaming_queries(self.query_list)

        # check that each element of the query list was processed
        self.nonstream_pump._process_nonstreaming_query.has_calls(
            [call(mock_faucet, self.query_list[0]),
             call(mock_faucet, self.query_list[1])])

        # check that combined results were returned
        self.assertEqual(result, [mock_result1, mock_result2])


class StartPumpBaseTestCase(TransactionTestCase):
    """
    Tests the start method.
    """
    fixtures = get_fixtures(['plumbers', 'gateways', 'funnels',
                             'pipes', 'streams', 'searchterms'])

    def setUp(self):
        term = SearchTerm.objects.get(pk=1)
        self.query = ReservoirQuery(searchterms=[term])
        self.subquery1 = Mock()
        self.subquery2 = Mock()
        self.query_list = [self.subquery1, self.subquery2]
        create_pumps(self)

    @close_old_connections
    def test_normal_streaming_query(self):
        """
        Tests the start method for a Pump with a streaming Pipe and a query that
        doesn't exceed the Pipe's specs.
        """
        with LogCapture() as log_capture:
            self.stream_pump._factor_query = Mock(return_value=[self.subquery1])
            self.stream_pump._process_streaming_query = Mock()
            self.stream_pump.start(self.subquery1)

            # check that _factor_query() was called with the value that was
            # passed to start()
            self.stream_pump._factor_query.assert_called_once_with(self.subquery1)

            # check that _process_nonstreaming_queries() was called with the
            # first element of the query list returned by _factor_query()
            self.stream_pump._process_streaming_query.assert_called_once_with(
                self.subquery1)

            log_capture.check()

    @close_old_connections
    def test_large_streaming_query(self):
        """
        Tests the start method for a Pump with a streaming Pipe and a query that
        exceeds the Pipe's specs.
        """
        with LogCapture() as log_capture:
            self.stream_pump._factor_query = Mock(return_value=self.query_list)
            self.stream_pump._process_streaming_query = Mock()
            self.stream_pump.start(self.query)

            # check that _factor_query() was called with the value that was
            # passed to start()
            self.stream_pump._factor_query.assert_called_once_with(self.query)

            # check that _process_nonstreaming_queries() was called with the
            # first element of the query list returned by _factor_query()
            self.stream_pump._process_streaming_query.assert_called_once_with(
                self.query_list[0])

            # check that a warning was generated
            msg = 'Query was too large for Pipe "Twitter PublicStreamsAPI." ' \
                  + 'A smaller version of the query was submitted.'
            log_capture.check(
                ('aggregator.pumproom.pump', 'WARNING', msg),
            )

    @close_old_connections
    def test_nonstreaming_query(self):
        """
        Tests the start method for a Pump with a non-streaming Pipe and a query
        that exceeds the Pipe's specs.
        """
        self.nonstream_pump._factor_query = Mock(return_value=self.query_list)
        self.nonstream_pump._process_nonstreaming_queries = Mock()
        self.nonstream_pump.start(self.query)

        # check that _factor_query() was called with the value passed to start()
        self.nonstream_pump._factor_query.assert_called_once_with(self.query)

        # check that _process_nonstreaming_queries() was called with the query
        # list returned by _factor_query()
        self.nonstream_pump._process_nonstreaming_queries.assert_called_once_with(
            self.query_list)
