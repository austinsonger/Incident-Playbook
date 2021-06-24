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
Views for the appuser package
"""

# third party
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination

# local
from cyphon.views import CustomModelViewSet
from .serializers import AppUserSerializer

_USER_SETTINGS = settings.APPUSERS


class AppUserPagination(PageNumberPagination):
    """
    Pagination class for appusers
    """
    page_size = 50


class AppUserViewSet(CustomModelViewSet):
    """
    A simple ViewSet for viewing and editing alerts.
    """
    queryset = get_user_model().objects.all()
    serializer_class = AppUserSerializer
    pagination_class = AppUserPagination

    def __init__(self, *args, **kwargs):

        # configure filter backends here so we can mock APPUSERS in tests
        self.custom_filter_backends = _USER_SETTINGS['CUSTOM_FILTER_BACKENDS']
        super(AppUserViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset

        if settings.APPUSERS.get('ONLY_SHOW_STAFF', False):
            queryset = queryset.filter(is_staff=True)

        return queryset


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': AppUserSerializer(user).data
    }
