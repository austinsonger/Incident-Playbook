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
Defines a ModelAdmin subclass for Monitors and registers Monitors with
Django Admin.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from .forms import MonitorForm
from .models import Monitor


class MonitorAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Monitors.
    """
    form = MonitorForm
    readonly_fields = (
        'status',
        'created_date',
        'last_updated',
        'last_healthy',
        'last_alert_date',
        'last_alert_id',
        'last_active_distillery',
        'last_saved_doc',
    )
    fieldsets = (
        (None, {
            'description': _('A Monitor monitors one or more Distilleries to '
                             'make sure data is being saved at a minimal rate.'
                             'If data is not being saved at the expected rate, '
                             'the Monitor will generate an Alert.'),
            'fields': (
                'name',
                'groups',
            )
        }),
        (_('Monitoring'), {
            'fields': (
                'enabled',
                'distilleries',
                'time_interval',
                'time_unit',
            )
        }),
        (_('Alerting'), {
            'fields': (
                'alerts_enabled',
                'repeating_alerts',
                'alert_level',
                'last_alert_date',
                'last_alert_id',
            )
        }),
        (_('Status'), {
            'fields': (
                'status',
                'last_updated',
                'last_healthy',

            ),
        }),
        (_('Most Recent Data'), {
            'classes': ('pre', ),
            'fields': (
                'last_active_distillery',
                'last_saved_doc',
            ),
        }),
        (_('History'), {
            'fields': (
                'created_date',
            ),
        }),
    )
    filter_horizontal = ('distilleries', )
    list_display = (
        'name',
        'enabled',
        'time_interval',
        'time_unit',
        'alerts_enabled',
        'repeating_alerts',
        'alert_level',
        'status',
        'last_updated',
        'last_healthy',
    )
    list_editable = (
        'time_interval',
        'time_unit',
        'alert_level',
    )
    list_filter = (
        'alerts_enabled',
        'repeating_alerts',
        'alert_level',
        'status',
    )
    save_as = True


admin.site.register(Monitor, MonitorAdmin)
