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
from bottler.containers.models import Container
from bottler.tastes.serializers import TasteSerializer


class ContainerSerializer(serializers.ModelSerializer):

    fields = serializers.ReadOnlyField(source='field_dicts')
    taste = TasteSerializer()

    class Meta:
        model = Container
        fields = (
            'bottle',
            'id',
            'fields',
            'label',
            'name',
            'url',
            'taste'
        )
        # depth = 2 # show datafield objects, not just datafield foreign keys
