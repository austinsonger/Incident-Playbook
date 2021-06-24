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
Tests the Inspection class and related classes.
"""

# third party
from django.test import TestCase

# local
from inspections.models import Inspection
from tests.fixture_manager import get_fixtures


class InspectionTestCase(TestCase):
    """
    Base class for testing the Inspection class.
    """
    fixtures = get_fixtures(['inspections'])

    def test_get_result(self):
        """
        Tests the get_result method of the Inspection class.
        """
        high_priority_msg = {'subject': '[CRIT-111]'}
        med_priority_msg = {'subject': '[WARN-222]'}
        low_priority_msg = {'subject': '[INFO-333]'}
        mixed_msg1 = {'subject': '[INFO-333][WARN-222][CRIT-111]'}
        mixed_msg2 = {'subject': '[WARN-222][CRIT-111]'}

        inspection = Inspection.objects.get_by_natural_key('prioritize_emails')

        actual = inspection.get_result(low_priority_msg)
        self.assertEqual(actual, 'LOW')

        actual = inspection.get_result(med_priority_msg)
        self.assertEqual(actual, 'MEDIUM')

        actual = inspection.get_result(high_priority_msg)
        self.assertEqual(actual, 'HIGH')

        actual = inspection.get_result(mixed_msg1)
        self.assertEqual(actual, 'LOW')

        actual = inspection.get_result(mixed_msg2)
        self.assertEqual(actual, 'HIGH')
