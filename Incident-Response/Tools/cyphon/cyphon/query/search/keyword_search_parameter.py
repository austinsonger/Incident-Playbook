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

# local
from .search_parameter import SearchParameter, SearchParameterType


class KeywordSearchParameter(SearchParameter):
    """ Class representation of a keyword search.

    Attributes
    ----------
    keyword : str
        Parsed keyword value.

    """

    EMPTY_VALUE = 'Keyword value is empty.'

    def __init__(self, index, parameter):
        """Keyword search parameter.

        Parameters
        ----------
        index : int
            Index of the search parameter in the search query.

        parameter : str
            Search query parameter string.

        """
        super(KeywordSearchParameter, self).__init__(
            index,
            parameter,
            SearchParameterType.KEYWORD,
        )
        self.keyword = parameter.strip('"')

        if not self.keyword:
            self._add_error(KeywordSearchParameter.EMPTY_VALUE)

    def as_dict(self):
        """Returns dict explaining the parameter.

        Returns
        -------
        dict

        """
        info = super(KeywordSearchParameter, self).as_dict()

        info['keyword'] = self.keyword

        return info
