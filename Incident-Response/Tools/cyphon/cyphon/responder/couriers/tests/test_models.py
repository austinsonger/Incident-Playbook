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
Tests |Courier| model methods.
"""

# standard library
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TestCase

# local
from responder.actions.models import Action
from responder.couriers.models import Courier
from tests.fixture_manager import get_fixtures


class CourierBaseTestCase(TestCase):
    """
    Base class for testing the Alerts.
    """
    fixtures = get_fixtures(['couriers'])

    def setUp(self):
        self.jira_courier = Courier.objects.get(pk=1)
        self.jira_action = Action.objects.get(pk=1)
        self.twitter_courier = Courier.objects.get(pk=3)
        self.twitter_action = Action.objects.get(pk=2)


# class HasEndpointTestCase(CourierBaseTestCase):
#     """
#     Tests the _has_endpoint() method.
#     """

#     def test_does_not_have_endpoint(self):
#         """

#         """
#         actual = self.courier._has_endpoint(self.jira_action)
#         expected = True
#         self.assertIs(actual, expected)

#     def test_has_endpoint(self):
#         """

#         """
#         actual = self.courier._has_endpoint(self.twitter_action)
#         expected = False
#         self.assertIs(actual, expected)


class VisaIsValidTestCase(CourierBaseTestCase):
    """
    Tests the visa_is_valid() method.
    """
    # assert self.visa is not None
    # return self.remaining_calls() > 0

    def test_has_remaining_calls(self):
        """

        """
        pass

    def test_no_remaining_calls(self):
        """

        """
        pass

    def test_no_visa(self):
        """

        """
        pass


class EnabledTestCase(CourierBaseTestCase):
    """
    Tests the enabled() method.
    """
    # if self._has_endpoint(endpoint):
    #   if endpoint.visa_required:
            # if self.visa is not None:
            #     return self.visa_is_valid()
            # else:
            #     return False
        # else:
        #     return True
    # else:
    #     return False

    def test_does_not_have_endpoint(self):
        """

        """
        actual = self.jira_courier.enabled(self.twitter_action)
        expected = False
        self.assertIs(actual, expected)

    def test_no_visa(self):
        """

        """
        self.twitter_courier.visa = None
        actual = self.twitter_courier.enabled(self.twitter_action)
        expected = False
        self.assertIs(actual, expected)

    def test_visa_is_valid(self):
        """

        """
        self.twitter_courier.visa_is_valid = Mock(return_value=True)
        actual = self.twitter_courier.enabled(self.twitter_action)
        expected = True
        self.assertIs(actual, expected)

    def test_visa_is_invalid(self):
        """

        """
        self.twitter_courier.visa_is_valid = Mock(return_value=False)
        actual = self.twitter_courier.enabled(self.twitter_action)
        expected = False
        self.assertIs(actual, expected)

