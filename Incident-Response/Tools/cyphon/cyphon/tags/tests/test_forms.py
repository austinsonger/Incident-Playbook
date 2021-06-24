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
Tests the Tag class and related classes.
"""

# local
from tags.forms import DataTaggerForm
from .test_models import DataTaggerManagerTestCase


class DataTaggerFormTestCase(DataTaggerManagerTestCase):
    """
    Test cases for the clean method the DataTaggerForm class.
    """

    def test_invalid_field_name(self):
        """
        Tests that a validation error is thrown for an invalid
        field_name value.
        """
        form_data = {
            'container': 2,
            'field_name': 'foobar',
            'exact_match': False,
            'create_tags': False
        }
        form = DataTaggerForm(data=form_data)
        msg = ('The given field name does not '
               'appear in the selected Container.')
        self.assertFalse(form.is_valid())
        self.assertTrue(msg in str(form.errors))

    def test_invalid_no_topics(self):
        """
        Tests that a validation error is thrown when `exact_match` is
        True but no `topics` are selected.
        """
        form_data = {
            'container': 2,
            'field_name': 'user.name',
            'exact_match': True,
            'create_tags': True
        }
        form = DataTaggerForm(data=form_data)
        msg = 'Select exactly one tag topic when using exact matches.'
        self.assertFalse(form.is_valid())
        self.assertTrue(msg in str(form.errors))

    def test_invalid_multiple_topics(self):
        """
        Tests that a validation error is thrown when `exact_match` is
        True but multiple `topics` are selected.
        """
        form_data = {
            'container': 2,
            'field_name': 'user.name',
            'exact_match': True,
            'create_tags': True,
            'topics': [1, 2]
        }
        form = DataTaggerForm(data=form_data)
        msg = 'Select exactly one tag topic when using exact matches.'
        self.assertFalse(form.is_valid())
        self.assertTrue(msg in str(form.errors))

    def test_invalid_create_tags(self):
        """
        Tests that a validation error is thrown for an invalid
        create_tags value.
        """
        form_data = {
            'container': 2,
            'field_name': 'user.name',
            'exact_match': False,
            'create_tags': True,
            'topics': [1, 2]
        }
        form = DataTaggerForm(data=form_data)
        msg = ('The &quot;create tags&quot; feature is only '
               'available for exact matches.')
        self.assertFalse(form.is_valid())
        self.assertTrue(msg in str(form.errors))
