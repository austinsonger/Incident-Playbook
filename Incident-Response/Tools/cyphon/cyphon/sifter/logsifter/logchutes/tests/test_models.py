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
Tests the LogChute class.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from sifter.logsifter.logchutes.models import LogChute
from sifter.logsifter.logmungers.models import LogMunger
from tests.fixture_manager import get_fixtures


class LogChuteTestCase(TestCase):
    """
    Base class for testing the LogChute class.
    """

    fixtures = get_fixtures(['logchutes'])

    def setUp(self):
        try:
            del LogChute.objects._default_munger
        except AttributeError:
            pass

    def test_get_default_w_chute(self):
        """
        Tests the _default_munger function when the default LogMunger
        does not exists.
        """
        mock_config = {
            'DEFAULT_MUNGER': 'default_log',
            'DEFAULT_MUNGER_ENABLED': True
        }
        with patch.dict('sifter.logsifter.logchutes.models.conf.LOGSIFTER',
                        mock_config):
            actual = LogChute.objects._default_munger
            expected = LogMunger.objects.get(name='default_log')
            self.assertEqual(actual.pk, expected.pk)
            self.assertTrue(LogChute.objects._default_munger_enabled)

    def test_get_default_disabled(self):
        """
        Tests the _default_munger function when the default LogMunger
        is disabled.
        """
        mock_config = {
            'DEFAULT_MUNGER': 'default_log',
            'DEFAULT_MUNGER_ENABLED': False
        }
        with patch.dict('sifter.logsifter.logchutes.models.conf.LOGSIFTER',
                        mock_config):
            actual = LogChute.objects._default_munger
            expected = LogMunger.objects.get(name='default_log')
            self.assertEqual(actual.pk, expected.pk)
            self.assertFalse(LogChute.objects._default_munger_enabled)

    def test_get_default_no_chute(self):
        """
        Tests the _default_munger function when the default LogMunger
        does not exist.
        """
        mock_config = {
            'DEFAULT_MUNGER': 'dummy_munger',
            'DEFAULT_MUNGER_ENABLED': True
        }
        with patch.dict('sifter.logsifter.logchutes.models.conf.LOGSIFTER',
                        mock_config):
            with LogCapture() as log_capture:
                actual = LogChute.objects._default_munger
                expected = None
                self.assertEqual(actual, expected)
                self.assertFalse(LogChute.objects._default_munger_enabled)
                log_capture.check(
                    ('sifter.chutes.models',
                     'ERROR',
                     'Default LogMunger "dummy_munger" is not configured.'),
                )
