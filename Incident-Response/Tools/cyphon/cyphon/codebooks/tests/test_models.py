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
Tests the CodeBook, RealName, and CodeName classes.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from codebooks.models import CodeName, RealName, CodeBook
from tests.fixture_manager import get_fixtures


class CodeBookBaseTestCase(TestCase):
    """
    Base class for testing the CodeBook class and related classes.
    """
    fixtures = get_fixtures(['codebooks'])

    mock_settings = {
        'CODENAME_PREFIX': '**',
        'CODENAME_SUFFIX': '**'
    }


class CodeNameTestCase(CodeBookBaseTestCase):
    """
    Tests the CodeName class.
    """

    def setUp(self):
        self.codename = CodeName.objects.get_by_natural_key('PEAK')

    def test__str__(self):
        """
        Tests the __str__ method.
        """
        self.assertEqual(str(self.codename), 'PEAK')

    def test_formatted_codename(self):
        """
        Tests the formatted_codename method.
        """
        with patch.dict('codebooks.models.settings.CODEBOOKS',
                        self.mock_settings):
            actual = self.codename.formatted_codename
            expected = '**PEAK**'
            self.assertEqual(actual, expected)


class RealNameManagerTestCase(CodeBookBaseTestCase):
    """
    Tests the RealNameManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method when the CodeBook exists.
        """
        realname = RealName.objects.get_by_natural_key('Acme.?Supply.?Co')
        self.assertEqual(realname.pk, 1)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the CodeBook does not exist.
        """
        with LogCapture() as log_capture:
            natural_key = 'fake.name'
            msg = 'RealName "%s" does not exist' % natural_key
            RealName.objects.get_by_natural_key(natural_key)
            log_capture.check(
                ('codebooks.models', 'ERROR', msg),
            )


class RealNameTestCase(CodeBookBaseTestCase):
    """
    Tests the RealName class.
    """

    def setUp(self):
        self.realname = RealName.objects.get_by_natural_key('Acme.?Supply.?Co')

    def test__str__(self):
        """
        Tests the __str__ method.
        """
        self.assertEqual(str(self.realname), 'PEAK: Acme.?Supply.?Co')

    def test_to_dict(self):
        """
        Tests the to_dict method.
        """
        actual = self.realname.to_dict()
        expected = {'Acme.?Supply.?Co': 'PEAK'}
        self.assertEqual(actual, expected)

    def test_redact(self):
        """
        Tests the redact method.
        """
        with patch.dict('codebooks.models.settings.CODEBOOKS',
                        self.mock_settings):
            text = 'John Smith is president of Acme Supply Co.'
            actual = self.realname.redact(text)
            expected = 'John Smith is president of **PEAK**.'
            self.assertEqual(actual, expected)


class CodeBookManagerTestCase(CodeBookBaseTestCase):
    """
    Tests the CodeBookManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method.
        """
        codebook = CodeBook.objects.get_by_natural_key('Acme')
        self.assertEqual(codebook.pk, 1)

    def test_get_by_nk_no_company(self):
        """
        Tests the get_by_natural_key method when the Company does not exist.
        """
        with LogCapture() as log_capture:
            natural_key = 'fake.name'
            msg1 = 'Company "%s" does not exist' % natural_key
            msg2 = 'Codebook for Company "%s" does not exist' % natural_key
            CodeBook.objects.get_by_natural_key(natural_key)
            log_capture.check(
                ('cyphon.models', 'ERROR', msg1),
                ('codebooks.models', 'ERROR', msg2),
            )


class CodeBookTestCase(CodeBookBaseTestCase):
    """
    Tests the CodeBook class.
    """

    def setUp(self):
        self.codebook = CodeBook.objects.get_by_natural_key('Acme')

    def test_str(self):
        """
        Tests the str method.
        """
        self.assertEqual(str(self.codebook), 'Acme')

    def test_preview(self):
        """
        Tests the preview method.
        """
        actual = self.codebook.preview()
        expected = \
"""{
    "Acme.?Supply.?Co": "PEAK",
    "John.?Smith": "FORGE",
    "Acme.?Supply": "PEAK",
    "Smith": "FORGE",
    "Acme": "PEAK"
}"""
        self.assertEqual(actual, expected)

    def test_redact(self):
        """
        Tests the redact method.
        """
        with patch.dict('codebooks.models.settings.CODEBOOKS',
                        self.mock_settings):
            text = 'John Smith is president of Acme Supply Co.'
            actual = self.codebook.redact(text)
            expected = '**FORGE** is president of **PEAK**.'
            self.assertEqual(actual, expected)
