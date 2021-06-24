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
Tests signal recievers in the MailSifter package.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django_mailbox.signals import message_received
from django.test import TestCase


class HandleMessageTestCase(TestCase):
    """
    Tests the handle_email signal receiver.
    """

    def test_match_with_default(self):
        """
        Tests the handle_email signal receiver.
        """
        mock_email = {'Message-ID': 'abc', 'Subject': 'This is a Critical Alert'}
        mock_message = Mock()
        mock_message.get_email_object = Mock(return_value=mock_email)
        with patch('sifter.mailsifter.mailchutes.models.MailChuteManager.process') \
                as mock_process:
            message_received.send(sender='message_received',
                                  message=mock_message)
            assert mock_process.call_count == 1
