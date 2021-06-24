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
Defines forms for Watchdogs.
"""

# third party
from django import forms

# local
from cyphon.forms import ConfigToolForm
from .models import Trigger, Watchdog


class TriggerForm(forms.ModelForm):
    """
    Defines a form for adding or updating a Trigger.
    """

    class Meta:
        model = Trigger
        exclude = []


class TriggerInlineForm(forms.ModelForm):
    """
    Defines an inline form for adding or updating a Trigger.
    """

    class Meta:
        model = Trigger
        exclude = []


class WatchdogForm(ConfigToolForm):
    """
    Defines a form for adding or updating a Watchdog.
    """

    class Meta(ConfigToolForm.Meta):
        model = Watchdog

