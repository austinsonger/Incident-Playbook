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
from datetime import timedelta
import json

# third party
from django.utils import timezone

# local
from cyphon.fieldsets import QueryFieldset
from bottler.datafields.models import DataField
from engines.queries import EngineQuery
from engines.sorter import SortParam, Sorter


class CRUDTestCaseMixin(object):
    """
    Mixin for use with an a EngineBaseTestCase subclass. Provides tests
    for the CRUD methods of an Engine subclass.
    """

    def test_insert(self):
        """
        Tests the insert method.
        """
        test_text = 'this is an insert test post'
        doc_id = self.engine.insert({'text': test_text})

        result = self.engine.find_by_id(doc_id)
        self.assertEqual(self._get_id([result], 0), doc_id)
        self.assertEqual(self._get_doc([result], 0)['text'], test_text)

    def test_find_by_id_single(self):
        """
        Tests the find_by_id method for a single document.
        """
        test_text1 = 'this is a find_by_id test post'
        test_text2 = 'this is another find_by_id test post'

        doc_id1 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': test_text1
        })
        doc_id2 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 2
            },
            'text': test_text2
        })

        result = self.engine.find_by_id(doc_id1) # leave out doc_id2
        self.assertEqual(self._get_id([result], 0), doc_id1)
        self.assertEqual(self._get_doc([result], 0)['text'], test_text1)

    def test_find_by_id_single_no_match(self):
        """
        Tests the find_by_id method for a single document id that doesn't match
        any documents.
        """
        actual = self.engine.find_by_id(1)
        self.assertEqual(actual, None)

    def test_find_by_id_multiple(self):
        """
        Tests the find_by_id method for multiple documents.
        """
        test_text1 = 'this is a find_by_id test post'
        test_text2 = 'this is another find_by_id test post'
        test_text3 = 'yet another test post'

        doc_id1 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': test_text1
        })
        doc_id2 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 2
            },
            'text': test_text2
        })
        doc_id3 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 3
            },
            'text': test_text3
        })

        results = self.engine.find_by_id([doc_id1, doc_id2]) # leave out doc_id3
        expected_ids = [doc_id1, doc_id2]

        self.assertEqual(len(results), 2)
        self.assertIn(self._get_id(results, 0), expected_ids)
        self.assertIn(self._get_id(results, 1), expected_ids)
        self.assertEqual(self._get_doc(results, 0)['text'], test_text1)
        self.assertEqual(self._get_doc(results, 1)['text'], test_text2)

    def test_find_by_id_multi_no_match(self):
        """
        Tests the find_by_id method for multiple document ids that don't
        match any documents.
        """
        actual = self.engine.find_by_id([1, 2])
        self.assertEqual(actual, None)

    def test_remove_by_id_single(self):
        """
        Tests the remove_by_id method for a single document.
        """
        test_text = 'this is a remove_by_id test post'

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
        results = self.engine.find_by_id([doc_id])
        self.assertEqual(results, None)

    def test_remove_by_id_multiple(self):
        """
        Tests the remove_by_id method for multiple documents.
        """
        doc_id1 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            'text': 'a remove_by_id test post'
        })
        doc_id2 = self.engine.insert({
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 2
            },
            'text': 'another remove_by_id test post'
        })

        results = self.engine.find_by_id([doc_id1, doc_id2])
        self.assertEqual(len(results), 2)

        self.engine.remove_by_id([doc_id1, doc_id2])
        results = self.engine.find_by_id([doc_id1, doc_id2])
        self.assertEqual(results, None)


class FilterTestCaseMixin(object):
    """
    Mixin for use with a EngineBaseTestCase subclass to test the find() method
    of an Engine subclass. Provides tests for the standard set of query
    selectors (eq, gte, etc.) that are used in defining queries.
    """
    time = timezone.now()

    test_docs = [
        {
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 1
            },
            '_saved_date': time - timedelta(days=1),
            'user': {
                'screen_name': 'john',
                'email': 'john@example.com',
                'link': 'http://www.acme.com/john',
                'age': 20,
                'last_login': '2015-10-21 14:46:44.329193-04'
            },
            'content': {
                'text': 'I like cats.',
                'tags': ['cats', 'pets']
            },
            'location': [75.0, 25.0]
        },
        {
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 2
            },
            '_saved_date': time,
            'user': {
                'screen_name': 'jane',
                'email': 'jane@example.com',
                'link': 'http://www.acme.com/jane',
                'age': 30,
                'last_login': None
            },
            'content': {
                'text': 'I like dogs.',
                'tags': ['dogs', 'pets']
            },
            'location': [25.0, 25.0]
        },
        {
            '_raw_data': {
                'backend': 'example_backend',
                'database': 'example_database',
                'collection': 'raw_data',
                'doc_id': 3
            },
            '_saved_date': time + timedelta(days=1),
            'user': {
                'screen_name': 'jack',
                'email': 'jack@example.com',
                'link': 'http://www.acme.com/jack',
                'age': 30
            },
            'content': {
                'text': 'I LIKE CATS AND DOGS.',
                'tags': ['cats', 'dogs', 'pets']
            }
        }
    ]

    polygon1 = {
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [
                [[50.0, 0.0], [100.0, 0.0], [100.0, 50.0],
                 [50.0, 50.0], [50.0, 0.0]]
            ]
        }
    }

    polygon2 = {
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [
                [[0.0, 0.0], [100.0, 0.0], [100.0, 0.0],
                 [00.0, 50.0], [0.0, 0.0]]
            ]
        }
    }

    nonpolygon = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [100.0, 0.5]
        },
    }

    fieldsets = [
        QueryFieldset(
            field_name='content.text',
            field_type='TextField',
            operator='regex',
            value='cat'
        ),
        QueryFieldset(
            field_name='content.text',
            field_type='TextField',
            operator='regex',
            value='dog'
        )
    ]

    timeframe = [
        QueryFieldset(
            field_name='_saved_date',
            field_type='DateTimeField',
            operator='gte',
            value=time
        ),
        QueryFieldset(
            field_name='_saved_date',
            field_type='DateTimeField',
            operator='lte',
            value=time + timedelta(days=2)
        )
    ]

    def test_within_single_polygon(self):
        """
        Tests the find method using a 'within' filter for a feature collection
        with a single polygon.
        """
        features = {
            'type': 'FeatureCollection',
            'features': [self.polygon1]
        }

        fieldsets = [
            QueryFieldset(
                field_name='location',
                field_type='PointField',
                operator='within',
                value=json.dumps(features)
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_name = 'john'
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'],
                         expected_name)

    def test_within_multiple_polygons(self):
        """
        Tests the find method using a 'within' filter for a feature collection
        with more than one polygon.
        """
        features = {
            'type': 'FeatureCollection',
            'features': [self.polygon1, self.polygon2]
        }

        fieldsets = [
            QueryFieldset(
                field_name='location',
                field_type='PointField',
                operator='within',
                value=json.dumps(features)
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jane']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'],
                      expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'],
                      expected_names)

    def test_within_non_polygon(self):
        """
        Tests the find method using a 'within' filter for a feature collection
        that includes a non-polygon feature.
        """
        features = {
            'type': 'FeatureCollection',
            'features': [self.polygon1, self.nonpolygon]
        }

        fieldsets = [
            QueryFieldset(
                field_name='location',
                field_type='PointField',
                operator='within',
                value=json.dumps(features)
            )
        ]
        with self.assertRaises(ValueError):
            query = EngineQuery(fieldsets, 'AND')
            self.engine.find(query)

    def test_not_missing(self):
        """
        Tests the find method using a 'not missing' filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.last_login',
                field_type='DateTimeField',
                operator='not:missing',
                value=''
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_name = 'john'
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'],
                         expected_name)

    def test_regex_with_fragment(self):
        """
        Tests the find method using a 'regex' filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.text',
                field_type='TextField',
                operator='regex',
                value='cat'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jack']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_regex_with_caps(self):
        """
        Tests that 'regex' filter is not case-sensitive.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.text',
                field_type='TextField',
                operator='regex',
                value='CAT'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jack']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_regex_with_multiple_words(self):
        """
        Tests the 'regex' filter with multiple words.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.text',
                field_type='TextField',
                operator='regex',
                value='I like cats'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jack']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_regex_unmatched_quote(self):
        """
        Tests the find method for a 'regex' filter with a string
        containing an unmatched quotation mark.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.screen_name',
                field_type='CharField',
                operator='regex',
                value='"john'
            )
        ]

        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        self.assertEqual(count, 0)

    def test_not_regex_with_fragment(self):
        """
        Tests the find method for a 'not:regex' filter with a word fragment.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.screen_name',
                field_type='CharField',
                operator='not:regex',
                value='ja'
            )
        ]

        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'john')

    def test_not_regex_with_multi_words(self):
        """
        Tests the find method for a 'not:regex' filter with multiple words.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.text',
                field_type='TextField',
                operator='not:regex',
                value='I like cats and dogs'
            )
        ]

        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jane']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_and(self):
        """
        Tests the find method using two query terms joined by 'AND'.
        """
        query = EngineQuery(self.fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'jack')

    def test_or(self):
        """
        Tests the find method using two query terms joined by 'OR'.
        """
        query = EngineQuery(self.fieldsets, 'OR')
        results = self.engine.find(query)
        count = results['count']
        self.assertEqual(count, 3)

    def test_eq_numeric(self):
        """
        Tests the find method for an 'eq' (equals) filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.age',
                field_type='IntegerField',
                operator='eq',
                value='20'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'john')

    def test_eq_text(self):
        """
        Tests the find method for an 'eq' (equals) filter on a CharField.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.text',
                field_type='TextField',
                operator='eq',
                value='I like dogs.'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'jane')

    def test_eq_email(self):
        """
        Tests the find method for an 'eq' (equals) filter on an EmailField.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.email',
                field_type='EmailField',
                operator='eq',
                value='jane@example.com'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'jane')

    def test_in(self):
        """
        Tests the find method for an 'in' filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.tags',
                field_type='ListField',
                operator='in',
                value='cats'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jack']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_gt(self):
        """
        Tests the find method for a 'gt' (greater than) filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.age',
                field_type='IntegerField',
                operator='gt',
                value=20
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        expected_names = ['jane', 'jack']
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_gte(self):
        """
        Tests the find method for a 'gte' (greater than or equal to) filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.age',
                field_type='IntegerField',
                operator='gte',
                value=20
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        expected_names = ['jane', 'jack']
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 3)

    def test_lt(self):
        """
        Tests the find method for an 'lt' (less than) filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.age',
                field_type='IntegerField',
                operator='lt',
                value=30
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'john')

    def test_lte(self):
        """
        Tests the find method for an 'lte' (less than or equal to) filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.age',
                field_type='IntegerField',
                operator='lte',
                value=30
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 3)

    def test_not_eq(self):
        """
        Tests the find method for a 'not:eq' filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='user.screen_name',
                field_type='CharField',
                operator='not:eq',
                value='jack'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        expected_names = ['john', 'jane']
        self.assertEqual(count, 2)
        self.assertIn(self._get_doc(docs, 0)['user']['screen_name'], expected_names)
        self.assertIn(self._get_doc(docs, 1)['user']['screen_name'], expected_names)

    def test_not_in(self):
        """
        Tests the find method for a 'not:in' filter.
        """
        fieldsets = [
            QueryFieldset(
                field_name='content.tags',
                field_type='CharField',
                operator='not:in',
                value='cats'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        results = self.engine.find(query)
        count = results['count']
        docs = results['results']
        self.assertEqual(count, 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'jane')

    def test_find_fields(self):
        """
        Tests that the find method only returns fields defined in the
        Engine's schema.
        """
        doc_id = self.engine.insert({
            'content': {
                'text': 'I like cats and dogs.',
                'tags': ['cats', 'dogs'],
            },
            'user': {
                'screen_name': 'Jill',
                'email': 'jill@example.com',
            },
        })
        self.engine.schema = [
            DataField(
                field_name='content.text',
                field_type='TextField',
                target_type='Keyword'
            ),
            DataField(
                field_name='user.screen_name',
                field_type='CharField',
                target_type='Account'
            )
        ]

        fieldsets = [
            QueryFieldset(
                field_name='user.screen_name',
                field_type='CharField',
                operator='eq',
                value='Jill'
            )
        ]
        query = EngineQuery(fieldsets, 'AND')
        actual = self.engine.find(query)
        expected = {
            'count': 1,
            'results': [
                {
                    '_id': doc_id,
                    'content': {
                        'text': 'I like cats and dogs.'
                    },
                    'user': {
                        'screen_name': 'Jill'
                    }
                }
            ]
        }
        self.assertEqual(actual, expected)

    def test_find_tf_no_tf_and(self):
        """
        Tests the find method with no timeframe and an 'AND' joiner.
        """
        fieldsets = self.fieldsets
        joiner = 'AND'
        query = EngineQuery(fieldsets, joiner)
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 1)
        self.assertEqual(len(docs), 1)
        self.assertEqual(self._get_doc(docs, 0)['user']['screen_name'], 'jack')

    def test_find_tf_no_tf_or(self):
        """
        Tests the find method with no timeframe and an 'OR' joiner.
        """
        fieldsets = self.fieldsets
        joiner = 'OR'
        query = EngineQuery(fieldsets, joiner)
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 3)
        self.assertEqual(len(docs), 3)

    def test_find_tf_w_tf_and(self):
        """
        Tests the find method with a timeframe and an 'AND' joiner.
        """
        field_query = EngineQuery(self.fieldsets, 'AND')
        timeframe = self.timeframe
        subqueries = [field_query] + timeframe
        query = EngineQuery(subqueries, 'AND')
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 1)
        self.assertEqual(len(docs), 1)

    def test_find_tf_w_tf_or(self):
        """
        Tests the find method with a timeframe and an 'OR' joiner.
        """
        field_query = EngineQuery(self.fieldsets, 'OR')
        timeframe = self.timeframe
        subqueries = [field_query] + timeframe
        query = EngineQuery(subqueries, 'AND')
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 2)
        self.assertEqual(len(docs), 2)

    def test_find_tf_start_time_or(self):
        """
        Tests the find method with an endtime and an 'OR' joiner.
        """
        field_query = EngineQuery(self.fieldsets, 'OR')
        timeframe = [
            QueryFieldset(
                field_name='_saved_date',
                field_type='DateTimeField',
                operator='gte',
                value=self.time - timedelta(days=2)
            )
        ]
        subqueries = [field_query] + timeframe
        query = EngineQuery(subqueries, 'AND')
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 3)
        self.assertEqual(len(docs), 3)

    def test_find_tf_end_time_or(self):
        """
        Tests the find method with an endtime and an 'OR' joiner.
        """
        field_query = EngineQuery(self.fieldsets, 'OR')
        timeframe = [
            QueryFieldset(
                field_name='_saved_date',
                field_type='DateTimeField',
                operator='gte',
                value=self.time + timedelta(hours=1)
            )
        ]
        subqueries = [field_query] + timeframe
        query = EngineQuery(subqueries, 'AND')
        results = self.engine.find(query)
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 1)
        self.assertEqual(len(docs), 1)

    def test_find_pagination_sort(self):
        """
        Tests pagination and sorting of find results.
        """
        sorter = Sorter([
            SortParam(
                field_name='user.age',
                field_type='IntegerField',
                order='DESC'
            ),
            SortParam(
                field_name='user.screen_name',
                field_type='CharField',
                order='ASC'
            )
        ])
        field_query = EngineQuery(self.fieldsets, 'OR')
        results = self.engine.find(
            query=field_query,
            sorter=sorter,
            page=1,
            page_size=2
        )
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 3)
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]['user']['screen_name'], 'jack')

        results = self.engine.find(
            query=field_query,
            sorter=sorter,
            page=2,
            page_size=2
        )
        docs = results['results']
        count = results['count']
        self.assertEqual(count, 3)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['user']['screen_name'], 'john')

    def test_filter_ids_analyzed(self):
        """
        Tests the filter_ids method.
        """
        id_0 = self.engine.insert(self.test_docs[0])
        id_1 = self.engine.insert(self.test_docs[1])
        id_2 = self.engine.insert(self.test_docs[2])
        ids = [id_0, id_1, id_2]
        actual = self.engine.filter_ids(
            doc_ids=ids,
            fields=[
                DataField(field_name='content.text', field_type='TextField'),
                DataField(field_name='content.tags', field_type='ListField')
            ],
            value='CATS'
        )
        expected = [id_0, id_2]
        actual.sort()
        expected.sort()
        self.assertEqual(actual, expected)

    def test_filter_ids_not_analyzed(self):
        """
        Tests the filter_ids method for a mixture of exact-text and
        full-text fields in ELasticsearch.
        """
        id_0 = self.engine.insert(self.test_docs[0])
        id_1 = self.engine.insert(self.test_docs[1])
        id_2 = self.engine.insert(self.test_docs[2])
        ids = [id_0, id_1, id_2]
        actual = self.engine.filter_ids(
            doc_ids=ids,
            fields=[
                DataField(field_name='user.link', field_type='URLField'),
                DataField(field_name='user.email', field_type='EmailField')
            ],
            value='example'
        )
        expected = [id_0, id_1, id_2]
        actual.sort()
        expected.sort()
        self.assertEqual(actual, expected)

    def test_filter_ids_mixed(self):
        """
        Tests the filter_ids method for a mixture of exact-text and
        full-text fields in ELasticsearch.
        """
        id_0 = self.engine.insert(self.test_docs[0])
        id_1 = self.engine.insert(self.test_docs[1])
        id_2 = self.engine.insert(self.test_docs[2])
        ids = [id_0, id_1, id_2]
        actual = self.engine.filter_ids(
            doc_ids=ids,
            fields=[
                DataField(field_name='content.text', field_type='TextField'),
                DataField(field_name='user.email', field_type='EmailField')
            ],
            value='example'
        )
        expected = [id_0, id_1, id_2]
        actual.sort()
        expected.sort()
        self.assertEqual(actual, expected)

