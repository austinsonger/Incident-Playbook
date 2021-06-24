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
Tests views for Monitors.
"""

# standard library
from collections import OrderedDict
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from rest_framework import status
from rest_framework.test import APITestCase

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find_by_id


class MonitorAPITestCase(CyphonAPITestCase):
    """
    Base class for testing REST API endpoints for Bottles and related objects.
    """
    fixtures = get_fixtures(['monitors'])

    model_url = 'monitors/'

    mock_doc = {
        'title': 'foo'
    }

    @patch_find_by_id(mock_doc)
    def test_get_monitor(self):
        """
        Tests the REST API endpoint for a Monitor instance.
        """
        response = self.get_api_response('1/')
        expected = {
            'last_active_distillery': {
                'name': 'mongodb.test_database.test_posts',
                'url': 'http://testserver/api/v1/distilleries/1/',
                'id': 1
            },
            'last_saved_doc': '10',
            'status': 'GREEN',
            'alert_level': 'HIGH',
            'last_healthy': '2016-01-01T09:00:00Z',
            'interval': '5m',
            'alerts_enabled': True,
            'enabled': True,
            'distilleries': [{
                'name': 'mongodb.test_database.test_docs',
                'url': 'http://testserver/api/v1/distilleries/2/',
                'id': 2
            }, {
                'name': 'mongodb.test_database.test_posts',
                'url': 'http://testserver/api/v1/distilleries/1/',
                'id': 1
            }],
            'name': 'health_alerts',
            'last_updated': '2016-01-01T09:01:00Z'
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected)

    @patch_find_by_id(mock_doc)
    def test_get_monitors(self):
        """
        Tests the REST API endpoint for Monitors.
        """
        # with patch('distilleries.models.Distillery.find_by_id',
        #            return_value=mock_doc):
        response = self.get_api_response()
        expected = OrderedDict([
            ('name', 'health_alerts'),
            ('enabled', True),
            ('distilleries', [
                OrderedDict([
                    ('id', 2),
                    ('name', 'mongodb.test_database.test_docs'),
                    ('url', 'http://testserver/api/v1/distilleries/2/')
                ]),
                OrderedDict([
                    ('id', 1),
                    ('name', 'mongodb.test_database.test_posts'),
                    ('url', 'http://testserver/api/v1/distilleries/1/')
                ])
            ]),
            ('interval', '5m'),
            ('alerts_enabled', True),
            ('alert_level', 'HIGH'),
            ('status', 'GREEN'),
            ('last_updated', '2016-01-01T09:01:00Z'),
            ('last_healthy', '2016-01-01T09:00:00Z'),
            ('last_active_distillery', OrderedDict([
                ('id', 1),
                ('name', 'mongodb.test_database.test_posts'),
                ('url', 'http://testserver/api/v1/distilleries/1/')
            ])),
            ('last_saved_doc', '10'),
        ])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
        self.assertEqual(response.data['results'][0], expected)

    @patch_find_by_id()
    def test_get_enabled_monitors(self):
        """
        Tests the monitors/enabled REST API endpoint.
        """
        response = self.get_api_response('enabled/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
