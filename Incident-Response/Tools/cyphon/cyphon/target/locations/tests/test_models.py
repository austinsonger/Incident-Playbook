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
Tests the Location class and its related classes.
"""

# third party
from django.test import TestCase
from geopy.distance import vincenty
from testfixtures import LogCapture

# local
from target.locations.models import Location
from tests.fixture_manager import get_fixtures
from utils.geometry import shapes, units


class LocationTestCase(TestCase):
    """
    Base class for testing the Location class.
    """
    fixtures = get_fixtures(['locations'])


class LocationManagerTestCase(LocationTestCase):
    """
    Tests the Location objects manager.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for Locations.
        """
        location = Location.objects.get_by_natural_key('Point')
        self.assertEqual(location.pk, 1)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method when the Location
        does not exist.
        """
        with LogCapture() as log_capture:
            Location.objects.get_by_natural_key('foobar')
            log_capture.check(
                ('target.locations.models',
                 'ERROR',
                 'Location "foobar" does not exist'),
            )


class StrTestCase(LocationTestCase):
    """
    Tests the __str__ method.
    """

    def test_str(self):
        """
        Tests the string representation of a Location.
        """
        location = Location.objects.get(pk=1)
        self.assertEqual(str(location), 'Point <Point>')


class HasBufferTestCase(LocationTestCase):
    """
    Tests the has_buffer method.
    """

    def test_has_buffer_when_false(self):
        """
        Tests case when buffer is zero.
        """
        point = Location.objects.get(pk=1)
        self.assertEqual(point.has_buffer(), False)

    def test_has_buffer_when_true(self):
        """
        Tests case when buffer is greater than zero.
        """
        circle = Location.objects.get(pk=2)
        self.assertEqual(circle.has_buffer(), True)


class ShapeTestCase(LocationTestCase):
    """
    Tests the shape property.
    """

    def test_shape_for_point(self):
        """
        Test case for a point.
        """
        point = Location.objects.get(pk=1)
        self.assertEqual(point.shape, 'Point')

    def test_shape_for_circle(self):
        """
        Test case for a circle.
        """
        circle = Location.objects.get(pk=2)
        self.assertEqual(circle.shape, 'Circle')

    def test_shape_for_rectangle(self):
        """
        Test case for a rectangle.
        """
        rectangle = Location.objects.get(pk=3)
        self.assertEqual(rectangle.shape, 'Rectangle')

    def test_shape_for_polygon(self):
        """
        Test case for a polygon.
        """
        polygon = Location.objects.get(pk=4)
        self.assertEqual(polygon.shape, 'Polygon')

    def test_shape_for_multipolygon(self):
        """
        Test case for a multipolygon.
        """
        multipolygon = Location.objects.get(pk=5)
        self.assertEqual(multipolygon.shape, 'MultiPolygon')

    def test_shape_for_line(self):
        """
        Test case for a line.
        """
        line = Location.objects.get(pk=6)
        self.assertEqual(line.shape, 'Other')


class BoundingBoxTestCase(LocationTestCase):
    """
    Tests the bbox property.
    """

    def test_bbox_for_point(self):
        """
        Test case for a point.
        """
        point = Location.objects.get(pk=1)
        actual = point.bbox
        expected = None
        self.assertEqual(actual, expected)

    def test_bbox_for_circle(self):
        """
        Test case for a circle.
        """
        circle = Location.objects.get(pk=2)
        actual = circle.bbox
        expected = shapes.convert_circle_to_rectangle(circle.geom,
                                                      circle.buffer_m)
        self.assertTrue(actual.equals(expected))

    def test_bbox_for_rectangle(self):
        """
        Test case for a rectangle.
        """
        rectangle = Location.objects.get(pk=3)
        actual = rectangle.bbox
        expected = rectangle.geom
        self.assertTrue(actual.equals(expected))

    def test_bbox_for_polygon(self):
        """
        Test case for a polygon.
        """
        polygon = Location.objects.get(pk=4)
        actual = polygon.bbox
        expected = polygon.geom.envelope
        self.assertTrue(actual.equals(expected))

    def test_bbox_for_multipoly(self):
        """
        Test case for a multipolygon.
        """
        multipolygon = Location.objects.get(pk=5)
        actual = multipolygon.bbox
        expected = multipolygon.geom.envelope
        self.assertTrue(actual.equals(expected))

    def test_bbox_for_line(self):
        """
        Test case for a line.
        """
        line = Location.objects.get(pk=6)
        actual = line.bbox
        expected = None
        self.assertEqual(actual, expected)


class RadiusKmTestCase(LocationTestCase):
    """
    Tests the radius_km property.
    """

    def test_radius_for_point(self):
        """
        Test case for a point.
        """
        point = Location.objects.get(pk=1)
        actual = point.radius_km
        expected = None
        self.assertEqual(actual, expected)

    def test_radius_for_circle(self):
        """
        Test case for a circle.
        """
        circle = Location.objects.get(pk=2)
        actual = circle.radius_km
        expected = units.meters_to_km(circle.radius_km)
        self.assertTrue(actual, expected)

    def test_radius_for_rectangle(self):
        """
        Test case for a rectangle.
        """
        rectangle = Location.objects.get(pk=3)
        actual = rectangle.radius_km
        expected = vincenty(rectangle.geom.centroid, (0, 1)).kilometers
        self.assertTrue(actual, expected)

    def test_radius_for_polygon(self):
        """
        Test case for a polygon.
        """
        polygon = Location.objects.get(pk=4)
        actual = polygon.radius_km
        point = shapes.reverse_coordinate_order(polygon.geom.centroid)
        expected = vincenty(point, (8, 0)).kilometers
        self.assertTrue(actual, expected)

    def test_radius_for_multipoly(self):
        """
        Test case for a multipolygon.
        """
        multipolygon = Location.objects.get(pk=8)
        actual = multipolygon.radius_km
        point = shapes.reverse_coordinate_order(multipolygon.geom.centroid)
        expected = vincenty(point, (20, 50)).kilometers
        self.assertTrue(actual, expected)

    def test_radius_for_line(self):
        """
        Test case for a line.
        """
        line = Location.objects.get(pk=6)
        actual = line.radius_km
        expected = None
        self.assertEqual(actual, expected)


class FactorByRadiusTestCase(LocationTestCase):
    """
    Tests the factor_by_radius method.
    """

    def test_for_circle_w_same_radius(self):
        """
        Tests factor_by_radius method for a circle with the same radius as
        the given radius.
        """
        circle = Location.objects.get(pk=2)
        new_locations = circle.factor_by_radius_km(0.1)
        self.assertTrue(len(new_locations) == 4)

    def test_for_circle_w_half_radius(self):
        """
        Tests factor_by_radius method for a circle with half the radius as
        the given radius.
        """
        circle = Location.objects.get(pk=2)
        new_locations = circle.factor_by_radius_km(0.2)
        self.assertTrue(len(new_locations) == 1)

    def test_for_circle_w_2x_radius(self):
        """
        Tests factor_by_radius method for a circle with twice the radius as
        the given radius.
        """
        circle = Location.objects.get(pk=2)
        new_locations = circle.factor_by_radius_km(0.05)
        self.assertTrue(len(new_locations) == 16)

    def test_for_polygon(self):
        """
        Tests factor_by_radius method for a polygon location.
        """
        polygon = Location.objects.get(pk=4)
        new_locations = polygon.factor_by_radius_km(1)
        self.assertTrue(new_locations[0].buffer_m == 1000)
