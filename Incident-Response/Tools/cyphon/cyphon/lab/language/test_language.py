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

"""

# standard library
from unittest import TestCase
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# local
from .language import get_language, PROBABILTY


class LanguageTestCase(TestCase):
    """
    Tests the get_language() function.
    """

    def setUp(self):
        self.mock_lang = Mock()

    def test_unsupported(self):
        """
        Tests the get_language() function for an unsupported language.
        """
        self.mock_lang.prob = 1.0
        self.mock_lang.lang = 'foo'
        with patch('lab.language.language.detect_langs',
                   return_value=[self.mock_lang]):
            self.assertEqual(get_language('foobar'), 'none')

    def test_below_threshold(self):
        """
        Tests the get_language() function for text below the probability
        threshold.
        """
        self.mock_lang.prob = PROBABILTY - 0.1
        self.mock_lang.lang = 'en'
        with patch('lab.language.language.detect_langs',
                   return_value=[self.mock_lang]):
            self.assertEqual(get_language('this is english'), 'none')

    def test_at_threshold(self):
        """
        Tests the get_language() function for text at the probability
        threshold.
        """
        self.mock_lang.prob = PROBABILTY
        self.mock_lang.lang = 'en'
        with patch('lab.language.language.detect_langs',
                   return_value=[self.mock_lang]):
            self.assertEqual(get_language('this is english'), 'en')

    def test_above_threshold(self):
        """
        Tests the get_language() function for text above the probability
        threshold.
        """
        self.mock_lang.prob = PROBABILTY + 0.1
        self.mock_lang.lang = 'en'
        with patch('lab.language.language.detect_langs',
                   return_value=[self.mock_lang]):
            self.assertEqual(get_language('this is english'), 'en')

    def test_english(self):
        """
        Tests the get_language() function for English text.
        """
        self.assertEqual(get_language('this is english'), 'en')
