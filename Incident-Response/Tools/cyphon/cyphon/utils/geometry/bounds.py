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
Defines a Bounds class to help with calculating dimensions of geographic
bounds
"""

# third party
from django.contrib.gis.geos import Polygon
from geopy.distance import vincenty


class Bounds(object):
    """
    Defines a northernmost latitude, southernmost latitude, easternmost
    longitude, and westernmost longitude. Allows calculation of bounds
    dimmensions in meters, as well as creation of a bounding box.
    """

    def __init__(self, w_lng=180.0, s_lat=90.0, e_lng=-180.0, n_lat=-90.0):
        """
        IMPORTANT: Initialization arguments are ordered w, s, e, n in order
        to accept arguments from a GEOSGeometry extent, which is a 4-tuple
        consisting of (xmin, ymin, xmax, ymax). This makes it easy to
        initialize bounds directly, e.g.:

        >>> from django.contrib.gis.geos import Polygon
        >>> polygon = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
        >>> bounds = Bounds(*polygon.extent)

        """
        self._n_lat = n_lat
        self._s_lat = s_lat
        self._e_lng = e_lng
        self._w_lng = w_lng

    # TODO(LH): add validations for lat/lng values

    @property
    def n_lat(self):
        return self._n_lat

    @n_lat.setter
    def n_lat(self, value):
        self._n_lat = value

    @property
    def s_lat(self):
        return self._s_lat

    @s_lat.setter
    def s_lat(self, value):
        self._s_lat = value

    @property
    def e_lng(self):
        return self._e_lng

    @e_lng.setter
    def e_lng(self, value):
        self._e_lng = value

    @property
    def w_lng(self):
        return self._w_lng

    @w_lng.setter
    def w_lng(self, value):
        self._w_lng = value

    @property
    def ne_corner(self):
        return (self.e_lng, self.n_lat)

    @property
    def nw_corner(self):
        return (self.w_lng, self.n_lat)

    @property
    def se_corner(self):
        return (self.e_lng, self.s_lat)

    @property
    def sw_corner(self):
        return (self.w_lng, self.s_lat)

    @property
    def bounding_box(self):
        """
        Returns a rectangular geos Polygon constrained by the Bounds' latitude
        and longitude limits.
        """
        return Polygon((self.sw_corner, self.nw_corner, self.ne_corner,
                        self.se_corner, self.sw_corner))

    @property
    def center_width_m(self):
        """
        Returns the width of the bounding box at its center latitude, in meters.
        """
        ave_lat = (self.n_lat + self.s_lat) / 2
        return vincenty((ave_lat, self.w_lng), (ave_lat, self.e_lng)).meters

    @property
    def height_m(self):
        """
        Returns the height of the bounding box in meters.
        """
        nw_pt = (self.n_lat, self.w_lng)
        sw_pt = (self.s_lat, self.w_lng)
        return vincenty(nw_pt, sw_pt).meters

    def get_width_at_latitude_m(self, lat):
        """
        Returns the width of the bounding box at the given latitude, in meters.
        """
        east = (lat, self.e_lng)
        west = (lat, self.w_lng)
        return vincenty(east, west).meters

    def buffer(self, buffer_m):
        """
        Takes a buffer distance in meters and extends the bounds by that
        distance. Uses the average latitude of the current bounds to calculate
        new latitude bounds. Over extremely large latitude bounds, the results
        will lose accuracy.
        """
        calculator = vincenty(meters=buffer_m)

        ave_lng = (self.w_lng + self.e_lng) / 2
        ave_lat = (self.n_lat + self.s_lat) / 2

        self.n_lat = calculator.destination((self.n_lat, ave_lng), 0).latitude
        self.s_lat = calculator.destination((self.s_lat, ave_lng), 180).latitude
        self.e_lng = calculator.destination((ave_lat, self.e_lng), 90).longitude
        self.w_lng = calculator.destination((ave_lat, self.w_lng), 270).longitude

        return self
