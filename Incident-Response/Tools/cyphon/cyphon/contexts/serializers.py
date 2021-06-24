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
Serializers for Contexts.
"""

# third party
from rest_framework import serializers

# local
from .models import Context, ContextFilter
from distilleries.models import Distillery


class ContextFilterSerializer(serializers.ModelSerializer):
    """
    Serializer for ContextFilters.
    """

    class Meta:
        model = ContextFilter
        fields = (
            'id',
            'context',
            'search_field',
            'operator',
            'operator_text',
            'value_field',
            'url',
        )

class ContextDistillerySerializer(serializers.ModelSerializer):
    """Serializer for a |Distillery| list."""

    id = serializers.ReadOnlyField(source='pk')  # pylint: disable=C0103
    name = serializers.CharField(source='__str__')

    class Meta(object):
        """Metadata options."""

        model = Distillery
        depth = 1
        fields = (
            'id',
            'name',
            'url',
        )

class ContextSerializer(serializers.ModelSerializer):
    """
    Serializer for Contexts.
    """

    primary_distillery = ContextDistillerySerializer()
    related_distillery = ContextDistillerySerializer()
    filters = ContextFilterSerializer(many=True)

    class Meta:
        model = Context
        fields = (
            'id',
            'name',
            'primary_distillery',
            'related_distillery',
            'before_time_interval',
            'before_time_unit',
            'after_time_interval',
            'after_time_unit',
            'filters',
            'filter_logic',
            'url',
        )

