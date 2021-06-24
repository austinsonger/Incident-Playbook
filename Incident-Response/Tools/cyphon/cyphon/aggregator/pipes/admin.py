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
Defines a |ModelAdmin| subclass for |Pipes| and registers them with
Django Admin.
"""

# third party
from django.contrib import admin

# local
from aggregator.pipes.models import Pipe, PipeSpecSheet


class PipeSpecSheetInLineAdmin(admin.StackedInline):
    """
    Customizes inline admin forms for |PipeSpecsheets|.
    """
    model = PipeSpecSheet
    classes = ('grp-open', )
    inline_classes = ('grp-open', )
    max_num = 1
    min_num = 1
    verbose_name_plural = 'spec sheet'
    can_delete = False


class PipeSpecSheetAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for |PipeSpecsheets|.
    """
    pass


class PipeAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for |Pipes|.
    """
    inlines = [PipeSpecSheetInLineAdmin, ]
    fields = [
        'platform',
        'api_module',
        'api_class',
        'visa_required',
    ]

admin.site.register(Pipe, PipeAdmin)
admin.site.register(PipeSpecSheet, PipeSpecSheetAdmin)

