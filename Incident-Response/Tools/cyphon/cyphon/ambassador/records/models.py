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
Defines a |Record| base class for storing a record of an API call.

Note
----
The |Record| class is the basis for the |Dispatch| and |Invoice| classes.

"""

# third party
from django.db import models

# local
from ambassador.stamps.models import Stamp
from cyphon.models import SelectRelatedManager


class RecordManager(SelectRelatedManager):
    """
    A model manager for |Records|.
    """
    pass


class Record(models.Model):
    """
    Provides a record of an API call.

    Attributes
    ----------
    stamp : Stamp
        A |Stamp| recording the details of the API call.

    Note
    ----
    Much of the information about the API call is stored in the
    |Record|'s |Stamp|, rather than in the |Record| itself. This is
    to permit development of |Record| subclasses -- such as |Dispatches|
    and |Invoices| -- that have more specialized attributes, while still
    allowing information common to all API calls to be stored in the
    same database table -- the one for |Stamps|.

    """
    stamp = models.ForeignKey(Stamp, null=True, blank=True)

    class Meta:
        abstract = True

    def get_endpoint(self):
        """Get the |Endpoint| associated with the |Record|.

        Returns
        -------
        |Endpoint|
            The |Endpoint| associated with the |Record|.

        """
        return self.stamp.endpoint

    def finalize(self, cargo):
        """Update the |Record|'s |Stamp| with the response from the API.

        Parameters
        ----------
        cargo : |Cargo|
              The |Cargo| returned by a |Transport| after calling an API.

        Returns
        -------
        |Record|
            self

        """
        self.stamp.finalize(status_code=cargo.status_code, notes=cargo.notes)
        return self

