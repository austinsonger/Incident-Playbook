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
Defines views for |Warehouses| and |Collections|.

===========================  ==========================================
Class                        Description
===========================  ==========================================
:class:`~CollectionFilter`   Filters views of |Collections|.
:class:`~CollectionViewSet`  REST API views for |Collections|.
:class:`~WarehouseViewSet`   REST API views for |Warehouses|.
===========================  ==========================================

"""

# third party
import django_filters
from rest_framework import viewsets

# local
from warehouses.models import Collection, Warehouse
from warehouses.serializers import CollectionSerializer, WarehouseSerializer


class WarehouseViewSet(viewsets.ReadOnlyModelViewSet):
    """REST API views for |Warehouses|."""

    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class CollectionFilter(django_filters.FilterSet):
    """Filter |Collections| by |Warehouse|.

    Filters REST API views of |Collections| using Django Filter's
    `FilterSet`_.
    """

    warehouse = django_filters.ModelMultipleChoiceFilter(
        name='warehouse',
        queryset=Warehouse.objects.all()
    )

    class Meta(object):
        """Metadata options."""

        model = Collection
        fields = ['warehouse']


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """REST API views for Collections."""

    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_class = CollectionFilter
