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
Defines forms for Monitors.
"""

# third party
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from distilleries.models import Distillery
from .models import Monitor


class MonitorForm(forms.ModelForm):
    """
    Defines a form for adding or updating a Monitor.
    """

    class Meta(object):
        model = Monitor
        exclude = []

    def clean(self):
        """
        Checks that the Monitor's Distilleries have a Datetime field
        defined.
        """
        super(MonitorForm, self).clean()
        distilleries = self.cleaned_data.get('distilleries', [])
        for distillery_pk in distilleries:
            distillery = Distillery.objects.get(pk=distillery_pk)
            if not distillery.get_searchable_date_field():
                msg = _('The Container for the Distillery "%s" must have a '
                        'Taste with a designated Datetime field.' % distillery)
                raise ValidationError(msg)

        return self.cleaned_data
