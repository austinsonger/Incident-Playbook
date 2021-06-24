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
import django_filters
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

# local
from bottler.containers.models import Container
from bottler.containers.serializers import ContainerSerializer
from warehouses.models import Warehouse


class ContainerFilter(django_filters.FilterSet):
    """
    Filters Container by Warehouse.
    """
    name = django_filters.AllValuesFilter(name='name')

    warehouse = django_filters.ModelChoiceFilter(
        name='distillery__collection__warehouse',
        queryset=Warehouse.objects.all()
    )

    class Meta:
        model = Container
        fields = ['name', 'warehouse']


class ContainerViewSet(viewsets.ModelViewSet):
    """
    REST API for Containers.
    """
    queryset = Container.objects.all().order_by('name')
    serializer_class = ContainerSerializer
    filter_class = ContainerFilter

    @staticmethod
    def _filter_by_names(queryset, names):
        """
        Takes a Queryset of Containers and a comma-separated list of Container
        names. Returns a filtered Queryset containing only the Containers listed.
        """
        if names is not None:

            # convert string to list and clean up any whitespaces
            names = names.split(',')
            for index, name in enumerate(names):
                names[index] = name.strip()

            queryset = queryset.filter(name__in=names)

        return queryset

    def _get_data_by_name(self, request):
        """
        Takes a REST API request with an optional names argument consisting of
        a comma-separated list of Container names. Returns the serialized data
        for the specified Containers or the data for all Containers if no names
        were given.
        """
        queryset = Container.objects.all().order_by('name')
        names = self.request.query_params.get('names', None)
        filtered_queryset = self._filter_by_names(queryset, names)
        serializer = ContainerSerializer(filtered_queryset, many=True,
                                         context={'request': request})
        return serializer.data

    @list_route(methods=['get'], url_path='in-use')
    def containers_in_use(self, request, *args, **kwargs):
        """
        Returns a list of Containers that are associated with Distilleries.
        This filters out any Containers that are unused.
        """
        filtered_queryset = Container.objects.filter(
            distillery__isnull=False)
        parents = filtered_queryset.distinct()

        serializer = ContainerSerializer(parents, many=True,
                                         context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='targets')
    def targets(self, request, *args, **kwargs):
        """
        Returns a list of target types (categories) of BottleFields and
        LabelFields present in a queryset of Containers. The results can
        be restricted to a subset of Containers by provided the 'names'
        argument with a comma-separated list of Container names.
        """
        data = self._get_data_by_name(request)

        targets = []

        for doc in data:
            container = Container.objects.get(name=doc['name'])
            for field in container.fields:
                target = field.target_type
                if target and target not in targets:
                    targets.append(target)

        targets.sort()
        return Response(targets)
