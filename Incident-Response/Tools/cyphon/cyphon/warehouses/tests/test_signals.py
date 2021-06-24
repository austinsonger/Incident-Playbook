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
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.test import TransactionTestCase

# local
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures
from warehouses.models import Collection


class PutTemplateTestCase(TransactionTestCase):
    """
    Tests the put_template signal receiver.
    """

    fixtures = get_fixtures(['distilleries'])

    @patch('engines.elasticsearch.engine.ElasticsearchEngine.create_template')
    def test_distillery_saved(self, mock_template):
        """
        Tests that the put_template is called when a Distllery is saved.
        """
        distillery = Distillery.objects.get_by_natural_key(
            'elasticsearch.test_index.test_docs')
        distillery.save()
        self.assertEqual(mock_template.call_count, 1)

    @patch('engines.elasticsearch.engine.ElasticsearchEngine.create_template')
    def test_collection_saved(self, mock_template):
        """
        Tests that the put_template is called when a Collection is saved.
        """
        collection = Collection.objects.get_by_natural_key(
            'elasticsearch', 'test_index', 'test_docs')
        collection.save()
        self.assertEqual(mock_template.call_count, 1)

    def test_no_template(self):
        """
        Tests that the put_template is called when a Distllery is saved.
        """
        distillery = Distillery.objects.get_by_natural_key(
            'mongodb.test_database.test_docs')
        try:
            distillery.save()
        except AttributeError:
            self.fail('put_template() raised AttributeError unexpectedly')
