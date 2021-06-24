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
Provides a serializer for the Taste model.
"""

# third party
from rest_framework import serializers

# local
from .models import Taste


class TasteSerializer(serializers.ModelSerializer):
    """

    """
    id = serializers.ReadOnlyField(source='pk')  # pylint: disable=C0103

    class Meta:
        model = Taste
        fields = (
            'id',
            'author',
            'title',
            'container',
            'content',
            'location',
            'location_format',
            'datetime',
            'date_string',
            'date_format',
            'url',
        )
