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
Defines forms for ContextFilters.
"""

# third party
from autocomplete_light import forms as auto_forms

# local
from cyphon.choices import OPERATOR_CHOICES
from cyphon.autocomplete import AutoCompleteModelFormMixin, ChoiceWidget
from .models import ContextFilter


class ContextFilterForm(auto_forms.ModelForm, AutoCompleteModelFormMixin):
    """
    Defines a form for adding or updating a ContextFilter using
    autocomplete fields.
    """

    def __init__(self, *args, **kwargs):
        super(ContextFilterForm, self).__init__(*args, **kwargs)
        self._restore_value('search_field', 'FilterSearchFieldsByContext')
        self._restore_value('value_field', 'FilterValueFieldsByContext')
        self._restore_choice('operator', OPERATOR_CHOICES, 'FilterOperatorsBySearchField')

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/contextfilter_autocomplete.js',
        ]

    class Meta:
        model = ContextFilter
        fields = ['context', 'search_field', 'operator', 'value_field']  # reorder
        widgets = {
            'search_field': ChoiceWidget('FilterSearchFieldsByContext'),
            'operator': ChoiceWidget('FilterOperatorsBySearchField'),
            'value_field': ChoiceWidget('FilterValueFieldsByContext'),
        }


class ContextFilterInlineForm(auto_forms.ModelForm, AutoCompleteModelFormMixin):
    """
    Defines an inline form for adding or updating a ContextFilter using
    autocomplete fields.
    """

    def __init__(self, *args, **kwargs):
        super(ContextFilterInlineForm, self).__init__(*args, **kwargs)
        self._restore_value('search_field', 'FilterSearchFieldsByRelatedDistillery')
        self._restore_value('value_field', 'FilterValueFieldsByFocalDistillery')
        self._restore_choice('operator', OPERATOR_CHOICES, 'FilterOperatorsBySearchField')

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/contextfilter_inline_autocomplete.js',
        ]

    class Meta:
        model = ContextFilter
        fields = ['context', 'search_field', 'operator', 'value_field']  # reorder
        widgets = {
            'search_field': ChoiceWidget('FilterSearchFieldsByRelatedDistillery'),
            'operator': ChoiceWidget('FilterOperatorsBySearchField'),
            'value_field': ChoiceWidget('FilterValueFieldsByFocalDistillery'),
        }

