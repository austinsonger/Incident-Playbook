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
Tests Alert views.
"""

# standard library
from smtplib import SMTPAuthenticationError
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from appusers.models import AppUser
from alerts.models import Comment
from tests.fixture_manager import get_fixtures


class SendCommentNotificationTestCase(TestCase):
    """
    Tests the send_comment_notification receiver.
    """
    fixtures = get_fixtures(['comments'])

    def setUp(self):
        self.comment = Comment.objects.get(pk=1)

    def test_old_alert(self):
        """
        Tests that the send_comment_notification receiver doesn't
        send an email when an existing alert is updated.
        """
        with patch('alerts.signals.emails_enabled', return_value=True):
            with patch('alerts.signals.compose_comment_email') as mock_compose:
                comment = Comment.objects.get(pk=1)
                comment.save()
                mock_compose.assert_not_called()

    def test_new_alert_emails_enabled(self):
        """
        Tests that the send_comment_notification receiver doesn't
        send an email when a new alert is updated and email notifcations
        are enabled.
        """
        mock_email = Mock()
        with patch('alerts.signals.emails_enabled', return_value=True):
            with patch('alerts.signals.compose_comment_email',
                       return_value=mock_email) as mock_compose:
                comment = Comment.objects.get(pk=1)
                user = AppUser.objects.get(pk=2)
                comment.pk = None
                comment.save()
                mock_compose.assert_called_with(comment, user)
                self.assertEqual(mock_compose.call_count, 1)
                self.assertEqual(mock_email.send.call_count, 1)

    def test_new_alert_emails_disabled(self):
        """
        Tests that the send_comment_notification receiver doesn't
        send an email when a new alert is updated and email notifcations
        are disabled.
        """
        mock_email = Mock()
        with patch('alerts.signals.emails_enabled', return_value=False):
            with patch('alerts.signals.compose_comment_email',
                       return_value=mock_email) as mock_compose:
                comment = Comment.objects.get(pk=1)
                comment.pk = None
                comment.save()
                mock_compose.assert_not_called()

    def test_email_error(self):
        """
        Tests that an error message is logged when an
        SMTPAuthenticationErro is encountered.
        """
        mock_email = Mock()
        mock_email.send = Mock(
            side_effect=SMTPAuthenticationError(535, 'foobar'))
        with patch('alerts.signals.emails_enabled', return_value=True):
            with patch('alerts.signals.compose_comment_email',
                       return_value=mock_email):
                with LogCapture() as log_capture:
                    comment = Comment.objects.get(pk=1)
                    comment.pk = None
                    comment.save()
                    log_capture.check(
                        ('alerts.signals',
                         'ERROR',
                         'An error occurred when sending an email '
                         'notification: (535, \'foobar\')'),
                    )
