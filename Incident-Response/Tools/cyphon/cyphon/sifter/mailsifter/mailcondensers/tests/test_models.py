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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import re

# third party
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
import six

# local
from bottler.bottles.models import BottleField
from sifter.mailsifter.accessors import get_content
from sifter.condensers.tests.mixins import CondenserTestCaseMixin, \
    FittingTestCaseMixin
from sifter.mailsifter.mailcondensers.models import (
    MailParser,
    MailCondenser,
    MailFitting,
)
from tests.fixture_manager import get_fixtures


class MailCondenserBaseTestCase(TestCase):
    """
    Base class for testing the MailCondensers app.
    """

    fixtures = get_fixtures(['mailcondensers'])

    msg_content = \
        """
        Customer:    Acme Supply Company
        Status:      Open
        Threat:      Medium
        Class:       application-attack
        Start Date:  Apr 2 2015 10:15am GMT
        End Date:    Apr 2 2015 10:15am GMT

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php

        <SCRIPT>document.write("<SCR =C2=BB I");</SCRIPT>PT =C2=BB SRC=3D"
http://ha.ckers.org/xss =C2=BB .js"></SCRIPT>"""

    def _create_example_msg(self):
        """
        Helper method that returns an example email message.
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Link"
        msg['From'] = "sender@email.com"
        msg['To'] = "recipient@email.com"

        text = self.msg_content
        html = """\
        <html>
          <head></head>
          <body>
            <div>
               self.msg_content
            </div>
          </body>
        </html>
        """
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        return msg

    def setUp(self):
        self.msg = self._create_example_msg()


class MailParserTestCase(MailCondenserBaseTestCase):
    """
    Tests the MailParser class.
    """

    def test_count_no_matches(self):
        """
        Tests the parse method for a 'count' method when a string has no
        matches.
        """
        parser = MailParser(
            source_field='Content',
            method='COUNT',
            regex='Bad Robots'
        )
        result = parser.process(self.msg)
        self.assertEqual(result, 0)

    def test_count_multi_matches(self):
        """
        Tests the parse method for a 'count' method when a string has
        multiple matches.
        """
        parser = MailParser(
            source_field='Content',
            method='COUNT',
            regex='Bad Bots'
        )
        result = parser.process(self.msg)
        self.assertEqual(result, 2)

    def test_presence_true(self):
        """
        Tests the parse method for a 'presence' method when a string has a
        match.
        """
        parser = MailParser(
            source_field='Content',
            method='P/A',
            regex='Bad Bots'
        )
        result = parser.process(self.msg)
        self.assertTrue(result)

    def test_presence_false(self):
        """
        Tests the parse method for a 'presence' method when a string has no
        match.
        """
        parser = MailParser(
            source_field='Content',
            method='P/A',
            regex='Bad Robots'
        )
        result = parser.process(self.msg)
        self.assertFalse(result)

    def test_value_match(self):
        """
        Tests the parse method for a 'value' method when a string has a
        match.
        """
        parser = MailParser(
            source_field='Content',
            method='SUBSTRING',
            regex='Threat:\s*(\w+)\n'
        )
        result = parser.process(self.msg)
        self.assertEqual(result, 'Medium')

    def test_value_no_match(self):
        """
        Tests the parse method for a 'value' method when a string has no
        match.
        """
        parser = MailParser(
            source_field='Content',
            method='SUBSTRING',
            regex='Threats:\s*(\w+)\n'
        )
        result = parser.process(self.msg)
        self.assertEqual(result, None)

    def test_sanitize(self):
        """
        Makes sure the _get_values method strips malicious code.
        """
        parser = MailParser(
            source_field='Content',
            method='COPY',
            regex='Bad Robots'
        )
        assert 'SCRIPT' in str(get_content(self.msg))
        result = parser.process(self.msg)
        self.assertFalse(re.search('SCRIPT', str(result), re.IGNORECASE))

    # TODO(LH) need to improve santizer tests


class MailCondenserTestCase(MailCondenserBaseTestCase, CondenserTestCaseMixin):
    """
    Tests the MailCondenser class.
    """

    @classmethod
    def setUpClass(cls):
        super(MailCondenserTestCase, cls).setUpClass()
        cls.condenser = MailCondenser.objects.get(name='post')

    def test_str(self):
        """
        Tests the __str__ method of the MailCondenser class.
        """
        self.assertEqual(str(self.condenser), 'post')

    def test_process(self):
        """
        Tests the process method of the MailCondenser class.
        """
        with patch('sifter.mailsifter.mailcondensers.models.MailParser.process',
                   return_value='some text'):
            actual = self.condenser.process({'Content': 'example text'})
            expected = {
                'content': {
                    'date': 'some text',
                    'from': 'some text',
                    'body': 'some text',
                    'subject': 'some text'
                }
            }
            for item in actual:
                self.assertEqual(actual[item], expected[item])


class MailFittingTestCase(MailCondenserBaseTestCase, FittingTestCaseMixin):
    """
    Tests the MailFitting class.
    """

    @classmethod
    def setUpClass(cls):
        super(MailFittingTestCase, cls).setUpClass()
        cls.parser_fitting = MailFitting.objects.get(pk=4)
        cls.condenser_fitting = MailFitting.objects.get(pk=5)
        cls.parser_type = ContentType.objects.get(app_label='mailcondensers',
                                                  model='mailparser')
        cls.condenser_type = ContentType.objects.get(app_label='mailcondensers',
                                                     model='mailcondenser')
        cls.condenser = MailCondenser.objects.get(name='post')

    def setUp(self):
        super(MailFittingTestCase, self).setUp()
        self.condenser = MailCondenser.objects.get(name='post')

    def test_invalid_target_field(self):
        """
        Tests that a validation error is raised if the target_field is not
        present in the Bottle associated with the Fitting's Condenser.
        """
        field = BottleField.objects.get_by_natural_key('subject')
        fitting = MailFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=2,
            content_type=self.parser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'The selected '
                                   'target field is not compatible with the '
                                   'condenser\'s bottle.'):
            fitting.clean()

    def test_target_is_not_embebbed_doc(self):
        """
        Tests that a validation error is raised if the target field is not an
        EmbeddedDocument and the content type is a Condenser.
        """
        field = BottleField.objects.get_by_natural_key('location')
        fitting = MailFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=2,
            content_type=self.condenser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'Unless the '
                                   'target field is an EmbeddedDocument, '
                                   'the content type must be a parser.'):
            fitting.clean()

    def test_fitting_is_not_condenser(self):
        """
        Tests that a validation error is raised if the target field is an
        EmbeddedDocument and the content type is not a Condenser.
        """
        field = BottleField.objects.get_by_natural_key('content')
        fitting = MailFitting(
            condenser=self.condenser,
            target_field=field,
            object_id=3,
            content_type=self.parser_type
        )

        with six.assertRaisesRegex(self, ValidationError, 'If the '
                                   'target field is an EmbeddedDocument, '
                                   'the content type must be a condenser.'):
            fitting.clean()

    def test_target_field_name(self):
        """
        Tests the field_name property.
        """
        self.assertEqual(self.parser_fitting.target_field_name, 'body')

    def test_target_field_type(self):
        """
        Tests the field_type property.
        """
        self.assertEqual(self.parser_fitting.target_field_type, 'TextField')

    def test_process(self):
        """
        Tests the process method.
        """
        self.maxDiff = None
        actual = self.parser_fitting.process(self.msg)
        expected = \
"""
        Customer:    Acme Supply Company
        Status:      Open
        Threat:      Medium
        Class:       application-attack
        Start Date:  Apr 2 2015 10:15am GMT
        End Date:    Apr 2 2015 10:15am GMT

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php

        Bad Bots

        *URL: * /blog/wp-admin/admin-ajax.php(GET)
        *Query string: * ?action=3Drevslider_show_image.php
        *Attempted on: *URL
        *Threat pattern: *dunbararmored.com/blog/wp-admin/admin-ajax.php

        document.write("&lt;SCR =C2=BB I");PT =C2=BB SRC=3D"
http://ha.ckers.org/xss =C2=BB .js"&gt;"""

        self.assertEqual(actual, expected)
