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
Functional tests for the DataCondenser app.
"""

# standard library
import json
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
from sifter.datasifter.datacondensers.models import DataCondenser

LOGGER = logging.getLogger(__name__)


class AddDataFittingFunctionalTest(FittingFunctionalTest):
    """
    Tests the DataFitting admin page.
    """
    fixtures = get_fixtures(['datacondensers'])

    url = '/admin/datacondensers/datafitting/add/'

    def test_add_fitting(self):
        """
        Tests autocomplete features on the Add DataFitting admin page.
        """
        condenser_href = self.live_server_url + '/admin/datacondensers/datacondenser/?'
        parser_href = self.live_server_url + '/admin/datacondensers/dataparser/?'

        # make sure default content_type is 'data parser'
        self.assertEqual(self.page.content_type, 'data parser')
        self.assertEqual(self.page.lookup, parser_href)

        # make sure target_field options are filtered
        self.assertEqual(self.page.target_field.count(), 0)
        self.page.condenser = 'instagram__post'
        self.assertEqual(self.page.target_field.count(), 4)

        # select a condenser target_field
        field = BottleField.objects.get_by_natural_key('content')
        self.page.target_field.select(field.pk)

        # make sure content_type changes
        self.assertEqual(self.page.content_type, 'data condenser')

        # make sure the generic relation link has changed
        self.assertEqual(self.page.lookup, condenser_href)

        # make sure target_field options change when condenser changes
        self.page.target_field.delete()
        self.page.condenser = 'mail'
        self.assertEqual(self.page.target_field.count(), 5)

        # select a different target_field that's not an EmbeddedDocument
        field = BottleField.objects.get_by_natural_key('date')
        self.page.target_field.select(field.pk)

        # check that 'data parser' is automatically selected
        self.assertEqual(self.page.content_type, 'data parser')
        self.assertEqual(self.page.lookup, parser_href)


class AddDataCondenserFunctionalTest(CondenserFunctionalTest):
    """
    Tests the DataCondenser admin page.
    """
    fixtures = get_fixtures(['datacondensers'])

    url = '/admin/datacondensers/datacondenser/add/'

    def test_filtering_and_autocomplete(self):
        """
        Tests the behavior of the select and input elements.
        """
        condenser_href = self.live_server_url + '/admin/datacondensers/datacondenser/?'
        parser_href = self.live_server_url + '/admin/datacondensers/dataparser/?'

        self.page.scroll_to_bottom()

        # make sure default content_type is 'data parser'
        self.assertEqual(self.page.content_type_0, 'data parser')
        self.assertEqual(self.page.lookup_0, parser_href)

        # make sure target_field options are filtered
        self.assertEqual(self.page.target_field_0.count(), 0)
        self.page.bottle = 'post'
        self.assertEqual(self.page.target_field_0.count(), 4)

        # select a condenser target_field
        field = BottleField.objects.get_by_natural_key('content')
        self.page.target_field_0.select(field.pk)

        # make sure content_type changes
        self.assertEqual(self.page.content_type_0, 'data condenser')
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
        field = BottleField.objects.get_by_natural_key('date')
        self.page.target_field_0.select(field.pk)

        # check that 'data parser' is automatically selected
        self.assertEqual(self.page.content_type_0, 'data parser')
        self.assertEqual(self.page.lookup_0, parser_href)

    def test_config_tool(self):
        """
        Tests the configuration test tool on a new DataCondenser.
        """
        self.page.config_test_value = json.dumps({'text': 'test'})

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
        self.page.object_id_0 = '3'
        actual = self.page.run_test()
        expected = '{\n    "body": "test"\n}'
        self.assertEqual(actual, expected)


class ChangeDataCondenserConfigToolTest(CondenserFunctionalTest):
    """
    Tests the configuration test tool on the Change DataCondenser admin page.
    """
    fixtures = get_fixtures(['datacondensers'])

    url = '/admin/datacondensers/datacondenser/1/change/'

    test_doc = json.dumps({
        'id_str': '0123456',
        'text': 'this is an example post',
        'user': {
            'screen_name': 'zebrafinch'
        }
    })

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
    "content": {
        "image": null,
        "link": "https://twitter.com/zebrafinch/statuses/0123456",
        "text": "this is an example post"
    },
    "created_date": null,
    "location": null,
    "user": {
        "id": null,
        "link": "https://twitter.com/zebrafinch/",
        "name": null,
        "profile_pic": null,
        "screen_name": "zebrafinch"
    }
}"""
        self.assertEqual(actual, expected)

    def test_improper_format(self):
        """
        Tests the configuration test tool when the test_string is not
        valid JSON.
        """
        self.page.config_test_value = 'bad json'
        actual = self.page.run_test()
        expected = 'The test string is improperly formatted: ' + \
                   'Expecting value: line 1 column 1 (char 0)'
        self.assertEqual(actual, expected)

    def test_change_and_rollback(self):
        """
        Tests that changes to the object are reflected in the test
        results but are not saved.
        """
        # save the original state of the condenser for comparison
        orig_obj = DataCondenser.objects.get(pk=1)

        self.page.delete_fitting()
        self.page.config_test_value = self.test_doc
        actual = self.page.run_test()
        expected = \
"""{
    "content": {
        "image": null,
        "link": "https://twitter.com/zebrafinch/statuses/0123456",
        "text": "this is an example post"
    },
    "location": null,
    "user": {
        "id": null,
        "link": "https://twitter.com/zebrafinch/",
        "name": null,
        "profile_pic": null,
        "screen_name": "zebrafinch"
    }
}"""
        self.assertEqual(actual, expected)

        # make sure the fitting we deleted for the test still belongs
        # to the condenser (i.e., database changes were rollbacked)
        updated_obj = DataCondenser.objects.get(pk=1)
        self.assertEqual(orig_obj.fittings.count(),
                         updated_obj.fittings.count())

    def test_integrity_error(self):
        """
        Tests the configuration test tool when an IntegrityError is raised.
        """
        self.page.config_test_value = json.dumps({'text': 'test'})

        with patch('django.forms.ModelForm.save',
                   side_effect=IntegrityError('foo')):
            with LogCapture('cyphon.admin') as log_capture:

                actual = self.page.run_test()
                expected = "Could not create an object for testing: foo"
                self.assertEqual(actual, expected)

                msg = 'An error occurred while creating a test instance: ' + \
                      '<WSGIRequest: POST ' + \
                      "'/admin/datacondensers/datacondenser/1/change/test/'>"
                log_capture.check(
                    ('cyphon.admin', 'ERROR', msg),
                )

    def test_validation_error(self):
        """
        Tests the configuration test tool when a ValidationError is raised.
        """
        self.page.config_test_value = json.dumps({'text': 'test'})

        with patch(
            'sifter.datasifter.datacondensers.admin.DataCondenserAdmin._get_result',
            side_effect=ValidationError('foo')):
            with LogCapture('cyphon.admin') as log_capture:

                actual = self.page.run_test()
                expected = "A validation error occurred: ['foo']"
                self.assertEqual(actual, expected)

                msg = 'An error occurred while initializing a config test: ' + \
                      '<WSGIRequest: POST ' + \
                      "'/admin/datacondensers/datacondenser/1/change/test/'>"
                log_capture.check(
                    ('cyphon.admin', 'ERROR', msg),
                )

