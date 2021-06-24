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

# standard library
import math

# third party
from django.conf import settings
from django.urls import reverse

DEFAULT_PAGE_SIZE = settings.PAGE_SIZE
"""int

The default page size of results to return.
"""


class SearchResults(object):
    """Base class for search results returned from a SearchQuery.

    Attributes
    ----------
    count : int
        Number of total results.

    page : int
        Current page number of results.

    page_size : int
        Total number of results per page.

    query : SearchQuery
        Query used to get these search results.

    view_name : str
        Named URL pattern of the view associated with this results list.

    """

    def __init__(
            self, view_name, query,
            page=1, page_size=DEFAULT_PAGE_SIZE, before=None, after=None):
        """Initialize a SearchResults object.

        Parameters
        ----------
        view_name : str
            URL pattern name for the view related to this result object.
        page : int
            Page number of results to retrieve.
        page_size : int
            Number of results to return per page.

        """
        self.count = 0
        self.query = query
        self.page = page
        self.before = before
        self.after = after
        self.page_size = page_size
        self.view_name = view_name

    @property
    def max_page(self):
        """Return the maximum page this result object can have.

        Returns
        -------
        int

        """
        return math.ceil(self.count / self.page_size)

    @staticmethod
    def _create_abs_uri_with_params(path, request, query_params):
        """Create an absolute URI with the given query parameters.

        Parameters
        ----------
        path : str
            URL path of the view to create the absolute URL for.
        request : django.http.HttpRequest
            Request object required for getting the host name and protocol.
        query_params : django.http.QueryDict
            Query parameters to include on the built URL.

        Returns
        -------
        str
        """
        protocol = 'https' if request.is_secure() else 'http'
        host = request.get_host()

        return '{}://{}{}?{}'.format(
            protocol, host, path, query_params.urlencode(),
        )

    def _get_path(self):
        """Return the URL path for this result objects view.

        Returns
        -------
        str
        """
        return reverse(self.view_name)

    def _get_next_uri(self, request):
        """Return the absolute URI of the next page of results.

        Parameters
        ----------
        request : django.http.HttpRequest
            Request object needed to build the URL.

        Returns
        -------
        str or None
        """
        if self.page >= self.max_page:
            return None

        results_path = self._get_path()
        query_params = request.GET.copy()
        query_params['page'] = self.page + 1

        return self._create_abs_uri_with_params(
            results_path, request, query_params,
        )

    def _get_previous_uri(self, request):
        """Return the absolute URI of the previous page of results.

        Parameters
        ----------
        request : django.http.HttpRequest

        Returns
        -------
        str or None
        """
        if self.page <= 1 or self.max_page < self.page:
            return None

        path = self._get_path()
        query_params = request.GET.copy()
        query_params['page'] = self.page - 1

        return self._create_abs_uri_with_params(
            path, request, query_params,
        )

    def as_dict(self, request):
        """Return a JSON serializable representation of this object.

        Parameters
        ----------
        request : django.http.HttpRequest

        Returns
        -------
        dict
        """
        return {
            'count': self.count,
            'next': self._get_next_uri(request),
            'previous': self._get_previous_uri(request),
        }
