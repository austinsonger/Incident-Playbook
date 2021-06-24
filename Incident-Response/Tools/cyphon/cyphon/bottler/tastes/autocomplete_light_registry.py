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
Defines Autocomplete models for use with admin forms for Tastes.
"""

# third party
import autocomplete_light.shortcuts as autocomplete_light
from django.utils.encoding import force_text

# local
from cyphon.choices import TEXT_FIELDS, DATE_FIELDS, LOCATION_FIELDS
from bottler.bottles.models import Bottle
from bottler.containers.models import Container
from bottler.labels.models import Label


class FilterFieldsAutocompleteBase(autocomplete_light.AutocompleteListBase):
    """
    Defines autocomplete rules for source on the Container admin page.
    """
    choices = []
    field_types = []

    @staticmethod
    def _query_is_match(field, query):
        """
        Takes a DataField and a query string. Returns a Boolean
        indicating whether the DataField's field_name contains the query
        string.
        """
        if query and query not in force_text(field.field_name).lower():
            return False
        else:
            return True

    def _field_type_is_match(self, field, query):
        """
        Takes a DataField and a query string. Returns a Boolean
        indicating whether the DataField's field_type matches one of
        the Autocomplete's field_types and the DataField's field_name
        contains the query string.
        """
        if self.field_types and field.field_type not in self.field_types:
            return False
        else:
            return self._query_is_match(field, query)


class FilterFieldsByContainer(FilterFieldsAutocompleteBase):
    """
    Defines autocomplete rules for source fields on the Taste admin page.
    """
    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a container and click to see options...'
    }

    def choices_for_request(self):
        """
        Filters field options based on a selected Container.
        """
        if self.choices is None:  # pragma: no cover
            raise RuntimeError('autocomplete.choices is not set')

        request_choices = []

        # text typed in autocomplete input
        query = self.request.GET.get('q', '').lower().strip()

        # selected container on Taste admin page
        container_id = self.request.GET.get('container', None)

        if container_id:
            container = Container.objects.get(pk=container_id)
            for field in container.fields:
                if self._field_type_is_match(field, query):
                    request_choices.append(field.field_name)

        return self.order_choices(request_choices)[0:self.limit_choices]


class FilterCharFieldsByContainer(FilterFieldsByContainer):
    """
    Defines autocomplete rules for CharFields/TextFields on the Container
    admin page.
    """
    field_types = TEXT_FIELDS


class FilterDateTimeFieldsByContainer(FilterFieldsByContainer):
    """
    Defines autocomplete rules for DataTimeFields on the Container admin page.
    """
    field_types = DATE_FIELDS


class FilterLocationFieldsByContainer(FilterFieldsByContainer):
    """
    Defines autocomplete rules for LocationFields on the Container admin page.
    """
    field_types = LOCATION_FIELDS


class FilterFieldsByBottleAndLabel(FilterFieldsAutocompleteBase):
    """
    Defines autocomplete rules for source fields for an inline
    Taste on the Container admin page.
    """
    attrs = {
        'data-autocomplete-minimum-characters': 0,
        'placeholder': 'select a bottle/label and click to see options...'
    }

    def choices_for_request(self):
        """
        Filters field options based on a selected Bottle and
        (optionally) Label.
        """
        if self.choices is None:
            raise RuntimeError('autocomplete.choices is not set')

        request_choices = []

        # text typed in autocomplete input
        query = self.request.GET.get('q', '').lower().strip()

        # selected bottle on Container admin page
        bottle_id = self.request.GET.get('bottle', None)

        # selected label on Container admin page
        label_id = self.request.GET.get('label', None)

        if bottle_id:
            bottle = Bottle.objects.get(pk=bottle_id)
            for bottle_field in bottle.get_fields():
                if self._field_type_is_match(bottle_field, query):
                    request_choices.append(bottle_field.field_name)

        if label_id:
            label = Label.objects.get(pk=label_id)
            for label_field in label.get_fields():
                if self._field_type_is_match(label_field, query):
                    request_choices.append(label_field.field_name)

        return self.order_choices(request_choices)[0:self.limit_choices]


class FilterCharFieldsByBottleAndLabel(FilterFieldsByBottleAndLabel):
    """
    Defines autocomplete rules for CharFields/TextFields for an inline
    Taste on the Container admin page.
    """
    field_types = TEXT_FIELDS


class FilterDateTimeFieldsByBottleAndLabel(FilterFieldsByBottleAndLabel):
    """
    Defines autocomplete rules for DataTimeFields for an inline
    Taste on the Container admin page.
    """
    field_types = DATE_FIELDS


class FilterLocationFieldsByBottleAndLabel(FilterFieldsByBottleAndLabel):
    """
    Defines autocomplete rules for LocationFields for an inline
    Taste on the Container admin page.
    """
    field_types = LOCATION_FIELDS


autocomplete_light.register(FilterCharFieldsByContainer)
autocomplete_light.register(FilterDateTimeFieldsByContainer)
autocomplete_light.register(FilterLocationFieldsByContainer)
autocomplete_light.register(FilterCharFieldsByBottleAndLabel)
autocomplete_light.register(FilterDateTimeFieldsByBottleAndLabel)
autocomplete_light.register(FilterLocationFieldsByBottleAndLabel)

