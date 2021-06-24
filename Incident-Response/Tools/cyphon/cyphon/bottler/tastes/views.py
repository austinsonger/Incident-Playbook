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
Provides views for Tastes.
"""

# third party
import django_filters
from rest_framework import viewsets

# local
from bottler.containers.models import Container
from .models import Taste
from .serializers import TasteSerializer


class TasteFilter(django_filters.FilterSet):
    """
    Filters Tastes by Container.
    """
    container = django_filters.ModelChoiceFilter(
        name='container',
        queryset=Container.objects.all()
    )

    class Meta:
        model = Taste
        fields = ['container']


class TasteViewSet(viewsets.ModelViewSet):
    """
    REST API for Tastes.
    """
    queryset = Taste.objects.all()
    serializer_class = TasteSerializer
    filter_class = TasteFilter
