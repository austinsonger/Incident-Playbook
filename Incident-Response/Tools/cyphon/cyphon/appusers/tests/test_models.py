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

"""

# third party
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTestCase(TestCase):
    """
    Tests the custom user model.
    """

    def setUp(self):
        self.email = 'john.smith@example.com'
        self.password = 'password'
        self.first_name = 'John'
        self.last_name = 'Smith'
        self.user_model = get_user_model()
        user = self.user_model.objects.create_user(self.email, self.password)
        user.first_name = self.first_name
        user.last_name = self.last_name
        user.save()

    def test_get_absolute_url(self):
        """
        Test the get_absolute_url method.
        """
        user = self.user_model.objects.get(email=self.email)
        self.assertEqual(user.get_absolute_url(),
                         '/users/john.smith%40example.com/')

    def test_get_full_name(self):
        """
        Test the get_full_name method.
        """
        user = self.user_model.objects.get(email=self.email)
        self.assertEqual(user.get_full_name(), 'John Smith')

    def test_get_short_name(self):
        """
        Test the get_short_name method.
        """
        user = self.user_model.objects.get(email=self.email)
        self.assertEqual(user.get_short_name(), 'John')
