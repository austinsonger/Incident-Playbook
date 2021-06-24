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
Tests the Bottle class.
"""

# standard library
from collections import OrderedDict

# third party
from django.core.exceptions import ValidationError
from django.test import TestCase
from testfixtures import LogCapture
import six

# local
from bottler.bottles.models import Bottle, BottleField
from tests.fixture_manager import get_fixtures


class BottleBaseTestCase(TestCase):
    """
    Base class for Bottle and BottleField test cases.
    """
    fixtures = get_fixtures(['bottles'])


class BottleFieldManagerTestCase(BottleBaseTestCase):
    """
    Tests the BottleFieldManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for an existing BottleField.
        """
        field = BottleField(
            field_name='test_field',
            field_type='CharField'
        )
        field.save()
        saved_field = BottleField.objects.get_by_natural_key('test_field')
        self.assertEqual(saved_field, field)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method for a BottleField that
        doesn't exist.
        """
        with LogCapture() as log_capture:
            BottleField.objects.get_by_natural_key('dummy_field')
            expected = 'BottleField "dummy_field" does not exist'
            log_capture.check(
                ('bottler.datafields.models', 'ERROR', expected),
            )


class BottleFieldTestCase(BottleBaseTestCase):
    """
    Tests the BottleField class.
    """

    def test_to_dict_no_parent(self):
        """
        Tests the to_dict method when no parent_name is provided.
        """
        field = BottleField.objects.get_by_natural_key('title')
        actual = field.to_dict()
        expected = {
            'field_name': 'title',
            'field_type': 'TextField',
            'target_type': 'Keyword'
        }
        self.assertEqual(actual, expected)

    def test_to_dict_with_parent(self):
        """
        Tests the to_dict method when no parent_name is provided.
        """
        field = BottleField.objects.get_by_natural_key('title')
        actual = field.to_dict('post')
        expected = {
            'field_name': 'post.title',
            'field_type': 'TextField',
            'target_type': 'Keyword'
        }
        self.assertEqual(actual, expected)

    def test_missing_embedded_doc(self):
        """
        Tests the clean method field_type is EmbeddedDocument but embedded_doc
        is undefined.
        """
        bottlefield = BottleField(
            field_name='test_field',
            field_type='EmbeddedDocument'
        )
        with six.assertRaisesRegex(self, ValidationError, 'An embedded doc must ' \
            + 'be defined for an EmbeddedDocument field.'):
            bottlefield.clean()

    def test_with_embedded_doc(self):
        """
        Tests the clean method field_type is EmbeddedDocument and an
        embedded_doc is defined.
        """
        bottlefield = BottleField(
            field_name='test_field',
            field_type='EmbeddedDocument',
            embedded_doc=Bottle.objects.get_by_natural_key('post')
        )
        try:
            bottlefield.clean()
        except ValidationError:
            self.fail('BottleField raised ValidationError unexpectedly')

    def test_misdefined_field_type(self):
        """
        Tests the clean method when an embedded_coc is defined by field_type
        is not EmbeddedDocument.
        """
        bottlefield = BottleField(
            field_name='test_field',
            field_type='CharField',
            embedded_doc=Bottle.objects.get_by_natural_key('post')
        )
        with six.assertRaisesRegex(self, ValidationError, 'If an embedded doc ' \
            + 'is defined, the field type must be EmbeddedDocument.'):
            bottlefield.clean()

    def test_correct_field_type(self):
        """
        Tests the clean method field_type is not an EmbeddedDocument and an
        embedded_doc is undefined.
        """
        bottlefield = BottleField(
            field_name='test_field',
            field_type='CharField',
        )
        try:
            bottlefield.clean()
        except ValidationError:
            self.fail('BottleField raised ValidationError unexpectedly')


class BottleTestCase(BottleBaseTestCase):
    """
    Tests the Bottle class.
    """

    @classmethod
    def setUpClass(cls):
        super(BottleTestCase, cls).setUpClass()
        cls.post_bottle = Bottle.objects.get_by_natural_key('post')
        cls.user_bottle = Bottle.objects.get_by_natural_key('user')

    def test_field_is_in_bottle_true(self):
        """
        Tests the field_exists method for a BottleField that is in the
        Bottle.
        """
        field = BottleField.objects.get_by_natural_key('user')
        actual = self.post_bottle.field_exists(field)
        self.assertEqual(actual, True)

    def test_field_is_in_bottle_false(self):
        """
        Tests the field_exists method for a BottleField that is not in
        the Bottle.
        """
        field = BottleField.objects.get_by_natural_key('subject')
        actual = self.post_bottle.field_exists(field)
        self.assertEqual(actual, False)

    def test_get_flat_fields(self):
        """
        Tests the get_fields method for nonnested fields.
        """
        fields = self.user_bottle.get_fields()
        self.assertEqual(len(fields), 6)
        self.assertTrue(fields[5].field_name, 'screen_name')
        self.assertTrue(fields[5].field_type, 'CharField')
        self.assertTrue(fields[5].target_type, 'Account')

    def test_get_nested_fields(self):
        """
        Tests the get_fields method for nonested and nested fields.
        """
        fields = self.post_bottle.get_fields()
        self.assertEqual(len(fields), 13)
        self.assertTrue(fields[12].field_name, 'user.screen_name')
        self.assertTrue(fields[12].field_type, 'CharField')
        self.assertTrue(fields[12].target_type, 'Account')

    def test_get_flat_field_choices(self):
        """
        Tests the get_field_choices method for nonnested fields.
        """
        actual = self.user_bottle.get_field_choices()
        expected = [
            ('email:EmailField', 'email'),
            ('id:CharField', 'id'),
            ('link:URLField', 'link'),
            ('name:CharField', 'name'),
            ('profile_pic:URLField', 'profile_pic'),
            ('screen_name:CharField', 'screen_name')
        ]
        self.assertEqual(actual, expected)

    def test_get_nested_field_choices(self):
        """
        Tests the get_field_choices method for nonested and nested fields.
        """
        fields = self.post_bottle.get_field_choices()
        self.assertEqual(len(fields), 13)
        self.assertEqual(fields[12][0], 'user.screen_name:CharField')
        self.assertEqual(fields[12][1], 'user.screen_name')

    def test_get_flat_structure(self):
        """
        Tests the get_structure method for nonnested fields.
        """
        actual = self.user_bottle.get_structure()
        expected = OrderedDict([
            ('email', 'EmailField (Account)'),
            ('id', 'CharField'),
            ('link', 'URLField'),
            ('name', 'CharField (Account)'),
            ('profile_pic', 'URLField'),
            ('screen_name', 'CharField (Account)')
        ])
        self.assertEqual(actual, expected)

    def test_get_nested_structure(self):
        """
        Tests the get_structure method for nonested and nested fields.
        """
        actual = self.post_bottle.get_structure()
        expected = OrderedDict([
            ('content', OrderedDict([
                ('image', 'URLField'),
                ('link', 'URLField'),
                ('text', 'TextField (Keyword)'),
                ('title', 'TextField (Keyword)'),
                ('video', 'URLField')
            ])),
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
        actual = self.post_bottle.preview()
        expected = \
"""{
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
