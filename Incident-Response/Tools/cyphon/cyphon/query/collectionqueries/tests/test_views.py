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

"""

# standard library
from unittest.mock import Mock, patch

# third party
from django.conf import settings
from rest_framework import status

# local
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures

_PAGE_SIZE = settings.PAGE_SIZE


class CollectionQueryAPITestCase(CyphonAPITestCase):
    """
    Tests REST API endpoints for CollectionQueries and related objects.
    """
    fixtures = get_fixtures(['warehouses'])

    model_url = 'collectionqueries/'

    mongodb_test_docs = [
        {
            'user': {
                'screen_name': 'john',
                'age': 20
            },
            'content': {
                'text': 'I like cats.',
                'tags': ['cats', 'pets']
            }
        },
        {
            'user': {
                'screen_name': 'jane',
                'age': 25
            },
            'content': {
                'text': 'I like dogs.',
                'tags': ['dogs', 'pets']
            }
        },
        {
            'user': {
                'screen_name': 'jack',
                'age': 30
            },
            'content': {
                'text': 'I like cats and dogs.',
                'tags': ['cats', 'dogs', 'pets']
            }
        }
    ]

    es_test_docs = [
        {
            'user': {
                'screen_name': 'alice',
                'age': 20
            },
            'content': {
                'text': 'I like cats.',
                'tags': ['cats', 'pets']
            }
        },
        {
            'user': {
                'screen_name': 'adam',
                'age': 25
            },
            'content': {
                'text': 'I like dogs.',
                'tags': ['dogs', 'pets']
            }
        },
        {
            'user': {
                'screen_name': 'amy',
                'age': 30
            },
            'content': {
                'text': 'I like cats and dogs.',
                'tags': ['cats', 'dogs', 'pets']
            }
        }
    ]

    query = {
        'collections': [2, 3],
        'fieldsets': [
            {
                'field_name': 'user.age',
                'field_type': 'IntegerField',
                'operator': 'eq',
                'value': '20'
            }, {
                'field_name': 'content.text',
                'field_type': 'CharField',
                'operator': 'regex',
                'value': 'cats'
            }
        ],
        'joiner': 'OR',
    }

    def test_create_query(self):
        """
        Tests the Fieldqueries REST API endpoint for POST requests.
        """
        response = self.post_to_api('', self.query)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['collections']), 2)
        self.assertEqual(len(response.data['fieldsets']), 2)
        self.assertEqual(response.data['joiner'], 'OR')

    # def test_submit_query(self):
    #     """
    #     Tests the /collectionqueries/query REST API endpoint for POST requests.
    #     Uses the class's example query to perform a simple test of the query
    #     machinery.
    #     """
    #     mongodb_docs = [self.mongodb_test_docs[0], self.mongodb_test_docs[1]]
    #     es_docs = [self.es_test_docs[0], self.es_test_docs[1]]

    #     mock_mongodb = Mock()
    #     mock_es = Mock()
    #     with patch('engines.mongodb.engine.MongoDb', return_value=mock_mongodb):
    #         with patch('engines.elasticsearch.engine.ElasticSearch',
    #                    return_value=mock_es):
    #             mock_mongodb.find = Mock(return_value={'results': mongodb_docs})
    #             mock_es.find = Mock(return_value={'results': es_docs})
    #             response = self.post_to_api('query/', self.query)

    #             mock_mongodb.find.assert_called_once()
    #             mongodb_query = mock_mongodb.find.call_args[0][0]
    #             self.assertEqual(mongodb_query, self.query)

    #             mock_es.find.assert_called_once()
    #             mock_es = mock_es.find.call_args[0][0]
    #             self.assertEqual(mock_es, self.query)

    #             self.assertEqual(len(response.data), 4)
    #             self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_or_query(self):
    #     """
    #     Tests a query that joins terms with 'OR' logic.
    #     """
    #     query = {
    #         'collections': [2, 3],
    #         'fieldsets': [
    #             {
    #                 'field_name': 'user.screen_name:CharField',
    #                 'field_type': 'CharField',
    #                 'operator': 'regex',
    #                 'value': 'jane'
    #             }, {
    #                 'field_name': 'user.age',
    #                 'field_type': 'IntegerField',
    #                 'operator': 'gte',
    #                 'value': '30'
    #             }, {
    #                 'field_name': 'content.text',
    #                 'field_type': 'CharField',
    #                 'operator': 'regex',
    #                 'value': 'cats'
    #             }
    #         ],
    #         'joiner': 'OR',
    #     }

    #     mongodb_docs = [
    #         self.mongodb_test_docs[0],
    #         self.mongodb_test_docs[1],
    #         self.mongodb_test_docs[2]
    #     ]
    #     es_docs = [self.es_test_docs[0], self.es_test_docs[2]]

    #     mock_mongodb = Mock()
    #     mock_es = Mock()
    #     with patch('engines.mongodb.engine.MongoDb', return_value=mock_mongodb):
    #         with patch('engines.elasticsearch.engine.ElasticSearch',
    #                    return_value=mock_es):
    #             mock_mongodb.find = Mock(return_value=mongodb_docs)
    #             mock_es.find = Mock(return_value={'results': es_docs})
    #             response = self.post_to_api('query/', self.query)
    #             self.assertEqual(len(response.data), 5)

    # def test_and_query(self):
    #     """
    #     Tests a query that joins terms with 'AND' logic.
    #     """
    #     query = {
    #         'collections': [2, 3],
    #         'fieldsets': [
    #             {
    #                 'field_name': 'user.screen_name',
    #                 'field_type': 'CharField',
    #                 'operator': 'regex',
    #                 'value': 'amy'
    #             }, {
    #                 'field_name': 'user.age',
    #                 'field_type': 'IntegerField',
    #                 'operator': 'gte',
    #                 'value': '25'
    #             }, {
    #                 'field_name': 'content.text',
    #                 'field_type': 'CharField',
    #                 'operator': 'regex',
    #                 'value': 'cats'
    #             }
    #         ],
    #         'joiner': 'AND',
    #     }

    #     mongodb_docs = []
    #     es_docs = [self.es_test_docs[2]]

    #     mock_mongodb = Mock()
    #     mock_es = Mock()
    #     with patch('engines.mongodb.engine.MongoDb', return_value=mock_mongodb):
    #         with patch('engines.elasticsearch.engine.ElasticSearch',
    #                    return_value=mock_es):
    #             mock_mongodb.find = Mock(return_value={'results': mock_mongodb})
    #             mock_es.find = Mock(return_value=es_docs)
    #             response = self.post_to_api('query/', self.query)
    #             self.assertEqual(len(response.data), 1)
