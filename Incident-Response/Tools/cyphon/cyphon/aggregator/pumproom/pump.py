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
Defines a Pump class, which coordinates the process of passing a ReservoirQuery
to an API and saving the results.
"""

# standard library
from collections import deque
import logging

# third party
from django.utils.functional import cached_property

# local
from aggregator.pumproom.engineer import Engineer
from aggregator.pumproom.exceptions import (
    PipeDoesNotExist,
    SpecsheetDoesNotExist,
)
from aggregator.pumproom.streamcontroller import StreamController
from cyphon.transaction import close_old_connections

LOGGER = logging.getLogger(__name__)


class Pump(object):
    """
    Coordinates the process of sending a |ReservoirQuery| to a
    |Reservoir| and retrieving the results.

    Attributes
    ----------
    reservoir : Reservoir
        A |Reservoir| representing an external data platform from which
        data should be retreved.

    task : str
        The type of task being performed. Corresponds to a value in
        |SEARCH_TASK_CHOICES|.

    user : AppUser
        The |AppUser| making the request.

    container : Container
        A |Container| to store the results.

    """

    def __init__(self, reservoir, task, user=None):
        self.reservoir = reservoir
        self.task = task
        self.user = user

    def __str__(self):
        return str(self._pipe)

    @cached_property
    def _pipe(self):
        """
        The Pipe that should be used for the |Pump|'s :attr:`~Pump.task`.
        """
        pipe = self.reservoir.get_pipe(self.task)
        if pipe:
            return pipe
        else:
            error_msg = 'The Reservoir "%s" has no Pipe for the Task "%s"'
            raise PipeDoesNotExist(error_msg % (self.reservoir, self.task))

    @cached_property
    def _faucet(self):
        """

        """
        return self._pipe.create_request_handler(
            user=self.user,
            params={'task': self.task}
        )

    @cached_property
    def _plumber(self):
        """

        """
        return self._faucet.emissary

    @cached_property
    def _specsheet(self):
        """
        Returns the SpecSheet associated with the Pump's Pipe.
        """
        if hasattr(self._pipe, 'specsheet'):
            return self._pipe.specsheet
        else:
            error_msg = 'The Pipe "%s" has no Specsheet'
            raise SpecsheetDoesNotExist(error_msg % self._pipe)

    def _is_stream(self):
        """
        Returns a Boolean indicating whether the Pump's Pipe is for a
        streaming API.
        """
        return self._specsheet.streaming

    def _factor_query(self, query):
        """
        Takes a ReservoirQuery and returns it as a list of one or more
        ReservoirQueries formatted for the Pump's Pipe.
        """
        engineer = Engineer(query=query, specs=self._specsheet)
        return engineer.factor_query()

    def _create_stream_controller(self, query):
        """
        Returns an instance of an ApiHandler subclass to contact the API
        associated with the Pump's Pipe.
        """
        return StreamController(faucet=self._faucet, query=query)

    def _process_streaming_query(self, query):
        """


        Takes a ReservoirQuery and, if a stream for the query is not currently
        running, starts a stream and saves an Invoice of the API call. Returns

        """
        controller = self._create_stream_controller(query)
        return controller.process_query()

    def _process_nonstreaming_query(self, query):
        """



        Takes a ReservoirQuery, passes it to the Pump's ApiHandler for
        processing, and saves an Invoice of the API call. Returns
        """
        # send query to API
        self._faucet.run(query)

        return self._faucet.process_results()

    def _process_nonstreaming_queries(self, queries):
        """


        Takes a list of ReservoirQueries and processes each through the
        Pump's Pipe. Returns
        """
        results = []
        query_queue = deque(queries)

        while len(query_queue) > 0:
            query = query_queue.popleft()
            result = self._process_nonstreaming_query(query)
            if isinstance(result, list):
                results.extend(result)
            else:
                results.append(result)

        return results

    def get_time_requirements(self, query_cnt):
        """
        Takes an integer query_cnt, representing the number of queries that
        need to be performed, and returns a float representing the number of
        minutes required to fulfill all the queries, given the rate limit of
        the API.
        """
        return self._plumber.calculate_query_time_in_minutes(query_cnt)

    @close_old_connections
    def start(self, query):
        """Send a query to the Pump's Reservoir.

        Parameters
        ----------
        query : |ReservoirQuery|
            The query to be sent to the |Reservoir|.

        Returns
        -------
        |list| of |Invoice| or |None|
            If the |Pump| uses a non-streaming API, returns a |list|
            of |Invoices|. If the |Pump| uses a streaming API,
            returns None (since a discrete set of results is not
            available).

        Notes
        -----
        If the Pipe is using a streaming API, it will start a stream as
        a daemon thread.

        Warning
        -------
        If the number of parameters in the `query` exceeds the number
        of parameters allowed by the API that the Pump is using, the
        query will be reformatted into smaller subqueries. If the Pump
        is using a streaming API, only the first subquery will be
        submitted to the API.

        """
        queries = self._factor_query(query)

        if self._specsheet:
            if self._is_stream():
                if len(queries) > 1:
                    LOGGER.warning('Query was too large for Pipe "%s." '
                                   'A smaller version of the query was '
                                   'submitted.', self._pipe)
                return self._process_streaming_query(queries[0])
            else:
                return self._process_nonstreaming_queries(queries)
        else:
            LOGGER.error('The Pipe %s is missing a Specsheet.', self.endpoint)
