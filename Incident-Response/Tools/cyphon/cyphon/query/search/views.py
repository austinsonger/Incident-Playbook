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
from dateutil import parser

# third party
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# local
from distilleries.models import Distillery
from .search_query import SearchQuery
from .all_search_results import AllSearchResults
from .alert_search_results import AlertSearchResults
from .distillery_search_results import (
    DistillerySearchResultsList, DistillerySearchResults
)
from .search_parameter import SearchParameterType
from .search_results import DEFAULT_PAGE_SIZE

SEARCH_VIEW_NAME = 'search'
ALERT_SEARCH_VIEW_NAME = AlertSearchResults.VIEW_NAME
DISTILLERY_SEARCH_VIEW_NAME = DistillerySearchResults.VIEW_NAME
DISTILLERIES_SEARCH_VIEW_NAME = 'search_distilleries'


class QueryParams(object):
    def __init__(self, params=None):
        params = params if params else {}

        self.query = params.get('query', '')
        self.before = self._parse_date(params.get('before'))
        self.after = self._parse_date(params.get('after'))
        self.page = self._parse_int(params.get('page'), 1)
        self.page_size = self._parse_int(
            params.get('page_size'), DEFAULT_PAGE_SIZE)

    @staticmethod
    def _parse_date(date):
        try:
            return parser.parse(date)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_int(integer, default):
        try:
            return int(integer)
        except (ValueError, TypeError):
            return default


@api_view(['GET'])
def search(request):
    """View that searches both alerts and distilleries based on a search query.

    Parameters
    ----------
    request : rest_framework.request.Request

    Returns
    -------

    """
    params = QueryParams(request.query_params)
    search_query = SearchQuery(params.query, request.user)
    response = _create_empty_response(search_query)

    if search_query.is_valid():
        search_results = AllSearchResults(
            search_query, page=params.page, page_size=params.page_size,
            after=params.after, before=params.before)
        response['results'] = search_results.as_dict(request)

        return Response(response)

    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_alerts(request):
    """View that searches alerts based on a search query.

    Parameters
    ----------
    request : rest_framework.request.Request

    Returns
    -------
    Response
    """
    params = QueryParams(request.query_params)
    search_query = SearchQuery(
        params.query, request.user,
        ignored_parameter_types=[SearchParameterType.FIELD],
    )
    response = _create_empty_response(search_query)

    if search_query.is_valid():
        search_results = AlertSearchResults(
            search_query, page=params.page, page_size=params.page_size,
            after=params.after, before=params.before)
        response['results'] = search_results.as_dict(request)

        return Response(response)

    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_distilleries(request):
    """View that searches all distilleries based on a search query.

    Parameters
    ----------
    request : rest_framework.request.Request

    Returns
    -------
    Response
    """
    params = QueryParams(request.query_params)
    search_query = SearchQuery(params.query, request.user)
    response = _create_empty_response(search_query)

    if search_query.is_valid():
        search_results = DistillerySearchResultsList(
            search_query, page=params.page, page_size=params.page_size,
            after=params.after, before=params.before)
        response['results'] = search_results.as_dict(request)

        return Response(response)

    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_distillery(request, pk):
    """View that searches a single distillery based on the search query.

    Parameters
    ----------
    request : rest_framework.request.Request
    pk: str
        Primary key of the distillery to search through.

    Returns
    -------
    Response
    """
    params = QueryParams(request.query_params)
    search_query = SearchQuery(
        params.query, request.user,
        ignored_parameter_types=[SearchParameterType.DISTILLERY],
    )
    response = _create_empty_response(search_query)

    if not search_query.is_valid():
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    try:
        distillery = Distillery.objects.get(pk=int(pk))
    except Distillery.DoesNotExist:
        return Response(
            data={'detail': 'Distillery {} not found.'.format(pk)},
            status=status.HTTP_404_NOT_FOUND)

    search_results = DistillerySearchResults(
        search_query, page=params.page,
        page_size=params.page_size,
        distillery=distillery,
        after=params.after, before=params.before)
    response['results'] = search_results.as_dict(request)

    return Response(response)


def _create_empty_response(search_query):
    """Creates a search response without any results.

    Parameters
    ----------
    search_query : SearchQuery

    Returns
    -------
    dict
    """
    return {
        'query': search_query.as_dict(),
        'results': None,
    }
