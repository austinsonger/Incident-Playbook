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
Defines a ModelAdmin subclasses for Fittings and Condensers.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.admin import ConfigToolAdmin, CONFIG_TOOL_CLASSES
from cyphon.forms import CONFIG_TOOL_INPUTS


class CondenserAdmin(ConfigToolAdmin):
    """
    Customizes admin pages for DataCondensers.
    """
    list_display = [
        'name',
        'bottle',
    ]
    list_display_links = ['name', ]
    save_as = True
    fieldsets = (
        ('Test this condenser', {
            'classes': CONFIG_TOOL_CLASSES,
            'description': _('Enter a test string and click "Run test" '
                             'to check how the data will be parsed.'),
            'fields': CONFIG_TOOL_INPUTS,
        }),
        (None, {
            'fields': [
                'name',
                'bottle',
            ]
        }),
    )


class FittingInLineAdmin(admin.TabularInline):
    """
    Customizes admin inline tables for Fittings.
    """
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }
    min_num = 1
    extra = 0


class FittingAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for DataFittings.
    """
    list_display = [
        'id',
        'condenser',
        'target_field_name',
        'target_field_type',
        'fitting_type',
    ]
    list_display_links = ['id', ]
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }
