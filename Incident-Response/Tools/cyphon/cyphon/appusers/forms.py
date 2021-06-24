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
Django forms for AppUser app.
"""

# third party
from django import forms
from django.contrib.auth import forms as auth_forms

# local
from appusers.models import AppUser


class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given
    username.
    """

    class Meta:
        model = AppUser
        fields = ('email', )


class CustomUserChangeForm(auth_forms.UserChangeForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with a password hash display field.
    """

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AppUser
        fields = '__all__'
