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

"""

# standard library
import logging

# third party
from django.utils.functional import cached_property

# local
from aggregator.invoices.models import Invoice
from ambassador.transport import Cargo, Transport
from cyphon.transaction import close_old_connections
from sifter.datasifter.datachutes.models import DataChute

LOGGER = logging.getLogger(__name__)


class Faucet(Transport):
    """

    Attributes
    ----------
    endpoint : Pipe

    emissary : Plumber

    user : AppUser

    cargo :  Cargo

    record : Invoice

    task : str


    """

    def __init__(self, task, *args, **kwargs):
        super(Faucet, self).__init__(*args, **kwargs)
        self.task = task

    @cached_property
    def _stamp(self):
        """

        """
        if self.record:
            return self.record.stamp

    @close_old_connections
    def is_obsolete(self):
        """
        Returns a Boolean indicating whether a more recent call has been
        made to the same endpoint with the same credentials.
        """
        if self._stamp:
            return self._stamp.is_obsolete()
        else:
            return False

    def load_cargo(self, data):
        """

        """
        self.cargo = Cargo(data=data, status_code='200')

    def stash_data(self, data):
        """
        For ad hoc searches, data from each endpoint should be
        temporarily saved in a separate collection associated with the
        user making the request.
        """
        pass

    def send_to_chutes(self, data):
        """

        """
        chutes = DataChute.objects.find_by_endpoint(self.endpoint)
        for chute in chutes:
            chute.bulk_process(data=data)

    def create_record(self, stamp, obj):
        """
        Create a record of the response

        Parameters
        ----------
        stamp : |Stamp|

        obj : |ReservoirQuery|


        Returns
        -------
        None

        """
        query = obj.to_dict()

        return Invoice.objects.create(
            stamp=stamp,
            query=query,
            task=self.task
        )

    def process_request(self, obj):
        """

        Parameters
        ----------
        obj : |ReservoirQuery|

        Returns
        -------
        |Cargo|


        Takes an a ReservoirQuery, formats and submits it to the API,
        returns a Cargo object. This method needs to be implemented in
        derived classes so it can be customized for specific APIs.

        """
        raise self.raise_method_not_implemented()

    @close_old_connections
    def process_results(self):
        """

        """
        if self.cargo is not None:
            data = self.cargo.data
            if self.task == 'ADHOC_SRCH':
                return self.stash_data(data)
            elif self.task == 'BKGD_SRCH':
                return self.send_to_chutes(data)
            else:
                return data
        else:
            LOGGER.error('There are no results to process. '
                         'Call the start() method to get data from the API.')
