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
Functional tests for the MailCondenser app.
"""

# standard library
import logging
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from testfixtures import LogCapture

# local
from bottler.bottles.models import BottleField
from tests.fixture_manager import get_fixtures
from sifter.condensers.tests.functional_tests import \
    CondenserFunctionalTest, FittingFunctionalTest
from sifter.mailsifter.mailcondensers.models import MailCondenser

LOGGER = logging.getLogger(__name__)

TEST_DOC = \
"""
Date: Mon, 18 Apr 2016 10:39:14 +0000 (UTC)
From: sender@email.com
To: "recipient@email.com" <recipient@email.com>
Subject: the meaning of life
MIME-Version: 1.0
Content-Type: multipart/mixed;
    boundary="----=_Part_18598_984397735.1460975954577"
X-Original-Sender: no_reply@example.com


------=_Part_18598_984397735.1460975954577
Content-Type: text/html; charset=UTF-8
Content-Transfer-Encoding: quoted-printable
<html>
  <head></head>
  <body>
    <div>The answer is 42.</div>
  </body>
</html>
------=_Part_18598_984397735.1460975954577--

# """


class AddMailFittingFunctionalTest(FittingFunctionalTest):
    """
    Tests the MailFitting admin page.
    """
    fixtures = get_fixtures(['mailcondensers'])

    url = '/admin/mailcondensers/mailfitting/add/'

    def test_add_fitting(self):
        """
        Tests autocomplete features on the Add MailFitting admin page.
        """
        condenser_href = self.live_server_url + '/admin/mailcondensers/mailcondenser/?'
        parser_href = self.live_server_url + '/admin/mailcondensers/mailparser/?'

        # make sure default content_type is 'mail parser'
        self.assertEqual(self.page.content_type, 'mail parser')
        self.assertEqual(self.page.lookup, parser_href)

        # make sure target_field options are filtered
        self.assertEqual(self.page.target_field.count(), 0)
        self.page.condenser = 'post'
        self.assertEqual(self.page.target_field.count(), 3)

        # select a condenser target_field
        field = BottleField.objects.get_by_natural_key('user')
        self.page.target_field.select(field.pk)

        # make sure content_type changes
        self.assertEqual(self.page.content_type, 'mail condenser')

        # make sure the generic relation link has changed
        self.assertEqual(self.page.lookup, condenser_href)

        # make sure target_field options change when condenser changes
        self.page.target_field.delete()
        self.page.condenser = 'mail'
        self.assertEqual(self.page.target_field.count(), 1)

        # select a different target_field that's not an EmbeddedDocument
        field = BottleField.objects.get_by_natural_key('priority')
        self.page.target_field.select(field.pk)

        # check that 'mail parser' is automatically selected
        self.assertEqual(self.page.content_type, 'mail parser')
        self.assertEqual(self.page.lookup, parser_href)


class AddMailCondenserFunctionalTest(CondenserFunctionalTest):
    """
    Tests the MailCondenser admin page.
    """
    fixtures = get_fixtures(['mailcondensers'])

    url = '/admin/mailcondensers/mailcondenser/add/'

    def test_filtering_and_autocomplete(self):
        """
        Tests the behavior of the select and input elements.
        """
        condenser_href = self.live_server_url + '/admin/mailcondensers/mailcondenser/?'
        parser_href = self.live_server_url + '/admin/mailcondensers/mailparser/?'

        self.page.scroll_to_bottom()

        # make sure default content_type is 'mail parser'
        self.assertEqual(self.page.content_type_0, 'mail parser')
        self.assertEqual(self.page.lookup_0, parser_href)

        # make sure target_field options are filtered
        self.assertEqual(self.page.target_field_0.count(), 0)
        self.page.bottle = 'post'
        self.assertEqual(self.page.target_field_0.count(), 4)

        # select a condenser target_field
        field = BottleField.objects.get_by_natural_key('content')
        self.page.target_field_0.select(field.pk)

        # make sure content_type changes
        self.assertEqual(self.page.content_type_0, 'mail condenser')
        self.assertEqual(self.page.lookup_0, condenser_href)

        self.page.add_fitting()

        # check that previously selected target_field has the been removed from
        # the options list
        self.assertEqual(self.page.target_field_1.count(), 3)

        # check that the deleted target field has reappeared as an option
        self.page.target_field_0.delete()
        self.assertEqual(self.page.target_field_1.count(), 4)

        # make sure target_field options change when bottle changes
        self.page.bottle = '---------'
        self.assertEqual(self.page.target_field_0.count(), 0)
        self.page.bottle = 'mail'
        self.assertEqual(self.page.target_field_0.count(), 5)

        # select a different target_field that's not an EmbeddedDocument
        field = BottleField.objects.get_by_natural_key('priority')
        self.page.target_field_0.select(field.pk)

        # check that 'mail parser' is automatically selected
        self.assertEqual(self.page.content_type_0, 'mail parser')
        self.assertEqual(self.page.lookup_0, parser_href)

    def test_config_tool(self):
        """
        Tests the configuration test tool on a new MailCondenser.
        """
        self.page.config_test_value = TEST_DOC

        actual = self.page.run_test()
        expected = 'Sorry! The following fields contained errors:' + \
                   '\n\n\tbottle: This field is required.' + \
                   '\n\tname: This field is required.' + \
                   '\n\nPlease correct these errors and try again.'
        self.assertEqual(actual, expected)

        self.page.name = 'test_bottle'
        actual = self.page.run_test()
        expected = 'Sorry! The following fields contained errors:' + \
                   '\n\n\tbottle: This field is required.' + \
                   '\n\nPlease correct these errors and try again.'
        self.assertEqual(actual, expected)

        self.page.bottle = 'mail'
        actual = self.page.run_test()
        expected = 'Sorry! The following fields contained errors:' + \
                   '\n\n\tfittings-0-object_id: This field is required.' + \
                   '\n\tfittings-0-target_field: This field is required.' + \
                   '\n\nPlease correct these errors and try again.'
        self.assertEqual(actual, expected)

        self.page.scroll_to_bottom()
        field = BottleField.objects.get_by_natural_key('body')
        self.page.target_field_0.select(field.pk)
        self.page.object_id_0 = '4'
        actual = self.page.run_test()
        expected = '{\n    "body": "   The answer is 42."\n}'
        self.assertEqual(actual, expected)


class ChangeMailCondenserConfigToolTest(CondenserFunctionalTest):
    """
    Tests the configuration test tool on the Change MailCondenser admin page.
    """
    fixtures = get_fixtures(['mailcondensers'])

    url = '/admin/mailcondensers/mailcondenser/1/change/'

    test_doc = TEST_DOC

    def test_invalid_form(self):
        """
        Tests the configuration test tool when the form is invalid.
        """
        self.page.add_fitting()
        self.page.config_test_value = self.test_doc
        actual = self.page.run_test()
        expected = 'Sorry! The following fields contained errors:' + \
                   '\n\n\tfittings-4-object_id: This field is required.' + \
                   '\n\tfittings-4-target_field: This field is required.' + \
                   '\n\nPlease correct these errors and try again.'
        self.assertEqual(actual, expected)

    def test_valid_form(self):
        """
        Tests the configuration test tool when no errors are raised.
        """
        self.page.config_test_value = self.test_doc
        actual = self.page.run_test()
        expected = \
"""{
    "body": "   The answer is 42.",
    "date": "2016-04-18T10:39:14+00:00",
    "from": "'' sender@email.com",
    "subject": "the meaning of life"
}"""
        self.assertEqual(actual, expected)

    def test_change_and_rollback(self):
        """
        Tests that changes to the object are reflected in the test
        results but are not saved.
        """
        # save the original state of the condenser for comparison
        orig_obj = MailCondenser.objects.get(pk=1)

        self.page.delete_fitting()
        self.page.config_test_value = self.test_doc
        actual = self.page.run_test()
        expected = \
"""{
    "body": "   The answer is 42.",
    "date": "2016-04-18T10:39:14+00:00",
    "subject": "the meaning of life"
}"""
        self.assertEqual(actual, expected)

        # make sure the fitting we deleted for the test still belongs
        # to the condenser (i.e., mailbase changes were rollbacked)
        updated_obj = MailCondenser.objects.get(pk=1)
        self.assertEqual(orig_obj.fittings.count(),
                         updated_obj.fittings.count())

    def test_integrity_error(self):
        """
        Tests the configuration test tool when an IntegrityError is raised.
        """
        self.page.config_test_value = 'test text'

        with patch('django.forms.ModelForm.save',
                   side_effect=IntegrityError('foo')):
            with LogCapture('cyphon.admin') as log_capture:

                actual = self.page.run_test()
                expected = "Could not create an object for testing: foo"
                self.assertEqual(actual, expected)

                msg = 'An error occurred while creating a test instance: ' + \
                      '<WSGIRequest: POST ' + \
                      "'/admin/mailcondensers/mailcondenser/1/change/test/'>"
                log_capture.check(
                    ('cyphon.admin', 'ERROR', msg),
                )

    def test_validation_error(self):
        """
        Tests the configuration test tool when a ValidationError is raised.
        """
        self.page.config_test_value = 'test text'

        with patch(
            'sifter.mailsifter.mailcondensers.admin.MailCondenserAdmin._get_result',
            side_effect=ValidationError('foo')):
            with LogCapture('cyphon.admin') as log_capture:

                actual = self.page.run_test()
                expected = "A validation error occurred: ['foo']"
                self.assertEqual(actual, expected)

                msg = 'An error occurred while initializing a config test: ' + \
                      '<WSGIRequest: POST ' + \
                      "'/admin/mailcondensers/mailcondenser/1/change/test/'>"
                log_capture.check(
                    ('cyphon.admin', 'ERROR', msg),
                )

