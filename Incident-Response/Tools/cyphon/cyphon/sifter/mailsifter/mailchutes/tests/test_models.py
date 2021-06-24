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
Tests the MailChute class.
"""

# standard library
from email.mime.text import MIMEText
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture

# local
from cyphon.documents import DocumentObj
from sifter.mailsifter.mailchutes.models import MailChute
from tests.fixture_manager import get_fixtures


class MailChuteTestCase(TestCase):
    """
    Base class for testing MailChutes.
    """
    fixtures = get_fixtures(['mailchutes'])

    def test_process_match(self):
        """
        Tests the process method for a matching email.
        """
        mock_doc_id = 1

        email = {'Message-ID': 'abc', 'Subject': 'This is a Critical Alert'}
        doc_obj = DocumentObj(data=email)

        mailchute = MailChute.objects.get(pk=1)
        mailchute.munger.process = Mock(return_value=mock_doc_id)

        doc_id = mailchute.process(doc_obj)

        mailchute.munger.process.assert_called_once_with(doc_obj)
        self.assertEqual(doc_id, mock_doc_id), None

    def test_process_nonmatch(self):
        """
        Tests the process method for a nonmatching email.
        """
        email = {'Message-ID': 'abc', 'Subject': 'This is an Urgent Alert'}
        doc_obj = DocumentObj(data=email)

        mailchute = MailChute.objects.get(pk=1)
        mailchute.munger.process = Mock(return_value=None)

        doc_id = mailchute.process(doc_obj)

        self.assertEqual(doc_id, None)

    def test_process_no_sieve(self):
        """
        Tests the process method for a chute with no sieve.
        """
        mock_doc_id = 1

        email = {'Message-ID': 'abc', 'Subject': 'This is an Urgent Alert'}
        doc_obj = DocumentObj(data=email)

        mailchute = MailChute.objects.get(pk=3)
        mailchute.enabled = True
        mailchute.munger.process = Mock(return_value=mock_doc_id)

        doc_id = mailchute.process(doc_obj)

        mailchute.munger.process.assert_called_once_with(doc_obj)
        self.assertEqual(doc_id, mock_doc_id)


# NOTE: use TransactionTestCase to handle threading

class MailChuteManagerTestCase(TransactionTestCase):
    """
    Tests the process_email receiver.
    """
    fixtures = get_fixtures(['mailchutes'])

    text = 'critical alert test'
    html = '<html><head></head><body><p>critical alert test</p></html>'
    count = 0

    def setUp(self):
        super(MailChuteManagerTestCase, self).setUp()
        self.msg = MIMEText('example text', 'plain')
        self.msg['Message-ID'] = 'NM615AA6A517B60AA16@email.com'
        self.msg['Date'] = 'Tue, 8 Sep 2015 16:08:59 -0400'
        self.doc_obj = DocumentObj(data=self.msg)

        # clear cached property
        try:
            del MailChute.objects._default_munger
        except AttributeError:
            pass

    def test_match_with_default(self):
        """
        Tests the process_email receiver for an email that matches an
        existing MailChute.
        """
        doc_obj = self.doc_obj
        doc_obj.data['Subject'] = 'critical alert'
        mock_config = {
            'DEFAULT_MUNGER': 'default_mail',
            'DEFAULT_MUNGER_ENABLED': True
        }
        with patch('distilleries.models.Distillery.save_data',
                   return_value='id_123') as mock_save:
            with patch.dict('sifter.mailsifter.mailchutes.models.conf.MAILSIFTER',
                            mock_config):
                with patch('sifter.mailsifter.mailchutes.models.MailChuteManager._process_with_default') \
                        as mock_catch_email:
                    MailChute.objects.process(doc_obj)
                    self.assertIs(mock_save.called, True)
                    self.assertIs(mock_catch_email.called, False)

    def test_no_match_without_default(self):
        """
        Tests the process_email receiver for an email that doesn't match
        an existing MailChute when a default MailMunger is not enabled.
        """
        doc_obj = self.doc_obj
        doc_obj.data['Subject'] = 'nothing to see here'
        mock_config = {
            'DEFAULT_MUNGER': 'default_mail',
            'DEFAULT_MUNGER_ENABLED': False
        }
        with patch('distilleries.models.Distillery.save_data') as mock_save:
            with patch.dict('sifter.mailsifter.mailchutes.models.conf.MAILSIFTER',
                            mock_config):
                with patch('sifter.mailsifter.mailchutes.models.MailChuteManager._process_with_default') \
                        as mock_catch_email:
                    MailChute.objects.process(doc_obj)
                    self.assertIs(mock_save.called, False)
                    self.assertIs(mock_catch_email.called, False)

    def test_no_match_with_default(self):
        """
        Tests the process_email receiver for an email that doesn't match
        an existing MailChute when a default MailMunger is enabled.
        """
        doc_obj = self.doc_obj
        doc_obj.data['Subject'] = 'nothing to see here'
        mock_config = {
            'DEFAULT_MUNGER': 'default_mail',
            'DEFAULT_MUNGER_ENABLED': True
        }
        with patch.dict('sifter.mailsifter.mailchutes.models.conf.MAILSIFTER',
                        mock_config):
            with patch('sifter.mailsifter.mailchutes.models.MailChuteManager._process_with_default') \
                    as mock_default_process:
                MailChute.objects.process(doc_obj)
                mock_default_process.assert_called_once_with(doc_obj)

    def test_no_match_missing_munger(self):
        """
        Tests the process_email receiver for an email that doesn't match
        an existing MailChute when a default MailChute is enabled but
        the defaul MailMunger can't be found.
        """
        doc_obj = self.doc_obj
        doc_obj.data['Subject'] = 'nothing to see here'
        mock_config = {
            'DEFAULT_MUNGER': 'missing_munger',
            'DEFAULT_MUNGER_ENABLED': True
        }
        with patch.dict('sifter.mailsifter.mailchutes.models.conf.MAILSIFTER',
                        mock_config):
            with LogCapture() as log_capture:
                msg = 'Default MailMunger "missing_munger" is not configured.'
                MailChute.objects.process(doc_obj)
                log_capture.check(
                    ('sifter.chutes.models', 'ERROR', msg),
                )
