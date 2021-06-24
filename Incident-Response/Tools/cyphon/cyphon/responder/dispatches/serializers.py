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
Serializers for Dispatches.
"""

# third party
from rest_framework import serializers

# local
from appusers.serializers import AppUserSerializer
from .models import Dispatch


class DispatchSerializer(serializers.ModelSerializer):
    """
    Serializer for Dispatches.
    """
    issued_by = AppUserSerializer()

    class Meta:
        model = Dispatch
        fields = (
            'id',
            'title',
            'issued_by',
            'status_code',
            'response_msg',
            'data',
        )
