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
Customizes admin pages for |Warehouses| and |Collections|.

=========================  ========================================
Class                      Description
=========================  ========================================
:class:`~CollectionAdmin`  Customize admin pages for |Collections|.
:class:`~WarehouseAdmin`   Customize admin pages for |Warehouses|.
=========================  ========================================

"""

# third party
from django.contrib import admin

# local
from warehouses.models import Warehouse, Collection


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Customize admin pages for |Warehouses|."""

    list_display = (
        'name',
        'backend',
        'time_series',
    )

    ordering = ['backend', 'name']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Customize admin pages for |Collections|."""

    list_display = (
        '__str__',
        'get_warehouse_name',
        'name',
        'get_backend',
        'in_time_series',
        'get_company',
    )

    ordering = ['warehouse__backend', 'warehouse__name', 'name']
