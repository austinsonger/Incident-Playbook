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
Defines views for |Distilleries| using the Django REST framework.

==============================  ===========================================
Class                           Description
==============================  ===========================================
:class:`~DistilleryPagination`  Pagination for |Distillery| views.
:class:`~DistilleryViewSet`     `ReadOnlyModelViewSet`_ for |Distilleries|.
==============================  ===========================================

"""

# third party
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination

# local
from .models import Distillery
from .serializers import DistilleryDetailSerializer


class DistilleryPagination(PageNumberPagination):
    """Pagination for |Distillery| views.

    Paginates |Distilleries| using Django REST framework's
    `PageNumberPagination`_.
    """

    page_size = 50


class DistilleryViewSet(viewsets.ReadOnlyModelViewSet):
    """REST API views for Distilleries."""

    queryset = Distillery.objects.all()
    serializer_class = DistilleryDetailSerializer
    pagination_class = DistilleryPagination

    def get_queryset(self):
        """Returns a queryset of |Distilleries| associated with a company."""
        user = self.request.user

        if user.is_staff:
            return self.queryset

        if user.company:
            return self.queryset.filter(company=user.company)

        return self.queryset.none()

    @list_route(methods=['get'], url_path='have-alerts')
    def have_alerts(self, request, *args, **kwargs):
        """Get |Distilleries| that are associated with |Alerts|.

        Parameters
        ----------
        request : :class:`rest_framework.request.Request`
            A Django REST framework HTTP `Request`_ object.

        Returns
        -------
        :class:`rest_framework.response.Response`
            A Django REST framework HTTP `Response`_ object containing
            a list of JSON serialized |Distilleries| associated with
            |Alerts|.

        """
        filtered_qs = self.filter_queryset(self.get_queryset())
        w_alerts_qs = Distillery.objects.have_alerts(filtered_qs)
        page = self.paginate_queryset(w_alerts_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_qs, many=True)
        return Response(serializer.data)
