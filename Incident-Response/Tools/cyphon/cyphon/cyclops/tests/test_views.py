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

# third party
from constance.test import override_config
from copy import deepcopy
from django.conf import settings
from django.test import TestCase
from django.utils.encoding import force_text
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

# local
from appusers.models import AppUser
from cyphon.version import VERSION


class CyclopsViewsTestCase(TestCase):
    """
    Base test class for Cyclops views.
    """
    def setUp(self):
        """
        Creates a user for the views.
        """
        secret = 'test12345'
        self.user = AppUser.objects.create_user(
            email='test@test.com',
            password=secret,
            first_name='Bob',
            last_name='Saget',
        )
        self.user.is_active = True
        self.user.save()

    def authenticate(self):
        """
        Authenticates a user for the view.
        """
        self.client.force_login(self.user)


class ApplicationTest(CyclopsViewsTestCase):
    """
    Test class for the cyclops application view.
    """
    url = '/app/'

    def get_application(self):
        """
        Gets the application response.
        """
        return self.client.get(self.url)

    def test_authentication_redirect(self):
        """
        Tests that an unauthenticated user gets redirected to the login page.
        """
        response = self.get_application()

        self.assertRedirects(response, '/login/?next=/app/')

    def test_template(self):
        """
        Tests that the correct template is used.
        """
        self.authenticate()

        response = self.get_application()

        self.assertTemplateUsed(response, template_name='cyclops/app.html')

    def test_notifications_enabled(self):
        """
        Tests that the notifications enabled context gets passed to the
        template.
        """
        self.authenticate()

        with override_config(PUSH_NOTIFICATIONS_ENABLED=True):
            response = self.get_application()

            self.assertTrue(response.context['notifications_enabled'])

        with override_config(PUSH_NOTIFICATIONS_ENABLED=False):
            response = self.get_application()

            self.assertFalse(response.context['notifications_enabled'])

    def test_mapbox_access_token(self):
        """
        Tests that the mapbox access token gets passed to the template.
        """
        self.authenticate()

        response = self.get_application()

        self.assertEqual(response.context['mapbox_access_token'], '')

        cyclops_settings = deepcopy(settings.CYCLOPS)
        cyclops_settings['MAPBOX_ACCESS_TOKEN'] = 'blah'

        with self.settings(CYCLOPS=cyclops_settings):
            response = self.get_application()

            self.assertEqual(response.context['mapbox_access_token'], 'blah')

    def test_cyphon_version(self):
        """
        Tests that the correct cyphon version is passed to the template.
        """
        self.authenticate()
        response = self.get_application()

        self.assertEqual(response.context['cyphon_version'], VERSION)

    def test_api_timeout(self):
        """
        Tests that the correct api_timeout is passed to the template.
        """
        self.authenticate()

        response = self.get_application()

        self.assertEqual(response.context['api_timeout'], 30000)
        self.assertContains(response, 'API_TIMEOUT: 30000,')

        cyclops_settings = deepcopy(settings.CYCLOPS)
        cyclops_settings['API_TIMEOUT'] = 60000

        with self.settings(CYCLOPS=cyclops_settings):
            response = self.get_application()

            self.assertEqual(response.context['api_timeout'], 60000)
            self.assertContains(response, 'API_TIMEOUT: 60000,')


class ManifestTest(CyclopsViewsTestCase):
    """
    View tests for the manifest.json view.
    """
    url = '/manifest.json'

    def test_response(self):
        """
        Tests that it returns a manifest.json with the correct gcm_sender_id.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), {
            'gcm_sender_id': '',
            'manifest_version': 2,
            'name': 'Cyphon Push Notifications',
            'version': '0.2',
        })

        notification_settings = deepcopy(settings.NOTIFICATIONS)
        notification_settings['GCM_SENDER_ID'] = 'BLAH'

        with self.settings(NOTIFICATIONS=notification_settings):
            response = self.client.get(self.url)

            self.assertEqual(response.status_code, 200)
            self.assertJSONEqual(force_text(response.content), {
                'gcm_sender_id': 'BLAH',
                'manifest_version': 2,
                'name': 'Cyphon Push Notifications',
                'version': '0.2',
            })
