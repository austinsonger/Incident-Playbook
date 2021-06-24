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
Tests the receiver module.
"""

# standard library
from collections import OrderedDict
import copy
import json
import logging
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TransactionTestCase
from testfixtures import LogCapture

# local
from cyphon.documents import DocumentObj
from receiver.receiver import create_doc_obj, process_msg, LOGGER
from tests.fixture_manager import get_fixtures

LOGGER.removeHandler('console')


class ProcessMsgTestCase(TransactionTestCase):
    """
    Tests the process_msg function.
    """

    fixtures = get_fixtures(['logchutes'])

    default_munger = 'default_log'

    mock_doc_obj = Mock()
    mock_channel = Mock()
    mock_method = Mock()
    mock_method.routing_key = 'logchutes'

    doc = {
        'message': 'foobar',
        '@uuid': '12345',
        'collection': 'elasticsearch.test_index.test_logs'
    }
    sorted_doc = OrderedDict(sorted(doc.items()))
    msg = bytes(json.dumps(sorted_doc), 'utf-8')
    decoded_msg = msg.decode('utf-8')

    def setUp(self):
        logging.disable(logging.ERROR)
        self.kwargs = {
            'channel': self.mock_channel,
            'method': self.mock_method,
            'properties': None,
            'body': self.msg
        }

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_create_doc_obj(self):
        """
        Tests the create_doc_obj function.
        """
        doc_obj = create_doc_obj(self.msg)
        expected_doc = copy.deepcopy(self.doc)
        expected_doc['_id'] = self.doc['@uuid']
        self.assertTrue(isinstance(doc_obj, DocumentObj))
        self.assertEqual(doc_obj.doc_id, self.doc['@uuid'])
        self.assertEqual(doc_obj.collection, self.doc['collection'])
        self.assertEqual(doc_obj.data, expected_doc)

    @patch('receiver.receiver.LogChute.objects.process')
    def test_process_msg_logchutes(self, mock_process):
        """
        Tests the process_msg function for LogChutes.
        """
        self.kwargs['method'].routing_key = 'logchutes'
        with patch('receiver.receiver.create_doc_obj',
                   return_value=self.mock_doc_obj) as mock_create:
            process_msg(**self.kwargs)
            mock_create.assert_called_once_with(self.decoded_msg)
            mock_process.assert_called_once_with(self.mock_doc_obj)

    @patch('receiver.receiver.DataChute.objects.process')
    def test_process_msg_datachutes(self, mock_process):
        """
        Tests the process_msg function for DataChutes.
        """
        self.kwargs['method'].routing_key = 'datachutes'
        with patch('receiver.receiver.create_doc_obj',
                   return_value=self.mock_doc_obj) as mock_create:
            process_msg(**self.kwargs)
            mock_create.assert_called_once_with(self.decoded_msg)
            mock_process.assert_called_once_with(self.mock_doc_obj)

    @patch('receiver.receiver.Watchdog.objects.process')
    def test_process_msg_watchdogs(self, mock_process):
        """
        Tests the process_msg function for Watchdogs.
        """
        self.kwargs['method'].routing_key = 'watchdogs'
        with patch('receiver.receiver.create_doc_obj',
                   return_value=self.mock_doc_obj) as mock_create:
            process_msg(**self.kwargs)
            mock_create.assert_called_once_with(self.decoded_msg)
            mock_process.assert_called_once_with(self.mock_doc_obj)

    def test_process_msg_exception(self):
        """
        Tests the process_msg function when an exception is raised.
        """
        logging.disable(logging.NOTSET)
        with patch('receiver.receiver.logging.getLogger', return_value=LOGGER):
            with patch('receiver.receiver.json.loads', side_effect=Exception('foo')):
                with LogCapture() as log_capture:
                    process_msg(**self.kwargs)
                    log_capture.check(
                        ('receiver',
                         'ERROR',
                         'An error occurred while processing the message \'{"@uuid": "12345", '
                         '"collection": "elasticsearch.test_index.test_logs", "message": '
                         '"foobar"}\':\n'
                         '  foo'),
                    )
