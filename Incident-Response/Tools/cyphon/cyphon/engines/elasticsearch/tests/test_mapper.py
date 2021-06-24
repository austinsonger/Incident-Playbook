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
"""Tests the :mod:`engines.elasticsearch.mapper` module.

"""

# standard library
import logging
from unittest import skipIf, TestCase

# third party
from elasticsearch.exceptions import ConnectionError

LOGGER = logging.getLogger(__name__)

try:
    # local
    from engines.elasticsearch import mapper
    from engines.elasticsearch.client import ELASTICSEARCH, VERSION
    NOT_CONNECTED = False

except ConnectionError:
    NOT_CONNECTED = True
    LOGGER.warning('Cannot connect to Elasticsearch. ' \
                   + 'Elasticsearch tests will be skipped.')


@skipIf(NOT_CONNECTED, 'Cannot connect to Elasticsearch')
class MapperTestCase(TestCase):
    """
    Tests helper functions for the ElasticSearch class.
    """
    maxDiff = None

    def test_map_field_base_case(self):
        """
        Tests a base case for the _map_field function.
        """
        field = 'title'
        mapping = {
            'type': 'text',
            'index': True
        }

        actual = mapper._map_field(mapping, field)
        expected = {
            'properties': {
                'title': {
                    'type': 'text',
                    'index': True
                }
            }
        }
        self.assertEqual(actual, expected)

    def test_map_field_recursive_case(self):
        """
        Tests a recusive case for the _map_field function.
        """
        field = 'content.title'
        mapping = {
            'type': 'text',
            'index': True
        }

        actual = mapper._map_field(mapping, field)
        expected = {
            'properties': {
                'content': {
                    'properties': {
                        'title': {
                            'type': 'text',
                            'index': True
                        }
                    }
                }
            }
        }
        self.assertEqual(actual, expected)
