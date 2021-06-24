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
Tests the MailSieve class and related classes.
"""

# stnndard library
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# third party
from django.test import TestCase

# local
from sifter.mailsifter.mailsieves.models import MailSieve


class MailSieveTestCase(TestCase):
    """
    Tests the MailSieve class.
    """

    fixtures = [
        'tests/fixtures/mailsieves.json',
    ]

    def setUp(self):
        self.subject_sieve = MailSieve.objects.get(name='check_subject')
        self.content_sieve = MailSieve.objects.get(name='check_content')

    def test_get_node_number(self):
        """
        Tests the get_node_number method.
        """
        self.assertTrue(self.content_sieve.get_node_number(), 2)

    def test_is_match_for_all_true(self):
        """
        Tests the is_match method for a MailSieve that uses 'AND' logic and a
        dataset that conforms to the MailSieve.
        """
        msg = MIMEText('this is some test content')
        msg['Subject'] = 'this is a critical alert'
        self.assertTrue(self.subject_sieve.is_match(msg))

    def test_is_match_for_all_false(self):
        """
        Tests the is_match method for a MailSieve that uses 'AND' logic and a
        dataset that does not conform to the MailSieve.
        """
        msg = MIMEText('this is some test content')
        msg['Subject'] = 'this is an urgent alert'
        self.assertFalse(self.subject_sieve.is_match(msg))

    def test_is_match_for_any_true(self):
        """
        Tests the is_match method for a MailSieve that uses 'OR' logic and a
        dataset that conforms to the MailSieve.
        """
        self.subject_sieve.logic = 'OR'
        msg = MIMEText('this is some test content')
        msg['Subject'] = 'this is an urgent alert'
        self.assertTrue(self.subject_sieve.is_match(msg))

    def test_is_match_for_any_false(self):
        """
        Tests the is_match method for a MailSieve that uses 'OR' logic and a
        dataset that does not conform to the MailSieve.
        """
        self.subject_sieve.logic = 'OR'
        msg = MIMEText('this is some test content')
        msg['Subject'] = 'this is an urgent notice'
        self.assertFalse(self.subject_sieve.is_match(msg))

    def test_search_content_true(self):
        """
        Tests the is_match method for a MailSieve where the search term is in
        the message content.
        """
        msg = MIMEText('this is some test content')
        self.assertTrue(self.content_sieve.is_match(msg))

    def test_search_content_false(self):
        """
        Tests the is_match method for a MailSieve where the search term is in
        the message content.
        """
        msg = MIMEText('this is some example content')
        self.assertFalse(self.content_sieve.is_match(msg))

    def test_negate(self):
        """
        Tests the is_match method for a negated MailSieve.
        """
        self.content_sieve.negate = True
        msg = MIMEText('this is some test content')
        self.assertFalse(self.content_sieve.is_match(msg))
