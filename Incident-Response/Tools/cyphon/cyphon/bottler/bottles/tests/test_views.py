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
Tests views for Bottles and BottleFields.
"""

# third party
from rest_framework import status

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class BottleBaseAPITestCase(CyphonAPITestCase):
    """
    Base class for testing REST API endpoints for Bottles and related objects.
    """
    fixtures = get_fixtures(['distilleries'])


class BottleFieldAPITests(BottleBaseAPITestCase):
    """
    Tests REST API endpoints for BottleFields.
    """
    model_url = 'bottlefields/'

    def test_get_bottlefields(self):
        """
        Tests the BottleFields REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 32)

    def test_get_bottlefield(self):
        """
        Tests the BottleFields detail REST API endpoint.
        """
        response = self.get_api_response('7/')
        actual = response.data
        expected = {
            'id': 7,
            'field_name': 'from',
            'field_type': 'EmailField',
            'target_type': 'Account',
            'embedded_doc': None,
            'url': 'http://testserver' + self.url + '7/',
            'bottles': [
                'http://testserver/api/v1/bottles/4/'
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual, expected)

    def test_get_bottlefields_by_bottle(self):
        """
        Tests the BottleFields detail endpoint allows filtering by
        bottle name.
        """
        response = self.get_api_response('?bottle=4')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)


class BottleAPITests(BottleBaseAPITestCase):
    """
    Tests REST API endpoints for Bottles.
    """
    model_url = 'bottles/'

    def test_get_bottles(self):
        """
        Tests the Bottles REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 7)

    def test_get_bottle(self):
        """
        Tests the Bottles detail REST API endpoint.
        """
        response = self.get_api_response('3/')
        bottle = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(bottle['name'], 'post')
        self.assertEqual(len(bottle['fields']), 4)
