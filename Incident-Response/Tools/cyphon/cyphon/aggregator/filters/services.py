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
Defines a function for creating and processing queries from |Filters|.
"""

# local
from aggregator.filters.models import Filter
from aggregator.reservoirs.models import Reservoir
from aggregator.pumproom.pumproom import PumpRoom


def execute_filter_queries():
    """
    Executes periodic background searches with enabled |Filters|.

    Gathers enabled |Filters|, creates a query for each enabled
    |Reservoir|, and sends the queries to the |Reservoir|.

    Returns
    -------
    |list| of |Invoices|
        |Invoices| recording the responses of the API calls made.

    """
    # ReservoirQuery object created from enabled Filters
    query = Filter.objects.create_reservoir_query()

    # QuerySet containing enabled Reservoirs
    active_reservoirs = Reservoir.objects.find_enabled()

    pumproom = PumpRoom(reservoirs=active_reservoirs, task='BKGD_SRCH')

    # update last_used fields of enabled Filters
    Filter.objects.update_enabled_filters()

    return pumproom.get_results(query)

