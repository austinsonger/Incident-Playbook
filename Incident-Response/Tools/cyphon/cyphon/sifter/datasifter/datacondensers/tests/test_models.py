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
Tests the Funnel class and related classes.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
import six

# local
from bottler.bottles.models import BottleField
from sifter.condensers.tests.mixins import CondenserTestCaseMixin, \
    FittingTestCaseMixin
from sifter.datasifter.datacondensers.models import DataCondenser, DataFitting
from tests.fixture_manager import get_fixtures


class DataCondenserBaseTestCase(TestCase):
    """
    Base class for testing the DataCondenser class and related classes.
    """
    fixtures = get_fixtures(['datacondensers'])

    @classmethod
    def setUpClass(cls):
        super(DataCondenserBaseTestCase, cls).setUpClass()
        cls.condenser = DataCondenser.objects.get(name='twitter__post')


class DataCondenserTestCase(DataCondenserBaseTestCase, CondenserTestCaseMixin):
    """
    Tests the DataCondenser class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the DataCondenser class.
        """
        self.assertEqual(str(self.condenser), 'twitter__post')

    def test_process(self):
        """
        Tests the process method of the DataCondenser class.
        """
        with patch('sifter.datasifter.datacondensers.models.DataParser.process',
                   return_value='some text'):
            actual = self.condenser.process({'text': 'example text'})
            expected = {
                'content': {
                    'link': 'some text',
                    'text': 'some text',
                    'image': 'some text'
                },
                'user': {
                    'link': 'some text',
                    'screen_name': 'some text',
                    'id': 'some text',
                    'name': 'some text',
                    'profile_pic': 'some text'
                },
                'location': 'some text',
                'created_date': 'some text'
            }
            for item in actual:
                self.assertEqual(actual[item], expected[item])


class DataFittingTestCase(DataCondenserBaseTestCase, FittingTestCaseMixin):
    """
    Tests the DataFitting class.
    """

    @classmethod
    def setUpClass(cls):
        super(DataFittingTestCase, cls).setUpClass()
        cls.parser_fitting = DataFitting.objects.get(pk=4)
        cls.condenser_fitting = DataFitting.objects.get(pk=11)
        cls.parser_type = ContentType.objects.get(app_label='datacondensers',
                                                  model='dataparser')
        cls.condenser_type = ContentType.objects.get(app_label='datacondensers',
                                                     model='datacondenser')

    def test_invalid_target_field(self):
        """
        Tests that a validation error is raised if the target_field is not
        present in the Bottle associated with the Fitting's Condenser.
        """
        field = BottleField.objects.get_by_natural_key('subject')
        fitting = DataFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=2,
            content_type=self.parser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'The selected '
                                   'target field is not compatible with the '
                                   'condenser\'s bottle.'):
            fitting.clean()

    def test_target_is_not_embebbed_doc(self):
        """
        Tests that a validation error is raised if the target field is not an
        EmbeddedDocument and the content type is a Condenser.
        """
        field = BottleField.objects.get_by_natural_key('location')
        fitting = DataFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=2,
            content_type=self.condenser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'Unless the '
                                   'target field is an EmbeddedDocument, '
                                   'the content type must be a parser.'):
            fitting.clean()

    def test_fitting_is_not_condenser(self):
        """
        Tests that a validation error is raised if the target field is an
        EmbeddedDocument and the content type is not a Condenser.
        """
        field = BottleField.objects.get_by_natural_key('content')
        fitting = DataFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=3,
            content_type=self.parser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'If the '
                                   'target field is an EmbeddedDocument, '
                                   'the content type must be a condenser.'):
            fitting.clean()

    def test_target_field_name(self):
        """
        Tests the target_field_name property.
        """
        self.assertEqual(self.parser_fitting.target_field_name, 'link')

    def test_target_field_type(self):
        """
        Tests the target_field_type property.
        """
        self.assertEqual(self.parser_fitting.target_field_type, 'URLField')

    def test_process(self):
        """
        Tests the process method.
        """
        doc = {
            'id_str': '0123456',
            'text': 'this is an example post',
            'user': {
                'screen_name': 'zebrafinch'
            }
        }
        actual = self.parser_fitting.process(doc)
        expected = 'https://twitter.com/zebrafinch/statuses/0123456'
        self.assertEqual(actual, expected)
