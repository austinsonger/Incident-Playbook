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
Serializers for Monitors.
"""

# third party
from rest_framework import serializers

# local
from distilleries.serializers import DistilleryListSerializer
from .models import Monitor


class MonitorSerializer(serializers.ModelSerializer):
    """
    Serializer for Distilleries.
    """
    distilleries = DistilleryListSerializer(many=True)
    last_active_distillery = DistilleryListSerializer()

    class Meta:
        model = Monitor
        depth = 1
        fields = (
            'name',
            'enabled',
            'distilleries',
            'interval',
            'alerts_enabled',
            'alert_level',
            'status',
            'last_updated',
            'last_healthy',
            'last_active_distillery',
            'last_saved_doc',
        )
