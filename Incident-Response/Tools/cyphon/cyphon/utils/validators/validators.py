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
Provides field validators.
"""

# standard library
import re

# third party
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

_DISTILLERY_SETTINGS = settings.DISTILLERIES

IDENTIFIER_VALIDATOR = RegexValidator(r'[a-zA-Z_][a-zA-Z0-9_]*',
                                      'Not a valid Python identifier')


def validate_str_substitution(template, value_count):
    """
    Ensures that the number of values provided for a string formatter
    matches the number of specifiers in the template.
    """
    if not template and value_count > 1:
        raise ValidationError(_('No template has been provided '
                                'for formatting multiple fields.'))
    elif template:
        specifiers = re.findall(r'{[0-9]?}', template)

        if len(specifiers) > value_count:
            if value_count == 1:
                raise ValidationError(_('The formatter should only contain one '
                                        '"{}" specifier for the source field.'))
            else:
                raise ValidationError(_('The number of "{}" specifiers in '
                                        'the formatter exceeds the number '
                                        'of source fields.'))

        elif len(specifiers) < value_count:
            if value_count == 1:
                raise ValidationError(_('The formatter should contain one "{}" '
                                        'specifier.'))
            else:
                raise ValidationError(_('The formatter contains too few "{}" '
                                        'specifiers for the number of source '
                                        'fields.'))


def validate_timeframe(start, end):
    """
    Validator to ensure that the start and end datetimes make sense (i.e.,
    that the start datetime is before the end datetime, and the endtime is no
    later than the current time).
    """
    if start >= end:
        raise ValidationError(u'Start date and time must precede '
                              'end date and time.')


def db_name_validator(db_name):
    """
    Validates a Collection or Warehouse name.
    """
    if re.search(r'\s', db_name):
        raise ValidationError(_('Name cannot contain spaces'))

    elif re.search(r'\W', db_name.replace('-', '')):
        raise ValidationError(_('Name cannot contain special characters '
                                'other than underscores and hypens.'))


def field_name_validator(field_name):
    """
    Validates a field name for a document.

    Note that this validator allows periods in the name. Dot notation
    is permitted because it will be used to nest the field within the
    document. E.g., a field name 'user.screen_name' will be saved as
    the field 'screen_name' within the embedded document 'user'.)
    """
    reserved_names = [
        '_id',
        _DISTILLERY_SETTINGS['LABEL_KEY'],
        _DISTILLERY_SETTINGS['RAW_DATA_KEY']
    ]

    if field_name in reserved_names:
        raise ValidationError(_('%s is a reserved field name' % field_name))

    elif re.match(r'^\$', field_name):
        raise ValidationError(_('Field name cannot start with "$"'))

    elif re.search(r'\s', field_name):
        raise ValidationError(_('Field name cannot contain spaces'))

    elif re.search(r'\W', field_name.replace('$', '').replace('@', '')):
        raise ValidationError(_('Field name cannot contain special characters'
                                'other than underscores, @, and $.'))


def key_file_validator(field_file):
    """
    Validates a FieldFile.
    """
    filename = field_file.name
    valid_ext = filename.endswith('.pem') or filename.endswith('.pub')
    if not valid_ext:
        raise ValidationError(_('The key file must be either '
                                'a .pem or .pub file.'))


def lowercase_validator(value):
    """
    Validates that a string is lowercase.
    """
    if value != value.lower():
        raise ValidationError(_('Value must be lowercase string.'))


def regex_validator(value):
    """
    Validates a regex.
    """
    try:
        re.compile(value)
    except re.error:
        raise ValidationError(_('Please provide a valid regular expression.'))
