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
Tests the MongoDbEngine class.
"""

# standard library
import logging
import time
from unittest import skipIf
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
import pymongo

# local
from engines.mongodb.client import MONGODB_CLIENT
from engines.mongodb.engine import MongoDbEngine
from engines.tests.test_engine import EngineBaseTestCase
from engines.tests.mixins import CRUDTestCaseMixin, FilterTestCaseMixin
from warehouses.models import Collection

LOGGER = logging.getLogger(__name__)

DATABASE = 'test_database_%s' % int(time.time())
COLLECTION = 'test_docs'

try:
    MONGODB_CLIENT[DATABASE][COLLECTION].drop_indexes()
    NOT_CONNECTED = False
except pymongo.errors.ServerSelectionTimeoutError as error:
    NOT_CONNECTED = True
    LOGGER.warning('Cannot connect to MongoDB. MongoDB tests will be skipped.')


@skipIf(NOT_CONNECTED, 'MongoDB is not running')
class MongoDbBaseTestCase(EngineBaseTestCase):
    """
    Class for testing the MongoDbEngine class.
    """
    def setUp(self):
        collection = Collection.objects.get_by_natural_key('mongodb',
                                                           'test_database',
                                                           'test_docs')
        # overide collection name so we can safely delete it on teardown
        with patch('warehouses.models.Collection.get_warehouse_name',
                   return_value=DATABASE):
            self.engine = MongoDbEngine(collection)
            self.mongodb = MONGODB_CLIENT[DATABASE][COLLECTION]
            self.mongodb.drop_indexes()

    def tearDown(self):
        MONGODB_CLIENT.drop_database(DATABASE)

    @staticmethod
    def _get_count(results):
        """
        Takes a MongoDB cursor and returns the number of documents it
        contains.
        """
        return len(results)

    @staticmethod
    def _get_id(results, index):
        """
        Takes a list of dictionaries and a list index. Returns the id
        for that index.
        """
        return results[index]['_id']

    @staticmethod
    def _get_doc(results, index):
        """
        Takes a list of dictionaries and a list index. Returns the
        document for that index.
        """
        return results[index]


class MongoDbHelperTestCase(MongoDbBaseTestCase):
    """
    Tests helper methods for the MongoDbEngine class.
    """

    def test_create_text_index_w_schema(self):
        """
        Tests the _create_text_index() method when a schema is provided.
        """
        actual = self.engine._create_text_index(self.engine.schema)
        expected = 'TextIndex'
        self.assertEqual(actual, expected)

    def test_create_text_index_noschema(self):
        """
        Tests the _create_text_index() method when a schema is not provided.
        """
        actual = self.engine._create_text_index()
        expected = 'TextIndex'
        self.assertEqual(actual, expected)


class MongoDbTestCase(MongoDbBaseTestCase):
    """
    Tests methods for the MongoDbEngine class.
    """

    def test_str(self):
        """
        Tests the __str__ method.
        """
        name = str(self.engine)
        self.assertTrue(name.startswith('test_database_'))
        self.assertTrue(name.endswith('.test_docs'))


class MongoDbCRUDTestCase(MongoDbBaseTestCase, CRUDTestCaseMixin):
    """
    Class for testing simple CRUD operations for the MongoDbEngine class. Inherits its
    test methods from CRUDTestCaseMixin.
    """
    pass


class MongoDbFilterTestCase(MongoDbBaseTestCase, FilterTestCaseMixin):
    """
    Class for testing filter operations for the ElasticSearch class. Inherits
    its test methods from FilterTestCaseMixin.
    """

    def setUp(self):
        """
        Sets up an ElasticSearch index and inserts the test_docs provided by
        FilterTestCaseMixin.
        """
        super(MongoDbFilterTestCase, self).setUp()

        for doc in self.test_docs:
            self.engine.insert(doc)
