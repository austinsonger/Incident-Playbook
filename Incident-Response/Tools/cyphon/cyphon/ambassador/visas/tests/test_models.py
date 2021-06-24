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

# local
from ambassador.visas.models import Visa
from tests.fixture_manager import get_fixtures


class VisaTestCase(TestCase):
    """
    Tests the PipeRateLimit class.
    """

    fixtures = get_fixtures(['plumbers'])

    def test_str(self):
        """
        Tests the string representation of a PipeRateLimit.
        """
        ratelimit = Visa.objects.get(plumber=1)
        self.assertEqual(str(ratelimit), 'Twitter Search API')

    def test_get_request_intrvl_in_mins(self):
        """
        Tests method for getting the minutes in the interval used to
        define an API's rate limit.
        """
        twitter_rate = Visa.objects.get(plumber=1)
        self.assertEqual(twitter_rate.get_request_interval_in_minutes(), 15)

        instagram_rate = Visa.objects.get(plumber=6)
        self.assertEqual(instagram_rate.get_request_interval_in_minutes(), 60)

