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
Test version middleware and helper functions.
"""

# standard library
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

# third party
from django.test import TestCase
from django.test.client import RequestFactory

# local
from cyphon.version import VersionMiddleware, VERSION


class VersionMiddlewareTest(TestCase):
    """
    Tests the VersionMiddleware class.
    """

    def setUp(self):
        self.get_response = MagicMock(return_value={})
        self.factory = RequestFactory()

    def create_middleware(self):
        """
        Creates a VersionMiddleware instance.
        """
        return VersionMiddleware(self.get_response)

    def check_get_response_is_called(self, request):
        """

        """
        self.get_response.assert_called_once_with(request)

    def test_correct_version_added(self):
        """
        Tests that the correct version number is returned when a call to
        """
        middleware = self.create_middleware()

        request = self.factory.get('/login/')
        response = middleware(request)

        self.check_get_response_is_called(request)
        self.assertEqual(
            response[VersionMiddleware.VERSION_HEADER], VERSION)

    def test_mock_view(self):
        """
        Tests that the version header is added to any requests.
        """
        response = self.client.get('/login/')
        self.assertEqual(
            response[VersionMiddleware.VERSION_HEADER], VERSION)

        response = self.client.get('/api/v1/')
        self.assertEqual(
            response[VersionMiddleware.VERSION_HEADER], VERSION)
