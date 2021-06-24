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
from functools import reduce

# third party
from django.urls import reverse

# local
from cyphon.fieldsets import QueryFieldset
from distilleries.models import Distillery
from distilleries.serializers import DistilleryListSerializer
from engines.queries import EngineQuery
from .search_results import SearchResults, DEFAULT_PAGE_SIZE


class DistillerySearchResults(SearchResults):
    """

    """

    VIEW_NAME = 'search_distillery'

    def __init__(self, query, distillery, page=1, page_size=DEFAULT_PAGE_SIZE,
                 before=None, after=None):
        """Create a DistillerySearchResults instance.

        Parameters
        ----------
        query : query.search.search_query.SearchQuery

        distillery : Distillery

        """
        super(DistillerySearchResults, self).__init__(
            self.VIEW_NAME, query, page, page_size,
        )
        self.results = []
        self.count = 0
        self.distillery = distillery
        self.engine_query = self._get_engine_query(
            distillery, query, before=before, after=after)

        if not self.engine_query:
            return

        if (before or after) and not distillery.get_searchable_date_field():
            results = None
        else:
            results = self.distillery.find(
                self.engine_query, page=page, page_size=page_size)

        if results and results['count']:
            self.count = results['count']
            self.results = results['results']

    @staticmethod
    def _serialize_distillery_object(distillery, request):
        """Return a JSON serializable representation of a distillery object.

        Parameters
        ----------
        distillery : Distillery
            Distillery object to serialize.

        request : django.http.HttpRequest
            Request object from the view requesting the serialized object.

        Returns
        -------
        dict

        """
        return DistilleryListSerializer(
            distillery,
            context={'request': request}
        ).data

    @staticmethod
    def _get_field_engine_query(distillery, field_parameters):
        """Return QueryFieldsets of FieldSearchParameters based on Distillery.

        Parameters
        ----------
        distillery : Distillery

        field_parameters : list of query.search.field_search_parameter.FieldSearchParameter

        Returns
        -------
        EngineQuery or None

        """
        if not field_parameters:
            return None

        fieldsets = [
            parameter.create_fieldset() for parameter in field_parameters
            if parameter.is_related_to_distillery(distillery)
        ]

        if not fieldsets:
            return None

        return EngineQuery(subqueries=fieldsets, joiner='AND')

    @staticmethod
    def _create_keyword_engine_query(text_fields, keyword):
        """

        Parameters
        ----------
        text_fields : list of DataField
        keyword: str

        Returns
        -------
        EngineQuery or None
        """
        fieldsets = [
            QueryFieldset(
                field_name=field.field_name,
                field_type=field.field_type,
                operator='regex',
                value=keyword,
            )
            for field in text_fields
        ]

        if not fieldsets:
            return None

        return EngineQuery(subqueries=fieldsets, joiner='OR')

    @staticmethod
    def _get_keyword_engine_query(distillery, keywords):
        """Return QueryFieldsets for all text fields of a distillery.

        Parameters
        ----------
        distillery : Distillery
            Distillery to get the text fields from.

        keywords : list of str
            Keywords to search for in the text fields.

        Returns
        -------
        EngineQuery or None

        """
        if not keywords:
            return None

        text_fields = distillery.get_text_fields()

        if not text_fields:
            return None

        keyword_engine_queries = []

        for keyword in keywords:
            keyword_engine_query = (
                DistillerySearchResults._create_keyword_engine_query(
                    text_fields, keyword))

            if keyword_engine_query:
                keyword_engine_queries.append(keyword_engine_query)

        return EngineQuery(subqueries=keyword_engine_queries, joiner='AND')

    @staticmethod
    def _get_engine_query(distillery, query, before=None, after=None):
        """Return QueryFieldsets of keyword and field searches for a distillery.

        Parameters
        ----------
        distillery : Distillery

        query: query.search.search_query.SearchQuery

        before: datetime.datetime or None

        after: datetime.datetime or None

        Returns
        -------
        EngineQuery or None

        """
        engine_queries = [
            DistillerySearchResults._get_field_engine_query(
                distillery, query.field_parameters),
            DistillerySearchResults._get_keyword_engine_query(
                distillery, query.keywords)
        ]
        subqueries = [
            engine_query for engine_query in engine_queries if engine_query
        ]

        if not subqueries:
            return None

        if before or after:
            searchable_date_field = distillery.get_searchable_date_field()

            if searchable_date_field:
                if before:
                    subqueries += [QueryFieldset(
                        field_name=searchable_date_field,
                        field_type='DateTimeField',
                        operator='lte',
                        value=before.isoformat()
                    )]

                if after:
                    subqueries += [QueryFieldset(
                        field_name=searchable_date_field,
                        field_type='DateTimeField',
                        operator='gte',
                        value=after.isoformat()
                    )]

        return EngineQuery(subqueries=subqueries, joiner='AND')

    def _get_path(self):
        return reverse(self.view_name, args=[self.distillery.pk])

    def as_dict(self, request):
        """Return a JSON serializable representation of this instance.

        Parameters
        ----------
        request : django.http.HttpRequest

        Returns
        -------
        dict

        """
        parent_dict = super(DistillerySearchResults, self).as_dict(request)

        parent_dict['results'] = self.results
        parent_dict['distillery'] = self._serialize_distillery_object(
            self.distillery, request,
        )

        return parent_dict


class DistillerySearchResultsList(object):
    """

    """

    def __init__(
            self, query, page=1, page_size=DEFAULT_PAGE_SIZE,
            before=None, after=None):
        """Create a DistillerySearchResultsList instance.

        Parameters
        ----------
        query: query.search.search_query.SearchQuery

        """
        self.count = 0
        self.distilleries = (
            query.distilleries or Distillery.objects.all()
        )
        self.results = self._get_distillery_search_results(
            self.distilleries, query,
            page=page, page_size=page_size, before=before, after=after
        )
        self.count = self._get_result_count(self.results)

    @staticmethod
    def _get_result_count(results):
        """Return the result count of all DistillerySearchResults.

        Parameters
        ----------
        results : list of DistillerySearchResult

        Returns
        -------
        int

        """
        return reduce((lambda count, result: count + result.count), results, 0)

    @staticmethod
    def _get_distillery_search_results(
            distilleries, query, page, page_size,
            before=None, after=None):
        """Return a list of DistillerySearchResults for a query.

        Parameters
        ----------
        distilleries : list of Distillery

        query : query.search.search_query.SearchQuery

        Returns
        -------
        list of DistillerySearchResults or None

        """
        if query.keywords or query.field_parameters:
            return [
                DistillerySearchResults(
                    query, distillery,
                    page=page, page_size=page_size, before=before, after=after)
                for distillery in distilleries
            ]

        return []

    def _get_results_as_dict(self, request):
        """Return a JSON serializable representation of earch results.

        Parameters
        ----------
        request : django.http.HttpRequest

        Returns
        -------
        list of dict

        """
        return [
            result.as_dict(request) for result in self.results
            if result.count
        ]

    def as_dict(self, request):
        """
        Return a JSON serializable representation of this instance.

        Parameters
        ----------
        request : rest_framework.request.Request

        Returns
        -------
        dict

        """
        return {
            'count': self.count,
            'results': self._get_results_as_dict(request)
        }
