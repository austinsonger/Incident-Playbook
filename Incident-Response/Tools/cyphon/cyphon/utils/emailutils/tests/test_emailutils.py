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

# standard library
import os
from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# local
from utils.emailutils.emailutils import emails_enabled, embed_image


class EmailsEnabledTestCase(TestCase):
    """
    Tests the emails_enabled function.
    """

    @patch('utils.emailutils.emailutils.config')
    def test_setting_is_true(self, mock_config):
        """
        Tests the emails_enabled function when the Constance config is
        True.
        """
        mock_config.EMAIL_NOTIFICATIONS_ENABLED = True
        self.assertTrue(emails_enabled())

    @patch('utils.emailutils.emailutils.config')
    def test_setting_is_false(self, mock_config):
        """
        Tests the emails_enabled function when the Constance config is
        False.
        """
        mock_config.EMAIL_NOTIFICATIONS_ENABLED = False
        self.assertFalse(emails_enabled())

    @patch('utils.emailutils.emailutils.config')
    def test_setting_does_not_exist(self, mock_config):
        """
        Tests the emails_enabled function when the Constance config
        doesn't exist.
        """
        del mock_config.EMAIL_NOTIFICATIONS_ENABLED
        self.assertEqual(emails_enabled(), True)


class EmbedImageTestCase(TestCase):
    """
    Tests the embed_image function.
    """

    def setUp(self):
        self.msg = EmailMultiAlternatives(
            subject='foobar',
            body='foobar',
            to=['sender@email.com'],
            from_email=settings.DEFAULT_FROM_EMAIL
        )

    def test_attach_image(self):
        """
        Tests the embed_image function.
        """
        dir_path = os.path.join(settings.PROJ_DIR, 'cyphon/static/images/')
        file_name = 'cyphon-sm.png'
        msg = embed_image(self.msg, dir_path, file_name)

        msg_dict = vars(msg)
        img_dict = vars(msg_dict['attachments'][0])

        self.assertEqual(msg_dict['mixed_subtype'], 'related')
        self.assertEqual(img_dict['_headers'][0],
                         ('Content-Type', 'image/png'))
        self.assertEqual(img_dict['_headers'][3],
                         ('Content-ID', '<%s>' % file_name))
