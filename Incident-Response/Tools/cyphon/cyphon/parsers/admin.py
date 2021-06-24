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
Defines a ModelAdmin for a FieldParser.
"""

# third party
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.admin import ConfigToolAdmin, CONFIG_TOOL_CLASSES
from cyphon.forms import CONFIG_TOOL_INPUTS
from .forms import ParserForm


class ParserAdmin(ConfigToolAdmin):
    """
    Customizes admin pages for DataParsers.
    """
    list_display = [
        'name',
        'method',
        'regex',
        'formatter',
    ]
    list_display_links = ['name', ]
    fieldsets = (
        ('Test this parser', {
            'classes': CONFIG_TOOL_CLASSES,
            'description': _('Enter a test string and click "Run test" '
                             'to check what the parser will return '
                             'for the string.'),
            'fields': CONFIG_TOOL_INPUTS,
        }),
        (None, {
            'fields': [
                'name',
                'method',
                'regex',
                'formatter',
            ]
        }),
    )
    save_as = True
    form = ParserForm


class FieldParserAdmin(ConfigToolAdmin):
    """
    Customizes admin pages for DataParsers.
    """
    list_display = [
        'name',
        'source_fields',
        'method',
        'regex',
        'formatter',
    ]
    list_display_links = ['name', ]
    fieldsets = (
        ('Test this parser', {
            'classes': CONFIG_TOOL_CLASSES,
            'description': _('Enter a test string and click "Run test" '
                             'to check what the parser will return '
                             'for the string.'),
            'fields': CONFIG_TOOL_INPUTS,
        }),
        (None, {
            'fields': [
                'name',
                'source_fields',
                'method',
                'regex',
                'formatter',
            ]
        }),
    )
    form = ParserForm

