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

# third party
from django.test import TestCase

# local
from query.search.keyword_search_parameter import KeywordSearchParameter


class KeywordSearchParameterTestCase(TestCase):
    """
    TestCase for the KeywordSearchParameter class.
    """
    def test_empty_keyword_value(self):
        """
        Tests that an EMPTY_VALUE error is added to the parameter
        error list if the given keyword is empty.
        """
        parameter = KeywordSearchParameter(2, '')

        self.assertFalse(parameter.is_valid())
        self.assertEqual(len(parameter.errors), 1)
        self.assertEqual(
            parameter.errors[0],
            KeywordSearchParameter.EMPTY_VALUE,
        )

    def test_keyword_clean(self):
        """
        Tests that the keyword is stripped of any quotes.
        """
        parameter = KeywordSearchParameter(2, '"test me"')

        self.assertTrue(parameter.is_valid())
        self.assertEqual(parameter.keyword, 'test me')

    def test_get_parameter_info(self):
        """
        Tests that .get_parameter_info() returns the extra properties
        besides the base dictionary.
        """
        parameter = KeywordSearchParameter(3, '"Oh my"')

        self.assertDictEqual(parameter.as_dict(), {
            'parameter': '"Oh my"',
            'type': 'keyword',
            'index': 3,
            'errors': [],
            'keyword': 'Oh my',
        })
