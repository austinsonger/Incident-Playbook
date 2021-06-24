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
Tests for notification views.
"""

# standard library
import logging
from unittest import skip

# third party
from rest_framework import status

# local
from alerts.models import Alert
from notifications.views import LEVEL_IMAGES
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class SubscribeAPITests(CyphonAPITestCase):
    """
    Test the API endpoint for subscribing to notifications.
    """
    fixtures = get_fixtures(['users'])

    model_url = 'notifications/subscribe/'

    def test_post_subscribe(self):
        """
        Test a successful subscribe.
        """
        new_id = '23456'
        data = {'registration_id': '23456'}
        response = self.post_to_api('', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.push_notification_id, new_id)

    def test_duplicate_subscribe(self):
        """
        Test subscribe when the registration id is already in use by
        another user.
        """
        dup_id = '22222'
        data = {'registration_id': dup_id}
        response = self.post_to_api('', data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_type_fail_post(self):
        """
        Test a failed call.
        """
        data = {'meh': True}
        response = self.post_to_api('', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NotificationsAPITests(CyphonAPITestCase):
    """
    Tests the notification API endpoint for getting notifications
    """
    fixtures = get_fixtures(['alerts'])

    model_url = 'notifications/'

    def setUp(self):
        super(NotificationsAPITests, self).setUp()
        logging.disable(logging.WARNING)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @skip
    def test_unauthorized_access(self):
        """
        Override this method since it doesn't apply to the
        /notifications/ endpoint.
        """
        pass

    def test_missing_registration_id(self):
        
        """
        Tests that a 400 response is sent when the url is missing a
        registration id.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], [
            'registration_id parameter was not given'
        ])

    def test_registration_id_exists(self):
        """
        Tests that a 400 response is sent when there is no user matching
        the given registration id.
        """
        response = self.get_api_response('?registration_id=gjr94')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], [
            'registration_id is not valid'
        ])

    def test_missing_alert(self):
        """
        Tests that a 400 response is sent when there is no new Alert.
        """
        Alert.objects.filter(status='NEW').delete()
        response = self.get_api_response('?registration_id=11111')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data['errors'],
            ['alert object not present']
        )

    def test_successful_call(self):
        """
        Tests that the correct notification object is passed when
        there is a successful call and the user associated with the
        registration id is staff.
        """
        response = self.get_api_response('?registration_id=11111')
        alert = Alert.objects.filter(status='NEW').first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['title'],
            '{}: {}'.format(alert.level, alert.distillery)
        )
        self.assertEqual(
            response.data['tag'],
            'cyphon-alert-{}'.format(alert.id)
        )
        self.assertEqual(
            response.data['message'],
            alert.title
        )
        self.assertEqual(
            response.data['icon'],
            LEVEL_IMAGES[alert.level]
        )

    def test_successful_call_nonstaff(self):
        """
        Tests that the correct notification object is passed when
        there is a successful call and the user associated with the
        registration id is not staff.
        """
        response = self.get_api_response('?registration_id=22222')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tag'], 'cyphon-alert-4')

        response = self.get_api_response('?registration_id=33333')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tag'], 'cyphon-alert-5')
