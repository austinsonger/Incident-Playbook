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
Tests the Pipe class and the related RateLimit and SpecSheet classes.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from rest_framework import status

# local
from appusers.models import AppUser
from alerts.models import Alert
from responder.couriers.models import Courier
from responder.dispatches.models import Dispatch
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class ActionsViewTestCase(CyphonAPITestCase):
    """
    Base class for testing the Action views.
    """

    fixtures = get_fixtures(['alerts', 'couriers', 'dispatches'])

    model_url = 'actions/'

    obj_url = '1/'

    def setUp(self, *args, **kwargs):
        self.user = AppUser.objects.get(id=2)

    def test_public_private_couriers(self):
        """
        Tests the run method when both a private and public courier for
        the user exists.
        """
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_public_courier_only(self):
        """
        Tests the run method when only a public courier for the user
        exists.
        """
        Courier.objects.filter(passport__public=False).delete()
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_private_courier_only(self):
        """
        Tests the run method when only a private courier for the user
        exists.
        """
        Courier.objects.filter(passport__public=True).delete()
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_no_courier(self):
        """
        Tests the run method when no courier for the user exists.
        """
        Courier.objects.all().delete()
        response = self.get_api_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_run(self):
        """
        Tests the run endpoint.
        """
        alert = Alert.objects.get(pk=3)
        dispatch = Dispatch.objects.get(pk=1)
        with patch('responder.actions.models.Action.get_dispatch',
                   return_value=dispatch) as mock_dispatch:
            response = self.post_to_api('1/run/', {'alert': 3})
            actual = response.json()
            expected = {
                'id': 1,
                'issued_by': {
                    'id': 1,
                    'email': 'testuser1@testdomain.com',
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'is_staff': True,
                    'company': None
                },
                'status_code': '200',
                'response_msg': None,
                'data': {
                    'foo': 'bar'
                }
            }
            mock_dispatch.assert_called_with(user=self.user, alert=alert)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(actual, expected)
