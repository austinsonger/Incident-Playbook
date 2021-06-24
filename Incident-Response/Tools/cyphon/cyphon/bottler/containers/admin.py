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
Defines a ModelAdmin subclass for Containers and registers them with
Django Admin.
"""

# third party
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# local
from bottler.containers.models import Container
from bottler.tastes.admin import TasteInLineAdmin


class ContainerAdmin(admin.ModelAdmin):
    """
    Customizes admin pages for Containers.
    """
    list_display = ['name', 'bottle', 'label']
    readonly_fields = ['preview']
    inlines = [TasteInLineAdmin, ]
    fieldsets = (
        (None, {
            'fields': ['name', 'bottle', 'label']
        }),
        ('Preview', {
            'description': _('Below is a preview of your model, '
                             'with field names mapped to field types. <br>'
                             'If the target type of a field is defined, it is '
                             'shown in parentheses after the field type. <br>'
                             'After making changes, save the model '
                             'to update the preview.'),
            'classes': ('collapse', 'pre'),
            'fields': ('preview', ),
        }),
    )
    save_as = True


admin.site.register(Container, ContainerAdmin)

