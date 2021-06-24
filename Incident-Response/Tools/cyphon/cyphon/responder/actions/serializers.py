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
from .models import Action
from alerts.models import Alert


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Actions.
    """
    name = serializers.CharField(source='description', read_only=True)

    class Meta:
        model = Action
        fields = (
            'url',
            'name',
            'id',
            'api_module',
            'api_class',
            'visa_required',
            'platform'
        )


class ActionRunSerializer(serializers.Serializer):
    """
    Serializer for the Action Run action.
    """
    alert = serializers.PrimaryKeyRelatedField(
        queryset=Alert.objects.all(),
        required=True
    )
