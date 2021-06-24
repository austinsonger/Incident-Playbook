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
Tests functions in the shapes module.
"""

# third party
from django.test import TestCase
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from geopy.distance import vincenty

# local
from target.locations.models import Location
from tests.fixture_manager import get_fixtures
from utils.geometry import shapes, units
from utils.geometry.bounds import Bounds


class ReverseCoordinateOrderTestCase(TestCase):
    """
    Test class for function reverse_coordinate_order.
    """

    def test_reverse_coordinates_2tuple(self):
        """
        Tests the function reverse_coordinate_order for a 2-tuple.
        """
        reversed_order = shapes.reverse_coordinate_order((0, 1))
        self.assertEqual(reversed_order[0], 1)
        self.assertEqual(reversed_order[1], 0)

    def test_reverse_coordinates_4tuple(self):
        """
        Tests the function reverse_coordinate_order for a 4-tuple.
        """
        with self.assertRaises(ValueError):
            shapes.reverse_coordinate_order((1, 2, 3, 1))


class TestIsRectangleTestCase(TestCase):
    """
    Test class for function is_rectangle.
    """

    def test_for_clockwise_rectangle(self):
        """
        Tests the function is_rectangle for a clockwise rectangle.
        """
        rectangle = ((
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        ))
        self.assertEqual(shapes.is_rectangle(rectangle), True)

    def test_for_counterclockwise(self):
        """
        Tests the function is_rectangle for a counterclockwise rectangle.
        """
        rectangle = ((
            (0.0, 0.0),
            (50.0, 0.0),
            (50.0, 50.0),
            (0.0, 50.0),
            (0.0, 0.0)
        ))
        self.assertEqual(shapes.is_rectangle(rectangle), True)

    def test_less_than_four_segments(self):
        """
        Tests the function is_rectangle for fewer than four line segments.
        """

        # a triangle
        coords = (
            (0.0, 0.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(coords), False)

    def test_more_than_four_segments(self):
        """
        Tests the function is_rectangle for more than four line segments.
        """

        # a pentagon
        coords = (
            (0.0, 0.0),
            (0.0, 50.0),
            (25.0, 75.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(coords), False)

    def test_not_closed(self):
        """
        Tests the function is_rectangle for a series of coordinates that are
        not closed.
        """

        coords = (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 1.0)  # doesn't match first point
        )
        self.assertEqual(shapes.is_rectangle(coords), False)

    def test_top_bottom_not_parallel(self):
        """
        Tests the function is_rectangle for a polygon whose top and bottom sides
        are not parallel.
        """

        # top crooked
        polygon = (
            (0.0, 0.0),
            (0.0, 25.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

        # botton crooked
        polygon = (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (50.0, 25.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

    def test_left_right_not_parallel(self):
        """
        Tests the function is_rectangle for a polygon whose left and right sides
        are not parallel.
        """

        # left side crooked
        polygon = (
            (0.0, 0.0),
            (25.0, 50.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

        # right side crooked
        polygon = (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (25.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

    def test_no_width(self):
        """
        Tests the function is_rectangle for a polygon whose bottom or top is
        a point.
        """

        # top is point
        polygon = (
            (0.0, 0.0),
            (0.0, 50.0),
            (0.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

        # bottom is point
        polygon = (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (0.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

    def test_no_height(self):
        """
        Tests the function is_rectangle for a polygon whose side is a point.
        """

        # left side is point
        polygon = (
            (0.0, 0.0),
            (0.0, 0.0),
            (50.0, 50.0),
            (50.0, 0.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)

        # right side is point
        polygon = (
            (0.0, 0.0),
            (0.0, 50.0),
            (50.0, 50.0),
            (50.0, 50.0),
            (0.0, 0.0)
        )
        self.assertEqual(shapes.is_rectangle(polygon), False)


class CircleToRectangleTestCase(TestCase):
    """
    Test class for the function convert_circle_to_rectangle.
    """

    def test_at_equator(self):
        """
        Tests the function convert_circle_to_rectangle at the Equator.
        This makes it easier to calculate expected values.
        """
        coord = (-78.0, 0)
        radius_m = 10000
        square = shapes.convert_circle_to_rectangle(coord, radius_m)

        # check that the shape is correct
        self.assertEqual(shapes.is_rectangle(square[0]), True,
                         'Shape is not a rectangle')

        # check that the rectangle center is at the original point
        bounds = Bounds(*square.extent)
        self.assertAlmostEqual(square.centroid[0], coord[0], places=6,
                               msg='The center longitude is incorrect')
        self.assertAlmostEqual(square.centroid[1], coord[1], places=6,
                               msg='The center latitude is incorrect')

        # check that rectangle has the correct area
        area_in_sq_m = bounds.center_width_m * bounds.height_m
        actual_sq_km = units.sq_meters_to_sq_km(area_in_sq_m)
        expected_sq_km = (2 * radius_m / 1000)**2
        self.assertAlmostEqual(actual_sq_km, expected_sq_km, delta=0.001)

        # check that the rectangle contains the circle
        radius_in_degrees = units.convert_meters_to_degrees(radius_m, 'down')
        point = Point(coord)
        circle = point.buffer(radius_in_degrees)
        self.assertTrue(square.contains(circle))


class CalculateFarthestDistanceTestCase(TestCase):
    """
    Test class for the function calculate_farthest_dist_km.
    """

    def test_dist_for_triangle(self):
        """
        Tests the function calculate_farthest_dist_km for a triangle.
        """
        points = ((0, 10), (0, 20), (20, 15))
        target = (0, 15)
        actual = shapes.calculate_farthest_dist_km(points, target)
        expected = vincenty((15, 20), (15, 0)).kilometers
        self.assertEqual(actual, expected)

    def test_dist_for_empty_tuple(self):
        """
        Tests the function calculate_farthest_dist_km for an empty tuple.
        """
        points = ()
        target = (0, 15)
        actual = shapes.calculate_farthest_dist_km(points, target)
        expected = 0
        self.assertEqual(actual, expected)


class CalculateRadiusTestCase(TestCase):
    """
    Base test class for polygon and multipoylgon radius calculators.
    """
    fixtures = get_fixtures(['locations'])


class CalculatePolygonRadiusTestCase(CalculateRadiusTestCase):
    """
    Test class for the function calculate_polygon_radius_km.
    """

    def test_radius_for_rectangle(self):
        """
        Tests the function calculate_polygon_radius_km for a rectangle.
        """
        rectangle = Location.objects.get(pk=3)
        actual = shapes.calculate_polygon_radius_km(rectangle.geom)
        point = shapes.reverse_coordinate_order(rectangle.geom.centroid)
        expected = vincenty(point, (0, 1)).kilometers
        self.assertEqual(actual, expected)

    def test_radius_for_polygon(self):
        """
        Tests the function calculate_polygon_radius_km for a nonrectangular
        polygon.
        """
        polygon = Location.objects.get(pk=7)
        actual = shapes.calculate_polygon_radius_km(polygon.geom)
        point = shapes.reverse_coordinate_order(polygon.geom.centroid)
        expected = vincenty(point, (8, 0)).kilometers
        self.assertEqual(actual, expected)


class CalculateMultiPolygonRadiusTestCase(CalculateRadiusTestCase):
    """
    Test class for the calculate_multipoly_radius_km function.
    """

    def test_radius_for_multipolygon(self):
        """
        Test case for a rectangle.
        """
        multipolygon = Location.objects.get(pk=8)
        actual = shapes.calculate_multipoly_radius_km(multipolygon.geom)
        point = shapes.reverse_coordinate_order(multipolygon.geom.centroid)
        expected = vincenty(point, (20, 50)).kilometers
        self.assertEqual(actual, expected)


class FactorPolygonTestCase(TestCase):
    """
    Tests factor_polygon_into_circles function.
    """

    def _process_parameters(self, coord, radius_m):
        """
        Helper function to process test parameters through
        the factor_polygon_into_circles function.
        """
        radius_km = units.meters_to_km(radius_m)
        polygon = Polygon(coord)
        points = shapes.factor_polygon_into_circles(polygon, radius_km)

        # take the generated points and turn them into "circles" (polygons)
        radius_in_deg = units.convert_meters_to_degrees(radius_m)
        circles = [Point(point).buffer(radius_in_deg) for point in points]

        # convert the list of circles into a multipolyon and merge them
        merged_circles = MultiPolygon(circles).cascaded_union

        # make sure the merged circles have no holes and completely cover
        # the original polygon
        self.assertTrue(merged_circles.num_interior_rings == 0,
                        'The merged circles had %s holes but should have none'
                        % merged_circles.num_interior_rings)
        self.assertTrue(merged_circles.prepared.covers(polygon),
                        'The merged circles do not cover the polygon')

    def test_around_equator_1km_radius(self):
        """
        Tests the function factor_polygon_into_circles for a location around the
        Equator and a radius of 1 km.
        """
        coord = ((0.0, -0.01), (0.0, 0.01),
                 (0.025, 0.01), (0.05, -0.01), (0.0, -0.01))
        radius_m = 1000
        self._process_parameters(coord, radius_m)

    def test_nothern_lat(self):
        """
        Tests the function factor_polygon_into_circles for a location at a
        northern latitude and a radius of 1 km.
        """
        coord = ((-78.0, 0.23), (-78.0, 0.25),
                 (-79.5, 0.25), (-79.5, 0.23), (-78.0, 0.23))
        radius_m = 1000
        self._process_parameters(coord, radius_m)

    def test_nothern_lat_5km_radius(self):
        """
        Tests the function factor_polygon_into_circles for a location at a
        northern latitude and a radius of 5 km.
        """
        coord = ((-78.0, 0.23), (-78.0, 0.25),
                 (-79.5, 0.25), (-79.5, 0.23), (-78.0, 0.23))
        radius_m = 5000
        self._process_parameters(coord, radius_m)

    def test_far_nothern_lat_5km_radius(self):
        """
        Tests the function factor_polygon_into_circles for a location at a far
        northern latitude and a radius of 5 km.
        """
        coord = ((-78.0, 0.43), (-78.0, 0.45),
                 (-79.5, 0.45), (-79.5, 0.43), (-78.0, 0.43))
        radius_m = 5000
        self._process_parameters(coord, radius_m)

    def test_far_south_1000km_radius(self):
        """
        Tests the function factor_polygon_into_circles for a location at a far
        southern latitude and a radius of 1000 km.
        """
        coord = ((0.0, -0.43), (0.0, -0.45),
                 (1.0, -0.45), (1.0, -0.43), (0.0, -0.43))
        radius_m = 1000000
        self._process_parameters(coord, radius_m)

    def test_radius_too_small(self):
        """
        Tests the function factor_polygon_into_circles for a radius of 10 m.
        """
        coord = ((0.0, -0.01), (0.0, 0.01),
                 (0.025, 0.01), (0.05, -0.01), (0.0, -0.01))
        radius_km = 0.01

        with self.assertRaises(ValueError):
            polygon = Polygon(coord)
            shapes.factor_polygon_into_circles(polygon, radius_km)


class ConvertToPointTestCase(TestCase):
    """
    Test class for the function convert_to_point function.
    """

    def test_convert_dict_to_point(self):
        """
        Tests the convert_to_point function with a dictionary.
        """
        point = shapes.convert_to_point({'lat': 40, 'lon': 100}, 'lon')
        self.assertEqual(point[0], 100)
        self.assertEqual(point[1], 40)

    def test_convert_lat_list_to_point(self):
        """
        Tests the convert_to_point function with a list that starts with
        latitude.
        """
        point = shapes.convert_to_point([40, 100], 'lat')
        self.assertEqual(point[0], 100)
        self.assertEqual(point[1], 40)

    def test_convert_lon_list_to_point(self):
        """
        Tests the convert_to_point function with a list that starts with
        longitude.
        """
        point = shapes.convert_to_point([100, 40], 'lon')
        self.assertEqual(point[0], 100)
        self.assertEqual(point[1], 40)
