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
Tests functions in the units module.
"""

# standard library
from unittest import TestCase

# local
from utils.geometry import units


class MeterstoKilometersTestCase(TestCase):
    """
    Tests the meters_to_km function.
    """

    def test_0_meters(self):
        """
        Test case for 0 meters.
        """
        self.assertEqual(units.meters_to_km(0), 0)

    def test_10_meters(self):
        """
        Test case for 10 meters.
        """
        self.assertEqual(units.meters_to_km(10), 0.01)

    def test_float_input(self):
        """
        Test case for floating point input.
        """
        self.assertEqual(units.meters_to_km(0.5), 0.0005)


class KilometerstoMetersTestCase(TestCase):
    """
    Tests the km_to_meters function.
    """

    def test_0_kilometers(self):
        """
        Test case for 0 kilometers.
        """
        self.assertEqual(units.km_to_meters(0), 0)

    def test_10_kilometers(self):
        """
        Test case for 10 kilometers.
        """
        self.assertEqual(units.km_to_meters(10), 10000)

    def test_float_output(self):
        """
        Test case for a floating point output.
        """
        self.assertAlmostEqual(units.km_to_meters(0.5001), 500.1,
                               delta=0.00000001) 


class SqMeterstoSqKilometersTestCase(TestCase):
    """
    Tests the sq_meters_to_sq_km function.
    """

    def test_0_sq_meters(self):
        """
        Test case for 0 square meters.
        """
        self.assertEqual(units.sq_meters_to_sq_km(0), 0)

    def test_1000_sq_meters(self):
        """
        Test case for 1000 square meters.
        """
        self.assertEqual(units.sq_meters_to_sq_km(1000), 0.001)

    def test_float_input(self):
        """
        Test case for floating point input.
        """
        self.assertEqual(units.sq_meters_to_sq_km(0.5), 0.0000005)


class SqKilometerstoSqMetersTestCase(TestCase):
    """
    Tests the sq_km_to_sq_meters function.
    """

    def test_0_sq_kilometers(self):
        """
        Test case for 0 meters.
        """
        self.assertEqual(units.sq_km_to_sq_meters(0), 0)

    def test_10000_sq_kilometers(self):
        """
        Test case for 10 meters.
        """
        self.assertEqual(units.sq_km_to_sq_meters(1000), 1000000000)

    def test_float_output(self):
        """
        Test case for a floating point output.
        """
        self.assertAlmostEqual(units.sq_km_to_sq_meters(0.1000001), 100000.1,
                               delta=0.00000001)


class KilometerstoMilesTestCase(TestCase):
    """
    Tests the km_to_mi function.
    """

    def test_0_kilometers(self):
        """
        Test case for 0 kilometers.
        """
        self.assertEqual(units.km_to_mi(0), 0)

    def test_10_kilometers(self):
        """
        Test case for 10 kilometers.
        """
        self.assertAlmostEqual(units.km_to_mi(10), 6.2137119,
                               delta=0.00000001)


class MeterstoDegreesTestCase(TestCase):
    """
    Tests the convert_meters_to_degrees function.
    """

    def test_default_result(self):
        """
        Tests the conversion using default values for rounding direction
        and decimal places.
        """
        actual = units.convert_meters_to_degrees(10000)
        expected = 0.0898316  # 0.089831566
        self.assertEqual(actual, expected)

    def test_round_closest(self):
        """
        Tests the conversion when rounding to the closest value.
        """
        actual = units.convert_meters_to_degrees(10000, 'closest')
        expected = 0.0898316
        self.assertEqual(actual, expected)

    def test_round_down(self):
        """
        Tests the conversion when rounding down.
        """
        actual = units.convert_meters_to_degrees(10000, 'down')
        expected = 0.0898315
        self.assertEqual(actual, expected)

    def test_round_up_to_five_places(self):
        """
        Tests the conversion when rounding up.
        """
        actual = units.convert_meters_to_degrees(10000, 'up', 5)
        expected = 0.08984
        self.assertEqual(actual, expected)

    def test_round_to_five_places(self):
        """
        Tests the conversion when using default rounding to five places.
        """
        actual = units.convert_meters_to_degrees(10000, places=5)
        expected = 0.08983
        self.assertEqual(actual, expected)
