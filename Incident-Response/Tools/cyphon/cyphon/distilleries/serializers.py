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
Defines serializers for |Distilleries|.

====================================  ========================================
Class                                 Description
====================================  ========================================
:class:`~DistilleryDetailSerializer`  Serializer for |Distillery| detail view.
:class:`~DistilleryListSerializer`    Serializer for |Distillery| list view.
====================================  ========================================

"""

# third party
from rest_framework import serializers

# local
from bottler.containers.serializers import ContainerSerializer
from contexts.serializers import ContextSerializer
from .models import Distillery


class DistilleryDetailSerializer(serializers.ModelSerializer):
    """Serializer for a |Distillery| object."""

    id = serializers.ReadOnlyField(source='pk')  # pylint: disable=C0103
    container = ContainerSerializer()
    contexts = ContextSerializer(many=True)

    class Meta(object):
        """Metadata options."""

        model = Distillery
        depth = 2
        fields = (
            'collection',
            'container',
            'contexts',
            'id',
            'name',
            'url',
        )


class DistilleryListSerializer(serializers.ModelSerializer):
    """Serializer for a |Distillery| list."""

    id = serializers.ReadOnlyField(source='pk')  # pylint: disable=C0103

    class Meta(object):
        """Metadata options."""

        model = Distillery
        depth = 1
        fields = (
            'id',
            'name',
            'url',
        )
