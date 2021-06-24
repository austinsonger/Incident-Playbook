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

# standard library
import os
import re
from operator import itemgetter

# third party
from django.conf import settings

# local
from bottler.bottles.models import BottleField
from bottler.labels.models import LabelField

_DISTILLERY_SETTINGS = settings.DISTILLERIES


def get_package_choices(path):
    """
    (str) -> tuple(tuple)

    Takes a path and returns a tuple of tuples representing the Python packages
    it contains. Each inner tuple provides a (value, label) choice for a package.

    Returns choices in a format suitable for use in a choices argument
    for a CharField in a Django Model, e.g.:

    >>> get_package_choices('platforms')
    (('facebook', 'facebook'), ('twitter', 'twitter'))

    """
    choices = []

    # get a list of directories in the path
    directories = next(os.walk(path))[1]

    for directory in directories:

        # skip the directory if it starts with '__' (e.g., '__pycache__')
        # or if it's only used for tests
        if not re.search('^(__|test)', directory):

            this_path = os.path.join(path, directory)

            # get the files in the directory
            files = next(os.walk(this_path))[2]

            # if the directory is a Python package...
            if '__init__.py' in files:

                # ...add the package name to the list of choices
                # (let's just make the key and value the same)
                choice = (directory, directory)
                choices.append(choice)

    choices.sort(key=itemgetter(0))
    return tuple(choices)


def get_field_type(field_name):
    """

    """
    field_segments = field_name.split('.')
    is_label = field_segments[0] == _DISTILLERY_SETTINGS['LABEL_KEY']

    if is_label:
        field = LabelField.objects.get_by_natural_key(field_segments[-1])
    else:
        field = BottleField.objects.get_by_natural_key(field_segments[-1])

    return field.field_type


def get_operator_choices(field_type):
    """

    """
    if (field_type in ['CharField', 'TextField']):
        options = [
            ('regex', 'contains'),
            ('eq', 'equals'),
            ('not:regex', 'does not contain'),
        ]

    elif (field_type == 'BooleanField'):
        options = [
            ('eq', 'is true'),
            ('not:eq', 'is false'),
        ]

    elif (field_type == 'DateTimeField'):
        options = [
            ('gte', 'occurred on or after'),
            ('lte', 'occurred on or before'),
        ]

    elif (field_type == 'ListField'):
        options = [
            ('in', 'contains'),
            ('not:in', 'does not contain'),
        ]

    elif (field_type in ['FloatField', 'IntegerField']):
        options = [
            ('eq', 'equals'),
            ('ne', 'does not equal'),
            ('gt', 'greater than'),
            ('gte', 'greater than or equal to'),
            ('lt', 'less than'),
            ('lte', 'less than or equal to'),
        ]

    else:
        options = [
            ('eq', 'equals'),
            ('not:eq', 'does not equal'),
        ]

    return options


def get_choice_by_value(choices, value):
    """

    """
    for choice in choices:
        if choice[0] == value:
            return choice
