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
Tests the MonitorForm.
"""

# third party
from django.test import TestCase

# local
from distilleries.models import Distillery
from monitors.forms import MonitorForm
from tests.fixture_manager import get_fixtures


class MonitorFormTestCase(TestCase):
    """
    Test cases for the clean method the MonitorForm class.
    """

    fixtures = get_fixtures(['monitors'])

    def test_invalid_distillery(self):
        """
        Tests that a validation error is thrown for an invalid
        field_name value.
        """
        distillery = Distillery.objects.get(pk=3)
        distillery.is_shell = True
        distillery.save()
        form_data = {
            'name': 'new monitor',
            'distilleries': [distillery.pk],
            'time_interval': 1,
            'time_unit': 'd',
            'alerts_enabled': True,
            'repeating_alerts': True,
            'alert_level': 'HIGH',
            'status': 'GREEN'
        }
        form = MonitorForm(data=form_data)
        msg = ('The Container for the Distillery &quot;%s&quot; must have a '
               'Taste with a designated Datetime field.' % distillery)
        self.assertFalse(form.is_valid())
        self.assertTrue(msg in str(form.errors))
