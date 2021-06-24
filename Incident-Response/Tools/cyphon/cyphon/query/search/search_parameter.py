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
import re


class SearchParameterType(object):
    """
    Contains values and helper functions to determine a search query
    parameter's type.
    """

    KEYWORD = 'keyword'
    """str

    String that indicates that a parameter is a keyword search.
    """

    FIELD = 'field'
    """str

    String indicating that a parameter is a field search.
    """

    DISTILLERY = 'distillery'
    """str

    String indicating that a parameter is a distillery filter.
    """

    TYPE_CHECK_REGEX_MAP = [
        (KEYWORD, r'^\".*\"$|^\w[\w.]*$'),
        (DISTILLERY, r'^@source=\".*\"$'),
        (FIELD, r'^\w[\w.]*[=<>!]{1,2}(?:$|\".*\"$|[\w.]*$)')
    ]
    """list of tuple

    Search parameter types paired with a regex pattern that determines if
    a string is that parameter type.
    """

    @staticmethod
    def get_parameter_type(parameter):
        """Return the search query parameter type.

        Parameters
        ----------
        parameter : str
            Search query parameter to return the type of.

        Returns
        -------
        str or None
            Parameter type.
        """
        for type_check in SearchParameterType.TYPE_CHECK_REGEX_MAP:
            if re.match(type_check[1], parameter):
                return type_check[0]

        return None


class SearchParameter(object):
    """

    Attributes
    ----------
    errors : list of str
        Errors that occurred while parsing data from the parameter string.

    index : int
        Index of the parameter in the search query string.

    parameter : str
        Parameter string this instance was made from.

    type : str
        The type of parameter.

    """

    def __init__(self, index, parameter, parameter_type):
        """Initialize a SearchParameter."""
        self.errors = []
        self.index = index
        self.parameter = parameter
        self.type = parameter_type

    def _add_error(self, error):
        """Add an error message to the parameter.

        Parameters
        ----------
        error : str
            Message explaining an error that occurred while parsing the
            parameter.

        """
        self.errors.append(error)

    def is_valid(self):
        """Check if any errors occurred during parsing.

        Returns
        -------
        bool
            If the search parameter is valid.

        """
        return not bool(self.errors)

    def as_dict(self):
        """Return a dict of info about the parameter.

        Used for debugging purposes and creating error messages.

        Returns
        -------
        dict

        """
        return {
            'parameter': self.parameter,
            'index': self.index,
            'type': self.type,
            'errors': self.errors,
        }
