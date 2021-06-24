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
# """
# Tests the Planner class.
# """

# # standard library
# import datetime

# # third party
# from django.test import TestCase
# from django.utils import timezone

# # local
# from aggregator.pipes.models import PipeRateLimit
# from aggregator.plumbers.models import Meter
# from aggregator.pumproom.planner import Planner
# from tests.fixture_manager import get_fixtures


# class PlannerTestCase(TestCase):
#     """
#     Base class for testing the Planner class.
#     """
#     fixtures = get_fixtures(['pipes'])

#     @staticmethod
#     def _create_example_planner():
#         """
#         Helper mthods that returns an example Planner instance.
#         """
#         delta = datetime.timedelta(seconds=30)
#         end_time = timezone.now() + delta
#         meter = Meter(end_time=end_time, remaining_calls=100)
#         ratelimit = PipeRateLimit.objects.get(pk=1)     # Twitter Search API
#         return Planner(meter=meter, ratelimit=ratelimit)

#     def setUp(self):
#         super(PlannerTestCase, self).setUp()
#         self.planner = self._create_example_planner()


# class GetTimeRemainingTestCase(PlannerTestCase):
#     """
#     Tests the get_time_remaining_in_minutes method.
#     """

#     def test_for_zero_time(self):
#         """
#         Tests the get_time_remaining_in_minutes method when there is no time
#         remaining in the current rate-limit interval.
#         """
#         meter = Meter(end_time=timezone.now())
#         ratelimit = PipeRateLimit.objects.get(pk=1)     # Twitter Search API
#         planner = Planner(meter=meter, ratelimit=ratelimit)
#         actual = planner.get_time_remaining_in_minutes()
#         self.assertAlmostEqual(actual, 0, delta=0.001)

#     def test_for_nonzero_time(self):
#         """
#         Tests the get_time_remaining_in_minutes method when there is time
#         remaining in the current rate-limit interval.
#         """
#         planner = self._create_example_planner()
#         actual = planner.get_time_remaining_in_minutes()
#         self.assertAlmostEqual(actual, 0.5, delta=0.001)


# class CalculateQueryTimeTestCase(PlannerTestCase):
#     """
#     Tests the calculate_query_time_in_minutes method.
#     """

#     def test_for_0_queries_10_remaining(self):
#         """
#         Tests the calculate_query_time_in_minutes method for no queries.
#         """
#         actual = self.planner.calculate_query_time_in_minutes(0)
#         self.assertAlmostEqual(actual, 0, delta=0.001)

#     def test_under_limit(self):
#         """
#         Tests the calculate_query_time_in_minutes method for a number of queries
#         less than the number remaining in the current rate-limit interval.
#         """
#         actual = self.planner.calculate_query_time_in_minutes(50)
#         self.assertAlmostEqual(actual, 0, delta=0.001)

#     def test_over_limit_by_1_interval(self):
#         """
#         Tests the calculate_query_time_in_minutes method for a number of queries
#         greater than the number remaining in the current rate-limit interval.
#         """
#         actual = self.planner.calculate_query_time_in_minutes(300)
#         self.assertAlmostEqual(actual, 0.5, delta=0.001)

#     def test_over_limit_by_2_intervals(self):
#         """
#         Tests the calculate_query_time_in_minutes method for a number of queries
#         greater than the number remaining in the current rate-limit interval and
#         the next interval.
#         """
#         actual = self.planner.calculate_query_time_in_minutes(999)
#         self.assertAlmostEqual(actual, 15.5, delta=0.001)

#     def test_over_limit_by_3_intervals(self):
#         """
#         Tests the calculate_query_time_in_minutes method for a number of queries
#         greater than the number remaining in the current rate-limit interval and
#         the next two intervals.
#         """
#         actual = self.planner.calculate_query_time_in_minutes(1000)
#         self.assertAlmostEqual(actual, 30.5, delta=0.001)

