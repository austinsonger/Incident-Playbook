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
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase

# local
from lab.procedures.models import Procedure, Protocol
from tests.fixture_manager import get_fixtures


class ProtocolTestCase(TestCase):
    """
    Tests Protocol model methods.
    """
    fixtures = get_fixtures(['procedures'])

    def setUp(self):
        self.protocol = Protocol.objects.get_by_natural_key('geoip')

    def test_str(self):
        """
        Tests the __str__ method for a Protocol.
        """
        self.assertEqual(str(self.protocol), 'geoip')


class ProcedureTestCase(TestCase):
    """
    Tests Procedure model methods.
    """
    fixtures = get_fixtures(['procedures'])

    data = {'source_ip': 'foobar'}
    mock_result = Mock()

    def setUp(self):
        self.procedure = Procedure.objects.get_by_natural_key('geocode_source_ip')

    def test_str(self):
        """
        Tests the __str__ method for a Procedure.
        """
        self.assertEqual(str(self.procedure), 'geocode_source_ip')

    def test_get_result_w_field_name(self):
        """
        Tests the get_result method for a Procedure with a field_name.
        """
        self.procedure.field_name = None
        with patch('lab.procedures.models.Protocol.process',
                   return_value=self.mock_result) as mock_process:
            actual = self.procedure.get_result(self.data)
            mock_process.assert_called_once_with(self.data)
            self.assertEqual(actual, self.mock_result)

    def test_get_result_wo_field_name(self):
        """
        Tests the get_result method for a Procedure without a field_name.
        """
        with patch('lab.procedures.models.Protocol.process',
                   return_value=self.mock_result) as mock_process:
            actual = self.procedure.get_result(self.data)
            value = self.data[self.procedure.field_name]
            mock_process.assert_called_once_with(value)
            self.assertEqual(actual, self.mock_result)
