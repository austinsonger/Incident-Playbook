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
Defines ModelAdmins for Inspections and InspectionSteps, and registers
them with Django Admin.
"""

# third party
from django.contrib import admin

# local
from . import models


class InspectionStepInLineAdmin(admin.TabularInline):
    """
    Customizes admin inline tables for InspectionSteps.
    """
    model = models.InspectionStep


class InspectionStepAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for InspectionSteps.
    """
    list_display = [
        'id',
        'inspection',
        'sieve',
        'result_value',
        'rank',
    ]
    list_display_links = ['id', ]


class InspectionAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Inspections.
    """
    inlines = [InspectionStepInLineAdmin, ]
    save_as = True


admin.site.register(models.InspectionStep, InspectionStepAdmin)
admin.site.register(models.Inspection, InspectionAdmin)
