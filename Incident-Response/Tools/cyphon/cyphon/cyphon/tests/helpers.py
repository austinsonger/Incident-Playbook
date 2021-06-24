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
Tests custom permissions classes.
"""

# standard library
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TestCase

# local
from alerts.models import Alert
from appusers.models import AppUser
from contexts.models import Context
from distilleries.models import Distillery
from monitors.models import Monitor
from tests.fixture_manager import get_fixtures
from warehouses.models import Warehouse


class CyphonTestCase(TestCase):
    """

    """
    fixtures = get_fixtures(['alerts', 'contexts', 'monitors'])

    @classmethod
    def setUpClass(cls):
        super(CyphonTestCase, cls).setUpClass()
        cls.alerts = Alert.objects.all()
        cls.contexts = Context.objects.all()
        cls.distilleries = Distillery.objects.all()
        cls.monitors = Monitor.objects.all()
        cls.warehouses = Warehouse.objects.all()
        cls.user_staff = AppUser.objects.get(pk=1)
        cls.user_nonstaff_w_company = AppUser.objects.get(pk=2)
        cls.user_nonstaff_wo_company = AppUser.objects.get(pk=4)

    def setUp(self):
        self.view = Mock()
        self.request = Mock()

