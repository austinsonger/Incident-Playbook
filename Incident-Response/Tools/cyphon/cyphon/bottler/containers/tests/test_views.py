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
Tests views for Containers.
"""

# third party
from rest_framework import status

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class ContainerAPITests(CyphonAPITestCase):
    """
    Tests REST API endpoints for Containers.
    """
    fixtures = get_fixtures(['distilleries'])

    model_url = 'containers/'

    def test_get_containers(self):
        """
        Tests the Containers REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)

    def test_get_container(self):
        """
        Tests the Container detail REST API endpoint.
        """
        response = self.get_api_response('2/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'labeled_post')

    def test_get_containers_by_name(self):
        """
        Tests that the Containers endpoint allows filtering by name.
        """
        response = self.get_api_response('?name=post')
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(results[0]['name'], 'post')

    def test_get_containers_by_wrhouse(self):
        """
        Tests that the Containers endpoint allows filtering by warehouse.
        """
        response = self.get_api_response('?warehouse=2')
        results = response.data['results']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(results[0]['name'], 'mail')
        self.assertEqual(results[1]['name'], 'snmptrap')
        self.assertEqual(results[2]['name'], 'test_doc')

    def test_get_containers_in_use(self):
        """
        Tests the /containers/in-use/ endpoint.
        """
        response = self.get_api_response('in-use/')
        self.assertEqual(len(response.data), 5)

    def test_get_targets(self):
        """
        Tests the /containers/targets/ REST API endpoint.
        """
        response = self.get_api_response('targets/')
        actual = response.data
        expected = [
            'Account',
            'DateTime',
            'IPAddress',
            'Keyword',
            'Location'
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual, expected)

    def test_get_targets_by_containers(self):
        """
        Tests that the /containers/targets/ endpoint allows filtering by
        multiple container names.
        """
        response = self.get_api_response('targets/?names=post,mail')
        actual = response.data
        expected = [
            'Account',
            'DateTime',
            'Keyword',
            'Location'
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual, expected)
