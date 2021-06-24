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
Tests signals for Distilleries.
"""

# standard library
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TransactionTestCase

# local
from cyphon.documents import DocumentObj
from distilleries.signals import document_saved
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures


class DocumentSavedSignalTestCase(TransactionTestCase):
    """
    Tests the Collection and CollectionManager classes.
    """

    fixtures = get_fixtures(['distilleries'])

    def setUp(self):
        self.distillery = Distillery.objects.get_by_natural_key(
            'mongodb.test_database.test_posts')
        doc = {'text': 'this is a text post'}
        self.doc_obj = DocumentObj(
            data=doc,
            doc_id=2,
            collection=str(self.distillery)
        )

    def test_document_saved_signal(self):
        """
        Tests that the document_saved signal is sent with arguments.
        """
        handler = Mock()

        document_saved.connect(handler, sender='test')
        document_saved.send(sender='test', doc_obj=self.doc_obj)

        handler.assert_called_once_with(
            sender='test',
            signal=document_saved,
            doc_obj=self.doc_obj
        )

    def test_save_data_sends_signal(self):
        """
        Tests that the document_saved signal is sent when a document is saved.
        """
        handler = Mock()
        mock_doc_obj = self.doc_obj
        mock_doc_id = '1'

        self.distillery.collection.insert = Mock(return_value=mock_doc_id)
        self.distillery._create_doc_obj = Mock(return_value=mock_doc_obj)

        document_saved.connect(handler, sender=Distillery)

        doc_id = self.distillery._save_and_send_signal(self.doc_obj)

        # Assert the signal was called only once with the args
        handler.assert_called_once_with(
            sender=Distillery,
            signal=document_saved,
            doc_obj=mock_doc_obj
        )
        self.assertEqual(mock_doc_id, doc_id)
