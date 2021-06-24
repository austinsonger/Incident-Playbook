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
Tests views for Tastes.
"""

# third party
from rest_framework import status

# local
from appusers.models import AppUser
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class TasteAPITestCase(CyphonAPITestCase):
    """
    Tests for REST API endpoints for Tastes.
    """
    fixtures = get_fixtures(['tastes', 'users'])

    model_url = 'tastes/'

    def test_get_tastes(self):
        """
        Tests the the Tastes REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_taste_by_container(self):
        """
        Tests that the Tastes endpoint allows filtering by container.
        """
        response = self.get_api_response('?container=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        response = self.get_api_response('?container=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
