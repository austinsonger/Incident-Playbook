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
Tests the Record class.
"""

# third party
from django.test import TestCase

# local
from aggregator.invoices.models import Invoice
from tests.fixture_manager import get_fixtures


class InvoiceTestCase(TestCase):
    """
    Tests the Record class.
    """
    fixtures = get_fixtures(['invoices'])

    def test_str(self):
        """
        Tests the __str__ method of the Invoice class.
        """
        invoice = Invoice.objects.get(pk=1)
        actual = str(invoice)
        expected = 'PK 1: Twitter SearchAPI (200) 2015-01-01 07:00:00+00:00'
        self.assertEqual(actual, expected)

    def test_query_str(self):
        """
        Tests the query_str method of the Invoice class.
        """
        invoice = Invoice.objects.get(pk=1)
        actual = invoice.query_str()
        expected = """{
    "bar": "foo",
    "foo": "bar"
}"""
        self.assertEqual(actual, expected)
