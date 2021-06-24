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
Defines classes for ordering documents.

=======================  =========================================
Class                    Description
=======================  =========================================
:class:`~SortParam`      Criteria to sort docs by a field.
:class:`~Sorter`         Criteria to sort docs by a set of fields.
=======================  =========================================

"""

# local
from cyphon.baseclass import BaseClass


class SortParam(object):
    """Criteria to sort documents by values of a particular field.

    Parameters
    ----------
    field_name : str
        The name of the field by which documents should be sorted.

    field_type : str
        The type of field by which documents should be sorted (e.g.,
        'CharField'). See |FIELD_TYPE_CHOICES| for a list of field types.

    order : str
        The order in which field values should be sorted. Choices are
        'ASC' (ascending) or 'DESC' (descending).

    Attributes
    ----------
    field_name : str
        The name of the field by which documents should be sorted.

    field_type : str
        The type of field by which documents should be sorted (e.g.,
        'CharField'). See |FIELD_TYPE_CHOICES| for a list of field types.

    order : str
        The order in which field values should be sorted. Choices are
        'ASC' (ascending) or 'DESC' (descending).

    """

    def __init__(self, field_name, field_type, order):
        """Initialize a SortParam instance."""
        self.field_name = field_name
        self.field_type = field_type
        self.order = order


class Sorter(BaseClass):
    """Criteria to sort documents by a set of fields.

    Parameters
    ----------
    sort_list : |list| of |SortParams|
        The |SortParams| used to define the overall order of documents.

    """

    def __init__(self, sort_list):
        """Initialize a Sorter instance."""
        self.sort_list = sort_list

    @property
    def params(self):
        """Format and return parameters to sort documents.

        Raises
        ------
        NotImplementedError
            If the method has not been implemented.

        """
        return self.raise_attr_not_implemented('params')
