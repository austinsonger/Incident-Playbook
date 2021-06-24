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

"""

# third party
from rest_framework import status

# local
from appusers.models import AppUser
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class AppUserViewTestCase(CyphonAPITestCase):
    """
    Base class for testing the AppUser views.
    """

    fixtures = get_fixtures(['users'])

    model_url = 'users/'

    def test_get_users_for_nonstaff(self):
        """
        Tests the AppUsers REST API endpoint for user who is not staff.
        """
        response = self.get_api_response(is_staff=False)
        count = AppUser.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), count)

    def test_only_show_staff_setting(self):
        """
        Tests that the user list endpoint only shows staff users if the
        ONLY_SHOW_STAFF setting is set to True.
        """

        with self.settings(APPUSERS={'ONLY_SHOW_STAFF': True}):
            response = self.get_api_response(is_staff=False)
            count = AppUser.objects.filter(is_staff=True).count()
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), count)
