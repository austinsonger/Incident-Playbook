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
Defines serializers for |Warehouses| and |Collections|.

==============================  =============================
Class                           Description
==============================  =============================
:class:`~CollectionSerializer`  Serializer for |Collections|.
:class:`~WarehouseSerializer`   Serializer for |Warehouses|.
==============================  =============================

"""

# third party
from rest_framework import serializers

# local
from warehouses.models import Warehouse, Collection


class WarehouseSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a |Warehouse| object."""

    class Meta(object):
        """Metadata options."""

        model = Warehouse
        fields = ('backend', 'name', 'collections', 'url', 'id')


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a |Collection| object."""

    class Meta(object):
        """Metadata options."""

        model = Collection
        fields = ('url', 'name', 'warehouse', 'id')
