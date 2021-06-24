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
Defines a Parser mixin for obtaining matches for regular expressions.
"""

# standard library
import logging
import re

# third party
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# local
from utils.dateutils import dateutils
from utils.parserutils import parserutils
from utils.validators import validators

LOGGER = logging.getLogger(__name__)


class Parser(models.Model):
    """
    An abstract base class for parsing a value from an object, such as a string
    or dictionary.

    Attributes:
        formatter: a template that will be used to format the parsed value,
            For example, 'https://twitter.com/{}/' may be used to construct a
            link to a Twitter profile.
        regex: a string representing a pattern to be compiled as a regular
            expression
        method: a string specifying the form of a result to be obtained from a
            regex search, e.g., the number of matches, presence/absence of a
            match, or the value of a substring from the first match
    """
    METHOD_CHOICES = (
        ('COPY', 'Copy'),
        ('COUNT', 'Number of Occurrences'),
        ('DATE', 'Date from string'),
        ('P/A', 'Presence/Absence'),
        ('SUBSTRING', 'Substring'),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_('It\'s a good idea to name parsers after the source '
                    'field(s) they are parsing and the method they use, e.g., '
                    '"screen_name__COPY."')
    )
    method = models.CharField(
        max_length=40,
        choices=METHOD_CHOICES,
        default='COPY',
        help_text=_('The method used to extract data. "Copy" will return the '
                    'entire contents of the source field(s). "Number of '
                    'Occurrences" will return the number of times a match for '
                    'the regex is found in the source field(s). "Presence/'
                    'Absence" will return a Boolean indicating whether a regex '
                    'match is found. "Substring" will return the first '
                    'substring group defined in the Parser\'s regex.')
    )
    regex = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
        validators=[validators.regex_validator],
        help_text=_('A regular expression used to match substrings in the '
                    'text of the source field(s). Not required if the method '
                    'is "Copy."')
    )
    formatter = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default=None,
        help_text=_('A Python format string that will be used to format the '
                    'parsed value. For example, "https://twitter.com/{}/" '
                    'may be used to construct a link to a Twitter profile. ')
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        super(Parser, self).clean()

        if self.method not in ['COPY', 'DATE'] and not self.regex:
            method_name = self.get_method_display()
            raise ValidationError(_('A regex must be provided to use the '
                                    '%s method.' % method_name))

    def _search(self, string):
        """
        Takes a string and returns a re.MatchObject for the Parser's regex.
        """
        # TODO(LH): catch exceptions for malformed regex
        return re.search(self.regex, string, re.DOTALL | re.IGNORECASE)

    def _is_present(self, string):
        """
        Takes a string and returns a Boolean indicating whether the string
        contains a match for the Parser's regex.
        """
        matches = self._search(string)
        if matches:
            return True
        return False

    def _get_substring(self, string):
        """
        Takes a string and, if the string contains a match for the Parser's
        regex, returns the first substring group defined in the Parser's regex.
        Otherwise, returns None.
        """
        match = self._search(string)
        if match:
            try:
                return match.group(1)
            except IndexError:
                LOGGER.error('The parser cannot return a value because no '
                             'group is defined in the r\'%s\'regex pattern.',
                             self.regex)
        return None

    def _get_date(self, string):
        """
        Converts a string into a datetime object.
        """
        if self.regex:
            string = self._get_substring(string)
        return dateutils.date_from_str(string)

    def _findall(self, string):
        """
        Takes a string and returns a list of strings matching the Parser's regex.
        """
        return re.findall(self.regex, string, re.DOTALL | re.IGNORECASE)

    def _get_count(self, string):
        """
        Takes a string and returns the number of matches for the Parser's regex.
        """
        matches = self._findall(string)
        return len(matches)

    def _parse(self, value):
        """
        Takes a string and returns a parsing result according to the Parser's
        method.
        """
        if self.method == 'COPY':
            return value
        else:
            methods = {
                'COUNT': self._get_count,
                'P/A': self._is_present,
                'SUBSTRING': self._get_substring,
                'DATE': self._get_date,
            }

            func = methods[self.method]
            return func(str(value))

    def _format(self, results):
        """

        """
        template = self.formatter
        return template.format(results)

    def _apply_template(self, results):
        """
        Takes a results string and returns a string that formats the result
        with the Parser's formatter.
        """
        if isinstance(results, list):
            return [self._format(item) for item in results]
        else:
            return self._format(results)

    def process(self, value):
        """
        Takes a value and returns a parsed result.
        """
        result = self._parse(value)

        if self.formatter and self.method != 'DATE':
            return self._apply_template(result)
        else:
            return result


class StringParser(Parser):
    """
    A StringParser provides proper validation for parsing and formatting strings.
    """

    def clean(self):
        """
        Adds custom validations to the model's clean() method.
        """
        super(StringParser, self).clean()

        validators.validate_str_substitution(self.formatter, 1)

    class Meta:
        abstract = True
        ordering = ['name']


class FieldParser(Parser):
    """
    A FieldParser is a Parser designed to parse objects that contain fields
    accessible through dictionary keys. It extends the Parser class with the
    source_fields attribute:

    Attribute:
        source_fields: comma-separated field names from a dictionary that will
            be used to assemble a value for a field in a custom object (defined
            by a DataField). For example, 'user.screen_name,id_str' may be
            used to construct a link to a tweet.

    """
    source_fields = models.CharField(
        max_length=255,
        verbose_name=_('source field(s)'),
        help_text=_('One or more fields in a raw data document from which '
                    'data will be extracted. Multiple field names should be '
                    'separated by commas. Nested fields should be denoted using '
                    'dot notation. For example, "user.first_name,user.last_name" '
                    'will parse the fields {user: {first_name: "Jane", '
                    'last_name: "Smith"}}.')
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def clean(self):
        """
        Adds custom validations to the model's clean() method.
        """
        super(FieldParser, self).clean()
        self._validate_formatter()

    def _validate_formatter(self):
        """
        Ensures that the formatter can accomodate the number of source_fields.
        """
        if self.method in ['COPY', 'SUBSTRING']:
            fields = self.source_fields.split(',')
            validators.validate_str_substitution(self.formatter, len(fields))
        else:
            # for COUNT and P/A, results will be aggregated into one value
            validators.validate_str_substitution(self.formatter, 1)

    def _get_values(self, doc):
        """
        Takes a dictionary and returns values for the keys specified by the
        source_fields.
        """
        fields = self.source_fields.split(',')
        values = []

        for field in fields:
            key = field.strip() # in case there were spaces after commas
            value = parserutils.get_dict_value(key, doc)
            values.append(value)

        return values

    def _parse_all(self, values):
        """
        Takes a list of values and returns a list of parsing results
        according to the Parser's method.
        """
        parsed_values = []
        for value in values:
            new_value = self._parse(value)
            parsed_values.append(new_value)
        return parsed_values

    def _aggregate(self, parsed_results):
        """
        Takes a list of parsed results. If the Parser's method is COUNT or P/A,
        aggregates the results into a single-item list. Otherwise, returns the
        original list.
        """
        if self.method == 'COUNT':
            return [sum(parsed_results)]
        elif self.method == 'P/A':
            return [True in parsed_results]
        else:
            return parsed_results

    @staticmethod
    def _extract_result(aggregated_results):
        """
        Takes a list of aggregated_results, and returns either a single result
        or a list of results, depending on the length of the original list.
        If more than one result is contained in the list, returns the orginal
        list. If only one result is in the list, returns that result. If no
        results are contained in the list, returns an empty string.
        """
        if len(aggregated_results) == 1:
            return aggregated_results[0]
        elif len(aggregated_results) > 1:
            return aggregated_results
        else:
            return ''

    def _apply_template(self, results):
        """
        Takes a list of results and returns a string that formats the results
        with the Parser's formatter.
        """
        template = self.formatter
        return template.format(*results)

    def _format(self, results):
        """
        Takes a list of aggregated results and formats them with the
        formatter if one is provided. Otherwise, formats them according to
        how many results are returned.
        """
        if self.formatter:
            return self._apply_template(results)
        else:
            return self._extract_result(results)

    def process(self, value):
        """
        Takes a dictionary and returns a parsed result from the dictionary.
        """
        values = self._get_values(value)
        parsed_results = self._parse_all(values)
        aggregated_results = self._aggregate(parsed_results)
        return self._format(aggregated_results)

