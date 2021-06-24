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
Defines a Taste class used to display a teaser for distilled data.
A Taste provides basic information about the data, specifing "Who,"
"What," "When," and "Where."
"""

# standard library
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# local
from bottler.containers.models import Container
from teasers.models import Teaser

LOGGER = logging.getLogger(__name__)


class TasteManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, name):
        """
        Allow retrieval of a Taste by its natural key instead of its primary key.
        """
        container = Container.objects.get_by_natural_key(name)
        try:
            return self.get(container=container)
        except ObjectDoesNotExist:
            LOGGER.error('%s for Container "%s" does not exist',
                         self.model.__name__, container)


class Taste(Teaser):
    """
    The Taste class specifies which fields of distilled data should be
    used to construct a teaser for those data. A Taste defines a
    crosswalk between the fields of a teaser and the fields in a
    |Container|. Nested fields (as for embedded documents) should be
    indicated with dot notation (e.g. 'user.name').

    The Taste is used to answer basic questions about a document, e.g.,
    Who?, What?, When?, and Where?.

    """
    container = models.OneToOneField(Container, primary_key=True)

    objects = TasteManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['container']

    def __str__(self):
        return str(self.container)
