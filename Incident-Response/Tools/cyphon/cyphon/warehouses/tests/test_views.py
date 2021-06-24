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
Tests views for Warehouses and Collections.
"""

# third party
from rest_framework import status

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class WarehouseAPITests(CyphonAPITestCase):
    """
    Tests REST API endpoints for Warehouses.
    """
    fixtures = get_fixtures(['warehouses'])

    model_url = 'warehouses/'

    def test_get_warehouses(self):
        """
        Tests the Warehouses REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_get_collection(self):
        """
        Tests the Warehouse detail REST API endpoint.
        """
        response = self.get_api_response('1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['backend'], 'mongodb')
        self.assertEqual(response.data['name'], 'test_database')


class CollectionAPITests(CyphonAPITestCase):
    """
    Tests REST API endpoints for Collections.
    """
    fixtures = get_fixtures(['warehouses'])

    model_url = 'collections/'

    def test_get_collections(self):
        """
        Tests the Collections REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 7)

    def test_get_collection(self):
        """
        Tests the Collection detail REST API endpoint.
        """
        response = self.get_api_response('1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_posts')

    def test_get_collections_by_warehs(self):
        """
        Tests the /collections/?warehouse REST API endpoint.
        """
        response = self.get_api_response('?warehouse=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
