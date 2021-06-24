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
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

# local
from appusers.forms import CustomUserChangeForm, CustomUserCreationForm
from appusers.models import AppUser


class AppUserAdmin(UserAdmin):
    """
    The forms to add and change user instances.

    The fields to be used in displaying the User model. These override
    the definitions on the base UserAdmin that reference the removed
    'username' field.
    """
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            )
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',),
        }),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(AppUser, AppUserAdmin)
