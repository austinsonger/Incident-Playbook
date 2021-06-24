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
Provides subclasses and mixins to add functionality to Django's default
model |Manager|.
"""

# standard library
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class GetByNameMixin(object):
    """
    Mixin for a |Manager| that provides a method for finding an object
    by its unique `name`.
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
            logging.getLogger(self.__module__).error('%s "%s" does not exist',
                                                     self.model.__name__, name)


class FindEnabledMixin(object):
    """
    Mixin for a |Manager| that provides a method for finding enabled
    objects.
    """

    def find_enabled(self):
        """Find enabled objects.

        Returns
        -------
        |QuerySet|
            A |QuerySet| of objects for which `enabled` is set to |True|.

        """
        default_queryset = self.get_queryset()
        return default_queryset.filter(enabled=True)


class GetByNameManager(models.Manager, GetByNameMixin):
    """
    A |Manager| that provides a `get_by_natural_key` method based on the
    object's `name`.
    """
    pass


class SelectRelatedManager(models.Manager):
    """
    A |Manager| whose default queryset includes related object data.
    """

    def get_queryset(self):
        """Get the default |QuerySet| for the model manager.

        Overrides the default get_queryset method. Includes related
        object data in search results to avoid additional database
        queries.

        Returns
        -------
        |QuerySet|
            A |Queryset| which selects related objects.

        See Also
        --------
        See Django's documentation for the `select related`_ method of a
        |QuerySet|.

        """
        default_queryset = super(SelectRelatedManager, self).get_queryset()
        return default_queryset.select_related()

