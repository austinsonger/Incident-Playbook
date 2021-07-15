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
Defines a class for a location (search area).
"""

# standard library
import logging

# third party
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# local
from utils.geometry import shapes, units

_LOGGER = logging.getLogger(__name__)


class LocationManager(models.GeoManager):
    """A GeoManager to allow geoqueries on |Locations|.

    Notes
    -----
    We can't use mixins with this class due to issues with mocking
    `django.contrib.gis.db` when building docs in Python 3.5 on
    Read The Docs.

    """

    def get_by_natural_key(self, name):
        """Get an object by its unique `name`.

        Parameters
        ----------
        name : str
            The object's `name`.

        Returns
        -------
        |Model|
            The |Model| object with the specified `name`.

        """
        try:
            return self.get(name=name)
        except ObjectDoesNotExist:
            _LOGGER.error('%s "%s" does not exist', self.model.__name__, name)


class Location(models.Model):
    """
    A geographic area that can be used in constructing a social media query.
    """
    name = models.CharField(max_length=255, unique=True)
    geom = models.GeometryField()
    buffer_m = models.PositiveIntegerField(default=0)   # buffer in meters
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   blank=True, null=True)
    editable = models.BooleanField(default=True)

    # use GeoManager to allow geoqueries
    objects = LocationManager()

    def __str__(self):
        """
        Returns a string providing the name of the location and the GeoJSON
        feature type (Point, Polygon, etc.), as determined by its GEOSGeometry
        class name.
        """
        return '%s <%s>' % (self.name, type(self.geom).__name__)

    def get_buffer(self):
        """
        Returns the buffer zone in meters.
        """
        return self.buffer_m

    def has_buffer(self):
        """
        Returns a Boolean indicating whether a Location has a buffer zone.
        """
        return self.buffer_m > 0

    @property
    def centroid(self):
        """
        Returns the centroid of the location.
        """
        return self.geom.centroid

    @property
    def shape(self):
        """
        Returns a string indicating the feature type. If the feature type is not
        a Point, Polygon, or Multipolygon, returns 'Other'.
        """
        if isinstance(self.geom, Point):
            if self.has_buffer():
                return 'Circle'
            else:
                return 'Point'

        elif isinstance(self.geom, Polygon):
            if shapes.is_rectangle(self.geom.exterior_ring):
                return 'Rectangle'
            else:
                return 'Polygon'

        elif isinstance(self.geom, MultiPolygon):
            return 'MultiPolygon'

        else:
            return 'Other'

    @property
    def bbox(self):
        """
        If the Location is a Circle, Rectangle, Polygon, or MultiPolygon,
        returns the smallest rectangle that encompasses the Location's
        geometry. Otherwise returns None.
        """
        if self.shape == 'Circle':
            return shapes.convert_circle_to_rectangle(self.geom, self.buffer_m)

        elif self.shape == 'Rectangle':
            return self.geom

        elif self.shape in ('Polygon', 'MultiPolygon'):
            return self.geom.envelope

        else:
            return None

    @property
    def radius_km(self):
        """
        If the Location is a Circle, Rectangle, Polygon, or Multipolygon,
        returns the distance in kilometers between the geometry's centroid and
        the point on the geometry farthest from the centroid. Otherwise returns
        None.
        """
        if self.shape == 'Circle':
            return units.meters_to_km(self.buffer_m)

        elif self.shape in ('Rectangle', 'Polygon'):
            return shapes.calculate_polygon_radius_km(self.geom)

        elif self.shape == 'MultiPolygon':
            return shapes.calculate_multipoly_radius_km(self.geom)

        else:
            return None

    def get_bbox(self):
        """
        Returns a Location based on the object's bounding box.
        """
        return Location(
            geom=self.bbox,
            name=self.name + '-bbox',
            created_by=self.created_by
        )

    def get_radius(self):
        """
        Returns a Location based on the object's radius.
        """
        return Location(
            geom=self.centroid,
            buffer_m=units.km_to_meters(self.radius_km),
            name=self.name + '-radius',
            created_by=self.created_by
        )

    def _create_radius(self, point, new_radius):
        """

        """
        return Location(
            geom=Point(point),
            buffer_m=new_radius,
            name=self.name + '-factored',
            created_by=self.created_by
        )

    def factor_by_radius_km(self, radius_km):
        """
        Takes a Location and a radius in kilometers. Returns a list of Locations
        representing circles of the specified radius that together cover the
        area of the original Location.
        """
        if self.shape == 'Other':  # pragma: no cover
            raise ValueError('Shape must be Point, Polygon, or Muiltpolygon')

        polygon = self.bbox
        points = shapes.factor_polygon_into_circles(polygon, radius_km)
        radius = units.km_to_meters(radius_km)
        return [self._create_radius(point, radius) for point in points]
