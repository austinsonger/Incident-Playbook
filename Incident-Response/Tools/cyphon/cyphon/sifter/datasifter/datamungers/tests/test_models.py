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
Tests the DataMunger class.
"""

# standard library
try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

# third party
from django.test import TestCase

# local
from cyphon.documents import DocumentObj
from sifter.datasifter.datamungers.models import DataMunger
from tests.fixture_manager import get_fixtures


class DataMungerTestCase(TestCase):
    """
    Base class for testing the DataMunger class.
    """
    fixtures = get_fixtures(['datamungers', 'distilleries'])

    def test_process(self):
        """
        Tests the process method.
        """
        mock_doc = Mock()
        mock_doc_id = 1

        data = {'id': 123, 'subject': 'This is a Critical Alert'}
        doc_obj = DocumentObj(data=data)

        datamunger = DataMunger.objects.get(pk=1)
        datamunger.condenser.process = Mock(return_value=mock_doc)
        datamunger.distillery.save_data = Mock(return_value=mock_doc_id)

        doc_id = datamunger.process(doc_obj)

        datamunger.condenser.process.assert_called_once_with(data)

        assert datamunger.distillery.save_data.call_count == 1
        self.assertEqual(doc_id, mock_doc_id)
