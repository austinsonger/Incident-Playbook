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
Defines forms for Fittings and Condensers.
"""

# third party
from autocomplete_light import forms as auto_forms

# local
from cyphon.forms import ConfigToolForm


class ParserForm(ConfigToolForm):
    """
    Defines a form for adding or updating a Parser.
    """
    pass


class CondenserForm(auto_forms.ModelForm, ConfigToolForm):
    """
    Defines a form for adding or updating a Condenser using autocomplete
    fields.
    """
    pass


class FittingForm(auto_forms.ModelForm):
    """
    Defines a form for adding or updating a Fitting using autocomplete
    fields.
    """

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/fitting_autocomplete.js',
        ]

    class Meta:
        exclude = []
        fields = ['condenser', 'target_field', 'content_type', 'object_id']
        autocomplete_fields = ['target_field']
        autocomplete_names = {'target_field': 'FilterTargetFieldsByCondenser'}


class FittingInlineForm(auto_forms.ModelForm):
    """
    Defines an inline form for adding or updating a Fitting using
    autocomplete fields.
    """

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/fitting_inline_autocomplete.js',
        ]

    class Meta:
        exclude = []
        fields = ['condenser', 'target_field', 'content_type', 'object_id']
        autocomplete_fields = ['target_field']
        autocomplete_names = {'target_field': 'FilterTargetFieldsByBottle'}

