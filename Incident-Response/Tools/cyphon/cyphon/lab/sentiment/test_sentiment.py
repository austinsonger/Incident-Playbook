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
from .sentiment import clean_text, get_polarity, get_sentiment


class CleanTextTestCase(TestCase):
    """
    Tests the clean_text() function.
    """

    def test_clean_url(self):
        """
        Tests the clean_text() function for text containing a URL.
        """
        actual = clean_text('check out this link: https://cyphon.io')
        expected = 'check out this link'
        self.assertEqual(actual, expected)

    def test_clean_at(self):
        """
        Tests the clean_text() function for text containing an @ symbol.
        """
        actual = clean_text('@foobar hey there')
        expected = 'hey there'
        self.assertEqual(actual, expected)

    def test_clean_hashtag(self):
        """
        Tests the clean_text() function for text containing a hasttag.
        """
        actual = clean_text('#foobar hey there')
        expected = 'foobar hey there'
        self.assertEqual(actual, expected)


class GetPolarityTestCase(TestCase):
    """
    Tests the get_polarity() function.
    """

    def setUp(self):
        self.mock_analysis = Mock()
        self.mock_analysis.sentiment = Mock()

    def test_positive_polarity(self):
        """
        Tests the get_polarity() function for a postive sentiment.
        """
        polarity = 0.1
        self.mock_analysis.sentiment.polarity = polarity

        with patch('lab.sentiment.sentiment.TextBlob',
                   return_value=self.mock_analysis):
            self.assertEqual(get_polarity('foobar'), polarity)

    def test_neutral_polarity(self):
        """
        Tests the get_polarity() function for a neutral sentiment.
        """
        polarity = 0
        self.mock_analysis.sentiment.polarity = polarity

        with patch('lab.sentiment.sentiment.TextBlob',
                   return_value=self.mock_analysis):
            self.assertEqual(get_polarity('foobar'), polarity)

    def test_negative_polarity(self):
        """
        Tests the get_polarity() function for a negative sentiment.
        """
        polarity = -0.1
        self.mock_analysis.sentiment.polarity = polarity

        with patch('lab.sentiment.sentiment.TextBlob',
                   return_value=self.mock_analysis):
            self.assertEqual(get_polarity('foobar'), polarity)


class GetSentimentTestCase(TestCase):
    """
    Tests the get_sentiment() function.
    """

    def test_sentiment(self):
        """
        Tests the get_sentiment() function for various sentiments.
        """
        self.assertEqual(get_sentiment('this is awesome'), 'positive')
        self.assertEqual(get_sentiment('this sucks'), 'negative')
        self.assertEqual(get_sentiment('yo'), 'neutral')

    def test_positive_sentiment(self):
        """
        Tests the threshold of the get_sentiment() function for a
        postive sentiment.
        """
        with patch('lab.sentiment.sentiment.get_polarity', return_value=0.1):
            self.assertEqual(get_sentiment('foobar'), 'positive')

    def test_neutral_sentiment(self):
        """
        Tests the threshold of the get_sentiment() function for a
        neutral sentiment.
        """
        with patch('lab.sentiment.sentiment.get_polarity', return_value=0):
            self.assertEqual(get_sentiment('foobar'), 'neutral')

    def test_negative_sentiment(self):
        """
        Tests the threshold of the get_sentiment() function for a
        negative sentiment.
        """
        with patch('lab.sentiment.sentiment.get_polarity', return_value=-0.1):
            self.assertEqual(get_sentiment('foobar'), 'negative')
