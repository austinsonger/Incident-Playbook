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
Tests the Container class.
"""

# standard library
from collections import OrderedDict
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from bottler.containers.models import _DISTILLERY_SETTINGS, Container
from tests.fixture_manager import get_fixtures


class ContainerTestCase(TestCase):
    """
    Test case for the Container class.
    """
    fixtures = get_fixtures(['containers', 'tastes'])

    post_fields = [
        {
            'field_name': 'content.image',
            'target_type': None,
            'field_type': 'URLField'
        },
        {
            'field_name': 'content.link',
            'target_type': None,
            'field_type': 'URLField'
        },
        {
            'field_name': 'content.text',
            'target_type': 'Keyword',
            'field_type': 'TextField'
        },
        {
            'field_name': 'content.title',
            'target_type': 'Keyword',
            'field_type': 'TextField'
        },
        {
            'field_name': 'content.video',
            'target_type': None,
            'field_type': 'URLField'
        },
        {
            'field_name': 'created_date',
            'target_type': 'DateTime',
            'field_type': 'DateTimeField'
        },
        {
            'field_name': 'location',
            'target_type': 'Location',
            'field_type': 'PointField'
        },
        {
            'field_name': 'user.email',
            'target_type': 'Account',
            'field_type': 'EmailField'
        },
        {
            'field_name': 'user.id',
            'target_type': None,
            'field_type': 'CharField'
        },
        {
            'field_name': 'user.link',
            'target_type': None,
            'field_type': 'URLField'
        },
        {
            'field_name': 'user.name',
            'target_type': 'Account',
            'field_type': 'CharField'
        },
        {
            'field_name': 'user.profile_pic',
            'target_type': None,
            'field_type': 'URLField'
        },
        {
            'field_name': 'user.screen_name',
            'target_type': 'Account',
            'field_type': 'CharField'
        }
    ]

    label_fields = [
        {
            'field_name': _DISTILLERY_SETTINGS['LABEL_KEY'] + '.priority',
            'target_type': 'Keyword',
            'field_type': 'CharField'
        },
        {
            'field_name': _DISTILLERY_SETTINGS['LABEL_KEY'] \
                         + '.source_ip_location',
            'field_type': 'PointField',
            'target_type': 'Location',
        }
    ]

    data = {
        _DISTILLERY_SETTINGS['RAW_DATA_KEY']: {
            _DISTILLERY_SETTINGS['DOC_ID_KEY']: '551d54e6f861c95f3123e5f6',
            _DISTILLERY_SETTINGS['BACKEND_KEY']: 'mongodb',
            _DISTILLERY_SETTINGS['WAREHOUSE_KEY']: 'test_database',
            _DISTILLERY_SETTINGS['COLLECTION_KEY']: 'twitter'
        },
        'subject': '[CRIT-111]'
    }

    def setUp(self):
        self.plain_container = Container.objects.get(pk=1)
        self.labeled_container = Container.objects.get(pk=2)

    def test_schema_with_label(self):
        """
        Tests the field_dicts property for a Container than has a Label.
        """
        actual = self.labeled_container.field_dicts
        expected = self.label_fields
        expected.extend(self.post_fields)
        self.assertEqual(actual, expected)

    def test_schema_no_label(self):
        """
        Tests the field_dicts property for a Container than has no Label.
        """
        actual = self.plain_container.field_dicts
        expected = self.post_fields
        self.assertEqual(actual, expected)

    def test_add_label_when_defined(self):
        """
        Tests the add_label method for a Container than has a Label.
        """
        mock_doc = Mock()
        self.labeled_container.label.add = Mock(return_value=mock_doc)
        actual = self.labeled_container.add_label(self.data)
        self.labeled_container.label.add.assert_called_once_with(self.data)
        self.assertEqual(actual, mock_doc)

    def test_add_label_when_undefined(self):
        """
        Tests the add_label method for a Container than has no Label.
        """
        actual = self.plain_container.add_label(self.data)
        expected = self.data
        self.assertEqual(actual, expected)

    def test_get_sample_with_taste(self):
        """
        Tests the get_sample method for a Container than has a Taste.
        """
        mock_sample = Mock()
        self.labeled_container.taste.get_sample = Mock(return_value=mock_sample)
        actual = self.labeled_container.get_sample(self.data)
        self.labeled_container.taste.get_sample.assert_called_once_with(
            self.data)
        self.assertEqual(actual, mock_sample)

    def test_get_sample_no_taste(self):
        """
        Tests the get_sample method for a Container than has no Taste.
        """
        with LogCapture() as log_capture:
            actual = self.plain_container.get_sample(self.data)
            expected = {}
            msg = 'Container "post" has no Taste to sample data'
            log_capture.check(
                ('bottler.containers.models', 'WARNING', msg),
            )
            self.assertEqual(actual, expected)

    def test_get_blind_sample_w_taste(self):
        """
        Tests the get_blind_sample method for a Container than has a
        Taste.
        """
        mock_sample = Mock()
        mock_codebook = Mock()
        self.labeled_container.taste.get_blind_sample = Mock(
            return_value=mock_sample)
        actual = self.labeled_container.get_blind_sample(self.data,
                                                         mock_codebook)
        self.labeled_container.taste.get_blind_sample.assert_called_once_with(
            self.data, mock_codebook)
        self.assertEqual(actual, mock_sample)

    def test_get_blind_sample_no_taste(self):
        """
        Tests the get_blind_sample method for a Container than has no
        Taste.
        """
        mock_codebook = Mock()
        with LogCapture() as log_capture:
            actual = self.plain_container.get_blind_sample(self.data,
                                                           mock_codebook)
            expected = {}
            msg = 'Container "post" has no Taste to sample data'
            log_capture.check(
                ('bottler.containers.models', 'WARNING', msg),
            )
            self.assertEqual(actual, expected)

    def test_get_taste_text_schema(self):
        """
        Tests the get_taste_text_fields method for a Container.
        """
        fields = self.labeled_container.get_taste_text_fields()
        self.assertEqual(fields[0].field_name, 'user.name')
        self.assertEqual(fields[0].field_type, 'CharField')
        self.assertEqual(fields[0].target_type, 'Account')

    def test_get_structure_w_label(self):
        """
        Tests the get_structure method for Container with a Label.
        """
        actual = self.labeled_container.get_structure()
        expected = OrderedDict([
            ('_metadata', OrderedDict([
                ('priority', 'CharField (Keyword)'),
                ('source_ip_location', 'PointField (Location)')
            ])),
            ('content', OrderedDict([
                ('image', 'URLField'),
                ('link', 'URLField'),
                ('text', 'TextField (Keyword)'),
                ('title', 'TextField (Keyword)'),
                ('video', 'URLField')])),
            ('created_date', 'DateTimeField (DateTime)'),
            ('location', 'PointField (Location)'),
            ('user', OrderedDict([
                ('email', 'EmailField (Account)'),
                ('id', 'CharField'),
                ('link', 'URLField'),
                ('name', 'CharField (Account)'),
                ('profile_pic', 'URLField'),
                ('screen_name', 'CharField (Account)')
            ]))
        ])
        self.assertEqual(actual, expected)

    def test_get_structure_wo_label(self):
        """
        Tests the get_structure method for Container witha Label.
        """
        actual = self.plain_container.get_structure()
        expected = OrderedDict([
            ('content', OrderedDict([
                ('image', 'URLField'),
                ('link', 'URLField'),
                ('text', 'TextField (Keyword)'),
                ('title', 'TextField (Keyword)'),
                ('video', 'URLField')])),
            ('created_date', 'DateTimeField (DateTime)'),
            ('location', 'PointField (Location)'),
            ('user', OrderedDict([
                ('email', 'EmailField (Account)'),
                ('id', 'CharField'),
                ('link', 'URLField'),
                ('name', 'CharField (Account)'),
                ('profile_pic', 'URLField'),
                ('screen_name', 'CharField (Account)')
            ]))
        ])
        self.assertEqual(actual, expected)

    def test_preview(self):
        """
        Tests the preview method.
        """
        actual = self.labeled_container.preview()
        expected = \
"""{
    "_metadata": {
        "priority": "CharField (Keyword)",
        "source_ip_location": "PointField (Location)"
    },
    "content": {
        "image": "URLField",
        "link": "URLField",
        "text": "TextField (Keyword)",
        "title": "TextField (Keyword)",
        "video": "URLField"
    },
    "created_date": "DateTimeField (DateTime)",
    "location": "PointField (Location)",
    "user": {
        "email": "EmailField (Account)",
        "id": "CharField",
        "link": "URLField",
        "name": "CharField (Account)",
        "profile_pic": "URLField",
        "screen_name": "CharField (Account)"
    }
}"""
        self.assertEqual(actual, expected)
