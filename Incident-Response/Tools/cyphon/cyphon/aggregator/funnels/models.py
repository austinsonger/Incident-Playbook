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
Defines a |Funnel| class, which funnels data from a |Pipe| through a
|DataCondenser| and into a |Bottle|.

Notes
-----

The |Funnel| class provides an intermediary model that controls the
many-to-many relationship between |DataCondensers| and |Pipes|.
It ensures that each |Pipe| is connected to only one |DataCondenser|
per |Bottle|.

**Rationale:**

In most cases, different |Pipes| will return data in different forms
(e.g., a tweet vs. an Instagram post). Thus, |Pipes| usually need
different |DataCondensers| to store data in a particular |Bottle|.
In some cases, however, |Pipes| may return data using the same model
(e.g., tweets returned by Twitter's Search API and Public Streams API).
In these cases, |Pipes| may use the same |DataCondenser| to store data
in a |Bottle|.

From the reverse persective, data from the same |Pipe| can be modeled
in different ways (i.e., stored in different |Bottles|). Thus, it is
possible for a |Pipe| to have more than one |Bottle| associated with it.

|DataCondensers| therefore have a many-to-one relationship with |Bottles|
and a many-to-many relationship with |Pipes|.

|Funnels| control these relationships to ensure that data flowing from
a |Pipe| have only one way to make into a given |Bottle|.

"""

# standard library
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# local
from aggregator.pipes.models import Pipe
from bottler.bottles.models import Bottle
from sifter.datasifter.datacondensers.models import DataCondenser

LOGGER = logging.getLogger(__name__)


class FunnelManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, bottle_name, pipe_natural_key):
        """
        Allows retrieval of a |Funnel| by its natural key instead of its
        primary key.

        Parameters
        ----------

        bottle_id : str
            The primary key of the |Bottle| associated with the |Funnel|.

        pipe_natural_key : list of str


        """
        pipe = Pipe.objects.get_by_natural_key(*pipe_natural_key)
        try:
            return self.get(bottle__name=bottle_name, pipe=pipe.pk)
        except ObjectDoesNotExist:
            LOGGER.error('%s for Bottle "%s" and Pipe %s does not exist',
                         self.model.__name__, bottle_name, pipe.pk)

    def get_condenser(self, bottle_name, pipe_natural_key):
        """
        Gets the |DataCondenser| used for saving data from the specified
        |Pipe| in the specified |Bottle|.
        """
        funnel = self.get_by_natural_key(bottle_name, pipe_natural_key)
        return funnel.condenser

    def get_bottle(self, condenser_id, pipe_id):
        """
        Takes the primary key of a |DataCondenser| and gets the primary
        key of the |Bottle| associated with it.
        """
        funnel = self.get(condenser=condenser_id, pipe=pipe_id)
        return funnel.bottle


class Funnel(models.Model):
    """
    An intermediary model that funnels data from |Pipes| into a
    |DataCondenser|. This class controls the many-to-many relationship
    between |DataCondensers| and |Pipes|. It ensures that each |Pipe|
    uses only one |DataCondenser| per |Bottle|.
    """
    pipe = models.ForeignKey(Pipe)
    bottle = models.ForeignKey(Bottle)
    condenser = models.ForeignKey(DataCondenser)

    objects = FunnelManager()

    class Meta:
        """
        Metadata options for a Django Model.
        """
        unique_together = ('bottle', 'pipe')

    def __str__(self):
        return "%s <- %s" % (self.bottle, self.pipe)
