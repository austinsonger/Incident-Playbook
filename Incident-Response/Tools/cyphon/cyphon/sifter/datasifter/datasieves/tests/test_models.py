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
Tests the DataSieve class and related classes.
"""

# third party
from django.core.exceptions import ValidationError
from django.test import TestCase

# local
from sifter.datasifter.datasieves.models import (
    DataRule,
    DataSieve,
    DataSieveNode,
)
from tests.fixture_manager import get_fixtures


class DataSieveTestCase(TestCase):
    """
    Tests the DataSieve class.
    """
    fixtures = get_fixtures(['datasieves'])

    def setUp(self):
        self.datasieve = DataSieve.objects.get(name="test_datasieve")

    def test_get_node_number(self):
        """
        Tests the get_node_number method.
        """
        self.assertTrue(self.datasieve.get_node_number(), 2)

    def test_is_match_for_all_true(self):
        """
        Tests the is_match method for a DataSieve that uses 'AND' logic and a
        dataset that conforms to the DataSieve.
        """
        data = {'subject': 'this is a critical alert'}
        self.assertTrue(self.datasieve.is_match(data))

    def test_is_match_for_all_false(self):
        """
        Tests the is_match method for a DataSieve that uses 'AND' logic and a
        dataset that does not conform to the DataSieve.
        """
        data = {'subject': 'this is an urgent alert'}
        self.assertFalse(self.datasieve.is_match(data))

    def test_is_match_for_any_true(self):
        """
        Tests the is_match method for a DataSieve that uses 'OR' logic and a
        dataset that conforms to the DataSieve.
        """
        self.datasieve.logic = 'OR'
        data = {'subject': 'this is an urgent alert'}
        self.assertTrue(self.datasieve.is_match(data))

    def test_is_match_for_any_false(self):
        """
        Tests the is_match method for a DataSieve that uses 'OR' logic and a
        dataset that does not conform to the DataSieve.
        """
        self.datasieve.logic = 'OR'
        data = {'subject': 'this is an urgent notice'}
        self.assertFalse(self.datasieve.is_match(data))

    def test_is_match_when_negated(self):
        """
        Tests the is_match method for a negated DataSieve.
        """
        self.datasieve.negate = True
        data = {'subject': 'this is a critical alert'}
        self.assertFalse(self.datasieve.is_match(data))


class DataSieveNodeTestCase(TestCase):
    """
    Tests the DataSieve class.
    """
    fixtures = get_fixtures(['datasieves'])

    def test_valid_rule(self):
        """
        Tests the clean() method when the SieveNode refers to a Rule.
        """
        sieve_1 = DataSieve.objects.get(pk=1)
        rule_2 = DataRule.objects.get(pk=2)
        node = DataSieveNode(sieve=sieve_1, node_object=rule_2)
        try:
            node.clean()
        except ValidationError:
            self.fail('DataSieveNode raised ValidationError unexpectedly')

    def test_valid_sieve(self):
        """
        Tests the clean() method when the SieveNode refers to a Sieve
        that doesn't contain its parent Sieve.
        """
        sieve_1 = DataSieve.objects.get(pk=1)
        sieve_2 = DataSieve.objects.get(pk=2)
        node = DataSieveNode(sieve=sieve_1, node_object=sieve_2)
        try:
            node.clean()
        except ValidationError:
            self.fail('DataSieveNode raised ValidationError unexpectedly')

    def test_invalid_direct_sieve(self):
        """
        Tests the clean() method when the SieveNode refers to a Sieve
        that's the same as its parent Sieve.
        """
        sieve_1 = DataSieve.objects.get(pk=1)
        node = DataSieveNode(sieve=sieve_1, node_object=sieve_1)
        with self.assertRaises(ValidationError):
            node.clean()

    def test_invalid_indirect_sieve(self):
        """
        Tests the clean() method when the SieveNode refers to a Sieve
        that contains its parent Sieve.
        """
        sieve_1 = DataSieve.objects.get(pk=1)
        sieve_2 = DataSieve.objects.get(pk=2)
        DataSieveNode.objects.create(sieve=sieve_2, node_object=sieve_1)
        node = DataSieveNode(sieve=sieve_1, node_object=sieve_2)
        with self.assertRaises(ValidationError):
            node.clean()
