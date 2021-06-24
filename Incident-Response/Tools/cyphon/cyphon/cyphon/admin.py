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
Defines a ModelAdmin subclasses for testing configurations on admin pages.
"""

# standard library
from collections import OrderedDict
import email
import json
import logging

# third party
from django.conf.urls import url
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

LOGGER = logging.getLogger(__name__)

CONFIG_TOOL_CLASSES = (
    'collapse',
    'grp-collapse',
    'grp-closed',
    'config-tool',
)


class ConfigToolAdmin(admin.ModelAdmin):
    """
    Provides an admin page with a configuration testing tool. The tool
    takes a test string and returns the result for the specified
    model method.

    Attributes:
        model_method: the method that is being tested
        data_format: defines how the test string should be interpreted
                     (e.g., as a str, json, int, or float)

    """
    # TODO(LH): assert form is a ConfigForm

    model_method = 'process'
    data_format = 'str'

    def get_urls(self):
        """
        Overrides the ModelAdmin get_urls method to add urls for running
        the configuration test and returning the result.
        """
        urls = super(ConfigToolAdmin, self).get_urls()
        custom_urls = [
            url(r'(?P<object_id>[\d]+)/change/test/$',
                self.admin_site.admin_view(self.run_test)),
            url(r'add/test/$', self.admin_site.admin_view(self.run_test)),
        ]
        return custom_urls + urls

    @staticmethod
    def _get_test_value(form):
        """
        Takes a ConfigToolForm and returns its test value.
        """
        return form.get_test_value()

    @staticmethod
    def _parse_email(text):
        """
        Takes a string represeting an email message and returns a
        Message object.
        """
        return email.message_from_string(text)

    def _format_test_value(self, form):
        """
        Takes a ConfigToolForm and returns its test value in a format
        that can be passed to the ConfigToolAdmin's model_method.
        """
        raw_value = self._get_test_value(form)
        formatters = {
            'str': str,
            'json': json.loads,
            'int': int,
            'float': float,
            'email': self._parse_email,
        }
        format_val = formatters.get(self.data_format, 'str')
        return format_val(raw_value)

    def _get_model_instance(self, object_id):
        """
        Takes a object id and returns the Model instance for that id.
        Returns None if the object id is None.
        """
        if object_id:
            obj = self.model.objects.get(pk=object_id)
            return obj

    def _create_form_instance(self, request, object_id):
        """
        Takes an HttpRequest and the object id for a Model instance.
        Returns a ModelForm instance initialized with the QueryDict from
        the request.
        """
        instance = self._get_model_instance(object_id)
        return self.form(request.POST, instance=instance)

    def _create_formset_instances(self, request, instance):
        """
        Takes an HttpRequest and a Model instance. Returns a list of
        ModelFormsets initialized with the POST data from the request.
        """
        formsets_with_inlines = self.get_formsets_with_inlines(request)
        return [inline_formset(request.POST, instance=instance) \
                for (inline_formset, dummy_admin) in formsets_with_inlines]

    @staticmethod
    def _formsets_are_valid(formsets):
        """
        Takes a list of ModelFormSets and returns a Boolean indicating
        whether all formsets are valid.
        """
        valid = True
        for formset in formsets:
            valid &= formset.is_valid()
        return valid

    @staticmethod
    def _get_related_name(formset):
        """
        Takes a ModelFormSet and a returns the name of the model with
        which it's associated.
        """
        return formset.fk.remote_field.get_accessor_name()

    @staticmethod
    def _get_form_errors(form):
        """
        Takes a ModelForm and a returns a dict of its validation errors.
        """
        form_errors = form.errors.as_json()
        return json.loads(form_errors)

    def _format_form_errors(self, form, prefix=''):
        """
        Takes a ModelForm and an optional field prefix. Returns a
        string detailing validation errors for fields in the form.
        """
        error_dict = self._get_form_errors(form)
        error_msg = ''

        for (field, errors) in sorted(error_dict.items()):
            msg_str = ' '.join([error['message'] for error in errors])
            error_msg += prefix + field + ': ' + msg_str + '\n'

        return error_msg

    def _format_formset_errors(self, formset):
        """
        Takes a ModelFormSet and returns a string detailing any
        validation errors for forms in the formset.
        """
        related_name = self._get_related_name(formset)
        error_mgs = ''

        for index in range(0, formset.total_form_count()):
            form = formset.forms[index]
            prefix = '\t%s-%s-' % (related_name, index)
            error_mgs += self._format_form_errors(form, prefix)

        return error_mgs

    def _format_errors(self, form, formsets):
        """
        Takes a ModelForm and a list of ModelFormSets and returns a
        string detailing any validation errors for the form or formsets.
        """
        error_msg = 'Sorry! The following fields contained errors:\n\n'

        # add errors for the parent form
        error_msg += self._format_form_errors(form, prefix='\t')

        # add errors for each formset
        for formset in formsets:
            error_msg += self._format_formset_errors(formset)

        error_msg += '\nPlease correct these errors and try again.'

        return error_msg

    def _sort_dict(self, data):
        """
        Takes a dictionary and returns an OrderedDict in which all keys
        are sorted.
        """
        result = OrderedDict()
        for (key, value) in sorted(data.items()):
            if isinstance(value, dict):
                result[key] = self._sort_dict(value)
            else:
                result[key] = value
        return result

    def _format_result(self, result):
        """
        Takes the result returned from the ConfigToolAdmin's model_method
        and returns it as a string. If the result is a dict, prettifies
        the string before returning it.
        """
        if isinstance(result, dict):
            sorted_dict = self._sort_dict(result)
            return json.dumps(sorted_dict, indent=4)
        return str(result)

    def _get_result(self, form, instance):
        """
        Takes a ConfigToolForm and a Model instance. Passes the test value
        in the form to the method of the Model instance specified by the
        ConfigToolAdmin's model_method. Returns the result as a string.
        """
        try:
            value = self._format_test_value(form)
            result = getattr(instance, self.model_method)(value)
            return self._format_result(result)
        except ValueError as error:
            return 'The test string is improperly formatted: %s' % error

    @method_decorator(csrf_protect)
    def run_test(self, request, object_id=None):
        """
        Takes an HttpRequest with data from a ConfigToolForm and the
        object id for a Model instance. Creates a temporary version
        of the Model instance using the form data and returns a
        JsonResponse with the result of the configuration test.
        """
        try:
            with transaction.atomic():

                forms_are_valid = True
                form = self._create_form_instance(request, object_id)

                if form.is_valid():
                    instance = form.save()

                    # pass the parent model instance to the formsets to create
                    # related instances
                    formsets = self._create_formset_instances(request, instance)

                    if self._formsets_are_valid(formsets):
                        for formset in formsets:
                            formset.save()

                        # all models are now saved, so get the test result
                        result = self._get_result(form, instance)
                    else:
                        forms_are_valid = False
                else:
                    formsets = []
                    forms_are_valid = False

                if not forms_are_valid:
                    result = self._format_errors(form, formsets)

                # rollback the database when exiting the atomic block
                transaction.set_rollback(True)

        except IntegrityError as error:
            LOGGER.error('An error occurred while creating a test instance: %s', request)
            result = 'Could not create an object for testing: %s' % error

        except ValidationError as error:
            LOGGER.error('An error occurred while initializing a config test: %s', request)
            result = 'A validation error occurred: %s' % error

        return JsonResponse({'result': result})


class JSONDataAdmin(admin.ModelAdmin):
    """
    Provides a |ModelAdmin| for a model with a |JSONField| named `data`.
    Creates a prettified version of the field for display.
    """
    readonly_fields = ('data_prettified',)

    def data_prettified(self, instance):
        """
        Displays sorted, pretty-printed JSON.
        """
        if hasattr(instance, 'data'):
            return json.dumps(instance.data, sort_keys=True, indent=4)
        else:
            LOGGER.error('Object has no data attribute.')

    data_prettified.short_description = 'data'
