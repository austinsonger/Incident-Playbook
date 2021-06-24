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
Defines views for Contexts.
"""

# third party
from django.conf import settings
import django_filters
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local
from cyphon.views import CustomModelViewSet
from distilleries.models import Distillery
from .models import Context, ContextFilter
from .serializers import ContextFilterSerializer, ContextSerializer

_PAGE_SIZE = settings.PAGE_SIZE


class ContextFilterDjangoFilter(django_filters.FilterSet):
    """
    Filter context filters by context
    """
    context = django_filters.ModelMultipleChoiceFilter(
        name='context',
        queryset=Context.objects.all()
    )

    class Meta:
        model = ContextFilter
        fields = ['context']


class ContextFilterViewSet(CustomModelViewSet):
    """
    REST API for ContextFilters.
    """
    queryset = ContextFilter.objects.all()
    serializer_class = ContextFilterSerializer
    filter_class = ContextFilterDjangoFilter
    custom_filter_backends = ['contexts.filters.ContextFilterFilterBackend']
    permission_classes = [IsAuthenticated]


class ContextDjangoFilter(django_filters.FilterSet):
    """
    Filter contexts by primary_distillery.
    """
    primary_distillery = django_filters.ModelMultipleChoiceFilter(
        name='primary_distillery',
        queryset=Distillery.objects.all()
    )

    class Meta:
        model = Context
        fields = ['primary_distillery']


class ContextViewSet(CustomModelViewSet):
    """
    REST API for Contexts.
    """
    queryset = Context.objects.all().order_by('name')
    serializer_class = ContextSerializer
    filter_class = ContextDjangoFilter
    custom_filter_backends = ['contexts.filters.ContextFilterBackend']
    permission_classes = [IsAuthenticated]

    @detail_route(methods=['get'], url_path='related-data-by-id')
    def related_data_by_id(self, request, pk=None):
        """
        Provides a REST API endpoint for GET requests for related data.
        Takes a document id for a document distilled by the Context's
        Focal Distillery and returns a list of related documents from
        the Context's Related Distillery.
        """
        context = self.get_object()
        doc_id = self.request.query_params.get('id')
        keyword = self.request.query_params.get('keyword')
        page = self.request.query_params.get('page', 1)
        page_size = self.request.query_params.get('page_size', _PAGE_SIZE)
        if doc_id:
            result = context.get_related_data_by_id(doc_id, keyword,
                                                    page, page_size)
        else:
            msg = 'A document id must be provided.'
            result = {'error': msg}

        if 'error' in result:
            return Response(data=result, status=400)

        return Response(result)
