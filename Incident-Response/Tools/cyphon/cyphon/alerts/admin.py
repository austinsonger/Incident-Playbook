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
Defines a ModelAdmin subclass for Alerts and registers Alerts with Django Admin.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from tags.admin import TagRelationInlineAdmin
from .models import Alert, Analysis, Comment


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for |Articles|.
    """

    fields = ['alert', 'notes', 'created_date', 'last_updated']
    readonly_fields = ['alert', 'created_date', 'last_updated']
    list_display = ['alert', 'analyst']
    link_display = ['alert', ]
    list_filter = ['alert__assigned_user', ]
    inlines = [TagRelationInlineAdmin, ]

    def has_add_permission(self, request):
        """Prevent users from adding an Analysis."""
        return False


class AnalysisInLineAdmin(admin.TabularInline):
    """
    Customizes inline admin forms for |Analyses|.
    """

    model = Analysis
    classes = ('grp-open', )
    inline_classes = ('grp-open', )
    max_num = 1
    min_num = 1
    verbose_name_plural = 'analysis'
    can_delete = False


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Alerts.

    WARNING
    -------
    'search_fields' will only let you search the actual title
    of Alerts, not the display_title. This means you can't search for
    CodeNames in Alert titles even if CodeNames are enabled.

    """

    readonly_fields = (
        'incidents',
        'display_title',
        'created_date',
        'content_date',
        'last_updated',
        'alarm',
        'distillery',
        'doc_id',
        'company',
        'get_data_str',
        'location',
    )
    fieldsets = (
        (None, {
            'fields': (
                'display_title',
                'created_date',
                'content_date',
                'last_updated',
            )
        }),
        (_('Workflow'), {
            'fields': (
                'level',
                'status',
                'assigned_user',
            ),
        }),
        (_('Source'), {
            'fields': (
                'incidents',
                'alarm',
                'company',
                'distillery',
                'doc_id',
            ),
        }),
        (_('Data'), {
            'classes': ('pre', ),
            'fields': (
                'get_data_str',
                'location',
            ),
        }),
    )
    list_display = (
        'id',
        'display_title',
        'content_date',
        'level',
        'status',
        'incidents',
        'outcome',
        'assigned_user',
        'alarm',
        'company',
        'distillery',
        'location',
    )
    list_editable = (
        'level',
        'status',
        'outcome',
        'assigned_user'
    )
    list_filter = (
        'content_date',
        'last_updated',
        'level',
        'status',
        'outcome',
        'assigned_user',
        'distillery',
        'alarm_type'
    )
    list_per_page = 25
    date_hierarchy = 'content_date'
    search_fields = (
        'title',
    )
    actions = [
        'set_status_to_new',
        'set_status_to_busy',
        'set_status_to_done',
        'set_level_to_critical',
        'set_level_to_high',
        'set_level_to_medium',
        'set_level_to_low',
        'set_outcome_to_true',
        'set_outcome_to_false',
    ]
    inlines = [AnalysisInLineAdmin, TagRelationInlineAdmin, ]

    @staticmethod
    def _format_msg(rows_updated):
        """
        Helper method that formats an update message according to the number
        of rows updated.
        """
        if rows_updated == 1:
            return '1 alert was'
        else:
            return '%s alerts were' % rows_updated

    def set_status_to_new(self, request, queryset):
        """
        Allows bulk update of Alert status to "New."
        """
        rows_updated = queryset.update(status='NEW')
        self.message_user(request, '%s successfully marked as New.'
                          % self._format_msg(rows_updated))

    def set_status_to_busy(self, request, queryset):
        """
        Allows bulk update of Alert status to "Busy."
        """
        rows_updated = queryset.update(status='BUSY')
        self.message_user(request, '%s successfully marked as Busy.'
                          % self._format_msg(rows_updated))

    def set_status_to_done(self, request, queryset):
        """
        Allows bulk update of Alert status to "Done."
        """
        rows_updated = queryset.update(status='DONE')
        self.message_user(request, '%s successfully marked as Done.'
                          % self._format_msg(rows_updated))

    def set_level_to_critical(self, request, queryset):
        """
        Allows bulk update of Alert level to "Critical."
        """
        rows_updated = queryset.update(level='CRITICAL')
        self.message_user(request, '%s successfully marked as critical priority.'
                          % self._format_msg(rows_updated))

    def set_level_to_high(self, request, queryset):
        """
        Allows bulk update of Alert level to "High."
        """
        rows_updated = queryset.update(level='HIGH')
        self.message_user(request, '%s successfully marked as high priority.'
                          % self._format_msg(rows_updated))

    def set_level_to_medium(self, request, queryset):
        """
        Allows bulk update of Alert level to "Medium."
        """
        rows_updated = queryset.update(level='MEDIUM')
        self.message_user(request, '%s successfully marked as medium priority.'
                          % self._format_msg(rows_updated))

    def set_level_to_low(self, request, queryset):
        """
        Allows bulk update of Alert level to "Low."
        """
        rows_updated = queryset.update(level='LOW')
        self.message_user(request, '%s successfully marked as low priority.'
                          % self._format_msg(rows_updated))

    def set_outcome_to_true(self, request, queryset):
        """
        Allows bulk update of Alert outcome to "True."
        """
        rows_updated = queryset.update(outcome=True)
        self.message_user(request, '%s successfully marked as True.'
                          % self._format_msg(rows_updated))

    def set_outcome_to_false(self, request, queryset):
        """
        Allows bulk update of Alert outcome to "False."
        """
        rows_updated = queryset.update(outcome=False)
        self.message_user(request, '%s successfully marked as False.'
                          % self._format_msg(rows_updated))

    # define option text for actions
    set_outcome_to_true.short_description = 'Mark as True'
    set_outcome_to_false.short_description = 'Mark as False'
    set_status_to_new.short_description = 'Mark as New'
    set_status_to_busy.short_description = 'Mark as Busy'
    set_status_to_done.short_description = 'Mark as Done'
    set_level_to_critical.short_description = 'Mark as Critical'
    set_level_to_high.short_description = 'Mark as High'
    set_level_to_medium.short_description = 'Mark as Medium'
    set_level_to_low.short_description = 'Mark as Low'


admin.site.register(Comment)
