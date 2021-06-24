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
Tests the validator for a MongoDb field name. Note that this validator does not
check for periods in the name, since these will be used to nest the field
within the MongoDb document prior to saving.
"""

# standard library
from datetime import timedelta
from unittest import TestCase
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.core.exceptions import ValidationError
from django.utils import timezone
import six

# local
from utils.validators.validators import (
    db_name_validator,
    field_name_validator,
    key_file_validator,
    lowercase_validator,
    validate_str_substitution,
    validate_timeframe,
)


class ValidateStrSubstitutionTestCase(TestCase):
    """
    Tests the validate_str_substitution function.
    """

    def test_no_template(self):
        """
        Test case for the validate_str_substitution function when no
        formatter is provided for multiple values.
        """
        template = ''
        value_count = 2
        msg = 'No template has been provided for formatting multiple fields.'
        with six.assertRaisesRegex(self, ValidationError, msg):
            validate_str_substitution(template, value_count)

    def test_single_specifier_needed(self):
        """
        Test case for the validate_str_substitution function when there
        are too many specifiers for a single value.
        """
        template = '{0} one too many {1}'
        value_count = 1
        msg = ('The formatter should only contain one '
               '"{}" specifier for the source field.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            validate_str_substitution(template, value_count)

    def test_too_many_specifiers(self):
        """
        Test case for the validate_str_substitution function when there
        are too many specifiers for a multiple values.
        """
        template = '{0} too {1} many {2}'
        value_count = 2
        msg = ('The number of "{}" specifiers in the formatter '
               'exceeds the number of source fields.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            validate_str_substitution(template, value_count)

    def test_single_specifier_missing(self):
        """
        Test case for the validate_str_substitution function when no
        specifier is provided for a single value.
        """
        template = 'missing'
        value_count = 1
        msg = 'The formatter should contain one "{}" specifier.'
        with six.assertRaisesRegex(self, ValidationError, msg):
            validate_str_substitution(template, value_count)

    def test_mult_specifiers_missing(self):
        """
        Test case for the validate_str_substitution function when not
        enough specifiers are provided for multiple values.
        """
        template = '{0} too few {1}'
        value_count = 3
        msg = ('The formatter contains too few "{}" '
               'specifiers for the number of source fields.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            validate_str_substitution(template, value_count)

    def test_valid(self):
        """
        Test case for the validate_str_substitution function for a valid
        number of specifiers.
        """
        template = '{0} just right {1}'
        value_count = 2
        try:
            validate_str_substitution(template, value_count)
        except ValidationError:
            self.fail('Name raised ValidationError unexpectedly')

    def test_no_template_or_value(self):
        """
        Test case for the validate_str_substitution function when there
        is no template and no values.
        """
        template = None
        value_count = 0
        try:
            validate_str_substitution(template, value_count)
        except ValidationError:
            self.fail('Name raised ValidationError unexpectedly')



class ValidateTimeframeTestCase(TestCase):
    """
    Tests the validate_timeframe function.
    """
    msg = 'Start date and time must precede end date and time.'

    def test_start_before_end(self):
        """
        Test case for a timeframe when the start is before the end.
        """
        start = timezone.now()
        end = start + timedelta(seconds=1)
        actual = validate_timeframe(start, end)
        expected = None
        self.assertEqual(actual, expected)

    def test_start_and_end_equal(self):
        """
        Test case for a timeframe when the start is the same as the end.
        """
        start = timezone.now()
        end = start
        with six.assertRaisesRegex(self, ValidationError, self.msg):
            validate_timeframe(start, end)

    def test_end_before_start(self):
        """
        Test case for a timeframe when the end is before the start.
        """
        start = timezone.now()
        end = start - timedelta(seconds=1)
        with six.assertRaisesRegex(self, ValidationError, self.msg):
            validate_timeframe(start, end)


class DbNameValidatorTestCase(TestCase):
    """
    Tests the db_name_validator function.
    """

    def test_starts_with_dollar_sign(self):
        """
        Test case for a name that starts with '$'.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('$id')

    def test_ends_with_dollar_sign(self):
        """
        Test case for a name that ends with '$'.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('id$')

    def test_underscore(self):
        """
        Test case for a name that contains an underscore.
        """
        try:
            db_name_validator('logstash_')
        except ValidationError:
            self.fail('Name raised ValidationError unexpectedly')

    def test_hyphen(self):
        """
        Test case for a name with an asterisk.
        """
        try:
            db_name_validator('logstash-')
        except ValidationError:
            self.fail('Name raised ValidationError unexpectedly')

    def test_asterisk(self):
        """
        Test case for a name with an asterisk.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('logstash*')

    def test_at_sign(self):
        """
        Test case for a field name with an 'at' sign.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('@timestamp')

    def test_white_space(self):
        """
        Test case for a name with a space.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('http log')

    def test_period(self):
        """
        Test case for a name with a period.
        """
        with self.assertRaises(ValidationError):
            db_name_validator('http.log')


class FieldNameValidatorTestCase(TestCase):
    """
    Tests the field_name_validator function.
    """

    def test_reserved_name(self):
        """
        Test case for a reserved field name.
        """
        with self.assertRaises(ValidationError):
            field_name_validator('_id')

    def test_nonreserved_name(self):
        """
        Test case for a nonreserved field name.
        """
        try:
            field_name_validator('_identifier')
        except ValidationError:
            self.fail('Field name raised ValidationError unexpectedly')

    def test_starts_with_dollar_sign(self):
        """
        Test case for a field name that starts with '$'.
        """
        with self.assertRaises(ValidationError):
            field_name_validator('$id')

    def test_ends_with_dollar_sign(self):
        """
        Test case for a field name that ends with '$'.
        """
        try:
            field_name_validator('id$')
        except ValidationError:
            self.fail('Field name raised ValidationError unexpectedly')

    def test_hyphen(self):
        """
        Test case for a field name with an asterisk.
        """
        with self.assertRaises(ValidationError):
            field_name_validator('logstash-')

    def test_asterisk(self):
        """
        Test case for a field name with an asterisk.
        """
        with self.assertRaises(ValidationError):
            field_name_validator('logstash*')

    def test_at_sign(self):
        """
        Test case for a field name with an 'at' sign.
        """
        try:
            field_name_validator('@timestamp')
        except ValidationError:
            self.fail('Name raised ValidationError unexpectedly')

    def test_white_space(self):
        """
        Test case for a field name with a space.
        """
        with self.assertRaises(ValidationError):
            field_name_validator('user id')

    def test_no_errors(self):
        """
        Test case for a valid field name.
        """
        try:
            field_name_validator('good_field_name')
        except ValidationError:
            self.fail('Field name raised ValidationError unexpectedly')


class KeyFieldValidatorTestCase(TestCase):
    """
    Tests the key_file_validator function.
    """

    def test_pem(self):
        """
        Test case for a .pem file.
        """
        mock_fieldfile = Mock()
        mock_fieldfile.name = 'good_file_name.pem'
        try:
            key_file_validator(mock_fieldfile)
        except ValidationError:
            self.fail('Key file raised ValidationError unexpectedly')

    def test_pub(self):
        """
        Test case for a .pub file.
        """
        mock_fieldfile = Mock()
        mock_fieldfile.name = 'good_file_name.pem'
        try:
            key_file_validator(mock_fieldfile)
        except ValidationError:
            self.fail('Field name raised ValidationError unexpectedly')

    def test_invalid(self):
        """
        Test case for an invalid file type.
        """
        mock_fieldfile = Mock()
        mock_fieldfile.name = 'bad_file_name.pem.jar'
        with self.assertRaises(ValidationError):
            key_file_validator(mock_fieldfile)


class LowercaseValidatorTestCase(TestCase):
    """
    Tests the lowercase_validator function.
    """

    def test_valid_str(self):
        """
        Test case for an all lowercase string.
        """
        try:
            lowercase_validator('hg213i75%^&$efg')
        except ValidationError:
            self.fail('String raised ValidationError unexpectedly')

    def test_invalid_str(self):
        """
        Test case for a string containing an uppercase character.
        """
        with self.assertRaises(ValidationError):
            lowercase_validator('hg213i75%^&$Efg')
