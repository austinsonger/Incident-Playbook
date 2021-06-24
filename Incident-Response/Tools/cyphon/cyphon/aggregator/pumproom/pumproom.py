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
Defines a |PumpRoom| class, which coordinates the process of passing a
|ReservoirQuery| to selected APIs and aggregating the results.
"""

# standard library
import logging
import threading

# local
from aggregator.pumproom.pump import Pump

LOGGER = logging.getLogger(__name__)


class PumpRoom(object):
    """
    Coordinates the process of sending a |ReservoirQuery| to set of
    |Reservoirs| and aggregating the results.

    Attributes
    ----------
    reservoirs : `QuerySet` of `Reservoirs`
        A |QuerySet| of |Reservoirs| from which data should be retrieved.

    task : str
        The type of task being performed. Corresponds to a value in
        |SEARCH_TASK_CHOICES|.

    user : AppUser
        The |AppUser| making the request.

    """

    def __init__(self, reservoirs, task, user=None):
        self.reservoirs = reservoirs
        self.task = task
        self.user = user
        self.records = []  # Invoices for the API calls made

    def _create_pump(self, reservoir):
        """
        Takes a Reservoir and creates a Pump to pull data from that Reservoir,
        appropriate to the PumpRoom's user and task.
        """
        return Pump(
            reservoir=reservoir,
            task=self.task,
            user=self.user,
        )

    def _start_pump(self, pump, query):
        """
        Takes a Pump and a ReservoirQuery and starts the Pump with that
        query. Adds the result to the PumpRoom's records.
        """
        records = pump.start(query)
        if isinstance(records, list):
            self.records.extend(records)
        else:
            self.records.append(records)

    def get_results(self, query):
        """Get query results from the PumpRoom's Reservoirs.

        Parameters
        ----------
        query : |ReservoirQuery|
            The query to be sent to the |PumpRoom|'s |Reservoirs|.

        Returns
        -------
        |list| of |Invoices|
            |Invoices| recording the responses of the API calls made.

        """
        threads = []
        for reservoir in self.reservoirs:
            pump = self._create_pump(reservoir)
            subquery = query.filter_accounts(reservoir)
            thread = threading.Thread(
                target=self._start_pump,
                kwargs={'pump': pump, 'query': subquery}
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.records
