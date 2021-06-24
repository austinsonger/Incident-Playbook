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
Tests the services of the sifter.mail package
"""

# standard library
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TestCase


class MailHelperTestCase(TestCase):
    """
    Base class for testing mail helper functions.
    """
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = '<html><head></head><body><p>Hi!<br>How are you?<br>Here ' + \
           'is the <a href="https://www.python.org">link</a> you wanted.</p></html>'
    uuid = 'ef739cc0fe5748fd9dabd832f9b3eac4'

    def setUp(self):
        self.msg = MIMEMultipart('alternative')
        self.msg['Date'] = 'Tue, 8 Sep 2015 16:08:59 -0400'
        self.msg['Subject'] = 'Link'
        self.msg['From'] = 'my@email.com'
        self.msg['To'] = 'your@email.com'
        self.msg['Message-ID'] = 'NM615AA6A517B60AA16@email.com'
        self.part1 = MIMEText(self.text, 'plain')
        self.part2 = MIMEText(self.html, 'html')

        self.javascript_file = 'test.js'
        self.javascript = MIMEText('mock_js_payload', 'plain')
        self.javascript['Content-Disposition'] = 'attachment; filename=' + self.javascript_file

        self.java_file = 'test.jar'
        self.java = MIMEApplication('', 'java')
        self.java['Content-Disposition'] = 'attachment; filename=' + self.java_file

        self.application = MIMEApplication('')
        self.application['Content-Disposition'] = 'attachment; filename=' + self.java_file

        self.text_file = 'test.txt'
        self.text_attach = MIMEText('mock_txt_payload', 'plain')
        self.text_attach['Content-Disposition'] = 'attachment; filename=' + self.text_file

        self.image_file = 'test.jpeg'
        self.image_payload = 'mock_jpeg_payload'
        self.image = MIMEImage(self.image_payload, 'jpeg')
        self.image['Content-Disposition'] = 'attachment; filename=' + self.image_file

        self.pdf_file = 'test.pdf'
        self.inline = MIMEImage('mock_pdf_payload', 'jpeg')
        self.pdf = MIMEApplication('', 'pdf')
        self.pdf['Content-Disposition'] = 'attachment; filename=' + self.pdf_file

        self.inline_file = 'test.jpeg'
        self.inline = MIMEImage('mock_jpeg_payload', 'jpeg')
        self.inline['Content-Disposition'] = 'inline; filename=' + self.inline_file

        self.mock_settings = Mock()
        self.mock_settings.BASE_URL = 'https://www.example.com/'
        self.mock_settings.MEDIA_ROOT = os.path.dirname(__file__)
        self.mock_settings.MEDIA_URL = '/media/'
        self.mock_settings.HOSTNAME = 'example.com'
        self.mock_mailsifter_settings = {
            'ATTACHMENTS_FOLDER': 'test-attachments/',
            'ALLOWED_EMAIL_ATTACHMENTS': ('text/plain', 'application/pdf', 'image/jpeg', 'image/png'),
            'ALLOWED_FILE_EXTENSIONS': ('.txt', '.pdf', '.jpeg', '.jpg', '.png')
        }

