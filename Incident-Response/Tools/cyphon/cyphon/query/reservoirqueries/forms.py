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
from django import forms
from django.utils.translation import ugettext_lazy as _

# local
from .models import ReservoirQueryParameters


class ReservoirQueryParametersForm(forms.ModelForm):
    """
    Form used for constructing a ReservoirQuery object.
    """
    locations = forms.CharField()


    class Meta:
        model = ReservoirQueryParameters
        exclude = ['created_by', 'locations']
        labels = {
            'start_time': _('After'),
            'end_time': _('Before')
        }

    def save(self, commit=True):
        # locations = self.cleaned_data.pop('locations')
        parameters = ReservoirQueryParameters(**self.cleaned_data)
        parameters.save()

        # for location in locations:
        #     parameters.locations.add(location)

        # if commit:
        #     parameters.save()

        return parameters
