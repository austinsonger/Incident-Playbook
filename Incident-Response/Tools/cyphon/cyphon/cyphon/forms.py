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
Defines forms for configurations.
"""

# third party
from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

# these values should correspond to the field in ConfigToolForm
CONFIG_TEST_VALUE_FIELD = 'config_test_string'
CONFIG_TEST_BUTTON = 'config_test_button'
CONFIG_TEST_RESULT_FIELD = 'config_test_result'

CONFIG_TOOL_INPUTS = (
    CONFIG_TEST_VALUE_FIELD,
    CONFIG_TEST_BUTTON,
    CONFIG_TEST_RESULT_FIELD,
)


class ConfigToolButtonWidget(forms.Widget):
    """
    A form Widget for a "Run Test" button for a configuration test.
    """
    template_name = 'config_test_button_widget.html'

    def render(self, name, value, attrs=None):
        context = {
            'url': '/'
        }
        return mark_safe(render_to_string(self.template_name, context))


class ConfigToolForm(forms.ModelForm):
    """
    Defines a ModelForm with a tool for testing a configuration.
    """

    class Meta:
        exclude = []

    config_test_string = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text='Enter a test string.',
        label=''
    )
    config_test_button = forms.CharField(
        widget=ConfigToolButtonWidget,
        required=False,
        label=''
    )
    config_test_result = forms.CharField(
        widget=forms.Textarea(attrs={'readonly':'readonly'}),
        required=False,
        label='Test result'
    )

    class Media:
        js = ['js/cookie.js', 'js/config-tool.js']

    def get_test_value(self):
        """
        Returns the test value from the form.
        """
        return self.cleaned_data[CONFIG_TEST_VALUE_FIELD]

