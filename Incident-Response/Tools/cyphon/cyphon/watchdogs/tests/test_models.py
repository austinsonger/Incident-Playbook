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
Tests the Watchdog and Triigger classes.
"""

# standard library
import logging
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import threading

# third party
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture

# local
from alerts.models import Alert
from cyphon.documents import DocumentObj
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find_by_id
from watchdogs.models import Watchdog, Trigger, Muzzle


DOC_ID = '666f6f2d6261722d71757578'

DATA = {
    '_meta': {
        'priority': 'HIGH',
    },
    '_raw_data': {
        'backend': 'mongodb',
        'distillery': 'test',
        'doc_id': DOC_ID
    },
    'content': {
        'subject': '[CRIT-111]'
    }
}


class WatchdogBaseTestCase(TestCase):
    """
    Tests the Watchdog class.
    """
    fixtures = get_fixtures(['watchdogs', 'distilleries'])

    doc_id = DOC_ID
    data = DATA
    doc_obj = DocumentObj(
        data=DATA,
        doc_id=DOC_ID,
        collection='mongodb.test_database.test_docs'
    )

    @classmethod
    def setUpClass(cls):
        super(WatchdogBaseTestCase, cls).setUpClass()
        logging.disable(logging.ERROR)

    @classmethod
    def tearDownClass(cls):
        logging.disable(logging.NOTSET)
        super(WatchdogBaseTestCase, cls).tearDownClass()

    def setUp(self):
        self.distillery = Distillery.objects.get_by_natural_key('mongodb.test_database.test_docs')
        self.email_wdog = Watchdog.objects.get_by_natural_key('inspect_emails')
        self.log_wdog = Watchdog.objects.get_by_natural_key('inspect_logs')


class WatchdogManagerTestCase(WatchdogBaseTestCase):
    """
    Tests the WatchdogManager class.
    """

    def test_find_relvnt_no_category(self):
        """
        Tests the find_relevant method for a Distillery that is not
        associated with any categories.
        """
        distillery = Distillery.objects.get_by_natural_key('mongodb.test_database.test_posts')
        relevant_watchdogs = Watchdog.objects.find_relevant(distillery)
        self.assertEqual(relevant_watchdogs.count(), 1)
        self.assertEqual(relevant_watchdogs[0].name, 'inspect_logs')
        self.assertEqual(relevant_watchdogs[0].categories.count(), 0)

    def test_find_rlvnt_one_category(self):
        """
        Tests the find_relevant method for a Distillery that is
        associated with one category.
        """
        distillery = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_docs')
        relevant_watchdogs = Watchdog.objects.find_relevant(distillery)
        self.assertEqual(relevant_watchdogs.count(), 2)
        self.assertEqual(relevant_watchdogs[0].name, 'inspect_emails')
        self.assertTrue(relevant_watchdogs[0].categories.count() > 0)

    def test_find_rlvnt_mult_category(self):
        """
        Tests the find_relevant method for a Distillery that is
        associated with multiple categories.
        """
        distillery = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_mail')
        relevant_watchdogs = Watchdog.objects.find_relevant(distillery)
        self.assertEqual(relevant_watchdogs.count(), 2)


class WatchdogTestCase(WatchdogBaseTestCase):
    """
    Tests the Watchdog class.
    """

    def test_str(self):
        """
        Tests the __str__ method for the Watchdog class.
        """
        self.assertEqual(str(self.email_wdog), 'inspect_emails')

    def test_inspect_true(self):
        """
        Tests the inspect method for a case that matches a ruleset.
        """
        actual = self.email_wdog.inspect(self.data)
        expected = 'HIGH'
        self.assertEqual(actual, expected)

    def test_inspect_false(self):
        """
        Tests the inspect method for a case that doesn't match a ruleset.
        """
        actual = self.log_wdog.inspect(self.data)
        expected = None
        self.assertEqual(actual, expected)

    def test_create_alert(self):
        """
        Tests the _create_alert method.
        """
        alert = self.email_wdog._create_alert(
            level='HIGH',
            doc_obj=self.doc_obj
        )
        self.assertEqual(alert.level, 'HIGH')
        self.assertEqual(alert.alarm_type.name, 'watchdog')
        self.assertEqual(alert.alarm_id, self.email_wdog.pk)
        self.assertEqual(alert.alarm, self.email_wdog)
        self.assertEqual(alert.distillery, self.distillery)
        self.assertEqual(alert.doc_id, self.doc_id)

    @patch_find_by_id
    def test_process_true(self):
        """
        Tests the process method for a case that matches a ruleset.
        """
        alert_count = Alert.objects.count()
        actual = self.email_wdog.process(self.doc_obj)
        self.assertEqual(actual, Alert.objects.get(doc_id=self.doc_id))
        self.assertEqual(actual.level, 'HIGH')
        self.assertEqual(actual.alarm_type.name, 'watchdog')
        self.assertEqual(actual.alarm_id, self.email_wdog.pk)
        self.assertEqual(actual.alarm, self.email_wdog)
        self.assertEqual(actual.distillery, self.distillery)
        self.assertEqual(Alert.objects.count(), alert_count + 1)

    @patch_find_by_id(DATA)
    def test_process_muzzled(self):
        """
        Tests the process method for a case that matches a ruleset but
        duplicates a previous Alert when the Watchdog is muzzled.
        """
        doc_obj = self.doc_obj
        alert_count = Alert.objects.count()
        alert = self.email_wdog.process(doc_obj)
        old_incidents = alert.incidents

        # check that a new Alert was created
        self.assertEqual(Alert.objects.count(), alert_count + 1)

        # try to create a duplicate Alert
        results = self.email_wdog.process(doc_obj)

        old_alert = Alert.objects.get(pk=alert.pk)

        # make sure no new Alert has been created
        self.assertEqual(Alert.objects.count(), alert_count + 1)

        # check that the previous Alert was incremented
        self.assertEqual(old_alert.incidents, old_incidents + 1)
        self.assertEqual(results, old_alert)

    @patch_find_by_id(DATA)
    def test_process_muzzled_disabled(self):
        """
        Tests the process method for a case that matches a ruleset but
        duplicates a previous Alert when the Watchdog is muzzled but the
        Muzzle is disabled.
        """
        self.email_wdog.muzzle.enabled = False

        alert_count = Alert.objects.count()
        alert = self.email_wdog.process(self.doc_obj)

        # check that a new Alert was created
        self.assertEqual(Alert.objects.count(), alert_count + 1)

        # try to create a duplicate Alert
        self.email_wdog.process(self.doc_obj)

        # make sure another Alert has been created
        self.assertEqual(Alert.objects.count(), alert_count + 2)

        # check that the previous Alert was not incremented
        alert = Alert.objects.get(pk=alert.pk)
        self.assertEqual(alert.incidents, 1)

    def test_process_not_muzzled(self):
        """
        Tests the process method for a case that matches a ruleset but
        duplicates a previous Alert when the Watchdog is not muzzled.
        """
        doc_obj = self.doc_obj
        data = {'message': 'CRIT-400'}
        doc_obj.data = data

        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=data):
            watchdog = Watchdog.objects.get(pk=2)

            alert_count = Alert.objects.count()
            alert = watchdog.process(doc_obj)

            # check that a new Alert was created
            self.assertEqual(Alert.objects.count(), alert_count + 1)

            # try to create a duplicate Alert
            watchdog.process(doc_obj)

            # make sure another Alert has been created
            self.assertEqual(Alert.objects.count(), alert_count + 2)

            # check that the previous Alert was not incremented
            alert = Alert.objects.get(pk=alert.pk)
            self.assertEqual(alert.incidents, 1)

    def test_disabled(self):
        """
        Tests the process method for a Watchdog that is disabled.
        """
        self.email_wdog.enabled = False
        result = self.email_wdog.process(self.doc_obj)
        self.assertEqual(result, None)

    def test_process_false(self):
        """
        Tests the process method for a case that doesn't match a ruleset.
        """
        actual = self.log_wdog.process(self.doc_obj)
        self.assertEqual(actual, None)
        alerts = Alert.objects.all()
        self.assertEqual(alerts.count(), 0)


class TriggerManagerTestCase(TestCase):
    """
    Tests the TriggerManager classes.
    """
    fixtures = get_fixtures(['watchdogs'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method of the WarehouseManager class.
        """
        trigger = Trigger.objects.get_by_natural_key('inspect_emails',
                                                     'high_priority_email')
        self.assertEqual(trigger.pk, 1)

    @staticmethod
    def test_get_by_natural_key_error():
        """
        Tests the get_by_natural_key method of the WarehouseManager class.
        """
        with LogCapture() as log_capture:
            Trigger.objects.get_by_natural_key('dummy_watchdog',
                                               'high_priority_email')
            expected_1 = 'Watchdog "dummy_watchdog" does not exist'
            expected_2 = ('Trigger dummy_watchdog:high_priority_email '
                          'does not exist')
            log_capture.check(
                ('watchdogs.models', 'ERROR', expected_1),
                ('watchdogs.models', 'ERROR', expected_2),
            )


class TriggerTestCase(TestCase):
    """
    Tests the Trigger class.
    """

    fixtures = get_fixtures(['watchdogs'])

    @classmethod
    def setUpClass(cls):
        super(TriggerTestCase, cls).setUpClass()
        cls.trigger = Trigger.objects.get(pk=1)

    def test_str(self):
        """
        Tests the __str__ method for a Trigger with a sieve.
        """
        self.assertEqual(str(self.trigger), 'high_priority_email <- HIGH (rank: 0)')

    def test_str_no_sieve(self):
        """
        Tests the __str__ method for a Trigger without a sieve.
        """
        self.assertEqual(str(Trigger()), 'Trigger object')

    def test_is_match(self):
        """
        Tests the is_match method.
        """
        with patch('watchdogs.models.Trigger.sieve') as mock_sieve:
            mock_sieve.is_match = Mock(return_value=True)
            data = {'title': 'test'}
            result = self.trigger.is_match(data)
            mock_sieve.is_match.assert_called_once_with(data)
            self.assertIs(result, True)


class MuzzleTestCase(TestCase):
    """
    Tests the Muzzle class.
    """

    fixtures = get_fixtures(['watchdogs', 'alerts'])

    mock_data = {
        'content': {
            'text': 'foo',
        },
        'user': 'bar',
    }

    @classmethod
    def setUpClass(cls):
        super(MuzzleTestCase, cls).setUpClass()
        cls.watchdog = Watchdog.objects.get(pk=1)

    def setUp(self):
        self.muzzle = Muzzle.objects.get(pk=1)

    def test_str(self):
        """
        Tests the __str__ method of a Muzzle.
        """
        self.assertEqual(str(self.muzzle), 'inspect_emails')

    def test_get_fields_wo_spaces(self):
        """
        Tests the _get_fields method when no spaces separate the fields.
        """
        actual = self.muzzle.get_fields()
        expected = ['content.subject', 'to']
        self.assertEqual(actual, expected)

    def test_get_fields_w_spaces(self):
        """
        Tests the _get_fields method when spaces separate the fields.
        """
        self.muzzle.matching_fields = ' message, source_ip '
        actual = self.muzzle.get_fields()
        expected = ['message', 'source_ip']
        self.assertEqual(actual, expected)

    def test_get_fields_single_field(self):
        """
        Tests the _get_fields method for a single field.
        """
        self.muzzle.matching_fields = ' message, '
        actual = self.muzzle.get_fields()
        expected = ['message']
        self.assertEqual(actual, expected)


class WatchdogTransactionTestCase(TransactionTestCase):
    """
    Tests the Watchdog class.
    """
    fixtures = get_fixtures(['watchdogs', 'distilleries'])

    doc_id = DOC_ID
    data = DATA
    doc_obj = DocumentObj(
        data=DATA,
        doc_id=DOC_ID,
        collection='mongodb.test_database.test_docs'
    )

    def setUp(self):
        self.distillery = Distillery.objects.get_by_natural_key('mongodb.test_database.test_docs')
        self.email_wdog = Watchdog.objects.get_by_natural_key('inspect_emails')

    @patch_find_by_id
    def test_multiprocess_muzzled(self):
        """
        Tests muzzling when multiple duplicate Alerts are being processed
        concurrently.
        """
        with patch('alerts.models.Alert._format_title',
                   return_value=self.data['content']['subject']):
            incident_num = 20

            alert_count = Alert.objects.count()

            args = [self.doc_obj]

            alert = self.email_wdog.process(*args)

            # check that a new Alert was created
            self.assertEqual(Alert.objects.count(), alert_count + 1)

            # NOTE: we can't use multiprocessing with Mocks,
            # so we have to settle for using threading to mimic concurrency

            threads = []
            for dummy_index in range(incident_num):
                new_thread = threading.Thread(target=self.email_wdog.process,
                                              args=args)
                threads.append(new_thread)
                new_thread.start()

            for thread in threads:
                thread.join()

            # NOTE: we can't check Alert counts because saved Alerts
            # won't be committed in the TransactionTestCase

            # but we can check that the previous Alert was incremented
            alert = Alert.objects.get(pk=alert.pk)
            self.assertEqual(alert.incidents, incident_num + 1)
