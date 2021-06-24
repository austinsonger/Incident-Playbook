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
Tests Alert views.
"""

# standard library
from datetime import timedelta
import logging
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework import status

# local
from appusers.models import AppUser
from alerts.models import Alert, Analysis
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures
from .expected_values import ALERT_DETAIL, ALERT_LIST

API_URL = settings.API_URL

ALERT_FIXTURES = get_fixtures(['alerts', 'comments', 'contexts',
                               'dispatches', 'tags'])


class AlertBaseAPITests(CyphonAPITestCase):
    """
    Base class for testing REST API endpoints for Alerts.
    """
    fixtures = ALERT_FIXTURES

    model_url = 'alerts/'

    obj_url = '1/'

    def setUp(self):
        self.user = AppUser.objects.get(id=2)
        self.group1 = Group.objects.get(pk=1)
        self.group2 = Group.objects.get(pk=2)
        self.alert = Alert.objects.get(pk=1)
        self.date = Alert.objects.get(pk=1).created_date
        self.error = {
            'error': 'Please provide an integer for the days parameter'
        }
        self.max_msg = {
            'error': 'A maximum of 30 days is permitted'
        }
        logging.disable(logging.WARNING)

    def tearDown(self):
        logging.disable(logging.NOTSET)


class AlertBasicAPITests(AlertBaseAPITests):
    """
    Tests basic REST API endpoints for Alerts.
    """

    def test_get_alert_list_staff(self):
        """
        Tests the Alerts REST API endpoint for staff.
        """
        self.user.use_redaction = False
        response = self.get_api_response()
        self.assertEqual(response.json(), ALERT_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(response.data['results'][3].get('title'),
                         'Acme Supply Co')
        self.assertFalse(response.data['results'][3].get('data'))

        self.user.groups.remove(self.group1)
        self.user.groups.add(self.group2)
        response = self.get_api_response()
        self.assertEqual(len(response.data['results']), 2)

    def test_get_alerts_list_non_staff(self):
        """
        Tests the Alerts REST API endpoint for non-staff.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_get_redacted_alerts(self):
        """
        Tests the REST API endpoint for Alerts when redaction is used.
        """
        self.user.use_redaction = True
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 7)
        self.assertEqual(response.data['results'][3].get('title'), '**PEAK**')
        self.assertFalse(response.data['results'][3].get('data'))

    def test_get_alert(self):
        """
        Tests the REST API endpoint for a specific Alert when the current
        user does not use redactions.
        """
        self.maxDiff = None
        self.user.use_redaction = False
        response = self.get_api_response('4/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), ALERT_DETAIL)
        self.assertEqual(response.data.get('title'), 'Acme Supply Co')
        self.assertEqual(response.data.get('data'),
                         {'content': {'link': 'url', 'text': 'foobar'}})

    def test_get_redacted_alert(self):
        """
        Tests the REST API endpoint for a specific Alert when the current
        user uses redactions.
        """
        self.user.use_redaction = True
        response = self.get_api_response('4/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), '**PEAK**')
        self.assertEqual(response.data.get('data'),
                         {'content': {'link': 'url', 'text': 'foobar'}})

    def test_user_w_alert_wo(self):
        """
        Tests AlertBackendFilter for a user with a Group and an Alert
        without Groups.
        """
        self.user.groups.add(self.group1)
        self.alert.alarm.groups.remove(self.group1)
        response = self.get_api_response(self.obj_url, is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_wo_alert_wo(self):
        """
        Tests AlertBackendFilter for a user and an Alert without Groups.
        """
        self.alert.alarm.groups.remove(self.group1)
        response = self.get_api_response(self.obj_url, is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_match(self):
        """
        Tests AlertBackendFilter for a user with the same Groups as an
        Alert.
        """
        self.user.groups.add(self.group1, self.group2)
        self.alert.alarm.groups.add(self.group1, self.group2)
        response = self.get_api_response(self.obj_url, is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_match(self):
        """
        Tests AlertBackendFilter for a user with groups partially in
        common with Alerts.
        """
        self.user.groups.add(self.group1)
        self.alert.alarm.groups.add(self.group1, self.group2)
        response = self.get_api_response(self.obj_url, is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_match(self):
        """
        Tests AlertBackendFilter for a user with a different Group than
        an Alert.
        """
        self.user.groups.add(self.group1)
        self.alert.alarm.groups.remove(self.group1)
        self.alert.alarm.groups.add(self.group2)
        response = self.get_api_response(self.obj_url, is_staff=False)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateAlertAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoint for updating an Alert.
    """

    def test_patch_alert(self):
        """
        Tests the partial_update view of the Alerts endpoint.
        """
        self.maxDiff = None
        self.user.use_redaction = False
        response = self.patch_to_api('4/', {
            'level': 'MEDIUM',
            'status': 'BUSY',
        })
        old_muzzle_hash = Alert.objects.get(pk=4).muzzle_hash
        updated_alert = ALERT_DETAIL.copy()
        updated_alert['data'] = {
            'content': {
                'link': 'url',
                'text': 'foobar',
            }
        }
        updated_alert['level'] = 'MEDIUM'
        updated_alert['status'] = 'BUSY'
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), updated_alert)
        self.assertEqual(response.data.get('level'), 'MEDIUM')
        self.assertEqual(response.data.get('status'), 'BUSY')

        # make sure muzzle_hash doesn't change on update
        response = self.patch_to_api('4/', {
            'level': 'MEDIUM',
        })
        new_muzzle_hash = Alert.objects.get(pk=4).muzzle_hash
        self.assertEqual(response.data.get('level'), 'MEDIUM')
        self.assertEqual(old_muzzle_hash, new_muzzle_hash)

    def test_create_analysis(self):
        """
        Tests the partial_update view of the Alerts endpoint when an
        Analysis is created.
        """
        self.assertFalse(Analysis.objects.filter(pk=4).exists())
        notes = 'Here are some notes.'
        self.patch_to_api('4/', {'notes': notes})
        analysis = Analysis.objects.get(pk=4)
        self.assertEqual(analysis.notes, notes)

    def test_update_analysis(self):
        """
        Tests the partial_update view of the Alerts endpoint when an
        Analysis is updated.
        """
        notes = 'Here are some updated notes.'
        self.patch_to_api('3/', {'notes': notes})
        analysis = Analysis.objects.get(pk=3)
        self.assertEqual(analysis.notes, notes)


class AlertCollectionAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/collections/'

    def test_get_alert_collections(self):
        """
        Tests the REST API endpoint for Alert counts by collection.
        """
        with patch('alerts.views.timezone.now', return_value=self.date):
            response = self.get_api_response('?days=7', is_staff=False)
            expected = {
                'elasticsearch.test_index.test_logs': 1,
                'mongodb.test_database.test_posts': 3,
            }
            self.assertEqual(response.json(), expected)

    def test_alert_collections_no_days(self):
        """
        Tests the REST API endpoint for Alert counts by collection when no
        days parameter is provided.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_galert_collections_no_int(self):
        """
        Tests the REST API endpoint for Alert counts by collection when the
        days parameter cannot be converted to an integer.
        """
        response = self.get_api_response('?days=hello', is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_collections_max(self):
        """
        Tests the REST API endpoint for Alert counts by collection when the
        days parameter exceeds the maximum.
        """
        response = self.get_api_response('?days=31', is_staff=False)
        self.assertEqual(response.json(), self.max_msg)


class AlertLevelAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/levels/'

    def test_get_alert_levels(self):
        """
        Tests the REST API endpoint for Alert counts by level.
        """
        with patch('alerts.views.timezone.now', return_value=self.date):
            response = self.get_api_response('?days=7', is_staff=False)
            expected = {
                'CRITICAL': 0,
                'HIGH': 2,
                'MEDIUM': 2,
                'LOW': 1,
                'INFO': 0,
            }
            self.assertEqual(response.json(), expected)

    def test_get_alert_levels_no_days(self):
        """
        Tests the REST API endpoint for Alert counts by level when no
        days parameter is provided.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_level_no_int(self):
        """
        Tests the REST API endpoint for Alert counts by level when the
        days parameter cannot be converted to an integer.
        """
        response = self.get_api_response('?days=hello', is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_level_max(self):
        """
        Tests the REST API endpoint for Alert counts by level when the
        days parameter exceeds the maximum.
        """
        response = self.get_api_response('?days=31', is_staff=False)
        self.assertEqual(response.json(), self.max_msg)


class AlertStatusAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/statuses/'

    def test_get_alert_statuses(self):
        """
        Tests the REST API endpoint for Alert counts by status.
        """
        with patch('alerts.views.timezone.now', return_value=self.date):
            response = self.get_api_response('?days=7', is_staff=False)
            expected = {
                'NEW': 2,
                'BUSY': 1,
                'DONE': 2,
            }
            self.assertEqual(response.json(), expected)

    def test_get_alert_statuses_no_days(self):
        """
        Tests the REST API endpoint for Alert counts by status when no
        days parameter is provided.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_statuses_no_int(self):
        """
        Tests the REST API endpoint for Alert counts by status when the
        days parameter cannot be converted to an integer.
        """
        response = self.get_api_response('?days=hello', is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_statuses_max(self):
        """
        Tests the REST API endpoint for Alert counts by status when the
        days parameter exceeds the maximum.
        """
        response = self.get_api_response('?days=31', is_staff=False)
        self.assertEqual(response.json(), self.max_msg)


class AlertLocationAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/locations/'

    def test_get_alert_locations(self):
        """
        Tests the REST API endpoint for Alert locations.
        """
        test_url = '?days=7'
        with patch('alerts.views.timezone.now', return_value=self.date):
            response = self.get_api_response(test_url, is_staff=False)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            actual = response.json()
            expected = {
                'features': [{
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-78.2, 36.4]
                    },
                    'type': 'Feature',
                    'properties': {
                        'pk': '2',
                        'title': 'Threat Alert',
                        'level': 'HIGH',
                        'incidents': 1
                    }
                }, {
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [-78.2, 36.4]
                    },
                    'type': 'Feature',
                    'properties': {
                        'pk': '1',
                        'title': 'Acme Supply Co',
                        'level': 'HIGH',
                        'incidents': 1
                    }
                }],
                'type': 'FeatureCollection',
                'crs': {
                    'type': 'name',
                    'properties': {
                        'name': 'EPSG:4326'
                    }
                }
            }
            self.assertEqual(actual, expected)

        new_year = self.date.year + 1
        date2 = self.date.replace(year=new_year)
        with patch('alerts.views.timezone.now', return_value=date2):
            response = self.get_api_response(test_url, is_staff=False)
            actual = response.json()
            expected = {
                'type': 'FeatureCollection',
                'crs': {
                    'properties': {
                        'name': 'EPSG:4326'
                    },
                    'type': 'name'
                },
                'features': []
            }
            self.assertEqual(actual, expected)

    def test_get_alert_locations_no_day(self):
        """
        Tests the REST API endpoint for Alert counts by location when no
        days parameter is provided.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_locations_no_int(self):
        """
        Tests the REST API endpoint for Alert locations when the
        days parameter cannot be converted to an integer.
        """
        response = self.get_api_response('?days=hello', is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_get_alert_locations_max(self):
        """
        Tests the REST API endpoint for Alert locations when the
        days parameter exceeds the maximum.
        """
        response = self.get_api_response('?days=31', is_staff=False)
        self.assertEqual(response.json(), self.max_msg)


class AlertTimeseriesAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/level-timeseries/'

    def test_level_timeseries(self):
        """
        Tests the REST API endpoint for Alert levels for the past week.
        """
        self.maxDiff = None
        test_url = '?days=7'
        date1 = self.date + timedelta(days=7)
        with patch('alerts.views.timezone.localtime', return_value=date1):
            response = self.get_api_response(test_url, is_staff=False)
            expected = {
                'CRITICAL': [0, 0, 0, 0, 0, 0, 0],
                'HIGH': [2, 0, 0, 0, 0, 0, 0],
                'MEDIUM': [2, 0, 0, 0, 0, 0, 0],
                'LOW': [1, 0, 0, 0, 0, 0, 0],
                'INFO': [0, 0, 0, 0, 0, 0, 0],
                'date': [
                    '2015-03-01',
                    '2015-03-02',
                    '2015-03-03',
                    '2015-03-04',
                    '2015-03-05',
                    '2015-03-06',
                    '2015-03-07'
                ]}
            self.assertEqual(response.json(), expected)

        date2 = self.date + timedelta(days=3)
        with patch('alerts.views.timezone.localtime', return_value=date2):
            response = self.get_api_response(test_url, is_staff=False)
            expected = {
                'CRITICAL': [0, 0, 0, 0, 0, 0, 0],
                'HIGH': [0, 0, 0, 0, 2, 0, 0],
                'MEDIUM': [0, 0, 0, 0, 2, 0, 0],
                'LOW': [0, 0, 0, 0, 1, 0, 0],
                'INFO': [0, 0, 0, 0, 0, 0, 0],
                'date': [
                    '2015-02-25',
                    '2015-02-26',
                    '2015-02-27',
                    '2015-02-28',
                    '2015-03-01',
                    '2015-03-02',
                    '2015-03-03'
                ]}
            self.assertEqual(response.json(), expected)

    def test_level_timeseries_no_days(self):
        """
        Tests the REST API endpoint for Alert level timeseries when no
        days parameter is provided.
        """
        response = self.get_api_response(is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_level_timeseries_no_int(self):
        """
        Tests the REST API endpoint for Alert level timeseries when the
        days parameter cannot be converted to an integer.
        """
        response = self.get_api_response('?days=hello', is_staff=False)
        self.assertEqual(response.json(), self.error)

    def test_level_timeseries_max(self):
        """
        Tests the REST API endpoint for Alert level timeseries when the
        days parameter exceeds the maximum.
        """
        response = self.get_api_response('?days=31', is_staff=False)
        self.assertEqual(response.json(), self.max_msg)


class AlertDistilleryAPITests(AlertBaseAPITests):
    """
    Tests REST API endpoints for Alert-related data.
    """
    model_url = 'alerts/distilleries/'

    def test_get_alert_distilleries(self):
        """
        Tests the REST API endpoint for Distilleries associated with
        Alerts.
        """
        response = self.get_api_response(is_staff=False)
        expected = [
            {
                'id': 5,
                'name': 'elasticsearch.test_index.test_logs',
                'url': 'http://testserver/api/v1/distilleries/5/'
            },
            {
                'id': 1,
                'name': 'mongodb.test_database.test_posts',
                'url': 'http://testserver/api/v1/distilleries/1/'
            },
        ]
        self.assertEqual(response.json()['results'], expected)


class AnalysisAPITests(CyphonAPITestCase):
    """
    Tests the API endpoint for alert analyses.
    """
    fixtures = get_fixtures(['alerts'])

    model_url = 'analyses/'

    def test_get_analyses(self):
        """
        Tests the REST API endpoint for Analyses.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0].get('notes'),
                         'Some example notes.')

    def test_get_analysis(self):
        """
        Tests getting a single Analysis.
        """
        response = self.get_api_response('1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('notes'), 'Some example notes.')

    def test_only_analysts_can_patch(self):
        """
        Tests that only the user who created the Analysis can alter it.
        """
        url = self.url + '1/'
        self.authenticate()
        response = self.client.patch(url, {'notes': 'new'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentAPITests(CyphonAPITestCase):
    """
    Tests the API endpoint for alert comments.
    """
    fixtures = get_fixtures(['alerts', 'comments'])

    model_url = 'comments/'

    def test_get_comments(self):
        """
        Tests the REST API endpoint for Comments.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0].get('content'),
                         'I have something to say')

    def test_get_comment(self):
        """
        Tests getting a single Comment.
        """
        response = self.get_api_response('1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('content'),
                         'I have something to say')

    def test_only_user_can_patch(self):
        """
        Tests that only the user who created the Comment can alter it.
        """
        url = self.url + '2/'
        self.authenticate()
        response = self.client.patch(url, {'content': 'new'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
