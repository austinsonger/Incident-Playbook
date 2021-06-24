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
Defines forms for Tastes.
"""

# third party
from autocomplete_light import forms as auto_forms

# local
from cyphon.autocomplete import AutoCompleteModelFormMixin, ChoiceWidget
from .models import Taste


class TasteForm(auto_forms.ModelForm, AutoCompleteModelFormMixin):
    """
    Defines a form for adding or updating a Taste using autocomplete
    fields.
    """

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/taste_autocomplete.js',
        ]

    class Meta:
        model = Taste
        exclude = []
        widgets = {
            'author': ChoiceWidget('FilterCharFieldsByContainer'),
            'title': ChoiceWidget('FilterCharFieldsByContainer'),
            'content': ChoiceWidget('FilterCharFieldsByContainer'),
            'location': ChoiceWidget('FilterLocationFieldsByContainer'),
            'datetime': ChoiceWidget('FilterDateTimeFieldsByContainer'),
            'date_string': ChoiceWidget('FilterCharFieldsByContainer'),
        }
        fields = [
            'container',
            'author',
            'title',
            'content',
            'location',
            'location_format',
            'datetime',
            'date_string',
            'date_format',
        ]

    def __init__(self, *args, **kwargs):
        super(TasteForm, self).__init__(*args, **kwargs)
        self._restore_value('author', 'FilterCharFieldsByContainer')
        self._restore_value('title', 'FilterCharFieldsByContainer')
        self._restore_value('content', 'FilterCharFieldsByContainer')
        self._restore_value('location', 'FilterLocationFieldsByContainer')
        self._restore_value('datetime', 'FilterDateTimeFieldsByContainer')
        self._restore_value('date_string', 'FilterCharFieldsByContainer')


class TasteInlineForm(auto_forms.ModelForm, AutoCompleteModelFormMixin):
    """
    Defines an inline form for adding or updating a Taste using
    autocomplete fields.
    """

    class Media:
        js = [
            'js/dependent_autocomplete.js',
            'js/taste_inline_autocomplete.js',
        ]

    class Meta:
        model = Taste
        exclude = []
        widgets = {
            'author': ChoiceWidget('FilterCharFieldsByBottleAndLabel'),
            'title': ChoiceWidget('FilterCharFieldsByBottleAndLabel'),
            'content': ChoiceWidget('FilterCharFieldsByBottleAndLabel'),
            'location': ChoiceWidget('FilterLocationFieldsByBottleAndLabel'),
            'datetime': ChoiceWidget('FilterDateTimeFieldsByBottleAndLabel'),
            'date_string': ChoiceWidget('FilterCharFieldsByBottleAndLabel'),
        }

    def __init__(self, *args, **kwargs):
        super(TasteInlineForm, self).__init__(*args, **kwargs)
        self._restore_value('author', 'FilterCharFieldsByBottleAndLabel')
        self._restore_value('title', 'FilterCharFieldsByBottleAndLabel')
        self._restore_value('content', 'FilterCharFieldsByBottleAndLabel')
        self._restore_value('location', 'FilterLocationFieldsByBottleAndLabel')
        self._restore_value('datetime', 'FilterDateTimeFieldsByBottleAndLabel')
        self._restore_value('date_string', 'FilterCharFieldsByBottleAndLabel')
