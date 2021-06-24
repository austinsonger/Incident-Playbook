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
Tests the attchement helper functions of the mailsifter package.
"""

# standard library
import datetime
import os
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.conf import settings
from testfixtures import LogCapture

# local
from companies.models import Company
from sifter.mailsifter.accessors import get_first_attachment
from sifter.mailsifter import attachments
from tests.fixture_manager import get_fixtures
from .base import MailHelperTestCase


class MailAttachmentTestCase(MailHelperTestCase):
    """
    Tests the get_file_name helper function.
    """
    fixtures = get_fixtures(['companies'])

    date = datetime.date(year=2016, month=12, day=10)

    def setUp(self):
        super(MailAttachmentTestCase, self).setUp()
        self.company = Company.objects.get(pk=1)


class GetFileName(MailAttachmentTestCase):
    """
    Tests the get_file_name helper function.
    """

    def test_get_file_name(self):
        """
        Tests the get_file_name function.
        """
        mock_uuid = Mock()
        mock_uuid.hex = self.uuid

        with patch('sifter.mailsifter.attachments.uuid.uuid4',
                   return_value=mock_uuid):
            actual = attachments.get_file_name()
            expected = self.uuid
            self.assertEqual(actual, expected)


class GetExtension(MailAttachmentTestCase):
    """
    Tests the get_extension helper function.
    """

    def test_no_filename_guessable(self):
        """
        Tests the get_extension function when no file name is present
        but the extension is guessable from the Content-Type.
        """
        self.image['Content-Disposition'] = 'attachment;'
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        actual = attachments.get_extension(attachment)
        expected = '.jpeg'
        self.assertEqual(actual, expected)

    def test_extension_is_empty_str(self):
        """
        Tests the get_extension function when the file name is an empty string
        but the extension is guessable from the Content-Type.
        """
        self.part1['Content-Disposition'] = 'attachment; filename=""'
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        actual = attachments.get_extension(attachment)
        expected = '.jpeg'
        self.assertEqual(actual, expected)

    def test_extension_is_none(self):
        """
        Tests the get_extension function when the file name has no extension
        but the extension is guessable from the Content-Type.
        """
        self.image['Content-Disposition'] = 'attachment; filename="profile_pic"'
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        actual = attachments.get_extension(attachment)
        expected = '.jpeg'
        self.assertEqual(actual, expected)

    def test_extension_not_guessable(self):
        """
        Tests the get_extension function when no file name is present
        and the extension is not guessable.
        """
        self.image['Content-Disposition'] = 'attachment; filename=""'
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        attachment.get_filename = Mock(return_value=None)
        with patch('sifter.mailsifter.attachments.mimetypes') as mock_mimetypes:
            mock_mimetypes.guess_extension = Mock(return_value=None)
            actual = attachments.get_extension(attachment)
            expected = '.bin'
            self.assertEqual(actual, expected)


class GetRawDirectoryPath(MailAttachmentTestCase):
    """
    Tests the get_raw_directory_path helper function.
    """

    def test_with_company(self):
        """
        Tests the get_raw_directory_path function when a Company is given.
        """
        self.mock_mailsifter_settings['ATTACHMENTS_FOLDER'] = 'attachments/%Y/%m/%d/'
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            actual = attachments.get_raw_directory_path(self.company)
            expected = '2d6f5a38306a40f3a5e14fc38a425531/'\
                       'attachments/%Y/%m/%d/'
            self.assertEqual(actual, expected)

    def test_without_company(self):
        """
        Tests the get_raw_directory_path function when a Company is not given.
        """
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            actual = attachments.get_raw_directory_path()
            expected = self.mock_mailsifter_settings['ATTACHMENTS_FOLDER']
            self.assertEqual(actual, expected)


class GetAttachmentPath(MailAttachmentTestCase):
    """
    Tests the get_attachment_path helper function.
    """

    def test_get_attachment_path(self):
        """
        Tests the get_attachment_path function when the path contains
        date variables.
        """
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            with patch('sifter.mailsifter.attachments.settings',
                       self.mock_settings):
                actual = attachments.get_attachment_path('attachments/')
                expected = os.path.join(os.path.dirname(__file__),
                                        'attachments/')
                self.assertEqual(actual, expected)


class GetAttachmentUrl(MailAttachmentTestCase):
    """
    Tests the get_attachment_url helper function.
    """

    def get_attachment_url_dup_slashes(self):
        """
        Tests the get_attachment_url function with redundant slashes.
        """
        mock_settings = Mock()
        mock_settings.BASE_URL = 'https://www.example.com/'
        mock_settings.MEDIA_URL = '/media/'
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        return_value=self.mock_mailsifter_settings):
            with patch('sifter.mailsifter.attachments.settings',
                       self.mock_settings):
                actual = attachments.get_attachment_url('/attachments/')
                expected = 'https://www.example.com/media/attachments/'
                self.assertEqual(actual, expected)

    def get_attachment_url_no_slashes(self):
        """
        Tests the get_attachment_url function with no slashes.
        """
        mock_settings = Mock()
        mock_settings.BASE_URL = 'https://www.example.com'
        mock_settings.MEDIA_URL = 'media'
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        return_value=self.mock_mailsifter_settings):
            with patch('sifter.mailsifter.attachments.settings',
                       self.mock_settings):
                actual = attachments.get_attachment_url('attachments')
                expected = 'https://www.example.com/media/attachments/'
                self.assertEqual(actual, expected)


class GetDirectoryPath(MailAttachmentTestCase):
    """
    Tests the get_directory_path helper function.
    """

    def test_with_company_and_date(self):
        """
        Tests the get_directory_path function when the path contains
        date variables.
        """
        with patch('sifter.mailsifter.attachments.datetime') as mock_datetime:
            mock_datetime.utcnow = Mock(return_value=self.date)
            with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                            return_value=self.mock_mailsifter_settings):
                self.mock_settings.ATTACHMENTS_FOLDER = 'attachments/%Y/%m/%d/'
                actual = attachments.get_directory_path(self.company)
                expected = '2d6f5a38306a40f3a5e14fc38a425531/attachments/2016/12/10/'
                self.assertEqual(actual, expected)

    def test_without_date_or_company(self):
        """
        Tests the get_directory_path function withuot a company and
        when the path does not contain date variables.
        """
        with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            actual = attachments.get_directory_path()
            expected = 'test-attachments/'
            self.assertEqual(actual, expected)


class GetFilePath(MailAttachmentTestCase):
    """
    Tests the get_file_path helper function.
    """

    def test_allowed_file(self):
        """
        Tests the get_file_path function for an allowed file type.
        """
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        mock_uuid = Mock()
        mock_uuid.hex = self.uuid
        with patch('sifter.mailsifter.attachments.uuid.uuid4',
                   return_value=mock_uuid):
            with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                            self.mock_mailsifter_settings):
                actual = attachments.get_file_path(attachment, self.company)
                expected = '%s/test-attachments/%s.jpeg' \
                           % (self.company.uuid.hex, self.uuid)
                self.assertEqual(actual, expected)

    def test_unallowed_file(self):
        """
        Tests the get_file_path function for an unallowed file type.
        """
        self.mock_mailsifter_settings['ALLOWED_EMAIL_ATTACHMENTS'] = ('application/java',)
        with patch.dict('sifter.mailsifter.accessors.settings.MAILSIFTER',
                        self.mock_mailsifter_settings):
            self.msg.attach(self.java)
            attachment = get_first_attachment(self.msg)
            with patch('sifter.mailsifter.attachments.settings',
                       return_value=self.mock_settings):
                with LogCapture() as log_capture:
                    actual = attachments.get_file_path(attachment)
                    expected = None
                    self.assertEqual(actual, expected)
                    msg = 'The attachment %s is not an allowed file type' \
                          % self.java_file
                    log_capture.check(
                        ('sifter.mailsifter.attachments', 'WARNING', msg),
                    )


class GetAttachmentContent(MailAttachmentTestCase):
    """
    Tests the get_attachment_content helper function.
    """

    def test_get_attachment_content(self):
        """
        Tests the get_attachment_content function.
        """
        self.msg.attach(self.image)
        attachment = get_first_attachment(self.msg)
        actual = attachments.get_attachment_content(attachment)
        expected = bytearray(self.image_payload, encoding='utf-8')
        self.assertEqual(actual, expected)


class SaveAttachmentContent(MailAttachmentTestCase):
    """
    Tests the save_attachment helper function.
    """

    def setUp(self):
        super(SaveAttachmentContent, self).setUp()
        self.company = Company.objects.get(pk=1)
        self.mock_settings.MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, 'tmp')

    def test_save_attachment(self):
        """
        Tests the save_attachment function.
        """
        mock_uuid = Mock()
        mock_uuid.hex = self.uuid
        self.msg.attach(self.text_attach)
        attachment = get_first_attachment(self.msg)

        with patch('sifter.mailsifter.attachments.uuid.uuid4',
                   return_value=mock_uuid):
            with patch.dict('sifter.mailsifter.attachments.settings.MAILSIFTER',
                            self.mock_mailsifter_settings):
                with patch('sifter.mailsifter.attachments.settings',
                           self.mock_settings):

                    file_path = attachments.get_file_path(attachment)
                    full_path = attachments.get_attachment_path(file_path)

                    # check that the test file doesn't already exist
                    error_msg = 'Please delete the test file %s' % full_path
                    assert not os.path.isfile(full_path), error_msg

                    actual = attachments.save_attachment(attachment)
                    expected = 'https://www.example.com/media/test-attachments/'\
                               'ef739cc0fe5748fd9dabd832f9b3eac4.txt'

                    # check that the test file was created
                    self.assertIs(os.path.isfile(full_path), True)

                    # clean up the test file before further tests
                    os.remove(full_path)

                    self.assertEqual(actual, expected)

    def test_no_file_path(self):
        """
        Tests the save_attachment function.
        """
        mock_settings_1 = {
            'ALLOWED_EMAIL_ATTACHMENTS': ('application/java',)
        }
        with patch.dict('sifter.mailsifter.accessors.settings.MAILSIFTER',
                        mock_settings_1):
            self.msg.attach(self.java)
            attachment = get_first_attachment(self.msg)
            with patch('sifter.mailsifter.attachments.settings',
                       self.mock_settings):
                with LogCapture() as log_capture:
                    actual = attachments.save_attachment(attachment)
                    expected = None
                    self.assertEqual(actual, expected)
                    msg = 'The attachment %s is not an allowed file type' \
                          % self.java_file
                    log_capture.check(
                        ('sifter.mailsifter.attachments', 'WARNING', msg),
                    )
