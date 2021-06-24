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
from rest_framework import serializers

# local
from bottler.bottles.models import Bottle, BottleField
from distilleries.models import Distillery


class DistilleryDetailSerializer(serializers.ModelSerializer):
    """

    """
    name = serializers.CharField(source='__str__')

    class Meta:
        model = Distillery
        fields = ('pk', 'name')


class BottleFieldSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    class Meta:
        model = BottleField
        fields = (
            'id',
            'field_name',
            'field_type',
            'target_type',
            'embedded_doc',
            'url',
            'bottles'
        )


class BottleSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    # get the collection's pk (distillery.pk = distillery.collection.pk)
    collections = DistilleryDetailSerializer(source='container__distilleries',
                                       many=True, read_only=True)

    class Meta:
        model = Bottle
        fields = ('id', 'name', 'fields', 'collections', 'url')

