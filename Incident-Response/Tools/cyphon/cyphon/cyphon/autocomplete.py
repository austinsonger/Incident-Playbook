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
from autocomplete_light.widgets import ChoiceWidget as _ChoiceWidget

# local
from utils.choices.choices import get_choice_by_value


class ChoiceWidget(_ChoiceWidget):

    def build_attrs(self, extra_attrs=None, autocomplete=None, **kwargs):
        extra_attrs.update(getattr(autocomplete, 'attrs', {}))
        return super(ChoiceWidget, self).build_attrs(
            extra_attrs, autocomplete, **kwargs)


class AutoCompleteModelFormMixin(object):
    """
    Provides a mixin for restoring values to autocomplete fields.
    """

    def _restore_value(self, field_name, autocomplete_name):
        """
        Takes the name of an form field and the name of a registered
        Autocomplete widget. If the form is initialized with a value
        for the field, the method restores the value to the Autocomplete
        widget.
        """
        value = self.initial.get(field_name, None)
        if value not in [None, '']:
            self.fields[field_name].widget = ChoiceWidget(
                autocomplete_name,
                extra_context={
                    'values': [value],
                    'choices': [value]
                }
            )

    def _restore_choice(self, field_name, choices, autocomplete_name):
        """
        Takes the name of an form field, a list of choices, and the name
        of a registered Autocomplete widget. If the form is initialized
        with a value for the field, the method restores the value to the
        Autocomplete widget.
        """
        value = self.initial.get(field_name, None)
        if value not in [None, '']:
            choice = get_choice_by_value(choices, value)
            if choice:
                self.fields[field_name].widget = ChoiceWidget(
                    autocomplete_name,
                    extra_context={
                        'values': [choice[0]],
                        'choices': [choice]
                    }
                )

