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
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.admin import ConfigToolAdmin, CONFIG_TOOL_CLASSES
from cyphon.forms import CONFIG_TOOL_INPUTS


class RuleAdmin(ConfigToolAdmin):
    """
    Customizes admin pages for Rules.
    """
    model_method = 'is_match'

    list_display = [
        'id',
        'name',
        'operator',
        'value',
        'is_regex',
        'case_sensitive',
        'negate',
        'protocol',
    ]
    list_display_links = ['name', ]
    fieldsets = (
        ('Test this rule', {
            'classes': CONFIG_TOOL_CLASSES,
            'description': _('Enter a test string and click "Run test" '
                             'to check whether the rule is True or False '
                             'for the string.'),
            'fields': CONFIG_TOOL_INPUTS,
        }),
        (None, {
            'fields': [
                'name',
                'operator',
                'value',
                'is_regex',
                'case_sensitive',
                'negate',
                'protocol',
            ]
        }),
    )
    save_as = True


class FieldRuleAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Rules.
    """
    list_display = [
        'id',
        'name',
        'field_name',
        'operator',
        'value',
        'is_regex',
        'case_sensitive',
        'negate',
        'protocol',
    ]
    list_display_links = ['name', ]
    fields = [
        'name',
        'field_name',
        'operator',
        'value',
        'is_regex',
        'case_sensitive',
        'negate',
        'protocol',
    ]
    save_as = True


class SieveNodeAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for SievesNodes.
    """
    list_display = [
        'id',
        'sieve',
        'node_object',
        'content_type'
    ]
    list_display_links = ['id', ]
    related_lookup_fields = {
        'generic': [['content_type', 'object_id'], ],
    }


class SieveNodeInLineAdmin(admin.TabularInline):
    """
    Customizes admin inline tables for SieveNodes.
    """
    related_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
    show_change_link = True


class SieveAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Sieves.
    """
    list_display = [
        'name',
        'logic',
        'negate',
        'get_node_number',
    ]
    list_display_links = ['name', ]
    save_as = True
