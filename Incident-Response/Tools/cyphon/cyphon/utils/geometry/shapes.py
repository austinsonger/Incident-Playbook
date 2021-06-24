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
Provides functions for measuring and transforming geometries.
"""

# standard library
import math
import logging

# third party
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from geopy.distance import vincenty

# local
from utils.geometry.bounds import Bounds

LOGGER = logging.getLogger(__name__)


def reverse_coordinate_order(coords):
    """
    Takes a tuple of (lat, lng) or (lng, lat) coordinates and reverses their
    order.
    """
    if len(coords) != 2:
        raise ValueError('coordinates must contain exactly 2 points')
    return (coords[1], coords[0])


def sides_parallel(coords, clockwise=True):
    """
    Takes a 5-tuple of (x, y) coordinate tuples for a clockwise or
    counterclockwise quadrilateral. Assumes coordinates start at
    (min_x, min_y) and end at (min_x, min_y). Returns True if the
    coordinates define a rectangle. Otherwise returns False.
    """
    if len(coords) != 5:  # pragma: no cover
        raise ValueError('quadrilateral must contain exactly 5 coordinates')

    # get coordinates for [bottom left, top left, top right, bottom right]
    if clockwise:
        corners = [coords[0], coords[1], coords[2], coords[3]]
    else:
        corners = [coords[0], coords[3], coords[2], coords[1]]

    # get (x, y) values for each corner
    (c0_min_x, c0_min_y) = corners[0]   # bottom left
    (c1_min_x, c1_max_y) = corners[1]   # top left
    (c2_max_x, c2_max_y) = corners[2]   # top right
    (c3_max_x, c3_min_y) = corners[3]   # bottom right

    left_rt_parallel = (c0_min_x == c1_min_x and c2_max_x == c3_max_x)
    top_btm_parallel = (c0_min_y == c3_min_y and c1_max_y == c2_max_y)

    has_width = (c0_min_x != c2_max_x and c1_min_x != c3_max_x)
    has_height = (c0_min_y != c1_max_y and c3_min_y != c2_max_y)

    return left_rt_parallel and top_btm_parallel and has_width and has_height


def is_rectangle(coords):
    """
    (tuple(tuple(float or int, float or int))) -> Boolean

    Takes a tuple of (x, y) coordinate tuples. Returns True if the
    coordinates represent a rectangle. Otherwise returns False.
    """
    # look for four segments defined by five points
    has_four_segments = (len(coords) == 5)

    if has_four_segments:

        # the fifth point should be the same as the first
        is_closed = (coords[0] == coords[4])

        if is_closed:

            # test sides for both clockwise or counterwise ordering of points
            return sides_parallel(coords, clockwise=True) or \
                sides_parallel(coords, clockwise=False)
        else:
            return False
    else:
        return False


def convert_circle_to_rectangle(point, radius_m):
    """
    (tuple(int or float, int or float), int or float) -> GEOSGeometry Polygon

    Takes a circle as a (lng, lat) tuple and a radius in meters. Returns the
    smallest rectangular Polygon that encompasses the circle.
    """
    # reverse the lng, lat order to convert to geopy Point format
    center = reverse_coordinate_order(point)

    # create a geopy coordinate calculator for the given distance
    calculator = vincenty(meters=radius_m)

    # calculate points at the given distance in the cardinal directions
    n_pt = calculator.destination(point=center, bearing=0)
    s_pt = calculator.destination(point=center, bearing=180)
    e_pt = calculator.destination(point=center, bearing=90)
    w_pt = calculator.destination(point=center, bearing=270)

    bounds = Bounds(n_lat=n_pt.latitude, s_lat=s_pt.latitude,
                    e_lng=e_pt.longitude, w_lng=w_pt.longitude)

    return bounds.bounding_box


def calculate_farthest_dist_km(points, target):
    """
    (tuple(tuple(lng, lat)), tuple(lng, lat)) -> float

    Takes a tuple of (lng, lat) points and a (lng, lat) target. Returns the
    distance in kilometers between the target and the point farthest from the
    target.
    """
    target_pt = reverse_coordinate_order(target)  # need (lat, lng) for vincenty
    max_radius_km = 0

    for point in points:
        point = reverse_coordinate_order(point)  # need (lat, lng) for vincenty
        distance = vincenty(point, target_pt).kilometers
        if distance > max_radius_km:
            max_radius_km = distance

    return max_radius_km


def calculate_polygon_radius_km(polygon):
    """
    Takes a GEOSGeometry Polygon and returns the distance in kilometers
    between the Polygon's centroid and the point on the polygon farthest
    from the centroid.
    """
    if not isinstance(polygon, Polygon):  # pragma: no cover
        raise TypeError('object is not a Polygon')
    target = polygon.centroid
    points = polygon.exterior_ring
    return calculate_farthest_dist_km(points, target)


def calculate_multipoly_radius_km(multipolygon):
    """
    Takes a GEOSGeometry MultiPolygon and returns the distance in kilometers
    between the MultiPolygon's centroid and the point on the MultiPolygon
    farthest from the centroid.
    """
    if not isinstance(multipolygon, MultiPolygon):  # pragma: no cover
        raise TypeError('object is not a MultiPolygon')

    target = multipolygon.centroid
    max_radius_km = 0

    for polygon in multipolygon:
        points = polygon.exterior_ring
        distance = calculate_farthest_dist_km(points, target)
        if distance > max_radius_km:
            max_radius_km = distance

    return max_radius_km


def create_buffered_bounds(polygon, buffer_m):
    """
    Takes a GEOSGeometry Polygon and a buffer distance in meters.
    Returns a Bounds object representing the polygon bounds buffered
    by the specified distance.
    """
    if not isinstance(polygon, Polygon):  # pragma: no cover
        raise TypeError('object is not a Polygon')
    return Bounds(*polygon.extent).buffer(buffer_m)


def calculate_circle_spacing(radius_m, overlap_m=0):
    """
    Takes a radius in meters and an overlap in meters. Calculates the minimum
    spacing of circles of the given radius that will ensure no gaps between
    them. This is equal to the width of a square that fits inside the circle.
    The overlap insures against gaps between circles when used to calculate
    geographic coordinates.
    """
    if radius_m <= overlap_m:  # pragma: no cover
        raise ValueError('radius_m must be greater than overlap_m')
    return (2 * radius_m / math.sqrt(2)) - overlap_m


def factor_polygon_into_circles(polygon, radius_km):
    """
    Takes a GEOSGeomtery Polygon and a radius in kilometers. Returns a list
    of (lng, lat) tuples representing the centers of circles of the specified
    radius that together cover the area of the Polygon.
    """
    safety_buffer = 0.01  # small safety buffer for overlap

    if not isinstance(polygon, Polygon):
        raise TypeError('object is not a Polygon')

    if radius_km <= safety_buffer:
        raise ValueError('radius must be greater than safety buffer')

    # get the bounds of the polygon with a small safety buffer
    buffer_dist_m = (radius_km * 1000) * safety_buffer
    bounds = create_buffered_bounds(polygon, buffer_dist_m)

    # get the space between circle centers, with a safety margin of 10 meters
    dist_bw_centers_m = calculate_circle_spacing(radius_km * 1000, overlap_m=10)

    # create a coordinate calculator for the increment distance
    calculator = vincenty(meters=dist_bw_centers_m)

    points = []  # array for collecting the circle centers

    # position first point so the circle intersects with the sw corner of bounds
    starting_pt = vincenty(kilometers=radius_km).destination(
        point=(bounds.s_lat, bounds.w_lng),
        bearing=45
    )

    # get the starting latitude
    lat = starting_pt.latitude

    # find the number of rows of circles needed to span the height of the polygon
    rows = int(math.ceil(bounds.height_m / dist_bw_centers_m))

    for dummy_row_idx in range(rows):

        # reset the starting longitude before each west-to-east loop
        lng = starting_pt.longitude

        # get the distance between w_lng and e_lng at the current latitude
        width_m = bounds.get_width_at_latitude_m(lat)

        # find the number of columns of circles needed to span the width
        cols = int(math.ceil(width_m / dist_bw_centers_m))

        for dummy_col_idx in range(cols):

            # add current coordinates to point array
            points.append((lng, lat))

            # calculate next point to the east and increment longitude
            lng = calculator.destination(point=(lat, lng), bearing=90).longitude

        # calculate next point to the north and increment latitude
        lat = calculator.destination(point=(lat, lng), bearing=0).latitude

    return points


def convert_to_point(location, location_format):
    """
    Takes a dict, tuple, or list of coordinates and converts them to a
    Point.
    """
    if isinstance(location, Point):
        return location
    try:
        if (isinstance(location, dict) and
                'lat' in location and 'lon' in location):
            return Point(location['lon'], location['lat'])
        if location_format.lower().startswith('lat'):
            location = reverse_coordinate_order(location)
        return Point(location)
    except Exception as error:
        LOGGER.error('There was an error processing the location %s: %s',
                     location, error)
