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
Tests the parserutils module.
"""

# standard library
import logging
from unittest import TestCase

# third party
from bson import ObjectId

# local
from bottler.datafields.models import DataField
from utils.parserutils import parserutils


class HtmlToTextTestCase(TestCase):
    """
    Tests the html_to_text function.
    """

    def test_html_to_text(self):
        """
        Tests the html_to_text function.
        """
        html = '<html><head></head><body><p>Hi!<br>How are you?<br>Here ' + \
               'is the <a href="https://www.python.org">link</a> you ' + \
               'wanted.</p></html>'
        actual = parserutils.html_to_text(html)
        expected = """\
   Hi!
   How are you?
   Here is the
    link
   you wanted."""
        self.assertEqual(actual, expected)


class GetDictValueTestCase(TestCase):
    """
    Tests the get_dict_value function.
    """

    def setUp(self):
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_value_from_empty_dict(self):
        """
        Tests method for getting a value from a nested dictionary.
        """
        doc = {}
        field = 'a.b.c'
        self.assertEqual(parserutils.get_dict_value(field, doc), None)

    def test_value_from_simple_dict(self):
        """
        Tests method for getting a value from a nested dictionary.
        """
        doc = {'a': 100}
        field = 'a'
        self.assertEqual(parserutils.get_dict_value(field, doc), 100)

    def test_value_from_nested_dict(self):
        """
        Tests method for getting a value from a nested dictionary.
        """
        doc = {'a': {'b': {'c': 100}}, 'd': {'e': {'f': 200}}}
        field = 'a.b.c'
        self.assertEqual(parserutils.get_dict_value(field, doc), 100)

    def test_empty_value_from_dict(self):
        """
        Tests method for getting a value from a nested dictionary.
        """
        doc = {'a': {'b': {'c': 100}}}
        field = ''
        self.assertEqual(parserutils.get_dict_value(field, doc), None)

    def test_wrong_value_from_dict(self):
        """
        Tests method for getting a nonexistent value from a nested dictionary.
        """
        doc = {'a': {'b': {'c': 100}}}
        field = 'a.c'
        self.assertEqual(parserutils.get_dict_value(field, doc), None)

    def test_get_array_item(self):
        """
        Tests method for getting a value from an array in a nested dictionary.
        """
        doc = {'a': {'b': [{'c': [100, [15, 20]]}, {'d': 40}], 'e': 10}}
        field = 'a.b[0].c[1][1]'
        self.assertEqual(parserutils.get_dict_value(field, doc), 20)


class AbridgeDictTestCase(TestCase):
    """
    Tests the abridge_dict function.
    """
    schema = [
        DataField(field_name='test1.foo', field_type='TextField'),
        DataField(field_name='test1.bar', field_type='TextField'),
        DataField(field_name='test3', field_type='TextField'),
        DataField(field_name='test4', field_type='TextField'),
    ]

    def test_abridge_dict(self):
        """
        Tests method for getting a value from a nested dictionary.
        """
        doc = {
            'test1': {
                'foo': 1,
                'bar': 2,
                'bogus': 3
            },
            'test2': 4,  # not in schema
            'test3': 5,
            'test4': None  # null value
        }
        actual = parserutils.abridge_dict(self.schema, doc)
        expected = {'test1': {'foo': 1, 'bar': 2}, 'test3': 5}
        self.assertEqual(actual, expected)


class DivideIntoGroupsTestCase(TestCase):
    """
    Tests the divide_into_groups function.
    """

    def test_negative_group_size(self):
        """
        Tests divide_into_groups for negative group size.
        """
        with self.assertRaises(ValueError):
            parserutils.divide_into_groups(['a', 'b', 'c', 'd', 'e'], -1)

    def test_group_size_of_zero(self):
        """
        Tests divide_into_groups for group size of 0.
        """
        with self.assertRaises(ValueError):
            parserutils.divide_into_groups(['a', 'b', 'c', 'd', 'e'], 0)

    def test_empty_list(self):
        """
        Tests divide_into_groups for an empty list.
        """
        actual = parserutils.divide_into_groups([], 10)
        expected = []
        self.assertEqual(actual, expected)

    def test_exact_multiple(self):
        """
        Tests divide_into_groups when the number of items is an exact multiple
        of the group size.
        """
        actual = parserutils.divide_into_groups(['a', 'b', 'c', 'd'], 2)
        expected = [['a', 'b'], ['c', 'd']]
        self.assertEqual(actual, expected)

    def test_not_exact_multiple(self):
        """
        Tests divide_into_groups when the number of items is not an exact
        multiple of the group size.
        """
        actual = parserutils.divide_into_groups(['a', 'b', 'c', 'd', 'e'], 2)
        expected = [['a', 'b'], ['c', 'd'], ['e']]
        self.assertEqual(actual, expected)

    def test_group_size_exceeds_items(self):
        """
        Tests divide_into_groups when the group size exceeds the number of items.
        """
        actual = parserutils.divide_into_groups(['a', 'b', 'c', 'd', 'e'], 10)
        expected = [['a', 'b', 'c', 'd', 'e']]
        self.assertEqual(actual, expected)


class ExtractSubstringTestCase(TestCase):
    """
    Tests the extract_substring function.
    """

    def test_default(self):
        """
        Tests extract_substring for the default setting.
        """
        string = 'dup key : { "123" }'
        actual = parserutils.extract_substring(string, ':', '}')
        expected = ' { "123" '
        self.assertEqual(actual, expected)

    def test_right(self):
        """
        Tests extract_substring when direction='right'.
        """
        string = '$_id_1'
        actual = parserutils.extract_substring(string, '$', '_', True)
        expected = '_id'
        self.assertEqual(actual, expected)


class RestoreTypeTestCase(TestCase):
    """
    Tests the restore_type function.
    """

    def test_boolean(self):
        """
        Tests restore_type function for a Boolean.
        """
        actual = parserutils.restore_type('BooleanField', 'false')
        self.assertFalse(actual)
        self.assertTrue(isinstance(actual, bool))

    def test_float(self):
        """
        Tests restore_type function for a FloatField.
        """
        actual = parserutils.restore_type('FloatField', '1.2')
        self.assertTrue(isinstance(actual, float))
        self.assertEqual(actual, 1.2)

    def test_integer(self):
        """
        Tests restore_type function for an integer.
        """
        actual = parserutils.restore_type('IntegerField', '1')
        self.assertTrue(isinstance(actual, int))
        self.assertEqual(actual, 1)

    def test_char(self):
        """
        Tests restore_type function for a CharField.
        """
        actual = parserutils.restore_type('CharField', '0')
        self.assertEqual(actual, '0')


class StringToBoolTestCase(TestCase):
    """
    Tests the string_to_bool function.
    """

    def test_true_strings(self):
        """
        Tests string_to_bool function for strings that should return True.
        """
        self.assertTrue(parserutils.string_to_bool('true'))
        self.assertTrue(parserutils.string_to_bool('True'))

    def test_false_strings(self):
        """
        Tests string_to_bool function for strings that should return False.
        """
        self.assertFalse(parserutils.string_to_bool('false'))
        self.assertFalse(parserutils.string_to_bool('False'))

    def test_other_values(self):
        """
        Tests string_to_bool function for values that are not predefined strings.
        """
        # values that should return True
        self.assertTrue(parserutils.string_to_bool('0'))
        self.assertTrue(parserutils.string_to_bool(True))

        # values that should return False
        self.assertFalse(parserutils.string_to_bool(0))
        self.assertFalse(parserutils.string_to_bool(None))
        self.assertFalse(parserutils.string_to_bool(False))


class RestoreTypeTestCase(TestCase):
    """
    Tests the restore_type_from_str function.
    """

    def test_string_single_quotes(self):
        """
        Tests restore_type_from_str for a string enclosed in double quotes.
        """
        self.assertEqual(parserutils.restore_type_from_str("'123'"), '123')

    def test_string_double_quotes(self):
        """
        Tests restore_type_from_str for a string enclosed in double quotes.
        """
        self.assertEqual(parserutils.restore_type_from_str('"123"'), '123')

    def test_object_id(self):
        """
        Tests restore_type_from_str for an ObjectId.
        """
        actual = parserutils.restore_type_from_str("ObjectId('5543769ef861c942838c7ee9')")
        expected = ObjectId('5543769ef861c942838c7ee9')
        self.assertEqual(actual, expected)

    def test_null(self):
        """
        Tests restore_type_from_str for a null value.
        """
        actual = parserutils.restore_type_from_str('null')
        expected = None
        self.assertEqual(actual, expected)

    def test_integer(self):
        """
        Tests restore_type_from_str for a integer.
        """
        self.assertEqual(parserutils.restore_type_from_str('123'), 123)

    def test_non_integer(self):
        """
        Tests restore_type_from_str for a non integer.
        """
        self.assertEqual(parserutils.restore_type_from_str('_123'), '_123')


class GetDupKeyValTestCase(TestCase):
    """
    Tests the get_dup_key_val function.
    """

    def test_simple_index(self):
        """
        Tests the get_dup_key_val function for a simple index
        """
        errmsg = 'E11000 duplicate key error collection: ' + \
                 'test_database_1482164012.test_docs index: _id_ dup key: ' + \
                 '{ : 593849043618549760 }'
        actual = parserutils.get_dup_key_val(errmsg)
        expected = {'_id': 593849043618549760}
        self.assertEqual(actual, expected)

    def test_compound_index(self):
        """
        Tests the get_dup_key_val function for a compound index
        """
        errmsg = 'insertDocument :: caused by :: 11000 E11000 ' + \
                 'duplicate key error collection: cyphon.posts index: _platform_1__raw_data_1  ' + \
                 'dup key: { : "twitter", : ObjectId(\'5543769ef861c942838c7ee9\') }'
        actual = parserutils.get_dup_key_val(errmsg)
        expected = {
            '_platform': 'twitter',
            '_raw_data': ObjectId('5543769ef861c942838c7ee9')
        }
        self.assertEqual(actual, expected)

    def test_nested_compound_index(self):
        """
        Tests the get_dup_key_val function for a compound index on nested fields.
        """
        errmsg = 'E11000 duplicate key error collection: test_database.test_posts index: ' + \
                 '_raw_data.backend_1__raw_data.collection_1__raw_data.doc_id_1 ' + \
                 'dup key: { : null, : null, : null }'
        actual = parserutils.get_dup_key_val(errmsg)
        expected = {
            '_raw_data.backend': None,
            '_raw_data.collection': None,
            '_raw_data.doc_id': None
        }
        self.assertEqual(actual, expected)


class FormatFieldsTestCase(TestCase):
    """
    Tests the format_fields function.
    """
    field_data = [('Name', 'Jane'), ('Age', 30), ('DOB', None)]

    def test_include_empty(self):
        """
        Tests the format_fields function when include_empty is True.
        """
        actual = parserutils.format_fields(self.field_data, include_empty=True)
        expected = """\
Name: Jane
Age:  30
DOB:  None"""
        self.assertEqual(actual, expected)

    def test_exclude_empty(self):
        """
        Tests the format_fields function when include_empty is False.
        """
        actual = parserutils.format_fields(self.field_data, include_empty=False)
        expected = """\
Name: Jane
Age:  30"""
        self.assertEqual(actual, expected)

