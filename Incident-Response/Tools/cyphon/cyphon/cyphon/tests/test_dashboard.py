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
Functional tests for the Dashboard app.
"""

# local
from tests.fixture_manager import get_fixtures
from tests.functional_tests import AdminFunctionalTest
from .pages import DashboardPage


class DashboardFunctionalTest(AdminFunctionalTest):
    """
    Tests the main dashboard for the admin site.
    """
    fixtures = get_fixtures(['containers'])

    def setUp(self):
        super(DashboardFunctionalTest, self).setUp()
        self.page = DashboardPage(self.driver)

    def test_dashboard(self):
        """
        Tests the main dashboard for the admin site.
        """
        self.assertIn('Shaping Data', self.page.module_1)
        self.assertIn('Filtering Data', self.page.module_2)
        self.assertIn('Sifting Data', self.page.module_3)
        self.assertIn('Condensing Data', self.page.module_4)
        self.assertIn('Enhancing Data', self.page.module_5)
        self.assertIn('Storing Data', self.page.module_6)
        self.assertIn('Distilling Data', self.page.module_7)
        self.assertIn('Investigating Data', self.page.module_8)
        self.assertIn('Configuring Alerts', self.page.module_9)
        self.assertIn('Manage Alerts', self.page.module_10)
        self.assertIn('Manage Mail', self.page.module_11)
        self.assertIn('People and Permissions', self.page.module_12)
        self.assertIn('Records', self.page.module_13)
        self.assertIn('App Configurations', self.page.module_14)
        # self.assertIn('Recent Actions', self.page.module_15)  # no listings
        self.assertIn('Support', self.page.module_16)
        self.assertIn('Latest Cyphon News', self.page.module_17)
