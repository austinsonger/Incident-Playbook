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
Views for Monitors.
"""

# third party
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

# local
from .models import Monitor
from .serializers import MonitorSerializer


class MonitorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for Monitors.
    """
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer

    @list_route(methods=['get'], url_path='enabled')
    def enabled(self, request, *args, **kwargs):
        """
        Returns a list of Monitors that are enabled.
        """
        enabled_qs = Monitor.objects.find_enabled()
        filtered_qs = self.filter_queryset(enabled_qs)
        page = self.paginate_queryset(filtered_qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filtered_qs, many=True)
        return Response(serializer.data)

