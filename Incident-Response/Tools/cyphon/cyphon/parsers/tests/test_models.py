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
Tests the Parser class.
"""

# standard library
from unittest import TestCase

# third party
from django.core.exceptions import ValidationError
import six

# local
from parsers.models import Parser, StringParser, FieldParser


class ParseTestCase(TestCase):
    """
    Tests the _parse method of the Parser class.
    """

    string = \
        """
        Customer:    Acme Supply Company
        Status:      Open
        Threat:      Medium
        Class:       application-attack
        Start Date:  Apr 2 2015 10:15am GMT
        End Date:    Apr 2 2015 10:15am GMT

        Source IP:      128.101.101.101

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php
        """

    def test_count_no_matches(self):
        """
        Tests the _parse method for a 'count' method when a string has no
        matches.
        """
        parser = Parser(
            method='COUNT',
            regex='Bad Robots'
        )
        result = parser._parse(self.string)
        self.assertEqual(result, 0)

    def test_count_multi_matches(self):
        """
        Tests the _parse method for a 'count' method when a string has
        multiple matches.
        """
        parser = Parser(
            method='COUNT',
            regex='Bad Bots'
        )
        result = parser._parse(self.string)
        self.assertEqual(result, 2)

    def test_presence_true(self):
        """
        Tests the _parse method for a 'presence' method when a string has a
        match.
        """
        parser = Parser(
            method='P/A',
            regex='Bad Bots'
        )
        result = parser._parse(self.string)
        self.assertTrue(result)

    def test_presence_false(self):
        """
        Tests the _parse method for a 'presence' method when a string has no
        match.
        """
        parser = Parser(
            method='P/A',
            regex='Bad Robots'
        )
        result = parser._parse(self.string)
        self.assertFalse(result)

    def test_value_match(self):
        """
        Tests the _parse method for a 'value' method when a string has a
        match.
        """
        parser = Parser(
            method='SUBSTRING',
            regex='Threat:\s*(\w+)\n'
        )
        result = parser._parse(self.string)
        self.assertEqual(result, 'Medium')

        parser = Parser(
            method='SUBSTRING',
            regex='source.?IP.*\s(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        )
        result = parser._parse(self.string)
        self.assertEqual(result, '128.101.101.101')

    def test_value_no_match(self):
        """
        Tests the _parse method for a 'value' method when a string has no
        match.
        """
        parser = Parser(
            method='SUBSTRING',
            regex='Threats:\s*(\w+)\n'
        )
        result = parser._parse(self.string)
        self.assertEqual(result, None)

    def test_copy(self):
        """
        Tests the _parse method for a 'value' method when a string has a
        match.
        """
        parser = Parser(method='COPY')
        result = parser._parse('this is an example post')
        self.assertEqual(result, 'this is an example post')


class StringParserTestCase(TestCase):
    """
    Tests clean method of the StringParser class.
    """

    def test_more_than_one_specifier(self):
        """
        Tests that a validation error is raised if more than one specifier is
        present in the string formatter.
        """
        parser = StringParser(
            method='COPY',
            formatter='https://twitter.com/{}/statuses/{}'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The formatter should '
                                   'only contain one "{}" specifier for the '
                                   'source field.'):
            parser.clean()

    def test_no_specifiers(self):
        """
        Tests that a validation error is raised if no specifiers are present
        the string formatter.
        """
        parser = StringParser(
            method='COPY',
            formatter='https://twitter.com/'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The formatter should '
                                    'contain one "{}" specifier.'):
            parser.clean()

    def test_one_specifier(self):
        """
        Tests that a validation error is not raised if only one specifier is
        present in the string formatter.
        """
        parser = StringParser(
            method='COPY',
            formatter='https://twitter.com/{}'
        )
        try:
            parser.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')


class CleanFieldParserTestCase(TestCase):
    """
    Tests clean method of the FieldParser class.
    """

    def test_too_many_specifiers_single(self):
        """
        Test that a validation error is raised when only one source field is
        defined and the formatter has multiple specifiers.
        """
        parser = FieldParser(
            name='user.screen_name',
            source_fields='user.screen_name',
            formatter='https://twitter.com/{}/statuses/{}'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The formatter should '
                                   'only contain one "{}" specifier for the '
                                   'source field.'):
            parser.clean()

    def test_too_many_specifiers_multi(self):
        """
        Test that a validation error is raised when multiple source fields are
        defined and the formatter has too many specifiers.
        """
        parser = FieldParser(
            name='user.screen_name',
            source_fields='user.screen_name, id_str',
            formatter='https://twitter.com/{}/statuses/{}/{}'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The number of "{}" '
                                   'specifiers in the formatter exceeds the '
                                   'number of source fields.'):
            parser.clean()

    def test_too_few_specifiers_single(self):
        """
        Test that a validation error is raised when one source field is
        defined and the formatter has no specifiers.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name',
            formatter='https://twitter.com/statuses/'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The formatter should '
                                   'contain one "{}" specifier.'):
            parser.clean()

    def test_too_few_specifiers_multi(self):
        """
        Test that a validation error is raised when the formatter has too few
        specifiers for the number of source fields.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name, id_str',
            formatter='https://twitter.com/{}/statuses/'
        )
        with six.assertRaisesRegex(self, ValidationError, 'The formatter contains '
                                   'too few "{}" specifiers for the number of '
                                   'source fields.'):
            parser.clean()

    def test_multi_fields_no_template(self):
        """
        Test case for when multiple source fields are provided but
        no formatter is given to format them.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name, id_str'
        )
        with six.assertRaisesRegex(self, ValidationError, 'No template has been '
                                   'provided for formatting multiple fields'):
            parser.clean()

    def test_single_field_no_template(self):
        """
        Test case for when a single source_filed is provided without a
        formatter.
        """
        parser = FieldParser(
            name='user.screen_name',
            source_fields='user.screen_name'
        )
        try:
            parser.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_no_regex_for_count(self):
        """
        Tests that a validation error is raised when no regex is defined when
        the COUNT method is chosen.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name',
            method='COUNT'
        )
        with six.assertRaisesRegex(self, ValidationError, 'A regex must be provided '
                                   'to use the Number of Occurrences method.'):
            parser.clean()

    def test_no_regex_for_pres_abs(self):
        """
        Tests that a validation error is raised when no regex is defined when
        the P/A method is chosen.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name',
            method='P/A'
        )
        with six.assertRaisesRegex(self, ValidationError, 'A regex must be provided '
                                   'to use the Presence/Absence method.'):
            parser.clean()

    def test_no_regex_for_substring(self):
        """
        Tests that a validation error is raised when no regex is defined when
        the SUBSTRING method is chosen.
        """
        parser = FieldParser(
            name='user.link',
            source_fields='user.screen_name',
            method='SUBSTRING'
        )
        with six.assertRaisesRegex(self, ValidationError, 'A regex must be provided '
                                   'to use the Substring method.'):
            parser.clean()

    def test_no_regex_for_copy(self):
        """
        Tests that no validation error is raised when the COPY method is chosen
        witha regex.
        """
        parser = FieldParser(
            name='screen_name',
            source_fields='user.screen_name',
            method='COPY'
        )
        try:
            parser.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')


class FieldParserProcessTestCase(TestCase):
    """
    Tests the process method of the FieldParser class.
    """

    doc = {
        'id_str': '0123456',
        'text': 'this is an example post',
        'user': {
            'screen_name': 'zebrafinch'
        }
    }

    def test_for_string_tenplate(self):
        """
        Tests method for assembling the value of a target_field that uses
        a string template.
        """
        parser = FieldParser(
            source_fields='user.screen_name, id_str',
            formatter='https://twitter.com/{}/statuses/{}'
        )
        actual = parser.process(self.doc)
        expected = 'https://twitter.com/zebrafinch/statuses/0123456'
        self.assertEqual(actual, expected)

    def test_for_no_tenplate(self):
        """
        Tests method for assembling the value of a target_field that doesn't use
        a string template.
        """
        parser = FieldParser(source_fields='text')
        actual = parser.process(self.doc)
        expected = 'this is an example post'
        self.assertEqual(actual, expected)

