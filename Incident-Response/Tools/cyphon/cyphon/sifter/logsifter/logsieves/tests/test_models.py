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
Tests the LogSieve class and related classes.
"""

# third party
from django.test import TestCase

# local
from sifter.logsifter.logsieves.models import LogSieve
from tests.fixture_manager import get_fixtures


class LogSieveTestCase(TestCase):
    """
    Tests the LogSieve class.
    """
    fixtures = get_fixtures(['logsieves'])

    def test_is_match_for_all_true(self):
        """
        Tests the is_match method for a LogSieve that uses 'AND' logic and a
        dataset that conforms to the LogSieve.
        """
        logsieve = LogSieve.objects.get(name="check_subject")
        msg = 'this is a critical alert'
        self.assertTrue(logsieve.is_match(msg))

    def test_is_match_for_all_false(self):
        """
        Tests the is_match method for a LogSieve that uses 'AND' logic and a
        dataset that does not conform to the LogSieve.
        """
        logsieve = LogSieve.objects.get(name="check_subject")
        msg = 'this is an urgent alert'
        self.assertFalse(logsieve.is_match(msg))

    def test_is_match_for_any_true(self):
        """
        Tests the is_match method for a LogSieve that uses 'OR' logic and a
        dataset that conforms to the LogSieve.
        """
        logsieve = LogSieve.objects.get(name="check_subject")
        logsieve.logic = 'OR'
        msg = 'this is an urgent alert'
        self.assertTrue(logsieve.is_match(msg))

    def test_is_match_for_any_false(self):
        """
        Tests the is_match method for a LogSieve that uses 'OR' logic and a
        dataset that does not conform to the LogSieve.
        """
        logsieve = LogSieve.objects.get(name="check_subject")
        logsieve.logic = 'OR'
        msg = 'this is an urgent notice'
        self.assertFalse(logsieve.is_match(msg))

