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
Defines a ModelAdmin subclass for Dispatches and registers them with
Django Admin.
"""

# third party
from django.contrib import admin

# local
from cyphon.admin import JSONDataAdmin
from .models import Dispatch


class DispatchAdmin(JSONDataAdmin):
    """
    Customizes admin pages for Dispatches.
    """
    exclude = ['data']
    readonly_fields = [
        'alert',
        'stamp',
        'data_prettified'
    ]
    list_display = [
        'id',
        'alert',
        'get_title',
        'get_status_code',
        'get_user'
    ]
    search_fields = [
        'alert__title',
        'stamp__user__email'
    ]
    list_per_page = 25
    list_select_related = True

    fieldsets = (
        (None, {
            'fields': ['alert', 'stamp', 'data_prettified'],
            'classes': ['pre'],
        }),
    )


admin.site.register(Dispatch, DispatchAdmin)

