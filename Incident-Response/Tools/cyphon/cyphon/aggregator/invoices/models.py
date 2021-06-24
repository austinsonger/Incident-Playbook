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
Defines an |Invoice| class for logging API calls to |Reservoirs|.
"""

# standard library
from collections import OrderedDict
import json

# third party
from django.contrib.postgres.fields.jsonb import JSONField
from django.db import models

# local
from ambassador.records.models import Record, RecordManager
from cyphon.choices import SEARCH_TASK_CHOICES


class Invoice(Record):
    """
    Provides a record of an API call, including the |Stamp| associated
    with the call and the |ReservoirQuery| that was sent.

    Attributes
    ----------

    stamp : Stamp
        The |Stamp| associated with the API call.

    query : dict
        A |dict| representation of the |ReservoirQuery| sent to the API.

    task : str


    """
    query = JSONField(default=dict)
    task = models.CharField(max_length=20, choices=SEARCH_TASK_CHOICES)

    objects = RecordManager()

    def __str__(self):
        return str(self.stamp)

    def query_str(self):
        """
        Returns a JSON string representing the :attr:`~Invoice.query`.
        """
        ordered_query = OrderedDict(sorted(self.query.items()))
        return json.dumps(ordered_query, indent=4)

    query_str.short_description = 'query'
