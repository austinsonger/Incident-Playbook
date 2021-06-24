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
from .distillery_search_results import DistillerySearchResultsList
from .alert_search_results import AlertSearchResults
from .search_results import DEFAULT_PAGE_SIZE


class AllSearchResults(object):
    """

    Attributes
    ----------
    count : int

    alert_results : AlertSearchResults

    distillery_results : DistillerySearchResultsList

    """
    def __init__(self, query, page=1, page_size=DEFAULT_PAGE_SIZE,
                 before=None, after=None):
        """Initialize an AllSearchResults object.

        Parameters
        ----------
        query : query.search.search_query.SearchQuery

        """
        self.distillery_results = DistillerySearchResultsList(
            query, page=page, page_size=page_size, before=before, after=after)
        self.alert_results = AlertSearchResults(
            query, page=page, page_size=page_size, before=before, after=after)
        self.count = self.distillery_results.count + self.alert_results.count

    def as_dict(self, request):
        """Return a JSON serializable representation of this object.

        Parameters
        ----------
        request : rest_framework.request.Request

        Returns
        -------
        dict

        """
        return {
            'count': self.count,
            'distilleries': self.distillery_results.as_dict(request),
            'alerts': self.alert_results.as_dict(request),
        }
