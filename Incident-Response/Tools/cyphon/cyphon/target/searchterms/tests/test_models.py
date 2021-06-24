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
Tests the SearchTerm class used for keywords and phrases.
"""

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from target.searchterms.models import SearchTerm
from tests.fixture_manager import get_fixtures


class SearchTermManagerTestCase(TestCase):
    """
    Tests the SearchTermManager class.
    """
    fixtures = get_fixtures(['searchterms'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for SearchTerms.
        """
        term = SearchTerm.objects.get_by_natural_key('police')
        self.assertEqual(term.pk, 1)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method when the SearchTerm
        does not exist.
        """
        with LogCapture() as log_capture:
            SearchTerm.objects.get_by_natural_key('foobar')
            log_capture.check(
                ('target.searchterms.models',
                 'ERROR',
                 'SearchTerm "foobar" does not exist'),
            )

class SearchTermTestCase(TestCase):
    """
    Tests the SearchTerm class.
    """

    def test_tag_for_word(self):
        """
        Tests the tag property for a phrase.
        """
        term = SearchTerm.objects.create(term='police')
        self.assertEqual(term.tag, 'police')

    def test_tag_for_phrase(self):
        """
        Tests the tag property for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer')
        self.assertEqual(term.tag, 'policeofficer')


class ParseSearchTermTestCase(TestCase):
    """
    Tests the parse_term method.
    """

    def test_parse_term_for_word(self):
        """
        Tests parse_term method for a keyword.
        """
        term = SearchTerm.objects.create(term='police')
        self.assertEqual(term.parse_term(), ['police'])

    def test_parse_term_for_phrase(self):
        """
        Tests parse_term method for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer')
        self.assertEqual(term.parse_term(), ['police', 'officer'])


class IsPhraseTestCase(TestCase):
    """
    Tests the is_phrase method.
    """

    def test_is_phrase_for_word(self):
        """
        Tests is_phrase method for a keyword.
        """
        term = SearchTerm.objects.create(term='police')
        self.assertEqual(term.is_phrase(), False)

    def test_is_phrase_for_phrase(self):
        """
        Tests is_phrase method for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer')
        self.assertEqual(term.is_phrase(), True)


class CreateSearchTermFromTagTestCase(TestCase):
    """
    Tests the create_term_from_tag method.
    """

    def test_create_term_from_tag(self):
        """
        Tests create_term_from_tag method for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer', negate=True)
        new_term = term.create_term_from_tag()

        self.assertEqual(new_term.term, 'policeofficer')
        self.assertEqual(new_term.negate, True)


class FormatPhraseAsWordsTestCase(TestCase):
    """
    Tests the create_terms_from_words method.
    """

    def test_format_phrase_as_words(self):
        """
        Tests create_terms_from_words method for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer', negate=True)
        new_terms = term.create_terms_from_words()

        self.assertEqual(len(new_terms), 2)
        self.assertEqual(new_terms[0].term, 'police')
        self.assertEqual(new_terms[1].term, 'officer')


class CreateSearchTermsFromPhrasesTestCase(TestCase):
    """
    Tests the create_terms_from_phrase method.
    """

    def test_for_phrase(self):
        """
        Tests create_terms_from_phrase method for a phrase.
        """
        term = SearchTerm.objects.create(term='police officer', negate=False)
        new_terms = term.create_terms_from_phrase()

        self.assertEqual(len(new_terms), 3)
        self.assertEqual(new_terms[0].term, 'police')
        self.assertEqual(new_terms[1].term, 'officer')
        self.assertEqual(new_terms[2].term, 'policeofficer')
        self.assertEqual(new_terms[0].negate, False)
        self.assertEqual(new_terms[2].negate, False)

    def test_for_negated_phrase(self):
        """
        Tests create_terms_from_phrase method for a negated phrase.
        """
        term = SearchTerm.objects.create(term='police officer', negate=True)
        new_terms = term.create_terms_from_phrase()
        self.assertEqual(len(new_terms), 0)


class WrapInQuotesTestCase(TestCase):
    """
    Tests the wrap_in_quotes method.
    """

    def test_wrap_in_quotes(self):
        """
        Tests wrap_in_quotes method.
        """
        term = SearchTerm.objects.create(term='police officer')
        term.wrap_in_quotes()
        self.assertEqual(term.term, '"police officer"')
