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
Tests the Alarm class.
"""

# third party
from django.test import TestCase

# local
from alarms.models import Alarm, AlarmManager


class AlarmManagerTestCase(TestCase):
    """
    Tests the AlarmManager base class.
    """

    def test_find_relevant(self):
        """
        Tests the find_relevant method for the AlarmManager base class.
        """
        with self.assertRaises(NotImplementedError):
            manager = AlarmManager()
            manager.find_relevant(None)


class AlarmTestCase(TestCase):
    """
    Tests the Alarm base class class.
    """

    def test_process(self):
        """
        Tests the process method for the Alarm base class.
        """
        with self.assertRaises(NotImplementedError):
            alarm = Alarm()
            alarm.process(None)
