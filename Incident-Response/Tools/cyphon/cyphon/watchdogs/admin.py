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
Defines ModelAdmins for Watchdogs and Triggers, and registers
them with Django Admin.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.admin import ConfigToolAdmin, CONFIG_TOOL_CLASSES
from cyphon.forms import CONFIG_TOOL_INPUTS
from .models import Watchdog, Trigger, Muzzle
from .forms import TriggerForm, TriggerInlineForm, WatchdogForm


class TriggerInLineAdmin(admin.TabularInline):
    """
    Customizes admin inline tables for Triggers.
    """
    model = Trigger
    show_change_link = True
    form = TriggerInlineForm
    extra = 0


class TriggerAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Triggers.
    """
    list_display = [
        'watchdog',
        'sieve',
        'alert_level',
        'rank',
    ]
    list_editable = [
        'alert_level',
        'rank',
    ]
    form = TriggerForm


class MuzzleAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Muzzles.
    """
    list_display = [
        'watchdog',
        'enabled',
        'matching_fields',
        'time_interval',
        'time_unit',
    ]
    list_editable = [
        'time_interval',
        'time_unit',
    ]
    fieldsets = (
        (None, {
            'description': _('Use a Muzzle to prevent a Watchdog from '
                             'generating duplicate Alerts.'),
            'fields': [
                'watchdog',
                'matching_fields',
                'time_interval',
                'time_unit',
                'enabled',
            ]
        }),
    )


class WatchdogAdmin(ConfigToolAdmin):
    """
    Customizes admin pages for Inspections.
    """
    model_method = 'inspect'
    test_data_format = 'json'

    list_display = ['name', 'enabled', ]
    inlines = [TriggerInLineAdmin, ]
    save_as = True
    form = WatchdogForm
    fieldsets = (
        ('Test this watchdog', {
            'classes': CONFIG_TOOL_CLASSES,
            'description': _('Enter a JSON string and click "Run test" '
                             'to check how the data will be classified.'),
            'fields': CONFIG_TOOL_INPUTS,
        }),
        (None, {
            'fields': [
                'name',
                'enabled',
                'categories',
                'groups',
            ]
        }),
    )


admin.site.register(Trigger, TriggerAdmin)
admin.site.register(Muzzle, MuzzleAdmin)
admin.site.register(Watchdog, WatchdogAdmin)

