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
Defines a ModelAdmin subclass for Contexts and registers Contexts with
Django Admin.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from .forms import ContextFilterForm, ContextFilterInlineForm
from .models import Context, ContextFilter


class ContextFilterInLineAdmin(admin.TabularInline):
    """
    Customizes admin inline tables for Fittings.
    """
    model = ContextFilter
    extra = 1
    form = ContextFilterInlineForm


class ContextFilterAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for ContextFilters.
    """
    fieldsets = (
        (None, {
            'description': _(''),
            'fields': (
                'context',
                'search_field',
                'operator',
                'value_field',
            )
        }),
    )
    list_display = (
        'context',
        'search_field',
        'operator',
        'value_field',
    )
    form = ContextFilterForm
    save_as = True


class ContextAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Contexts.
    """
    fieldsets = (
        (None, {
            'description': _(''),
            'fields': (
                'name',
                'primary_distillery',
                'related_distillery',
            )
        }),
        (_('Time Frame'), {
            'description': _(''),
            'fields': (
                ('before_time_interval', 'before_time_unit', ),
                ('after_time_interval', 'after_time_unit', ),
            )
        }),
        (_('Filters'), {
            'description': _(''),
            'fields': (
                'filter_logic',
            )
        }),
    )
    list_display = (
        'name',
        'primary_distillery',
        'related_distillery',
        'before_time_interval',
        'before_time_unit',
        'after_time_interval',
        'after_time_unit',
    )
    list_editable = (
        'before_time_interval',
        'before_time_unit',
        'after_time_interval',
        'after_time_unit',
    )
    list_filter = ('primary_distillery', )
    inlines = [ContextFilterInLineAdmin]
    save_as = True


admin.site.register(Context, ContextAdmin)
admin.site.register(ContextFilter, ContextFilterAdmin)

