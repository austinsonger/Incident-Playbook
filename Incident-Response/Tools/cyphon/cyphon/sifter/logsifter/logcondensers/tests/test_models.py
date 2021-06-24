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
Tests the LogChute class.
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
from sifter.logsifter.logcondensers.models import LogCondenser, LogFitting
from tests.fixture_manager import get_fixtures


class LogCondenserBaseTestCase(TestCase):
    """
    Base class for testing the LogCondenser class and related classes.
    """
    fixtures = get_fixtures(['logcondensers'])

    test_doc = 'Mar 29 13:02:58 0.0.0.0 [3:19187:7] THIS IS A TEST'

    @classmethod
    def setUpClass(cls):
        super(LogCondenserBaseTestCase, cls).setUpClass()
        cls.condenser = LogCondenser.objects.get(name='nested_log')


class LogCondenserTestCase(LogCondenserBaseTestCase, CondenserTestCaseMixin):
    """
    Tests the LogCondenser class.
    """

    def test_str(self):
        """
        Tests the __str__ method of the LogCondenser class.
        """
        self.assertEqual(str(self.condenser), 'nested_log')

    def test_process(self):
        """
        Tests the process method of the LogCondenser class.
        """
        with patch('sifter.logsifter.logcondensers.models.LogParser.process',
                   return_value='some text'):
            actual = self.condenser.process(self.test_doc)
            expected = {
                'message': 'some text',
                'content': {
                    'host': 'some text',
                    'date_str': 'some text'
                }
            }
            for item in actual:
                self.assertEqual(actual[item], expected[item])


class LogFittingTestCase(LogCondenserBaseTestCase, FittingTestCaseMixin):
    """
    Tests the LogFitting class.
    """

    @classmethod
    def setUpClass(cls):
        super(LogFittingTestCase, cls).setUpClass()
        cls.parser_fitting = LogFitting.objects.get(pk=1)
        cls.condenser_fitting = LogFitting.objects.get(pk=4)
        cls.parser_type = ContentType.objects.get(app_label='logcondensers',
                                                  model='logparser')
        cls.condenser_type = ContentType.objects.get(app_label='logcondensers',
                                                     model='logcondenser')

    def test_invalid_target_field(self):
        """
        Tests that a validation error is raised if the target_field is not
        present in the Bottle associated with the Fitting's Condenser.
        """
        field = BottleField.objects.get_by_natural_key('subject')
        fitting = LogFitting(
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
        fitting = LogFitting(
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
        fitting = LogFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=3,
            content_type=self.parser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'If the '
                                   'target field is an EmbeddedDocument, '
                                   'the content type must be a condenser.'):
            fitting.clean()

    def test_process(self):
        """
        Tests the process method.
        """
        actual = self.parser_fitting.process(self.test_doc)
        expected = 'Mar 29 13:02:58'
        self.assertEqual(actual, expected)

