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
Defines Autocomplete models for use in Condenser admin pages.
"""

# standard library
import json

# third party
import autocomplete_light.shortcuts as autocomplete_light
from django.utils.translation import ugettext_lazy as _

# local
from bottler.bottles.models import BottleField
from sifter.condensers.models import Condenser, Fitting


class FilterTargetFieldsAutocomplete(autocomplete_light.AutocompleteModelBase):
    """
    Defines autocomplete rules for target_fields on Fitting and
    Condenser admin pages.
    """
    model = BottleField
    search_fields = ('field_name', )

    def autocomplete_html(self):
        """
        Overrides rendering of the autocomplete.
        """
        no_matches_msg = 'no unmapped fields found'

        html = ''.join(
            [self.choice_html(c) for c in self.choices_for_request()])

        if not html:
            html = self.empty_html_format % _(no_matches_msg).capitalize()

        return self.autocomplete_html_format % html


class FilterTargetFieldsByBottle(FilterTargetFieldsAutocomplete):
    """
    Defines autocomplete rules for target_field on a Condenser admin page.
    """
    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a bottle and click to see options...'
    }

    def choices_for_request(self):
        """
        Filters target_field options based on a selected Bottle/Condenser
        and previously selected target_fields.
        """
        choices = ()

        # text typed in autocomplete input
        query = self.request.GET.get('q', '').lower().strip()

        # selected bottle on Condenser admin page
        bottle_id = self.request.GET.get('bottle', None)

        # list of target_fields already selected on Condenser admin page
        target_field_list = self.request.GET.get('target_field_list', None)

        if bottle_id:

            choices = BottleField.objects.filter(bottle=bottle_id)

            if target_field_list:
                target_fields = json.loads(target_field_list)
                choices = choices.exclude(pk__in=target_fields)

            if query:
                choices = choices.filter(field_name__icontains=query)

        return self.order_choices(choices)[0:self.limit_choices]


class FilterTargetFieldsByCondenser(FilterTargetFieldsAutocomplete):
    """
    Defines autocomplete rules for target_field on a Fitting admin page.
    """
    model = None

    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a condenser and click to see options...'
    }

    @property
    def fitting(self):
        """
        Returns the model_name of the Conderser's Fitting.
        """
        for field in self.model._meta.get_fields():
            if hasattr(field, 'related_model') \
                    and issubclass(field.related_model, Fitting):
                return field.related_model._meta.model_name

    def choices_for_request(self):
        """
        Filters target_field options based on a selected Bottle/Condenser
        and previously selected target_fields.
        """
        if not issubclass(self.model, Condenser):  # pragma: no cover
            raise TypeError('model must be a type of condenser')

        choices = ()

        # text typed in autocomplete input
        query = self.request.GET.get('q', '').lower().strip()

        # selected condenser on Fitting admin page
        condenser_id = self.request.GET.get('condenser', None)

        if condenser_id:

            condenser = self.model.objects.get(pk=condenser_id)
            choices = BottleField.objects.filter(bottle=condenser.bottle)

            # exclude BottleFields that are already fitted to this condenser
            if self.fitting:
                kwargs = {self.fitting + '__condenser': condenser}
                choices = choices.exclude(**kwargs)

            if query:
                choices = choices.filter(field_name__icontains=query)

        return self.order_choices(choices)[0:self.limit_choices]
