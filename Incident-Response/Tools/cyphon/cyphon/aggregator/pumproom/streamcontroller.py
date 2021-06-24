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
Defines a StreamController class, which handles queries for streaming APIs.
"""

# standard library
import logging
import threading

# third party
from django.db import transaction
from django.utils.functional import cached_property

# local
from aggregator.streams.models import Stream
from cyphon.transaction import require_lock

_LOGGER = logging.getLogger(__name__)


class StreamController(object):
    """
    Attributes
    ----------
    query : dict

    """
    def __init__(self, faucet, query):
        self.faucet = faucet
        self.query = query

    @property
    def stream(self):
        """
        Checks whether a Stream associated with the StreamController's
        ApiHandler already exists in the database. If so, returns the
        Stream object; otherwise, returns a newly created Stream object.
        """
        return Stream.objects.find_stream(self.faucet)

    def _run_faucet(self):
        """
        Passes the StreamController's query to the Pump's ApiHandler for
        processing. Updates Stream record as active and saves the
        current query.

        """
        try:
            # make the API call
            self.faucet.start(self.query)

        except Exception as error:
            _LOGGER.exception('An error occurred in the stream: %s', error)
            self.faucet.ensure_cargo()

        # update the Invoice
        self.faucet.stop()

        # update the Stream
        self.stream.save_as_closed()

    def _start_stream(self):
        """
        Starts a daemon thread to process the StreamController's query.
        Returns the created thread.
        """
        thread = threading.Thread(target=self._run_faucet)
        thread.daemon = True
        thread.start()
        return thread

    def _query_is_running(self):
        """
        Returns a Boolean indicating whether the StreamController's
        query is already being processed by a thread.
        """
        return self.stream.is_running(self.query)

    @transaction.atomic
    @require_lock(Stream, 'ACCESS EXCLUSIVE')
    def process_query(self):
        """
        Checks if a stream for the ReservoirQuery is already running. If not,
        starts a stream, updates the Stream object keeping track of the stream,
        and returns True. Otherwise, does nothing with the query and returns
        False.
        """
        if not self._query_is_running():

            # create an Invoice for the call
            self.faucet.prepare(self.query)
            record = self.faucet.record

            # associate the Invoice with the Stream
            self.stream.save_as_open(record)

            self._start_stream()
            return True
        else:
            return False
