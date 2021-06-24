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
Defines a Stream class for saving the status of a stream.
"""

# standard library
import logging

# third party
from django.db import models
from django.db.utils import OperationalError

# local
from aggregator.invoices.models import Invoice
from aggregator.pipes.models import Pipe
from ambassador.passports.models import Passport

_LOGGER = logging.getLogger(__name__)


class StreamManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def find_stream(self, faucet):
        """
        Checks whether a Stream associated with the StreamController's ApiHandler
        already exists in the database. If so, returns the Stream object;
        otherwise, returns None.
        """
        (stream, dummy_created) = self.get_or_create(pipe=faucet.endpoint,
                                                     auth=faucet.passport)
        return stream

    def close_all(self):
        """Set all |Streams| to inactive.

        Catches and logs any `:class:~OperationalError` raised when
        attempting to close |Streams|.

        Returns
        -------
        None

        """
        try:
            self.update(active=False)
        except OperationalError as err:
            _LOGGER.error('An error occurred while closing Streams: %s', err)


class Stream(models.Model):
    """
    Records the status of a streaming API connection.
    """
    pipe = models.ForeignKey(Pipe)
    auth = models.ForeignKey(Passport)
    record = models.ForeignKey(Invoice, null=True, blank=True)
    active = models.BooleanField(default=False)

    objects = StreamManager()

    class Meta:
        unique_together = ['pipe', 'auth']

    def __str__(self):
        return '%s: %s' % (self.pipe, self.auth.name)

    def save_as_closed(self):
        """
        Sets active to False.
        """
        self.active = False
        self.save()

    def save_as_open(self, record):
        """
        Sets active to True.
        """
        self.record = record
        self.active = True
        self.save()

    def _query_is_unchanged(self, query):
        """
        Takes a ReservoirQuery
        """
        query_dict = query.to_dict()
        self.record.query.pop('timeframe', None)
        query_dict.pop('timeframe', None)
        return query_dict == self.record.query

    def is_running(self, query):
        """
        query : |ReservoirQuery|

        Returns a Boolean indicating whether the StreamController's query is
        already being processed by a thread.
        """
        return self.active and \
            self.record and \
            self._query_is_unchanged(query)
