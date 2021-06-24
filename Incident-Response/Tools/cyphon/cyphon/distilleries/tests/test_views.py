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
Tests views for Distilleries.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.contrib.auth.models import Group
from rest_framework import status

# local
from appusers.models import AppUser
from distilleries.models import Distillery
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class DistilleryAPITests(CyphonAPITestCase):
    """
    Tests REST API endpoints for Distilleries.
    """
    fixtures = get_fixtures(['distilleries', 'alerts', 'contexts'])

    model_url = 'distilleries/'
    obj_url = '1/'

    def setUp(self):
        self.user = AppUser.objects.get(id=1)
        self.group1 = Group.objects.get(pk=1)
        self.group2 = Group.objects.get(pk=2)
        self.distillery = Distillery.objects.get(pk=1)

    def test_get_distillery(self):
        """
        Tests the GET /api/v1/distilleries/1 REST API endpoint.
        """
        response = self.get_api_response(self.obj_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_distilleries(self):
        """
        Tests the GET /api/v1/distilleries/ REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)

    def test_filtered_distilleries(self):
        """
        Tests that GET /api/v1/distilleries/ filters distilleries by company.
        """
        self.user = AppUser.objects.get(id=2)
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_no_company_nonstaff(self):
        """
        Tests that GET /api/v1/distilleries/ returns no distilleries
        if the user has no company and is not staff.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_have_alerts(self):
        """
        Tests the GET /api/v1/distilleries/have-alerts/ REST API endpoint.
        """
        response = self.get_api_response('have-alerts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    @patch('distilleries.views.DistilleryViewSet.paginate_queryset',
           return_value=None)
    def test_have_alerts_no_paging(self, mock_page):
        """
        Tests the GET /api/v1/distilleries/have-alerts/ REST API endpoint
        without pagination.
        """
        response = self.get_api_response('have-alerts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
