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

# third party
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

# local
from cyphon.fieldsets import QueryFieldset
from engines.queries import EngineQuery
from query.collectionqueries.models import CollectionQuery, Fieldset
from query.collectionqueries.serializers import CollectionQuerySerializer, FieldsetSerializer


class CollectionQueryViewSet(viewsets.ModelViewSet):
    """
    REST API views for CollectionQueries.
    """
    queryset = CollectionQuery.objects.all()
    serializer_class = CollectionQuerySerializer

    @staticmethod
    def _get_results(query):
        """
        Takes a query dictionary and returns a list of documents that match the
        query criteria.
        """
        subqueries = [QueryFieldset(**fieldset) \
                      for fieldset in query['fieldsets']]
        engine_query = EngineQuery(subqueries=subqueries,
                                   joiner=query['joiner'])
        docs = []
        for collection in query['collections']:
            results = collection.find(engine_query)
            docs.extend(results['results'])
        return docs

    @staticmethod
    def _get_teaser_results(query):
        """
        Takes a query dictionary and returns a list of teasers for documents
        that match the query criteria.
        """
        results = []
        for collection in query['collections']:
            docs = collection.find(query)
            for doc in docs:
                teaser = collection.get_sample(doc)
                results.append(teaser)
        return results

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @list_route(methods=['post'], url_path='query')
    def query(self, request, *args, **kwargs):
        """
        REST API endpoint for field-based queries. Takes a query request and
        returns a list of matching documents.
        """
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data
        results = self._get_results(query)
        return Response(results)


class QueryFieldsetViewSet(viewsets.ModelViewSet):
    """
    REST API views for QueryFieldsets.
    """
    queryset = Fieldset.objects.all()
    serializer_class = FieldsetSerializer
    # permission_classes = (IsAuthenticated, )

