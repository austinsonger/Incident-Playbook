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
Defines a |Visa| class for storing an API rate limit.
"""

# third party
from django.db import models

# local
from cyphon.choices import TIME_UNIT_CHOICES
from cyphon.models import GetByNameManager
from utils.dateutils import dateutils as dt


class Visa(models.Model):
    """
    Defines an API rate limit. Specifies the number of requests (calls)
    that can be made in a given time interval.

    Attributes
    ----------
    name : str
        The identifier for the |Visa|.

    calls : int
        The number of requests allowed in the rate limit interval.

    time_interval : int
        The number of units in the rate limit interval. The type of
        unit is specified by the :attr:`~Visa.time_unit` attribute.

    time_unit : str
        Defines the units of measure for the :attr:`~Visa.time_interval`.
        Choices are limited to |TIME_UNIT_CHOICES|.

    """
    name = models.CharField(max_length=40, unique=True)
    calls = models.IntegerField()
    time_interval = models.IntegerField()
    time_unit = models.CharField(max_length=3, choices=TIME_UNIT_CHOICES)

    objects = GetByNameManager()

    def __str__(self):
        return self.name

    def get_request_interval_in_minutes(self):
        """Get the number of minutes in the rate limit interval.

        Returns
        -------
        int
            The number of minutes in the rate limit interval.

        """
        return dt.convert_time_to_whole_minutes(self.time_interval,
                                                self.time_unit)

