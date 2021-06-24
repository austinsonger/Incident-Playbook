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
Tests functions in the bounds module.
"""

# standard library
from unittest import TestCase

# third party
from geopy.distance import vincenty

# local
from utils.geometry.bounds import Bounds


class BoundsTestCase(TestCase):
    """
    Tests the Bounds class.
    """

    def test_default_corners(self):
        """
        Tests the methods for getting corners using the default values for a
        new Bounds instance.
        """
        bounds = Bounds()
        points = (bounds.sw_corner, bounds.nw_corner,
                  bounds.ne_corner, bounds.se_corner)
        self.assertEqual(points, ((180.0, 90.0), (180.0, -90.0),
                                  (-180.0, -90.0), (-180.0, 90.0)))

    def test_center_width(self):
        """
        Tests method for finding the average width of the bounding box in meters.
        """
        bounds = Bounds(n_lat=50.0, s_lat=0.0, e_lng=25.0, w_lng=0.0)
        expected = vincenty((25.0, 0), (25.0, 25.0)).meters
        self.assertEqual(bounds.center_width_m, expected)

    def test_get_width_at_latitude(self):
        """
        Tests method for finding the width of the bounding box at the given
        latitude, in meters.
        """
        bounds = Bounds(n_lat=50.0, s_lat=0.0, e_lng=50.0, w_lng=0.0)
        width = bounds.get_width_at_latitude_m(25.0)
        self.assertAlmostEqual(width, 5017040, delta=5)

    def test_height(self):
        """
        Tests method for finding the height of the bounding box in meters.
        """
        bounds = Bounds(n_lat=50.0, s_lat=0.0, e_lng=25.0, w_lng=0.0)
        self.assertAlmostEqual(bounds.height_m, 5540850, delta=5)

    def test_buffer(self):
        """
        Tests method for buffering the bounds.
        """
        bounds = Bounds(n_lat=28.0, s_lat=26.0, e_lng=0.0, w_lng=-2.0)
        old_height = bounds.height_m
        old_width = bounds.center_width_m
        buffer_m = 10
        bounds.buffer(buffer_m)

        actual_height = bounds.height_m
        actual_width = bounds.center_width_m
        expected_height = old_height + (buffer_m * 2)
        expected_width = old_width + (buffer_m * 2)
        self.assertAlmostEqual(actual_height, expected_height, delta=0.001)
        self.assertAlmostEqual(actual_width, expected_width, delta=0.001)

