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
Tests the ApiHandler class.
"""

# standard library
import datetime

# third party
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

# local
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Account
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame
from tests.fixture_manager import get_fixtures

BASE_FIXTURES = get_fixtures(['plumbers', 'funnels', 'distilleries',
                              'followees', 'locations', 'searchterms',
                              'timeframes'])


class ApiHandlerMixin(object):
    """
    Mixin for testing the ApiHandler class.
    """
    data = {
        "text" : "this is an example post",
        "id" : int("123456789"),
        "user" : {
            "screen_name" : "JohnSmith76",
            "profile_image_url" : "http://www.example.com/123.jpeg",
            "id" : 9999999,
        },
        "created_at" : "Sat Feb 21 23:13:31 +0000 2015",
    }

    @staticmethod
    def _create_example_timeframe():
        """
        Helper method that returns an example TimeFrame.
        """
        start_time = timezone.now()
        delta = datetime.timedelta(days=10)
        end_time = timezone.now() + delta
        return TimeFrame(start=start_time, end=end_time)

    @staticmethod
    def _create_example_query():
        """
        Helper method that returns an example ReservoirQuery.
        """
        accounts = Account.objects.filter(pk__in=[1, 2])
        locations = Location.objects.filter(pk__in=[3, 4])
        searchterms = SearchTerm.objects.filter(pk__in=[10, 11, 12])
        timeframe = TimeFrame.objects.get(pk=1)

        return ReservoirQuery(
            accounts=accounts,
            locations=locations,
            searchterms=searchterms,
            timeframe=timeframe
        )


class ApiHandlerTestCase(TestCase, ApiHandlerMixin):
    """
    Base class for testing the ApiHandler class.
    """
    fixtures = BASE_FIXTURES

    def setUp(self):
        super(ApiHandlerTestCase, self).setUp()
        self.timeframe = self._create_example_timeframe()
        self.query = self._create_example_query()


class ApiHandlerTransactionTestCase(TransactionTestCase, ApiHandlerMixin):
    """
    Base class for testing the ApiHandler class.
    """
    fixtures = BASE_FIXTURES

    def setUp(self):
        super(ApiHandlerTransactionTestCase, self).setUp()
        self.timeframe = self._create_example_timeframe()
        self.query = self._create_example_query()

