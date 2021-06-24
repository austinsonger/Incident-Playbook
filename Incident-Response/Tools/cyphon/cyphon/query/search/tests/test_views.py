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
Tests for the search endpoints.
"""

# standard library
from unittest.mock import patch
from unittest import TestCase
from datetime import datetime

# local
from appusers.models import AppUser
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures
from ..views import QueryParams
from ..search_results import DEFAULT_PAGE_SIZE

MOCK_RESULTS_LIST = [{'id': 1, 'content': 'content'}]
MOCK_RESULTS = {
    'count': 1,
    'results': MOCK_RESULTS_LIST,
}
MOCK_FIND = patch(
    'distilleries.models.Distillery.find',
    return_value=MOCK_RESULTS,
)


class QueryParamsTestCase(TestCase):
    def test_correct_default_params(self):
        """
        Tests that the object uses the correct default parameters.
        """
        params = QueryParams()

        self.assertEqual(params.query, '')
        self.assertEqual(params.page, 1)
        self.assertEqual(params.page_size, DEFAULT_PAGE_SIZE)
        self.assertEqual(params.before, None)
        self.assertEqual(params.after, None)

    def test_query_parsing(self):
        """
        Tests that the query parameter is passed through.
        """
        params = QueryParams({'query': 'oh la la'})

        self.assertEqual(params.query, 'oh la la')

    def test_page_parsing(self):
        """
        Tests that an integer is parsed from the page parameter.
        """
        params = QueryParams({'page': '34'})

        self.assertTrue(type(params.page) is int)
        self.assertEqual(params.page, 34)

    def test_string_page_type(self):
        """
        Tests that a word in the page parameter is ignored.
        """
        params = QueryParams({'page': 'meep'})

        self.assertEqual(params.page, 1)

    def test_page_size_parsing(self):
        """
        Tests that page_size is correctly parsed.
        """
        params = QueryParams({'page_size': '32'})

        self.assertTrue(type(params.page_size) is int)
        self.assertEqual(params.page_size, 32)

    def test_string_page_size_type(self):
        """
        Tests that a word in the page_size parameter is ignored.
        """
        params = QueryParams({'page_size': 'meep'})

        self.assertEqual(params.page_size, DEFAULT_PAGE_SIZE)

    def test_date_parsing(self):
        """
        Tests that a date is correctly parsed.
        """
        params = QueryParams({'before': '2017-11-27T06:00:00+05:00'})

        self.assertTrue(isinstance(params.before, datetime))
        self.assertEqual(params.before.year, 2017)
        self.assertEqual(params.before.month, 11)
        self.assertEqual(params.before.hour, 6)
        self.assertEqual(params.before.minute, 0)
        self.assertEqual(params.before.second, 0)
        self.assertEqual(params.before.day, 27)

    def test_incorrect_date_type(self):
        """
        Tests that an incorrect date string is ignored.
        """
        params = QueryParams({'before': 'wrong'})

        self.assertIsNone(params.before)


class SearchViewBaseTestCase(CyphonAPITestCase):
    """

    """

    fixtures = get_fixtures(
        ['alerts', 'distilleries', 'bottles', 'comments', 'users'],
    )
    MOCK_RESULTS_LIST = [{'id': 1, 'content': 'content'}]
    MOCK_RESULTS = {
        'count': 1,
        'results': MOCK_RESULTS_LIST,
    }
    MOCK_FIND = patch(
        'distilleries.models.Distillery.find',
        return_value=MOCK_RESULTS,
    )
    EMPTY_MOCK_FIND = patch(
        'distilleries.models.Distillery.find',
        return_value={'count': 0, 'results': []},
    )

    def setUp(self):
        self.user = AppUser.objects.get(id=2)

    def _get_mock_response(self, url):
        """Returns an api response with a mocked version of distillery.find

        Parameters
        ----------
        url : str
            URL to navigate to.

        Returns
        -------
        rest_framework.response.Response
        """
        with self.MOCK_FIND:
            return self.get_api_response(url)

    def _get_empty_mock_response(self, url):
        """Returns an API response with an empty mocked promise.

        Parameters
        ----------
        url : str
            URL to navigate to.

        Returns
        -------
        rest_framework.response.Response
        """
        with self.EMPTY_MOCK_FIND:
            return self.get_api_response(url)

    def _is_valid_response(self, response):
        """Tests that the API response is valid.

        Parameters
        ----------
        response : rest_framework.response.Response
        """
        self.assertEqual(response.status_code, 200)

    def _is_invalid_response(self, response):
        """Tests that the API response is invalid.

        Parameters
        ----------
        response : rest_framework.response.Response
        """
        self.assertEqual(response.status_code, 400)


class SearchViewTestCase(SearchViewBaseTestCase):
    model_url = 'search/'

    def test_valid_query(self):
        """
        Tests that a valid response is returned when hitting the endpoint.
        """
        response = self.get_api_response('?query=something')
        self._is_valid_response(response)
        self.assertEqual(
            response.data['results']['count'],
            1
        )

    def test_invalid_query(self):
        """
        Tests that a 400 error is thrown for an invalid query string.
        """
        response = self.get_api_response('?query=e#4390812@!FE#@GE')
        self._is_invalid_response(response)
        self.assertEqual(
            response.data['query']['unknown'][0]['errors'][0],
            'Parameter type is unknown.',
        )

        response = self.get_api_response('')
        self._is_invalid_response(response)
        self.assertEqual(
            response.data['query']['errors'][0],
            'Search query is empty.'
        )

    def test_query_data(self):
        """
        Tests that a query description is sent with the result data.
        """
        response = self.get_api_response('?query=keyword')
        self._is_valid_response(response)
        self.assertEqual(len(response.data['query']['keywords']), 1)

    def test_alert_data(self):
        """
        Tests that alert data gets grouped into it's own dictionary.
        """
        response = self.get_api_response('?query=keyword')
        self._is_valid_response(response)
        self.assertEqual(response.data['results']['alerts']['count'], 0)
        self.assertEqual(response.data['results']['alerts']['next'], None)
        self.assertEqual(response.data['results']['alerts']['previous'], None)
        self.assertEqual(response.data['results']['alerts']['results'], [])

    def test_distilleries_data(self):
        """
        Tests that distillery data gets grouped into it's own dictionary.
        """
        response = self.get_api_response('?query=keyword')
        self._is_valid_response(response)
        self.assertEqual(
            response.data['results']['distilleries']['count'], 0)
        self.assertEqual(
            response.data['results']['distilleries']['results'], [])


class AlertSearchViewTestCase(SearchViewBaseTestCase):
    """

    """

    fixtures = get_fixtures(
        ['alerts', 'distilleries', 'bottles', 'comments', 'users'],
    )
    model_url = 'search/alerts/'

    def test_field_parameters_ignored(self):
        """
        Tests that field parameters are ignored when searching through
        alerts.
        """
        response = self.get_api_response('?query=ip_address=14')
        self._is_valid_response(response)
        self.assertEqual(response.data['query']['fields'], [])

    def test_400_response(self):
        """
        Tests that a 400 response is returned for an invalid search query.
        """
        response = self.get_api_response('')
        self._is_invalid_response(response)
        self.assertEqual(
            response.data['query']['errors'][0],
            'Search query is empty.',
        )

    def test_results(self):
        """
        Tests that the correct result shape is returned from the endpoint.
        """
        response = self.get_api_response('?query=something')
        self._is_valid_response(response)
        self.assertEqual(response.data['results']['count'], 1)
        self.assertEqual(response.data['results']['next'], None)
        self.assertEqual(response.data['results']['previous'], None)
        self.assertEqual(len(response.data['results']['results']), 1)


class SearchDistilleriesViewTestCase(SearchViewBaseTestCase):
    """

    """

    model_url = 'search/distilleries/'

    def test_results(self):
        """
        Tests that the correct result shape is returned from the endpoint.
        """
        response = self._get_mock_response(
            '?query=%40source%3D%22test_mail%22+something'
        )
        self._is_valid_response(response)
        self.assertEqual(response.data['results']['count'], 1)
        self.assertEqual(len(response.data['results']['results']), 1)
        self.assertEqual(response.data['results']['results'][0], {
            'count': 1,
            'next': None,
            'previous': None,
            'distillery': {
                'id': 6,
                'name': 'elasticsearch.test_index.test_mail',
                'url': 'http://testserver/api/v1/distilleries/6/',
            },
            'results': self.MOCK_RESULTS_LIST
        })

    def test_invalid_response(self):
        """
        Tests that a 400 response with errors is returned from the endpoint.
        """
        response = self._get_mock_response('')
        self._is_invalid_response(response)
        self.assertEqual(
            response.data['query']['errors'][0],
            'Search query is empty.',
        )


class SearchDistilleryViewTestCase(SearchViewBaseTestCase):
    """

    """

    model_url = 'search/distilleries/'

    def test_results(self):
        """
        Tests that the correct result shape is returned from the endpoint.
        """
        response = self._get_mock_response('6/?query=something')
        self._is_valid_response(response)
        self.assertEqual(response.data['results']['count'], 1)
        self.assertEqual(response.data['results']['next'], None)
        self.assertEqual(response.data['results']['previous'], None)
        self.assertEqual(response.data['results']['distillery'], {
            'id': 6,
            'name': 'elasticsearch.test_index.test_mail',
            'url': 'http://testserver/api/v1/distilleries/6/',
        })
        self.assertEqual(
            response.data['results']['results'],
            self.MOCK_RESULTS_LIST,
        )

    def test_ignored_distillery_filter(self):
        """
        Tests that distillery filter parameters are ignored.
        """
        response = self._get_empty_mock_response(
            '2/?query=%40source%3D%22test_mail%22+something',
        )
        self._is_valid_response(response)
        self.assertEqual(response.data['query']['distilleries'], None)
        self.assertEqual(response.data['results']['distillery'], {
            'id': 2,
            'name': 'mongodb.test_database.test_docs',
            'url': 'http://testserver/api/v1/distilleries/2/',
        })

    def test_distillery_not_found(self):
        response = self._get_empty_mock_response('12/?query=woo')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Distillery 12 not found.')

    def test_empty_search_query(self):
        response = self._get_empty_mock_response('6/?query=')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['query']['errors'][0],
                         'Search query is empty.')
