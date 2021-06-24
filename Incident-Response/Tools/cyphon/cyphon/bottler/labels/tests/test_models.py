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
Tests the Label class and related classes.
"""

# standard library
from collections import OrderedDict

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from bottler.labels.models import _DISTILLERY_SETTINGS, Label, LabelField
from tests.fixture_manager import get_fixtures


class LabelBaseTestCase(TestCase):
    """
    Base class for testing the Label and LabelField classes.
    """
    fixtures = get_fixtures(['labels'])

    high_priority_msg = {'subject': '[CRIT-111]'}
    med_priority_msg = {'subject': '[WARN-222]'}
    low_priority_msg = {'subject': '[INFO-333]'}

    def setUp(self):
        self.label_field = LabelField.objects.get(pk=1)
        self.label = Label.objects.get_by_natural_key('mail')


# TODO(LH): mock out LabelField.analyzer.get_result()


class LabelFieldManagerTestCase(LabelBaseTestCase):
    """
    Tests the LabelFieldManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for an existing LabelField.
        """
        labelfield = LabelField.objects.get_by_natural_key('priority')
        self.assertEqual(labelfield.pk, 1)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method for a LabelField that
        doesn't exist.
        """
        with LogCapture() as log_capture:
            LabelField.objects.get_by_natural_key('dummy_field')
            expected = 'LabelField "dummy_field" does not exist'
            log_capture.check(
                ('bottler.datafields.models', 'ERROR', expected),
            )


class LabelFieldTestCase(LabelBaseTestCase):
    """
    Tests the LabelField class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the LabelField class.
        """
        actual = str(self.label_field)
        expected = 'priority:CharField <- prioritize_emails (inspection)'
        self.assertEqual(actual, expected)

    def test_create(self):
        """
        Tests the create method of the LabelField class.
        """
        actual = self.label_field.create(self.low_priority_msg)
        self.assertEqual(actual, {'priority': 'LOW'})

        actual = self.label_field.create(self.med_priority_msg)
        self.assertEqual(actual, {'priority': 'MEDIUM'})

        actual = self.label_field.create(self.high_priority_msg)
        self.assertEqual(actual, {'priority': 'HIGH'})


class LabelTestCase(LabelBaseTestCase):
    """
    Tests the Label class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the LabelField class.
        """
        self.assertEqual(str(self.label), 'mail')

    def test_label_create(self):
        """
        Tests the create method of the Label class.
        """
        actual = self.label.create(self.low_priority_msg)
        expected = {
            _DISTILLERY_SETTINGS['LABEL_KEY']: {
                'priority': 'LOW',
                'source_ip_location': None
            }
        }
        self.assertEqual(actual, expected)

    def test_label_add(self):
        """
        Tests the add method of the Label class.
        """
        actual = self.label.add(self.low_priority_msg)
        expected = {
            'subject': '[INFO-333]',
            _DISTILLERY_SETTINGS['LABEL_KEY']: {
                'priority': 'LOW',
                'source_ip_location': None
            }
        }
        self.assertEqual(actual, expected)

    def test_get_fields(self):
        """
        Tests the get_fields method.
        """
        actual = self.label.get_fields()
        self.assertEqual(actual[0].field_name,
                         _DISTILLERY_SETTINGS['LABEL_KEY'] + '.priority')
        self.assertEqual(actual[0].field_type, 'CharField')
        self.assertEqual(actual[0].target_type, 'Keyword')
        self.assertEqual(actual[1].field_name,
                         _DISTILLERY_SETTINGS['LABEL_KEY'] + '.source_ip_location')
        self.assertEqual(actual[1].field_type, 'PointField')
        self.assertEqual(actual[1].target_type, 'Location')

    def test_get_structure(self):
        """
        Tests the get_structure method for nonnested fields.
        """
        actual = self.label.get_structure()
        expected = OrderedDict([
            ('priority', 'CharField (Keyword)'),
            ('source_ip_location', 'PointField (Location)')
        ])
        self.assertEqual(actual, expected)

    def test_preview(self):
        """
        Tests the preview method for nonnested fields.
        """
        actual = self.label.preview()
        expected = \
"""{
    "priority": "CharField (Keyword)",
    "source_ip_location": "PointField (Location)"
}"""
        self.assertEqual(actual, expected)
