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
Tests signals in the Watchdog app.
"""

# standard library
import logging
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TransactionTestCase

# local
from alerts.models import Alert
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find_by_id
from watchdogs.models import Watchdog
from watchdogs.tests.test_models import DATA


class SignalRecieverTestCase(TransactionTestCase):
    """
    Tests the reciever of the document_saved signal.
    """
    fixtures = get_fixtures(['watchdogs', 'distilleries'])

    data = DATA

    mock_doc_id = '666f6f2d6261722d71757578'

    @classmethod
    def setUpClass(cls):
        super(SignalRecieverTestCase, cls).setUpClass()
        logging.disable(logging.ERROR)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super(SignalRecieverTestCase, cls).tearDownClass()

    @patch_find_by_id(data)
    def test_watchdogs_no_relevant(self):
        """
        Tests that no alert is created when a Distillery saves a document
        and no relevant Watchdogs are enabled.
        """

        # distillery with no categories
        distillery = Distillery.objects.get_by_natural_key('mongodb.test_database.test_docs')
        distillery.collection.insert = Mock(return_value=self.mock_doc_id)

        doc_id = distillery._save_and_send_signal(self.data)

        alerts = Alert.objects.all()
        self.assertEqual(alerts.count(), 0)
        self.assertEqual(doc_id, self.mock_doc_id)

    @patch_find_by_id(data)
    def test_watchdogs_no_enabled(self):
        """
        Tests that an alert is created when a Distillery saves a document
        and a relevant Watchdogs exists but is not enabled.
        """
        watchdog = Watchdog.objects.get_by_natural_key('inspect_emails')
        watchdog.enabled = False
        watchdog.save()

        # distillery with categories
        distillery = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_docs')
        distillery.collection.insert = Mock(return_value=self.mock_doc_id)
        doc_id = distillery._save_and_send_signal(self.data)

        alerts = Alert.objects.all()
        self.assertEqual(alerts.count(), 0)
        self.assertEqual(doc_id, self.mock_doc_id)

    @patch_find_by_id(data)
    def test_watchdogs_create_alert(self):
        """
        Tests that an alert is created when a Distillery saves a document
        and a relevant Watchdogs is enabled.
        """

        # distillery with categories
        distillery = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_docs')
        distillery.collection.insert = Mock(return_value=self.mock_doc_id)
        doc_id = distillery._save_and_send_signal(self.data)
        watchdog = Watchdog.objects.get_by_natural_key('inspect_emails')

        alerts = Alert.objects.all()
        self.assertEqual(alerts.count(), 1)

        self.assertEqual(alerts[0].alarm_type.name, 'watchdog')
        self.assertEqual(alerts[0].alarm_id, watchdog.pk)
        self.assertEqual(alerts[0].alarm, watchdog)
        self.assertEqual(alerts[0].level, 'HIGH')
        self.assertEqual(doc_id, self.mock_doc_id)
