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
"""Tests the :mod:`engines.elasticsearch.engine` module.

"""

# standard library
import logging
import time
from unittest import skipIf
try:
    from unittest.mock import call, patch
except ImportError:
    from mock import call, patch

# third party
from elasticsearch.exceptions import ConnectionError
from testfixtures import LogCapture

# local
from engines.tests.test_engine import EngineBaseTestCase
from engines.tests.mixins import CRUDTestCaseMixin, FilterTestCaseMixin
from warehouses.models import Collection

LOGGER = logging.getLogger(__name__)

try:
    # local
    from engines.elasticsearch.client import ELASTICSEARCH, VERSION
    from engines.elasticsearch.engine import (
        catch_connection_error,
        ElasticsearchEngine,
    )
    NOT_CONNECTED = False

except ConnectionError:
    ELASTICSEARCH = None
    NOT_CONNECTED = True
    LOGGER.warning('Cannot connect to Elasticsearch. '
                   'Elasticsearch tests will be skipped.')

INDEX = '%s_%s' % ('test_index', int(time.time()))


@skipIf(NOT_CONNECTED, 'Cannot connect to Elasticsearch')
class ElasticsearchBaseTestCase(EngineBaseTestCase):
    """
    Base class for testing the ElasticsearchEngine class.
    """
    index = INDEX
    doctype = 'test_docs'
    elasticsearch = ELASTICSEARCH

    def setUp(self):
        logging.disable(logging.WARNING)
        collection = Collection.objects.get_by_natural_key('elasticsearch',
                                                           'test_index',
                                                           'test_docs')
        with patch('warehouses.models.Collection.get_warehouse_name',
                   return_value=INDEX):
            self.engine = ElasticsearchEngine(collection)

    def tearDown(self):
        self.elasticsearch.indices.delete(index=self.index)
        logging.disable(logging.NOTSET)

    @staticmethod
    def _get_count(results):
        """
        Takes a list of results and returns the number of documents
        it contains.
        """
        return len(results)

    @staticmethod
    def _get_id(results, index):
        """
        Takes a list of Elasticsearch results and a list index.
        Returns the id for the document at that index.
        """
        return results[index]['_id']

    @staticmethod
    def _get_doc(results, index):
        """
        Takes a list of Elasticsearch results and a list index.
        Returns the document for that index.
        """
        return results[index]


class ElasticsearchTestCase(ElasticsearchBaseTestCase):
    """
    Tests methods for the Elasticsearch class.
    """

    def test_str(self):
        """
        Tests the __str__ method.
        """
        name = str(self.engine)
        self.assertTrue(name.startswith('test_index_'))
        self.assertTrue(name.endswith('.test_docs'))


class CatchConnectionError(ElasticsearchBaseTestCase):
    """
    Tests methods for the catch_connection_error decorator.
    """

    def test_can_connect(self):
        """
        Tests the catch_connection_error decorator when a connection
        is established.
        """
        with LogCapture() as log_capture:
            catch_connection_error(self.engine.insert({'foo': 'bar'}))
            log_capture.check()

    @patch('engines.elasticsearch.engine.ELASTICSEARCH.index',
           side_effect=ConnectionError())
    def test_cannot_connect(self, mock_index):
        """
        Tests the catch_connection_error decorator when a connection
        is established.
        """
        @catch_connection_error
        def test_decorator():
            """Test the catch_connection_error decorator."""
            self.engine.insert({'foo': 'bar'})

        with LogCapture() as log_capture:
            test_decorator()
            expected = 'Cannot connect to Elasticsearch'
            log_capture.check(
                ('engines.elasticsearch.engine', 'ERROR', expected),
            )


class ElasticsearchHelperTestCase(ElasticsearchBaseTestCase):
    """
    Tests helper methods for the Elasticsearch class.
    """
    maxDiff = None

    expected_properties_v2 = {
        '_saved_date': {
            'format': 'strict_date_optional_time||epoch_millis',
            'ignore_malformed': True,
            'type': 'date'
        },
        'content': {
            'properties': {
                'image': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'link': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'text': {
                    'type': 'string'
                },
                'title': {
                    'type': 'string'
                },
                'video': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
            }
        },
        'created_date': {
            'format': 'strict_date_optional_time||epoch_millis',
            'ignore_malformed': True,
            'type': 'date'
        },
        'ip_address': {
            'index': 'not_analyzed',
            'type': 'string'
        },
        'likes': {
            'type': 'integer'
        },
        'location': {
            'ignore_malformed': True,
            'type': 'geo_point'
        },
        'platform': {
            'index': 'not_analyzed',
            'type': 'string'
        },
        'tags': {
            'index': 'not_analyzed',
            'type': 'string'
        },
        'user': {
            'properties': {
                'email': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'id': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'link': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'name': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'profile_pic': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
                'screen_name': {
                    'index': 'not_analyzed',
                    'type': 'string'
                },
            }
        },
        'verified': {
            'type': 'boolean'
        },
    }

    expected_properties_v5 = {
        '_saved_date': {
            'ignore_malformed': True,
            'type': 'date',
        },
        'content': {
            'properties': {
                'image': {
                    'type': 'keyword',
                },
                'link': {
                    'type': 'keyword',
                },
                'text': {
                    'type': 'text'
                },
                'title': {
                    'type': 'text'
                },
                'video': {
                    'type': 'keyword',
                },
            }
        },
        'created_date': {
            'ignore_malformed': True,
            'type': 'date',
        },
        'ip_address': {
            'type': 'keyword',
        },
        'likes': {
            'type': 'integer',
        },
        'location': {
            'ignore_malformed': True,
            'type': 'geo_point',
        },
        'platform': {
            'type': 'keyword',
        },
        'tags': {
            'type': 'keyword',
        },
        'user': {
            'properties': {
                'email': {
                    'type': 'keyword',
                },
                'id': {
                    'type': 'keyword'
                },
                'link': {
                    'type': 'keyword',
                },
                'name': {
                    'type': 'keyword'
                },
                'profile_pic': {
                    'type': 'keyword',
                },
                'screen_name': {
                    'type': 'keyword'
                },
            }
        },
        'verified': {
            'type': 'boolean',
        },
    }

    index_settings = {
        'settings': {
            'index.mapping.ignore_malformed': True,
            'number_of_shards': 1,
        },
    }

    def test_init(self):
        """
        Tests the __init__ method of an Elasticsearch object. Checks
        that the correct mapping was used when the index was created.
        """
        actual = self.elasticsearch.indices.get_mapping(index=self.index,
                                                        doc_type=self.doctype)
        if VERSION < '5.0':
            expected = {
                self.index: {
                    'mappings': {
                        self.doctype: {
                            'properties': self.expected_properties_v2
                        }
                    }
                }
            }
        else:
            expected = {
                self.index: {
                    'mappings': {
                        self.doctype: {
                            'properties': self.expected_properties_v5
                        }
                    }
                }
            }
        self.assertEqual(actual, expected)

    def test_create_mapping(self):
        """
        Tests the _create_mapping method.
        """
        actual = self.engine._create_mapping()
        expected = self.index_settings
        if VERSION < '5.0':
            expected.update({
                'mappings': {
                    'test_docs': {
                        'properties': self.expected_properties_v2
                    }
                }
            })

        else:
            expected.update({
                'mappings': {
                    'test_docs': {
                        'properties': self.expected_properties_v5
                    }
                }
            })
        self.assertEqual(actual, expected)

    @patch('engines.elasticsearch.engine.ELASTICSEARCH.indices.put_template')
    def test_create_template(self, mock_template):
        """
        Tests the create_template method.
        """
        self.engine.create_template()
        body = self.index_settings
        body.update({'template': self.engine._index_for_template})

        if VERSION < '5.0':
            body.update({
                'mappings': {
                    'test_docs': {
                        'properties': self.expected_properties_v2
                    }
                }
            })
        else:
            body.update({
                'mappings': {
                    'test_docs': {
                        'properties': self.expected_properties_v5
                    }
                }
            })
        mock_template.assert_has_calls([
            call(name=str(self.engine), body=body),
        ])


class ElasticsearchCRUDTestCase(ElasticsearchBaseTestCase, CRUDTestCaseMixin):
    """
    Class for testing simple CRUD operations for the Elasticsearch class.
    Inherits its test methods from CRUDTestCaseMixin.
    """
    pass


class ElasticsearchWildcardTestCase(ElasticsearchBaseTestCase):
    """

    """
    def setUp(self):
        logging.disable(logging.WARNING)
        collection = Collection.objects.get_by_natural_key('elasticsearch',
                                                           'test_index',
                                                           'test_docs')
        with patch('warehouses.models.Collection.get_warehouse_name',
                   return_value=INDEX):
            with patch('warehouses.models.Collection.in_time_series',
                       return_value=True):
                self.engine = ElasticsearchEngine(collection)

        # self.elasticsearch.indices.create(index=self.index, ignore=400)

    def tearDown(self):
        self.elasticsearch.indices.delete(index=self.engine._index_for_insert)
        logging.disable(logging.NOTSET)

    def test_find_by_id(self):
        """
        Tests the find_by_id method for a wildcard index name.
        """
        test_text = 'this is a find_by_id test post'

        doc_id = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': test_text
        })

        results = self.engine.find_by_id([doc_id])
        expected_ids = [doc_id]
        self.assertEqual(len(results), 1)
        self.assertIn(self._get_id(results, 0), expected_ids)
        self.assertEqual(self._get_doc(results, 0)['text'], test_text)

    def test_remove_by_id(self):
        """
        Tests the remove_by_id method for a wildcard index name.
        """
        test_text = 'this is a find_by_id test post'

        doc_id = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': test_text
        })

        results = self.engine.find_by_id([doc_id])
        self.assertEqual(len(results), 1)

        self.engine.remove_by_id(doc_id)
        results = self.engine.find_by_id(doc_id)
        self.assertEqual(results, None)

    def test_insert(self):
        """
        Tests the insert method for a wildcard index name.
        """
        test_text = 'this is a find_by_id test post'

        doc_id = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': test_text
        })

        results = self.engine.find_by_id([doc_id])
        self.assertEqual(len(results), 1)

        self.engine.remove_by_id(doc_id)
        results = self.engine.find_by_id(doc_id)
        self.assertEqual(results, None)

    def test_malformed(self):
        """
        Tests the insert method for a malformed geopoint.
        """
        doc_id = self.engine.insert({
            'location': 'foobar'
        })

        results = self.engine.find_by_id([doc_id])
        self.assertEqual(len(results), 1)

        self.engine.remove_by_id(doc_id)
        results = self.engine.find_by_id(doc_id)
        self.assertEqual(results, None)


class ElasticsearchFilterTestCase(ElasticsearchBaseTestCase, FilterTestCaseMixin):
    """
    Class for testing filter operations for the Elasticsearch class. Inherits
    its test methods from FilterTestCaseMixin.
    """

    def setUp(self):
        """
        Sets up an Elasticsearch index and inserts the test_docs provided by
        FilterTestCaseMixin.
        """
        super(ElasticsearchFilterTestCase, self).setUp()

        for doc in self.test_docs:
            self.engine.insert(doc)
