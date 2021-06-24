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
Tests for the Contexts app REST API.
"""


# third party
from django.conf import settings
from rest_framework import status

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find, patch_find_by_id

API_URL = settings.API_URL


class ContextAPITest(CyphonAPITestCase):
    """
    Tests REST API pages for Contexts.
    """
    fixtures = get_fixtures(['contexts'])

    model_url = 'contexts/'

    mock_data = {'host': 'foo', 'message': 'bar'}
    mock_results = {
        'count': 1,
        'results': [{'foo2': 'bar2'}]
    }

    def test_get_contexts(self):
        """
        Tests the Contexts REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)

    @patch_find(mock_results)
    @patch_find_by_id(mock_data)
    def test_related_data_by_id(self):
        """
        Tests the related_data_by_id view.
        """
        url = self.url + '1/related-data-by-id/'
        self.authenticate()
        query = {'id': '1'}
        response = self.client.get(url, query)
        actual = response.json()
        actual = response.json()
        expected = {
            'distillery': 'elasticsearch.test_index.test_docs',
            'count': 1,
            'results': [{'foo2': 'bar2'}]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual, expected)

    def test_related_data_by_id_no_id(self):
        """
        Tests the related_data_by_id view when no id is provided.
        """
        url = self.url + '1/related-data-by-id/'
        self.authenticate()
        query = {'foo': '1'}
        response = self.client.get(url, query)
        actual = response.json()
        expected = {'error': 'A document id must be provided.'}
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual, expected)


class ContextFiltersAPITest(CyphonAPITestCase):
    """
    Tests REST API pages for ContextFilters.
    """
    fixtures = get_fixtures(['contexts'])

    model_url = 'contextfilters/'

    def test_get_contexts(self):
        """
        Tests the ContextFilters REST API endpoint.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
