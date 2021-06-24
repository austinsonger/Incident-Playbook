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
Views for Labels and LabelFields.
"""

# third party
from rest_framework import viewsets

# local
from .serializers import LabelSerializer, LabelFieldSerializer
from .models import Label, LabelField


class LabelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for Labels.
    """
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class LabelFieldViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for LabelFields.
    """
    queryset = LabelField.objects.all()
    serializer_class = LabelFieldSerializer

