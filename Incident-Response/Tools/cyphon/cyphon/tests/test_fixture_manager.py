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
Tests the fixtures module.
"""

# standard library
from unittest import TestCase
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
import six
from testfixtures import LogCapture

# local
from tests.fixture_manager import get_fixtures


class FixtureListTestCase(TestCase):
    """
    Tests the get_fixtures function.
    """

    def test_single_item_no_dependency(self):
        """
        Tests the get_fixtures function for a single base dependency
        that has no child dependencies.
        """
        actual = get_fixtures(['companies'])
        expected = ['tests/fixtures/companies.json']
        self.assertEqual(actual, expected)

    def test_multiple_items(self):
        """
        Tests the get_fixtures function for multiple dependencies.
        """
        mock_dependencies = {
            'bottles': [],
            'codebooks': ['companies'],
            'companies': [],
            'containers': ['bottles', 'labels'],
            'distilleries': ['warehouses', 'containers', 'companies', 'codebooks'],
            'inspections': [],
            'labels': ['inspections', 'procedures'],
            'procedures': [],
            'searchtasks': ['distilleries'],
            'tastes': ['containers'],
            'warehouses': [],
            'watchdogs': [],
            'users': ['companies']
        }

        with patch.dict('tests.fixture_manager.FIXTURE_DEPENDENCIES',
                        mock_dependencies, clear=True):
            actual = get_fixtures(['watchdogs', 'distilleries'])
            expected = [
                'tests/fixtures/companies.json',
                'tests/fixtures/inspections.json',
                'tests/fixtures/procedures.json',
                'tests/fixtures/bottles.json',
                'tests/fixtures/labels.json',
                'tests/fixtures/warehouses.json',
                'tests/fixtures/containers.json',
                'tests/fixtures/codebooks.json',
                'tests/fixtures/watchdogs.json',
                'tests/fixtures/distilleries.json',
            ]
            self.assertEqual(actual, expected)

    def test_empty_list(self):
        """
        Tests the get_fixtures function for an emty dependency list.
        """
        actual = get_fixtures([])
        expected = []
        self.assertEqual(actual, expected)

    def test_non_list(self):
        """
        Tests the get_fixtures function for a non-list.
        """
        msg = 'Dependencies must be a list'
        with six.assertRaisesRegex(self, AssertionError, msg):
            get_fixtures('watchdogs')

    def test_missing_fixture(self):
        """
        Tests the get_fixtures function for a missing dependency.
        """
        msg = 'Fixture file tests/fixtures/missing_fixture.json is missing'
        with LogCapture() as log_capture:
            get_fixtures(['missing_fixture'])
            log_capture.check(
                ('tests.fixture_manager', 'ERROR', msg),
            )

