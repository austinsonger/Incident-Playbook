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
Tests for notification signals.
"""

# standard library
import logging
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.test import TestCase
from httmock import response
from testfixtures import LogCapture

# local
from alerts.models import Alert
from notifications.signals import (
    _PUSH_NOTIFICATION_URL,
    _PUSH_NOTIFICATION_REQUEST_HEADERS,
    _LOGGER,
)
from tests.fixture_manager import get_fixtures

_LOGGER.removeHandler('console')


class NotificationSignalTestCase(TestCase):
    """
    Tests for notification signals.
    """
    fixtures = get_fixtures(['alerts', 'users'])

    mock_settings = {
        'PUSH_NOTIFICATION_KEY': 'abc',
        'IGNORED_ALERT_LEVELS': ['LOW'],
    }

    def setUp(self):
        self.alert = Alert.objects.get(pk=2)
        self.alert.distillery = None
        self.alert.pk = None

    @patch('requests.post')
    @patch('alerts.models.Alert._add_data')
    @patch('notifications.signals.config')
    @patch('notifications.signals._NOTIFICATION_SETTINGS', mock_settings)
    def test_signal_sent(self, mock_config, mock_add_data, mock_post):
        """
        Test that the signal is received.
        """
        logging.disable(logging.WARNING)
        mock_config.PUSH_NOTIFICATIONS_ENABLED = True
        mock_post.return_value = response(200)
        self.alert.distillery = Alert.objects.get(pk=2).distillery
        self.alert.save()
        self.assertTrue(mock_post.called)
        self.assertEqual(mock_post.call_count, 1)
        mock_post.assert_called_with(
            _PUSH_NOTIFICATION_URL,
            headers=_PUSH_NOTIFICATION_REQUEST_HEADERS,
            json={
                'registration_ids': ['22222', '11111']
            }
        )
        logging.disable(logging.NOTSET)

    @patch('requests.post')
    @patch('notifications.signals.config')
    @patch('notifications.signals._NOTIFICATION_SETTINGS', mock_settings)
    def test_signal_failure(self, mock_config, mock_post):
        """
        Tests that errors are logged to the console.
        """
        mock_config.PUSH_NOTIFICATIONS_ENABLED = True
        with LogCapture('notifications.signals') as log_capture:
            mock_post.return_value = response(400, 'Error occurred')
            self.alert.save()
            self.assertTrue(mock_post.called)
            self.assertEqual(mock_post.call_count, 1)
            log_capture.check(
                ('notifications.signals', 'ERROR', "Could not send push "
                 "notifications. Received error from Chrome server: "
                 "Error occurred")
            )

    @patch('requests.post')
    @patch('notifications.signals.config')
    @patch('notifications.signals._NOTIFICATION_SETTINGS', mock_settings)
    def test_signal_not_sent(self, mock_config, mock_post):
        """
        Tests that a signal is not sent when they are turned off.
        """
        mock_config.PUSH_NOTIFICATIONS_ENABLED = False
        self.alert.save()
        self.assertFalse(mock_post.called)

    @patch('requests.post')
    def test_no_signal_on_update(self, mock_post):
        """
        Tests that no signal is sent when an alert object is updated.
        """
        alert = Alert.objects.all().first()
        alert.level = 'LOW'
        alert.data = {'foo': 'bar'}
        alert.save()
        self.assertFalse(mock_post.called)

    @patch('requests.post')
    def test_info_sends_no_notifs(self, mock_post):
        """
        Tests that a signal is not sent when the alert is only info level.
        """
        self.alert.level = 'INFO'
        self.alert.save()
        self.assertFalse(mock_post.called)
