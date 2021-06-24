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

# standard library
import math


def meters_to_km(meters):
    """
    (int or float) -> float

    Takes a distance in meters and returns the distance in kilometers.
    """
    return meters / 1000.0


def km_to_meters(kilometers):
    """
    (int or float) -> float

    Takes a distance in kilometers and returns the distance in meters.
    """
    return kilometers * 1000.0


def sq_meters_to_sq_km(sq_meters):
    """
    (int or float) -> float

    Takes a distance in square meters and returns the distance in square
    kilometers.
    """
    return sq_meters / 1000000.0


def sq_km_to_sq_meters(kilometers):
    """
    (int or float) -> float

    Takes a distance in square kilometers and returns the distance in square
    meters.
    """
    return kilometers * 1000000.0


def km_to_mi(kilometers):
    """
    (int or float) -> float

    Takes a distance in kilometers and returns the distance in miles.
    """
    return kilometers * 0.62137119


def convert_meters_to_degrees(radius_m, rnd_dir='closest', places=7):
    """
    Takes a measurement in meters and, optionally, a direction in which to
    round the conversion and the number of decimal places for the result.
    Returns the degrees latitude at the Equator. Because the conversion is based
    on the circumference of the Earth at the Equator, conersions at other
    latitudes will not be accurate.
    """
    raw_degrees = radius_m / 111319.444

    conversion = {
        'closest': round(raw_degrees, places),
        'down': (math.floor(raw_degrees * 10**places)) / 10**places,
        'up': (math.ceil(raw_degrees * 10**places)) / 10**places
    }

    return conversion[rnd_dir]

