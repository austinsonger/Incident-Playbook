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
Tests accessor functions for the mailsifter package.
"""

# standard library
from email.mime.multipart import MIMEMultipart
import datetime
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from testfixtures import LogCapture

# local
from sifter.mailsifter import accessors
from .base import MailHelperTestCase


class GetDateTestCase(MailHelperTestCase):
    """
    Tests the get_date helper function.
    """

    def test_get_date_valid(self):
        """
        Tests the get_date function for a valid date string.
        """
        actual = accessors.get_date(self.msg)
        expected = '2015-09-08T16:08:59-04:00'
        self.assertEqual(actual, expected)

    def test_get_date_not_valid(self):
        """
        Tests the get_date function for an invalid date string.
        """
        with LogCapture() as log_capture:
            msg = MIMEMultipart('alternative')
            msg['Message-ID'] = 'msgID'
            msg['Date'] = 'bad'
            actual = accessors.get_date(msg)
            expected = None
            self.assertEqual(actual, expected)
            log_msg = 'Email date for msgID could not be parsed.'
            log_capture.check(
                ('sifter.mailsifter.accessors', 'WARNING', log_msg),
            )


class GetSubjectTestCase(MailHelperTestCase):
    """
    Tests the get_subject helper function.
    """

    def test_base64(self):
        """
        Tests the get_subject function for a base64 encoded string.
        """
        subject = '=?utf-8?B?U3RpbGwgdGltZSB0byByZWdpc3RlciE==?='
        email = {'Subject': subject}
        actual = accessors.get_subject(email)
        expected = 'Still time to register!'
        self.assertEqual(actual, expected)

    def test_unicode(self):
        """
        Tests the get_subject function for a unicode string.
        """
        subject = 'Still time to register!'
        email = {'Subject': subject}
        actual = accessors.get_subject(email)
        expected = subject
        self.assertEqual(actual, expected)

    def test_empty(self):
        """
        Tests the get_subject function for an email without a subject field.
        """
        email = {'Content': 'foo'}
        actual = accessors.get_subject(email)
        expected = ''
        self.assertEqual(actual, expected)


class GetContentTestCase(MailHelperTestCase):
    """
    Tests the get_content helper function.
    """
    cleaned_html = \
"""   Hi!
   How are you?
   Here is the
    link
   you wanted."""

    def test_multipart_default(self):
        """
        Tests the get_content function with a multipart email and default
        settings for content_types and remove_tags.
        """
        self.msg.attach(self.part1)
        self.msg.attach(self.part2)
        actual = accessors.get_content(self.msg)
        expected = self.text.encode('UTF-8')
        self.assertEqual(actual, expected)

    def test_multipart_html(self):
        """
        Tests the get_content function for a multipart email with
        text/html content preferred and default setting for remove_tags.
        """
        self.msg.attach(self.part1)
        self.msg.attach(self.part2)
        content_types = ('text/html', 'text/plain')
        self.mock_mailsifter_settings['EMAIL_CONTENT_PREFERENCES'] = content_types
        with patch.dict('sifter.mailsifter.accessors.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            actual = accessors.get_content(self.msg, content_types=('text/html',
                                                                    'text/plain'))
            expected = self.cleaned_html
            self.assertEqual(actual, expected)

    def test_multipart_html_with_tags(self):
        """
        Tests the get_content function for a multipart email with
        text/html content preferred and remove_tags=False.
        """
        self.msg.attach(self.part1)
        self.msg.attach(self.part2)
        actual = accessors.get_content(
            email=self.msg,
            content_types=('text/html', 'text/plain'),
            remove_tags=False
        )
        expected = self.html.encode('UTF-8')
        self.assertEqual(actual, expected)

    def test_nonmultipart_text(self):
        """
        Tests the get_content function with a nonmultipart plain text
        email and default settings for content_types and remove_tags.
        """
        self.msg.attach(self.part1)
        content_types = ('text/html', 'text/plain')
        self.mock_mailsifter_settings['EMAIL_CONTENT_PREFERENCES'] = content_types
        with patch('sifter.mailsifter.accessors.settings.MAILSIFTER',
                   self.mock_mailsifter_settings):
            actual = accessors.get_content(self.msg)
            expected = self.text.encode('UTF-8')
            self.assertEqual(actual, expected)

    def test_nonmultipart_html(self):
        """
        Tests the get_content function with a nonmultipart html email
        and default settings for content_types and remove_tags.
        """
        self.msg.attach(self.part2)
        content_types = ('text/html', 'text/plain')
        self.mock_mailsifter_settings['EMAIL_CONTENT_PREFERENCES'] = content_types
        with patch('sifter.mailsifter.accessors.settings.MAILSIFTER',
                   self.mock_mailsifter_settings):
            actual = accessors.get_content(self.msg)
            expected = self.cleaned_html
            self.assertEqual(actual, expected)

    def test_nonmultipart_html_w_tags(self):
        """
        Tests the get_content function with a nonmultipart html email,
        the default setting for content_types, and remove_tags=False.
        """
        self.msg.attach(self.part2)
        content_types = ('text/html', 'text/plain')
        self.mock_mailsifter_settings['EMAIL_CONTENT_PREFERENCES'] = content_types
        with patch('sifter.mailsifter.accessors.settings.MAILSIFTER',
                   return_value=content_types):
            actual = accessors.get_content(self.msg, remove_tags=False)
            expected = self.html.encode('UTF-8')
            self.assertEqual(actual, expected)

    def test_multipart_no_text(self):
        """
        Tests the get_content function with a multipart email with
        no text.
        """
        self.assertEqual(accessors.get_content(self.msg), None)

    def test_nonmultipart_no_text(self):
        """
        Tests the get_content function with a nonmultipart email that
        doesn't contain the requested content type.
        """
        msg = self.part2
        actual = accessors.get_content(email=msg, content_types=('text/plain', ))
        self.assertEqual(actual, None)

    def test_nested_multipart(self):
        """
        Tests the get_content function with a multipart email that
        contains another multipart message.
        """
        msg = MIMEMultipart('alternative')
        self.msg.attach(self.part2)
        self.msg.attach(self.part1)
        msg.attach(self.msg)
        actual = accessors.get_content(msg)
        expected = self.text.encode('UTF-8')
        self.assertEqual(actual, expected)


class GetFirstAttachmentTestCase(MailHelperTestCase):
    """
    Tests the get_first_attachment function.
    """
    date = datetime.date(year=2016, month=12, day=10)

    def test_attachment_single(self):
        """
        Tests the get_first_attachment function for an attachment.
        """
        self.msg.attach(self.pdf)
        self.msg.attach(self.image)
        actual = accessors.get_first_attachment(self.msg)
        expected = self.pdf
        self.assertEqual(actual, expected)

    def test_unallowed_attachment(self):
        """
        Tests the get_first_attachment function for an unallowed file
        type.
        """
        self.msg.attach(self.java)
        self.msg.attach(self.image)
        actual = accessors.get_first_attachment(self.msg)
        expected = self.image
        self.assertEqual(actual, expected)

    def test_inline(self):
        """
        Tests the get_first_attachment function for inline content.
        """
        self.msg.attach(self.inline)
        self.msg.attach(self.pdf)
        actual = accessors.get_first_attachment(self.msg)
        expected = self.pdf
        self.assertEqual(actual, expected)

    def test_none(self):
        """
        Tests the get_first_attachment function for no attachment.
        """
        actual = accessors.get_first_attachment(self.msg)
        expected = None
        self.assertEqual(actual, expected)

    def test_using_file_extension(self):
        """
        Tests the get_first_attachment function using file extension.
        """
        mock_settings_1 = {
            'ALLOWED_EMAIL_ATTACHMENTS': (),
            'ALLOWED_FILE_EXTENSIONS': ('.jar',),
        }
        with patch.dict('sifter.mailsifter.accessors.settings.MAILSIFTER',
                        mock_settings_1):
            self.msg.attach(self.application)
            attachment = accessors.get_first_attachment(self.msg)
            self.assertIsNotNone(attachment)


class GetAttachmentsTestCase(MailHelperTestCase):
    """
    Tests the get_attachments function.
    """
    date = datetime.date(year=2016, month=12, day=10)

    def test_attachments(self):
        """
        Tests the get_attachments function for an attachment.
        """
        self.msg.attach(self.pdf)
        self.msg.attach(self.image)
        actual = accessors.get_attachments(self.msg)
        expected = [self.pdf, self.image]
        self.assertEqual(actual, expected)

    def test_inline(self):
        """
        Tests the get_attachments function for inline content.
        """
        self.msg.attach(self.inline)
        self.msg.attach(self.pdf)
        actual = accessors.get_attachments(self.msg)
        expected = [self.pdf]
        self.assertEqual(actual, expected)

    def test_none(self):
        """
        Tests the get_attachments function for no attachment.
        """
        actual = accessors.get_attachments(self.msg)
        expected = []
        self.assertEqual(actual, expected)


class GetEmailValueTestCase(MailHelperTestCase):
    """
    Tests the get_email_value function.
    """

    def test_content(self):
        """
        Tests the get_email_value function for the 'Content' field.
        """
        self.msg.attach(self.part1)
        self.msg.attach(self.part2)
        actual = accessors.get_email_value('Content', self.msg)
        expected = self.text
        self.assertEqual(actual, expected)

    def test_date(self):
        """
        Tests the get_email_value function for the 'Date' field.
        """
        actual = accessors.get_email_value('Date', self.msg)
        expected = '2015-09-08T16:08:59-04:00'
        self.assertEqual(actual, expected)

    def test_subject(self):
        """
        Tests the get_email_value function for the 'Subject' field.
        """
        actual = accessors.get_email_value('Subject', self.msg)
        expected = self.msg['Subject']
        self.assertEqual(actual, expected)

    def test_attachment(self):
        """
        Tests the get_email_value function for the 'Attachment' field.
        """
        self.msg.attach(self.image)
        self.msg.attach(self.pdf)
        actual = accessors.get_email_value('Attachment', self.msg)
        expected = self.image
        self.assertEqual(actual, expected)

    def test_attachments(self):
        """
        Tests the get_email_value function for the 'Attachments' field.
        """
        self.msg.attach(self.image)
        self.msg.attach(self.pdf)
        actual = accessors.get_email_value('Attachments', self.msg)
        expected = [self.image, self.pdf]
        self.assertEqual(actual, expected)

    def test_no_attachment(self):
        """
        Tests the get_email_value function for the 'Attachment' field
        when there is no attachment.
        """
        actual = accessors.get_email_value('Attachment', self.msg)
        expected = None
        self.assertEqual(actual, expected)

    def test_no_attachments(self):
        """
        Tests the get_email_value function for the 'Attachments' field
        when there are no attachments.
        """
        actual = accessors.get_email_value('Attachments', self.msg)
        expected = []
        self.assertEqual(actual, expected)

    def test_other_field(self):
        """
        Tests the get_email_value function for an email field that is
        not Content, Date, or Subject.
        """
        actual = accessors.get_email_value('Message-ID', self.msg)
        expected = self.msg['Message-ID']
        self.assertEqual(actual, expected)

    def test_bad_field(self):
        """
        Tests the get_email_value function for a field that doesn't exist.
        """
        actual = accessors.get_email_value('foo', self.msg)
        expected = ''
        self.assertEqual(actual, expected)

    def test_decode_error(self):
        """
        Tests the get_email_value function when a UnicodeDecodeError is
        raised.
        """
        error = UnicodeDecodeError('funnycodec', b'\x00\x00', 1, 2,
                                   'Something went wrong!')
        with patch('sifter.mailsifter.accessors.bleach.clean',
                   side_effect=error):
            with LogCapture() as log_capture:
                actual = accessors.get_email_value('Subject', {'Subject': 'test'})
                expected = 'The Subject of this email could not be displayed ' + \
                           'due to an error.'
                self.assertEqual(actual, expected)

                msg = ('An error was encountered while parsing the '
                       'Subject field of an email.')
                log_capture.check(
                    ('sifter.mailsifter.accessors', 'ERROR', msg),
                )

