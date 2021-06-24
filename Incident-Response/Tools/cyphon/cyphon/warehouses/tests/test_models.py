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
Tests the Warehouse class.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
import six
from testfixtures import LogCapture

# local
from companies.models import Company
from cyphon.fieldsets import QueryFieldset
from engines.queries import EngineQuery
from tests.fixture_manager import get_fixtures
from warehouses.models import Warehouse, Collection

PAGE_SIZE = settings.PAGE_SIZE


class WarehouseTestCase(TestCase):
    """
    Tests the Warehouse and WarehouseManager classes.
    """
    fixtures = get_fixtures(['warehouses'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method of the WarehouseManager class.
        """
        warehouse = Warehouse.objects.get_by_natural_key(
            backend='mongodb',
            name='test_database',
        )
        self.assertEqual(warehouse.pk, 1)

    def test_get_by_natural_key_error(self):
        """
        Tests the get_by_natural_key method of the WarehouseManager class.
        """
        with LogCapture() as log_capture:
            Warehouse.objects.get_by_natural_key(
                backend='mongodb',
                name='test_dummy',
            )
            expected = 'Warehouse mongodb.test_dummy does not exist'
            log_capture.check(
                ('warehouses.models', 'ERROR', expected),
            )

    def test_str(self):
        """
        Tests the __str__ method of the Warehouse class.
        """
        warehouse = Warehouse.objects.get_by_natural_key(
            backend='mongodb',
            name='test_database',
        )
        self.assertEqual(str(warehouse), 'mongodb.test_database')

    def test_special_character_name(self):
        """
        Tests the clean method when the name contains a special
        character.
        """
        warehouse = Warehouse(
            backend='elasticsearch',
            name='test_databa$e',
            time_series=True
        )
        msg = ('Name cannot contain special characters other than '
               'underscores and hypens.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            warehouse.full_clean()

    def test_upppercase_name(self):
        """
        Tests the clean method when the name contains an uppercase
        character.
        """
        warehouse = Warehouse(
            backend='elasticsearch',
            name='testDatabase',
            time_series=True
        )
        msg = 'Value must be lowercase string.'
        with six.assertRaisesRegex(self, ValidationError, msg):
            warehouse.full_clean()

    def test_disallowed_time_series(self):
        """
        Tests the clean method when time_series is selected but not is
        allowed with the selected backend.
        """
        warehouse = Warehouse(
            backend='mongodb',
            name='test_database',
            time_series=True
        )
        msg = ('The time series feature is not enabled '
               'for the selected backend.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            warehouse.clean()

    def test_allowed_time_series(self):
        """
        Tests the clean method when time_series is selected and is
        allowed with the selected backend.
        """
        mock_module = Mock()
        mock_module.TIME_SERIES_ENABLED = True

        # patch this to avoid errors if Elasticsearch is not connected
        with patch('warehouses.models.Warehouse.get_module',
                   return_value=mock_module):
            warehouse = Warehouse(
                backend='elasticsearch',
                name='test_index',
                time_series=True
            )
            try:
                warehouse.clean()
            except ValidationError:
                self.fail('A ValidationError was raised unexpectedly')

    def test_get_module(self):
        """
        Tests the get_module method of the Warehouse class.
        """
        warehouse = Warehouse.objects.get_by_natural_key(
            backend='mongodb',
            name='test_database',
        )
        import engines.mongodb.engine
        actual = warehouse.get_module()
        expected = engines.mongodb.engine
        self.assertEqual(actual, expected)


class CollectionTestCase(TestCase):
    """
    Tests the Collection and CollectionManager classes.
    """
    fixtures = get_fixtures(['warehouses', 'distilleries'])

    mock_doc_id = 1

    doc = {
        'text': 'this is a test post',
        '_raw_data': {
            'backend': 'mongodb',
            'collection': 'test',
            'doc_id': 1
        }
    }

    @classmethod
    def setUpClass(cls):
        super(CollectionTestCase, cls).setUpClass()
        cls.collection = Collection.objects.get_by_natural_key(
            backend='mongodb',
            database='test_database',
            name='test_docs'
        )

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method of the CollectionManager
        class.
        """
        collection = Collection.objects.get_by_natural_key(
            backend='mongodb',
            database='test_database',
            name='test_posts'
        )
        self.assertEqual(collection.pk, 1)

    def test_get_by_natural_key_error(self):
        """
        Tests the get_by_natural_key method of the CollectionManager
        class when the Collection does not exist.
        """
        with LogCapture() as log_capture:
            Collection.objects.get_by_natural_key(
                backend='mongodb',
                database='test_database',
                name='dummy'
            )
            expected = 'Collection mongodb.test_database.dummy does not exist'
            log_capture.check(
                ('warehouses.models', 'ERROR', expected),
            )

    def test_str(self):
        """
        Tests the __str__ method of the Collection class.
        """
        actual = str(self.collection)
        expected = 'mongodb.test_database.test_docs'
        self.assertEqual(actual, expected)

    def test_company(self):
        """
        Tests the company property.
        """
        company = self.collection.company
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.name, 'ECorp')

    def test_company_none(self):
        """
        Tests the company property when the Collection has no associated
        Distillery.
        """
        collection = Collection.objects.get_by_natural_key(
            backend='mongodb',
            database='test_database',
            name='orphan'
        )
        company = collection.company
        self.assertEqual(company, None)

    def test_get_company(self):
        """
        Tests the get_company method.
        """
        company = self.collection.get_company()
        self.assertTrue(isinstance(company, Company))
        self.assertEqual(company.name, 'ECorp')

    def test_get_backend(self):
        """
        Tests the get_backend method.
        """
        actual = self.collection.get_backend()
        expected = 'mongodb'
        self.assertEqual(actual, expected)

    def test_in_time_series_false(self):
        """
        Tests the in_time_series method when the Collection is not part
        of a time_series.
        """
        collection = Collection.objects.get(pk=3)
        actual = collection.in_time_series()
        expected = False
        self.assertIs(actual, expected)

    def test_in_time_series_true(self):
        """
        Tests the in_time_series method when the Collection is part of a
        time_series.
        """
        collection = Collection.objects.get(pk=4)
        actual = collection.in_time_series()
        expected = True
        self.assertIs(actual, expected)

    def test_get_warehouse_none(self):
        """
        Tests the get_warehouse_name method.
        """
        actual = self.collection.get_warehouse_name()
        expected = 'test_database'
        self.assertEqual(actual, expected)

    def test_get_schema_w_distillery(self):
        """
        Tests the get_schema method when the Collection is associated
        with a Distilllery.
        """
        collection = Collection.objects.get_by_natural_key(
            backend='elasticsearch',
            database='test_time_series',
            name='test_syslogs'
        )
        fields = collection.get_schema()

        self.assertEqual(fields[0].field_name, 'date_str')
        self.assertEqual(fields[0].field_type, 'CharField')
        self.assertEqual(fields[0].target_type, None)

        self.assertEqual(fields[1].field_name, 'host')
        self.assertEqual(fields[1].field_type, 'GenericIPAddressField')
        self.assertEqual(fields[1].target_type, 'IPAddress')

        self.assertEqual(fields[2].field_name, 'message')
        self.assertEqual(fields[2].field_type, 'TextField')
        self.assertEqual(fields[2].target_type, 'Keyword')

    def test_get_schema_no_distillery(self):
        """
        Tests the get_schema method when the Collection is not
        associated with a Distilllery.
        """
        collection = Collection.objects.get_by_natural_key(
            backend='mongodb',
            database='test_database',
            name='orphan'
        )
        actual = collection.get_schema()
        expected = []
        self.assertEqual(actual, expected)

    @patch('engines.mongodb.engine.MongoDbEngine')
    def test_engine(self, mock_engine):
        """
        Tests the engine property of the Collection class.
        """
        self.collection.engine
        mock_engine.called_once_with(self.collection)

    def test_engine_connection_error(self):
        """
        Tests the _get_engine method of the Collection class when there is
        a connection error.
        """
        error_msg = 'Engine initialization error'
        with patch('engines.mongodb.engine.MongoDbEngine',
                   side_effect=ConnectionRefusedError(error_msg)):
            with LogCapture() as log_capture:
                self.collection._get_engine()
                error_msg = 'Engine initialization error'
                log_capture.check(
                    ('warehouses.models', 'ERROR', error_msg),
                )

    @patch('warehouses.models.Collection.engine')
    def test_filter_ids(self, mock_engine):
        """
        Tests the filter_ids method of the Collection class.
        """
        self.collection.engine.filter_ids = Mock()
        args = (1, 2, 3)
        self.collection.filter_ids(*args)
        self.collection.engine.filter_ids.assert_called_once_with(*args)

    @patch('warehouses.models.Collection.engine')
    def test_insert(self, mock_engine):
        """
        Tests the insert method of the Collection class.
        """
        self.collection.engine.insert = Mock(return_value=self.mock_doc_id)
        doc_id = self.collection.insert(self.doc)
        self.collection.engine.insert.assert_called_once_with(self.doc)
        self.assertEqual(doc_id, self.mock_doc_id)

    @patch('warehouses.models.Collection.engine')
    def test_insert_error(self, mock_engine):
        """
        Tests the insert method of the Collection class when an
        Exception occurs.
        """
        msg = 'msg'
        self.collection.engine.insert = Mock(side_effect=Exception(msg))
        with LogCapture() as log_capture:
            self.collection.insert(self.doc)
            log_capture.check(
                ('warehouses.models', 'ERROR', 'Insertion error: %s' % msg),
            )

    @patch('warehouses.models.Collection.engine')
    def test_find(self, mock_engine):
        """
        Tests the find method of the Collection class.
        """
        collection = Collection()
        fieldset = QueryFieldset(
            field_name='text',
            field_type='CharField',
            operator='regex',
            value='test'
        )
        joiner = 'AND'
        query = EngineQuery([fieldset], joiner)
        collection.engine.find = Mock(return_value=[self.doc])
        docs = collection.find(query)
        collection.engine.find.assert_called_once_with(query, None, 1, PAGE_SIZE)
        self.assertEqual(docs, [self.doc])

    @patch('warehouses.models.Collection.engine')
    def test_find_by_id(self, mock_engine):
        """
        Tests the find_by_id method of the Collection class.
        """
        collection = Collection()
        collection.engine.find_by_id = Mock(return_value=[self.doc])
        docs = collection.find_by_id(self.mock_doc_id)
        collection.engine.find_by_id.assert_called_once_with(self.mock_doc_id)
        self.assertEqual(docs, [self.doc])

    @patch('warehouses.models.Collection.engine')
    def test_remove_by_id(self, mock_engine):
        """
        Tests the remove_by_id method of the Collection class.
        """
        collection = Collection()
        collection.engine.remove_by_id = Mock()
        collection.remove_by_id(self.mock_doc_id)
        collection.engine.remove_by_id.assert_called_once_with(self.mock_doc_id)

    @patch('warehouses.models.Collection.engine')
    @patch('warehouses.models.Collection.distillery')
    def test_get_sample(self, mock_distillery, mock_engine):
        """
        Tests the get_sample method of the Collection class.
        """
        collection = Collection()
        taste = {'title': 'test'}
        collection.distillery.get_sample = Mock(return_value=taste)
        sample = collection.get_sample(self.doc)
        collection.distillery.get_sample.assert_called_once_with(self.doc)
        self.assertEqual(sample, taste)
