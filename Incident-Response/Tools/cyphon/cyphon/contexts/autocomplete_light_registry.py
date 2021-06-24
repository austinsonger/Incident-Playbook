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
Defines Autocomplete models for use in admin pages for the Contexts app.
"""

# third party
import autocomplete_light.shortcuts as autocomplete_light

# local
from distilleries.models import Distillery
from utils.choices.choices import get_operator_choices, get_field_type
from .models import Context


class FilterValueFieldsByFocalDistillery(autocomplete_light.AutocompleteListBase):
    """
    Defines autocomplete rules for the value_field on the Context admin
    page.
    """
    choices = ()

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a distillery and click to see options...'
    }

    def choices_for_request(self):
        """
        Overrides the choices_for_request method of the AutocompleteListBase
        class. Filters options based on the selected primary_distillery.
        """
        choices = self.choices
        distillery_id = self.request.GET.get('primary_distillery', None)

        if distillery_id:
            distillery = Distillery.objects.get(pk=distillery_id)
            choices = distillery.get_field_list()

        return self.order_choices(choices)[0:self.limit_choices]


class FilterSearchFieldsByRelatedDistillery(autocomplete_light.AutocompleteListBase):
    """
    Defines autocomplete rules for the value_field on the Context admin
    page.
    """
    choices = ()

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a related distillery and click to see options...'
    }

    def choices_for_request(self):
        """
        Overrides the choices_for_request method of the AutocompleteListBase
        class. Filters options based on the selected related_distillery.
        """
        choices = self.choices
        distillery_id = self.request.GET.get('related_distillery', None)

        if distillery_id:
            distillery = Distillery.objects.get(pk=distillery_id)
            choices = distillery.get_field_list()

        return self.order_choices(choices)[0:self.limit_choices]


class FilterValueFieldsByContext(autocomplete_light.AutocompleteListBase):
    """
    Defines autocomplete rules for the value_field on the ContextFilter
    admin page.
    """
    choices = ()

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a distillery and click to see options...'
    }

    def choices_for_request(self):
        """
        Overrides the choices_for_request method of the AutocompleteListBase
        class. Filters options based on the primary_distillery of the selected
        Context.
        """
        choices = self.choices
        context_id = self.request.GET.get('context', None)

        if context_id:
            context = Context.objects.select_related('primary_distillery')\
                             .get(pk=context_id)
            choices = context.primary_distillery.get_field_list()

        return self.order_choices(choices)[0:self.limit_choices]


class FilterSearchFieldsByContext(autocomplete_light.AutocompleteListBase):
    """
    Defines autocomplete rules for the value_field on the ContextFilter
    admin page.
    """
    choices = ()

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a distillery and click to see options...'
    }

    def choices_for_request(self):
        """
        Overrides the choices_for_request method of the AutocompleteListBase
        class. Filters options based on the related_distillery of the
        selected Context.
        """
        choices = self.choices
        context_id = self.request.GET.get('context', None)

        if context_id:
            context = Context.objects.select_related('related_distillery')\
                             .get(pk=context_id)
            choices = context.related_distillery.get_field_list()

        return self.order_choices(choices)[0:self.limit_choices]


class FilterOperatorsBySearchField(autocomplete_light.AutocompleteChoiceListBase):
    """
    Defines autocomplete rules for the operator field on the ContextFilter
    admin page.
    """
    choices = ()

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a search field and click to see options...'
    }

    def choices_for_request(self):
        """
        Overrides the choices_for_request method of the AutocompleteListBase
        class. Filters options based on the selected search_field.
        """
        choices = self.choices
        search_field = self.request.GET.get('search_field', None)

        if search_field:
            field_type = get_field_type(search_field)
            choices = get_operator_choices(field_type)

        return self.order_choices(choices)[0:self.limit_choices]


autocomplete_light.register(FilterValueFieldsByFocalDistillery)
autocomplete_light.register(FilterSearchFieldsByRelatedDistillery)
autocomplete_light.register(FilterValueFieldsByContext)
autocomplete_light.register(FilterSearchFieldsByContext)
autocomplete_light.register(FilterOperatorsBySearchField)

