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
Defines a Sample class to create a teaser for data from a |Pipe|.
A Sample provides basic information about the data, specifing "Who,"
"What," "When," and "Where."
"""

# standard library
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# local
from aggregator.pipes.models import Pipe
from teasers.models import Teaser

LOGGER = logging.getLogger(__name__)


class SampleManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, platform, api_class):
        """
        Allow retrieval of a Sample by its natural key instead of its
        primary key.
        """
        pipe = Pipe.objects.get_by_natural_key(platform, api_class)
        try:
            return self.get(pipe=pipe)
        except ObjectDoesNotExist:
            LOGGER.error('%s for Pipe "%s %s" does not exist',
                         self.model.__name__, platform, api_class)


class Sample(Teaser):
    """
    The Sample class specifies which fields of distilled data should be
    used to construct a teaser for those data. A Taste defines a
    crosswalk between the fields of a teaser and the fields in a
    |Container|. Nested fields (as for embedded documents) should be
    indicated with dot notation (e.g. 'user.name').

    The Sample is used to answer basic questions about a document, e.g.,
    Who?, What?, When?, and Where?.

    """
    pipe = models.OneToOneField(Pipe, primary_key=True)

    objects = SampleManager()

    def __str__(self):
        return str(self.pipe)

