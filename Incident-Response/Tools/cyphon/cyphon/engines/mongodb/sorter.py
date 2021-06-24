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
Defines a Sorter subclass for ordering MongoDB documents.

=======================  ==============================
Class                    Description
=======================  ==============================
:class:`~MongoDbSorter`  Criteria to sort MongoDB docs.
=======================  ==============================

"""

# third party
import pymongo

# local
from engines.sorter import Sorter


class MongoDbSorter(Sorter):
    """Criteria to sort documents by a set of fields.

    Parameters
    ----------
    sort_list : |list| of |SortParams|
        The |SortParams| used to define the overall order of documents.

    """

    _SORT_ORDERS = {
        'ASC': pymongo.ASCENDING,
        'DESC': pymongo.DESCENDING
    }
    """Map generic sort orders to MongoDB sort orders."""

    @property
    def params(self):
        """Format and return parameters to sort documents.

        Returns
        -------
        dict
           MongoDB parameters for sorting documents.

        """
        return [(sort.field_name, self._SORT_ORDERS[sort.order])
                for sort in self.sort_list]
