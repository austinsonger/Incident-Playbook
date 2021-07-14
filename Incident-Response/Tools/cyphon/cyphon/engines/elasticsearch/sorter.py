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
Defines a Sorter subclass for ordering Elasticsearch documents.

=============================  ====================================
Class                          Description
=============================  ====================================
:class:`~ElasticsearchSorter`  Criteria to sort Elasticsearch docs.
=============================  ====================================

"""

# local
from engines.sorter import Sorter
from .mapper import get_data_type


class ElasticsearchSorter(Sorter):
    """Criteria to sort documents by a set of fields.

    Parameters
    ----------
    sort_list : |list| of |SortParams|
        The |SortParams| used to define the overall order of documents.

    """

    _SORT_ORDERS = {
        'ASC': 'asc',
        'DESC': 'desc'
    }
    """Map generic sort orders to Elasticsearch sort orders."""

    @property
    def params(self):
        """Format and return parameters to sort documents.

        Returns
        -------
        dict
           Elasticsearch parameters for sorting documents.

        """
        params = []
        for sort in self.sort_list:
            data_type = get_data_type(sort.field_type)

            # don't sort fields that are analyzed/tokenized
            if data_type != 'text':
                params.append({
                    sort.field_name: {
                        'order': self._SORT_ORDERS[sort.order],
                    }
                })
        return {
            'sort': params
        }
