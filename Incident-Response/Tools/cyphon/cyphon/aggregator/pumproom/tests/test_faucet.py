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
Tests the Faucet class.
"""

# standard library
from unittest import skip

try:
    from unittest.mock import Mock, call, patch
except ImportError:
    from mock import Mock, call, patch

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture

# local
from aggregator.invoices.models import Invoice
from aggregator.pipes.models import Pipe
from aggregator.pumproom.faucet import Faucet
from aggregator.streams.models import Stream
from aggregator.pumproom.streamcontroller import StreamController
from ambassador.stamps.models import Stamp
from query.reservoirqueries.models import ReservoirQuery
from sifter.datasifter.datachutes.models import DataChute
from target.searchterms.models import SearchTerm
from tests.fixture_manager import get_fixtures

User = get_user_model()

_FIXTURES = get_fixtures(['users', 'datachutes', 'plumbers', 'stamps',
                          'searchterms'])

# pylint: disable=W0212
# allow use of protected members in tests


def _setup_objects(obj):
    """

    """
    obj.user = User.objects.get(pk=1)
    obj.twitter_search = Pipe.objects.get(pk=1)
    obj.twitter_stream = Pipe.objects.get(pk=2)
    obj.instagram = Pipe.objects.get(pk=4)

    obj.search_faucet = Faucet(
        endpoint=obj.twitter_search,
        user=obj.user,
        task='ADHOC_SRCH'
    )

    obj.stream_faucet = Faucet(
        endpoint=obj.twitter_stream,
        user=obj.user,
        task='BKGD_SRCH'
    )

    obj.other_faucet = Faucet(
        endpoint=obj.instagram,
        user=obj.user,
        task='OTHER_TASK'
    )
    obj.stamp = Stamp.objects.get(pk=1)
    term = SearchTerm.objects.get(pk=1)
    obj.query = ReservoirQuery(searchterms=[term])


class FaucetTestCase(TestCase):
    """
    Base class for testing the Pump class.
    """
    fixtures = _FIXTURES

    def setUp(self):
        _setup_objects(self)


class FaucetTransactionTestCase(TransactionTestCase):
    """
    Base class for testing the Pump class.
    """
    fixtures = _FIXTURES

    def setUp(self):
        _setup_objects(self)


class IsObsoleteTestCase(FaucetTransactionTestCase):
    """
    Tests the is_obsolete method.
    """

    def setUp(self):
        super(IsObsoleteTestCase, self).setUp()
        record = self.stream_faucet.create_record(self.stamp, self.query)
        self.stream_faucet.record = record

    def test_is_latest(self):
        """
        Tests the is_obsolete method when the faucet is associated with
        the latest successful call.
        """
        self.assertFalse(self.stream_faucet.is_obsolete())

    def test_is_not_latest(self):
        """
        Tests the is_obsolete method when the faucet is not associated
        with the latest successful call.
        """
        stamp = Stamp.objects.get(pk=2)
        stamp.passport = self.stamp.passport
        stamp.save()
        self.assertTrue(self.stream_faucet.is_obsolete())

        # make sure null value for status code still qualifies
        stamp.status_code = None
        stamp.save()
        self.assertTrue(self.stream_faucet.is_obsolete())


class StashDataTestCase(FaucetTestCase):
    """
    Tests the stash_data method.
    """

    @skip
    def test_stash_data(self):
        """
        Tests the stash_data method.
        """
        pass


class SendToChutesTestCase(FaucetTestCase):
    """
    Tests the send_to_chutes method.
    """

    def test_send_to_chutes(self):
        """
        Tests the send_to_chutes method.
        """
        data = [Mock()]
        with patch('sifter.datasifter.datachutes.models.DataChute.bulk_process') \
                as mock_process:
            search_count = DataChute.objects.find_enabled()\
                                    .filter(endpoint=self.search_faucet.endpoint).count()
            stream_count = DataChute.objects.find_enabled()\
                                    .filter(endpoint=self.stream_faucet.endpoint).count()
            self.search_faucet.send_to_chutes(data)
            self.assertEqual(mock_process.call_count, search_count)

            self.stream_faucet.send_to_chutes(data)
            self.assertEqual(mock_process.call_count, stream_count)
            self.assertEqual(mock_process.call_args, call(data=data))


class CreateRecordTestCase(FaucetTestCase):
    """
    Tests the create_record method.
    """

    def test_create_record(self):
        """
        Tests the create_record method.
        """
        self.assertTrue(self.search_faucet.record is None)
        record = self.search_faucet.create_record(self.stamp, self.query)
        self.assertTrue(isinstance(record, Invoice))
        self.assertTrue(hasattr(record, 'pk'))
        self.assertEqual(record.stamp, self.stamp)
        self.assertEqual(record.query, self.query.to_dict())
        self.assertEqual(record.task, self.search_faucet.task)


class ProcessRequestTestCase(FaucetTestCase):
    """
    Tests the process_request method.
    """

    def test_process_request(self):
        """
        Tests the process_request method.
        """
        with self.assertRaises(NotImplementedError):
            self.search_faucet.process_request(self.query)


class ProcessResultsTestCase(FaucetTransactionTestCase):
    """
    Tests the process_results method.
    """

    def test_adhoc_search(self):
        """
        Tests the process_results method for an ad hoc search.
        """
        mock_data = Mock()
        self.search_faucet.cargo = Mock()
        self.search_faucet.cargo.data = mock_data
        self.search_faucet.stash_data = Mock()
        self.search_faucet.process_results()
        self.search_faucet.stash_data.assert_called_once_with(mock_data)

    def test_bkgd_search(self):
        """
        Tests the process_results method for a background search.
        """
        mock_data = Mock()
        self.stream_faucet.cargo = Mock()
        self.stream_faucet.cargo.data = mock_data
        self.stream_faucet.send_to_chutes = Mock()
        self.stream_faucet.process_results()
        self.stream_faucet.send_to_chutes.assert_called_once_with(mock_data)

    def test_other_search(self):
        """
        Tests the process_results method for unrecognized search type.
        """
        mock_data = Mock()
        self.other_faucet.cargo = Mock()
        self.other_faucet.cargo.data = mock_data
        results = self.other_faucet.process_results()
        self.assertEqual(results, mock_data)

    def test_no_cargo(self):
        """
        Tests the process_results method when no cargo has been stored.
        """
        with LogCapture() as log_capture:
            self.search_faucet.process_results()
            msg = ('There are no results to process. '
                   'Call the start() method to get data from the API.')
            log_capture.check(
                ('aggregator.pumproom.faucet', 'ERROR', msg),
            )
