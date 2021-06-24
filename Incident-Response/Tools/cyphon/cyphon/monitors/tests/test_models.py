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
Tests the Monitor class.
"""

# standard library
from datetime import datetime
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import logging

# third party
from django.test import TestCase

# local
from alerts.models import Alert
from distilleries.models import Distillery
from monitors.models import Monitor
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find_by_id

EARLY = datetime.strptime('2016-01-01 09:04:00 +0000', '%Y-%m-%d %H:%M:%S %z')
ON_TIME = datetime.strptime('2016-01-01 09:05:00 +0000', '%Y-%m-%d %H:%M:%S %z')
LATE = datetime.strptime('2016-01-01 09:06:00 +0000', '%Y-%m-%d %H:%M:%S %z')
VERY_LATE = datetime.strptime('2016-01-02 09:05:00 +0000', '%Y-%m-%d %H:%M:%S %z')


class MonitorManagerTestCase(TestCase):
    """
    Tests clean method of the MonitorManager class.
    """

    fixtures = get_fixtures(['monitors'])

    def test_find_enabled(self):
        """
        Tests the find_enabled method of the MonitorManager class.
        """
        assert Monitor.objects.filter(enabled=False).count() > 0

        enabled_monitors = Monitor.objects.find_enabled()

        for monitor in enabled_monitors:
            self.assertEqual(monitor.enabled, True)

        self.assertEqual(enabled_monitors.count(),
                         Monitor.objects.filter(enabled=True).count())

    def test_find_relevant(self):
        """
        Tests the find_relevant method of the MonitorManager class.
        """
        distillery = Distillery.objects.get(pk=1)
        relevant_monitors = Monitor.objects.find_relevant(distillery)
        self.assertEqual(relevant_monitors.count(), 3)


class MonitorTestCase(TestCase):
    """
    Tests clean method of the Monitor class.
    """
    fixtures = get_fixtures(['monitors'])

    def setUp(self):
        self.monitor_grn = Monitor.objects.get(pk=1)
        self.monitor_grn_disabled = Monitor.objects.get(pk=2)
        self.monitor_red = Monitor.objects.get(pk=3)
        self.monitor_red_disabled = Monitor.objects.get(pk=4)
        self.monitor_red_repeating = Monitor.objects.get(pk=5)
        logging.disable(logging.WARNING)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_str(self):
        """
        Tests the __str__ method for the Monitor class.
        """
        self.assertEqual(str(self.monitor_grn), 'health_alerts')

    def test_save_new(self):
        """
        Tests that the status is to GREEN on a new Monitor.
        """
        monitor = Monitor.objects.create(
            name='new monitor',
            time_interval=1,
            time_unit='d',
            alerts_enabled=True,
            repeating_alerts=True,
            alert_level='HIGH'
        )
        self.assertEqual(monitor.status, 'GREEN')

    @patch('monitors.models.timezone.now', return_value=EARLY)
    def test_save_overdue(self, mock_now):
        """
        Tests the save method for a green Monitor when the interval
        is shortened.
        """
        self.monitor_grn.time_unit = 's'
        self.monitor_grn.save()
        monitor_grn = Monitor.objects.get(pk=1)
        self.assertEqual(monitor_grn.status, 'RED')

    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_save_not_overdue(self, mock_now):
        """
        Tests the save method for a red Monitor when the interval
        is lengthened.
        """
        self.monitor_red.time_unit = 'd'
        self.monitor_red.save()
        monitor_red = Monitor.objects.get(pk=3)
        self.assertEqual(monitor_red.status, 'GREEN')

    def test_get_interval_in_seconds(self):
        """
        Tests the _get_interval_in_seconds method of the Monitor class
        when there is a last_healthy value.
        """
        self.assertEqual(self.monitor_grn._get_interval_in_seconds(), 300)

    @patch('monitors.models.timezone.now', return_value=VERY_LATE)
    def test_get_inactive_no_lasthealth(self, mock_now):
        """
        Tests the _get_inactive_seconds method of the Monitor class when
        there is no last_healthy value.
        """
        monitor = self.monitor_red_repeating
        assert monitor.last_healthy == None
        self.assertEqual(monitor._get_inactive_seconds(), 86700)

    @patch('monitors.models.timezone.now', return_value=VERY_LATE)
    def test_get_inactive_seconds(self, mock_now):
        """
        Tests the _get_inactive_seconds method of the Monitor class.
        """
        self.assertEqual(self.monitor_grn._get_inactive_seconds(), 86700)

    @patch('monitors.models.timezone.now', return_value=EARLY)
    def test_is_overdue_for_not_late(self, mock_now):
        """
        Tests the _is_overdue method of the Monitor class when the
        difference between the last_healthy time and the current time
        is less than the monitoring interval.
        """
        self.assertEqual(self.monitor_grn._is_overdue(), False)

    @patch('monitors.models.timezone.now', return_value=ON_TIME)
    def test_is_overdue_for_on_time(self, mock_now):
        """
        Tests the _is_overdue method of the Monitor class when the
        difference between the last_healthy time and the current time
        is equal to the monitoring interval.
        """
        self.assertEqual(self.monitor_grn._is_overdue(), False)

    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_is_overdue_for_late(self, mock_now):
        """
        Tests the _is_overdue method of the Monitor class when the
        difference between the last_healthy time and the current time
        is greater than the monitoring interval.
        """
        self.assertEqual(self.monitor_grn._is_overdue(), True)

    @patch_find_by_id()
    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_create_alert(self, mock_now):
        """
        Tests the _create_alert method of the Monitor class.
        """
        alert = self.monitor_red._create_alert()
        title = 'Health monitor "unhealthy_alerts" has seen no activity for over 6 m.'
        self.assertEqual(alert.title, title)
        self.assertEqual(alert.alarm, self.monitor_red)
        self.assertEqual(alert.level, self.monitor_red.alert_level)
        self.assertEqual(alert.distillery, self.monitor_red.last_active_distillery)
        self.assertEqual(alert.doc_id, self.monitor_red.last_saved_doc)

    @patch('monitors.models.timezone.now', return_value=ON_TIME)
    def test_update_status(self, mock_now):
        """
        Tests the update_status method of the Monitor class.
        """
        monitor = self.monitor_red
        assert monitor.last_healthy != ON_TIME
        assert monitor.last_active_distillery.pk != 1
        assert monitor.last_saved_doc != '11'
        assert monitor.status != 'GREEN'

        docs = [
            {'count': 1, 'results': [{'_id': 1, 'created_date': LATE}]},
            {'count': 1, 'results': [{'_id': 2, 'created_date': VERY_LATE}]},
        ]
        with patch('monitors.models.Distillery.find', side_effect=docs) \
                as mock_find:
            monitor.update_status()
            mock_find.call_count = 2

            # get a fresh instance from the database
            updated_monitor = Monitor.objects.get(pk=monitor.pk)
            self.assertEqual(updated_monitor.last_healthy, VERY_LATE)
            self.assertEqual(updated_monitor.last_active_distillery.pk, 1)
            self.assertEqual(updated_monitor.last_saved_doc, '2')
            self.assertEqual(updated_monitor.status, 'GREEN')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=EARLY)
    def test_not_overdue_red(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is not overdue, the current status is not 'RED',
        and alerts are enabled.
        """
        monitor = self.monitor_red
        assert monitor.status == 'RED'
        assert Alert.objects.count() == 0

        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, EARLY)
        self.assertEqual(updated_monitor.status, 'GREEN')
        self.assertEqual(Alert.objects.count(), 0)
        self.assertEqual(result, 'GREEN')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=EARLY)
    def test_not_overdue_not_red(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is not overdue, the current status is not 'RED',
        and alerts are enabled.
        """
        monitor = self.monitor_grn
        assert monitor.status == 'GREEN'
        assert Alert.objects.count() == 0

        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, EARLY)
        self.assertEqual(updated_monitor.status, 'GREEN')
        self.assertEqual(Alert.objects.count(), 0)
        self.assertEqual(result, 'GREEN')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_overdue_red_enabled(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is overdue, the current status is 'RED', alerts
        are enabled, but repeating alerts are disabled.
        """
        monitor = self.monitor_red
        assert self.monitor_red.status == 'RED'
        assert Alert.objects.count() == 0

        mock_teaser.get = Mock(return_value=None)
        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, LATE)
        self.assertEqual(updated_monitor.status, 'RED')
        self.assertEqual(Alert.objects.count(), 0)
        self.assertEqual(result, 'RED')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_overdue_red_disabled(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is overdue, the current status is 'RED', repeating
        alerts are enabled, but alerts are disabled.
        """
        monitor = self.monitor_red_disabled
        assert monitor.status == 'RED'
        assert Alert.objects.count() == 0

        mock_teaser.get = Mock(return_value=None)
        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, LATE)
        self.assertEqual(updated_monitor.status, 'RED')
        self.assertEqual(Alert.objects.count(), 0)
        self.assertEqual(result, 'RED')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=VERY_LATE)
    def test_overdue_red_repeating(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is overdue, the current status is 'RED', alerts
        are enabled, and repeating alerts are enabled.
        """
        monitor = self.monitor_red_repeating
        assert monitor.status == 'RED'
        assert monitor.alerts_enabled == True
        assert monitor.repeating_alerts == True
        assert Alert.objects.count() == 0

        mock_teaser.get = Mock(return_value=None)
        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, VERY_LATE)
        self.assertEqual(updated_monitor.status, 'RED')
        self.assertEqual(Alert.objects.count(), 1)
        self.assertEqual(result, 'RED')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=VERY_LATE)
    def test_overdue_not_red_enabled(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is overdue, the current status is not 'RED', and
        alerts are enabled.
        """
        monitor = self.monitor_grn
        assert monitor.status == 'GREEN'
        assert Alert.objects.count() == 0

        mock_teaser.get = Mock(return_value=None)
        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, VERY_LATE)
        self.assertEqual(updated_monitor.status, 'RED')
        self.assertEqual(Alert.objects.count(), 1)
        alert = Alert.objects.all()[0]
        title = 'Health monitor "health_alerts" has seen no activity for over 1 d.'
        self.assertEqual(alert.title, title)
        self.assertEqual(alert.alarm, monitor)
        self.assertEqual(alert.level, monitor.alert_level)
        self.assertEqual(alert.distillery, monitor.last_active_distillery)
        self.assertEqual(alert.doc_id, monitor.last_saved_doc)
        self.assertEqual(alert.created_date, monitor.last_alert_date)
        self.assertEqual(alert.pk, monitor.last_alert_id)
        self.assertEqual(result, 'RED')

    @patch_find_by_id()
    @patch('alerts.models.Alert.teaser')
    @patch('monitors.models.timezone.now', return_value=LATE)
    def test_overdue_not_red_disabled(self, mock_now, mock_teaser):
        """
        Tests the update_status method of the Monitor class when the
        health check is overdue, the current status is not 'RED', and
        alerts are disabled.
        """
        monitor = self.monitor_grn_disabled
        assert monitor.status == 'GREEN'
        assert Alert.objects.count() == 0

        mock_teaser.get = Mock(return_value=None)
        result = monitor.update_status()

        # get a fresh instance from the database
        updated_monitor = Monitor.objects.get(pk=monitor.pk)
        self.assertEqual(updated_monitor.last_updated, LATE)
        self.assertEqual(updated_monitor.status, 'RED')
        self.assertEqual(Alert.objects.count(), 0)
        self.assertEqual(result, 'RED')

    @patch_find_by_id({'title': 'foo'})
    def test_last_doc(self):
        """
        Tests the last_doc method of the Monitor class.
        """
        monitor = self.monitor_grn
        actual = monitor.last_doc()
        expected = '{\n    "title": "foo"\n}'
        self.assertEqual(actual, expected)

    def test_last_doc_no_distillery(self):
        """
        Tests the last_doc method of the Monitor class when the Monitor
        has no saved Distillery activity.
        """
        monitor = self.monitor_red_repeating
        self.assertEqual(monitor.last_doc(), None)
