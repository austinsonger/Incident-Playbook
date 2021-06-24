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
Tests the CollectionQuerySerializer class.
"""

# standard library
from django.test import TestCase

# local
from query.collectionqueries.serializers import CollectionQuerySerializer
from tests.fixture_manager import get_fixtures


class CollectionQuerySerializerTestCase(TestCase):
    """
    Class for testing the CollectionQuerySerializer.
    """
    fixtures = get_fixtures(['users', 'warehouses'])

    def test_create_query(self):
        """
        Ensures an example query is properly validated.
        """
        query = {
            'collections': [3, 4],
            'fieldsets': [
                {
                    'field_name': 'age',
                    'field_type': 'IntegerField',
                    'operator': 'eq',
                    'value': 10
                }, {
                    'field_name': 'text',
                    'field_type': 'CharField',
                    'operator': 'regex',
                    'value': 'cat'
                }
            ],
            'joiner': 'AND'
        }

        serializer = CollectionQuerySerializer(data=query)
        self.assertTrue(serializer.is_valid(raise_exception=True))

        validated_data = serializer.validated_data
        self.assertEqual(len(validated_data['collections']), 2)
        self.assertEqual(len(validated_data['collections']), 2)
        self.assertEqual(len(validated_data['fieldsets']), 2)
        self.assertEqual(validated_data['joiner'], 'AND')
