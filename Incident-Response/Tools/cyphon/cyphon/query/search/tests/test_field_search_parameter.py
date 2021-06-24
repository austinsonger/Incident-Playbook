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

# standard library
from django.test import TestCase

# local
from query.search.field_search_parameter import (
    FieldOperator,
    FieldSearchParameter,
    FieldTypes,
    FieldValue,
    FieldValueParsers,
    FieldValueParsingError,
)
from tests.fixture_manager import get_fixtures
from cyphon.fieldsets import QueryFieldset
from distilleries.models import Distillery
from bottler.bottles.models import BottleField


class FieldValueParsersTestCase(TestCase):
    """
    Test case for the FieldValueParsers class.
    """
    def test_boolean_parser_raises_error(self):
        """
        Tests that the boolean parser raises a FieldValueParsingError
        with an INVALID_BOOLEAN_CHOICE message if the given value is
        not 'true' or 'false'
        """
        with self.assertRaises(FieldValueParsingError) as error:
            FieldValueParsers.boolean_parser('blah')

        self.assertEqual(
            str(error.exception),
            FieldValueParsers.INVALID_BOOLEAN_CHOICE,
        )

    def test_boolean_parser_returns_true(self):
        """
        Tests that the boolean parser returns true for string values that
        say 'true'
        """
        self.assertTrue(FieldValueParsers.boolean_parser('true'))
        self.assertTrue(FieldValueParsers.boolean_parser('TRUE'))

    def test_boolean_parser_returns_false(self):
        """
        Tests that the boolean parser returns false for string values
        that say 'false'.
        """
        self.assertFalse(FieldValueParsers.boolean_parser('false'))
        self.assertFalse(FieldValueParsers.boolean_parser('FALSE'))

    def test_text_parser_returns(self):
        """
        Tests that the text parser simply returns the given value.
        """
        self.assertEqual(FieldValueParsers.text_parser('meh'), 'meh')

    def test_int_parser_raises_error(self):
        """
        Tests that the integer parser raises a FieldValueParsingError
        with the correct message if the given string is not an integer.
        """
        with self.assertRaises(FieldValueParsingError) as error:
            FieldValueParsers.int_parser('meh')

        self.assertEqual(
            str(error.exception),
            FieldValueParsers.INVALID_INTEGER_VALUE.format('meh'),
        )

    def test_int_parser_returns_int(self):
        """
        Tests that the integer parser parses an integer from a string.
        """
        self.assertEqual(FieldValueParsers.int_parser('4'), 4)

    def test_float_parser_raises_error(self):
        """
        Tests that the float parser raises a FieldValueParsingError
        with a INVALID_FLOAT_VALUE message if the given string is not
        a float.
        """
        with self.assertRaises(FieldValueParsingError) as error:
            FieldValueParsers.float_parser('meh')

        self.assertEqual(
            str(error.exception),
            FieldValueParsers.INVALID_FLOAT_VALUE.format('meh'),
        )

    def test_float_parser_returns_float(self):
        """
        Tests that the float parser parses a float.
        """
        self.assertEqual(FieldValueParsers.float_parser('4.5'), 4.5)


class FieldValueTestCase(TestCase):
    """
    TestCase for the FieldValue class.
    """
    def test_raises_invalid_field(self):
        """
        Tests that an INVALID_FIELD_TYPE error message is added to
        the error messages if the field_type is not in the known list of
        field types.
        """
        field_value = FieldValue('test', 'test')

        self.assertEqual(len(field_value.errors), 1)
        self.assertEqual(
            field_value.errors[0],
            FieldValue.INVALID_FIELD_TYPE.format('test'),
        )

    def test_missing_parser(self):
        """
        Tests that a MISSING_PARSER error message is added to the error
        messages if there is no assigned FieldValueParser parser to the
        known field_type.
        """
        field_value = FieldValue('test', FieldTypes.LIST)

        self.assertEqual(len(field_value.errors), 1)
        self.assertEqual(
            field_value.errors[0],
            FieldValue.MISSING_PARSER.format(FieldTypes.LIST),
        )

    def test_empty_value(self):
        """
        Tests that an EMPTY_VALUE error message is added to the error
        messages if the string value is empty.
        """
        field_value = FieldValue('', FieldTypes.BOOLEAN)

        self.assertEqual(len(field_value.errors), 1)
        self.assertEqual(
            field_value.errors[0],
            FieldValue.EMPTY_VALUE,
        )

    def test_parsing_error(self):
        """
        Tests that a FieldValueParserError message is added to the list
        of FieldValue messages if the exception is raised during parsing.
        """
        field_value = FieldValue('blah', FieldTypes.BOOLEAN)

        self.assertEqual(len(field_value.errors), 1)
        self.assertEqual(
            field_value.errors[0],
            FieldValueParsers.INVALID_BOOLEAN_CHOICE,
        )

    def test_parsed_value(self):
        """
        Tests that the parsed value from the string value is placed on
        the parsed_value property.
        """
        self.assertEqual(
            FieldValue('true', FieldTypes.BOOLEAN).parsed_value,
            True,
        )
        self.assertEqual(
            FieldValue('4.5', FieldTypes.FLOAT).parsed_value,
            4.5,
        )
        self.assertEqual(
            FieldValue('10.43.23.43', FieldTypes.IP_ADDR).parsed_value,
            '10.43.23.43',
        )


class FieldOperatorTestCase(TestCase):
    """
    TestCase for the FieldOperator class.
    """
    def test_mising_field_mapping(self):
        """
        Tests that a NO_FIELD_MAPPING error is added to the list of
        operator errors if the field_type is unknown.
        """
        operator = FieldOperator('=', 'test')

        self.assertEqual(len(operator.errors), 1)
        self.assertEqual(
            operator.errors[0],
            FieldOperator.NO_FIELD_MAPPING.format('test')
        )

    def test_mismatched_operator(self):
        """
        Tests that a MISMATCHED_OPERATOR error is added to the list
        of errors if the given operator is not assigned to the given
        field_type.
        """
        operator = FieldOperator('>', FieldTypes.CHAR)

        self.assertEqual(len(operator.errors), 1)
        self.assertEqual(
            operator.errors[0],
            FieldOperator.MISMATCHED_OPERATOR.format('>', FieldTypes.CHAR)
        )

    def test_fieldset_operator(self):
        """
        Tests that the correct fieldset operator is mapped to the
        operator.
        """
        self.assertEqual(
            FieldOperator('>', FieldTypes.INT).fieldset_operator,
            'gt',
        )


class FieldSearchParameterTestCase(TestCase):
    """
    TestCase for the FieldSearchParameter class.
    """
    fixtures = get_fixtures(['distilleries'])

    def test_invalid_parameter_error(self):
        """
        Tests that an INVALID_PARAMETER error is added to the list of
        errors if the given parameter string is invalid.
        """
        field_parameter = FieldSearchParameter(1, '')

        self.assertEqual(len(field_parameter.combined_errors), 1)
        self.assertEqual(
            field_parameter.combined_errors[0],
            FieldSearchParameter.INVALID_PARAMETER,
        )

        field_parameter = FieldSearchParameter(1, 'test')

        self.assertEqual(len(field_parameter.combined_errors), 1)
        self.assertEqual(
            field_parameter.combined_errors[0],
            FieldSearchParameter.INVALID_PARAMETER,
        )

        field_parameter = FieldSearchParameter(1, '"phrase"')

        self.assertEqual(len(field_parameter.combined_errors), 1)
        self.assertEqual(
            field_parameter.combined_errors[0],
            FieldSearchParameter.INVALID_PARAMETER,
        )

    def test_valid_parameter(self):
        """
        Tests that .is_valid() returns True for valid parameters.
        """
        self.assertTrue(
            FieldSearchParameter(3, 'ip_address=10.45.32.34').is_valid()
        )
        self.assertTrue(
            FieldSearchParameter(3, 'likes<10').is_valid()
        )
        self.assertTrue(
            FieldSearchParameter(3, 'verified=False').is_valid()
        )
        self.assertTrue(
            FieldSearchParameter(4, 'priority="something fancy"').is_valid()
        )

    def test_invalid_parameter(self):
        """
        Tests that .is_valid() returns False for invalid parameters.
        """
        self.assertFalse(
            FieldSearchParameter(3, 'ip_address<4').is_valid()
        )
        self.assertFalse(
            FieldSearchParameter(3, 'verified=meh').is_valid()
        )

    def test_get_parameter_info(self):
        """
        Tests that .get_parameter_info() returns the correct dictionary.
        """
        field_parameter = FieldSearchParameter(2, 'meh=true')

        self.assertFalse(field_parameter.is_valid())

        error_dict = field_parameter.as_dict()

        self.assertDictEqual(error_dict, {
            'parameter': 'meh=true',
            'index': 2,
            'type': 'field',
            'field_name': 'meh',
            'operator': None,
            'value': None,
            'errors': ['Field `meh` does not exist.'],
        })

        field_parameter = FieldSearchParameter(2, 'ip_address<"30.43.23"')

        self.assertFalse(field_parameter.is_valid())

        error_dict = field_parameter.as_dict()

        self.assertDictEqual(error_dict, {
            'parameter': 'ip_address<"30.43.23"',
            'index': 2,
            'type': 'field',
            'field_name': 'ip_address',
            'operator': '<',
            'value': '"30.43.23"',
            'errors': [
                'The operator `<` is not used for fields of type '
                '`GenericIPAddressField`'
            ],
        })

    def test_create_fieldset_raises_error(self):
        """
        Tests that .create_fieldset() returns an AssertionError with
        a CANNOT_CREATE_FIELDSET message if the parameter is not valid.
        """
        with self.assertRaises(ValueError) as error:
            FieldSearchParameter(3, 'ip_address<4').create_fieldset()

        self.assertEqual(
            str(error.exception),
            FieldSearchParameter.CANNOT_CREATE_FIELDSET,
        )

    def test_create_fieldset(self):
        """
        Tests that .create_fieldset() returns a QueryFieldset with the
        correct properties.
        """
        fieldset = FieldSearchParameter(3, 'ip_address="4"').create_fieldset()

        self.assertIsInstance(fieldset, QueryFieldset)
        self.assertEqual(fieldset.field_name, 'ip_address')
        self.assertEqual(fieldset.operator, 'regex')
        self.assertEqual(fieldset.field_type, 'GenericIPAddressField')
        self.assertEqual(fieldset.value, '4')

        fieldset = FieldSearchParameter(3, 'likes=4').create_fieldset()

        self.assertIsInstance(fieldset, QueryFieldset)
        self.assertEqual(fieldset.field_name, 'likes')
        self.assertEqual(fieldset.operator, 'eq')
        self.assertEqual(fieldset.field_type, 'IntegerField')
        self.assertEqual(fieldset.value, 4)

    def test_is_related_to_distillery(self):
        parameter = FieldSearchParameter(0, 'ip_address=10.2.32.2')
        distilleries = Distillery.objects.filter(
            container__bottle__name='test_doc',
        )

        self.assertTrue(parameter.is_valid())
        self.assertEqual(distilleries.count(), 1)

        for distillery in distilleries:
            self.assertTrue(parameter.is_related_to_distillery(distillery))

    def test_ip_address_value(self):
        parameter = FieldSearchParameter(0, 'ip_address=123.123.123.123')

        self.assertTrue(parameter.is_valid())
        self.assertEqual(
            parameter.data_field.field_type, 'GenericIPAddressField')

    def test_nested_field(self):
        """
        Tests that a nested field returns a data field.
        """
        parameter = FieldSearchParameter(0, 'content.text=test')

        self.assertTrue(parameter.is_valid())
        self.assertEqual(parameter.data_field.field_type, 'TextField')

        parameter = FieldSearchParameter(0, 'not.exist=test')

        self.assertFalse(parameter.is_valid())
        self.assertEqual(
            parameter.errors,
            [FieldSearchParameter.FIELD_DOES_NOT_EXIST.format('not.exist')])

        parameter = FieldSearchParameter(0, 'content.exist=test')

        self.assertFalse(parameter.is_valid())
        self.assertEqual(
            parameter.errors,
            [FieldSearchParameter.FIELD_DOES_NOT_EXIST.format('content.exist')])
