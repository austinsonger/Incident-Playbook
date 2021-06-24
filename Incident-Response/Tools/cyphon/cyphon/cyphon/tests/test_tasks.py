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
Tests Permissions classes.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.test import TestCase
from django_mailbox.models import Mailbox

# local
from cyphon.tasks import get_new_mail, run_health_check
from monitors.models import Monitor
from tests.fixture_manager import get_fixtures


class GetNewMailTestCase(TestCase):
    """
    Tests the get_new_mail task.
    """
    fixtures = get_fixtures(['monitors'])

    def test_run_health_check(self):
        """
        Tests the get_new_mail task.
        """
        mailbox_count = Mailbox.objects.all().count()

        with patch('django_mailbox.models.Mailbox.get_new_mail') as mock_get_mail:
            get_new_mail()
            self.assertEqual(mock_get_mail.call_count, mailbox_count)


class RunHealthCheckTestCase(TestCase):
    """
    Tests the run_health_check task.
    """
    fixtures = get_fixtures(['monitors'])

    def test_run_health_check(self):
        """
        Tests the run_health_check task.
        """
        all_monitors_count = Monitor.objects.all().count()
        enabled_monitors_count = Monitor.objects.find_enabled().count()
        assert all_monitors_count > enabled_monitors_count

        with patch('monitors.models.Monitor.update_status') as mock_update:
            run_health_check()
            self.assertEqual(mock_update.call_count, enabled_monitors_count)

