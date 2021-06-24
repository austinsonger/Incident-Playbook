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
Tests the Distillery class.
"""

# standard library
import copy
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
import dateutil.parser
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
from testfixtures import LogCapture

# local
from bottler.containers.models import Container
from cyphon.documents import DocumentObj
from distilleries.models import _DISTILLERY_SETTINGS, _PAGE_SIZE, Distillery
from tests.fixture_manager import get_fixtures
from warehouses.models import Collection


class DistilleryManagerTestCase(TestCase):
    """
    Tests the DistilleryManager class.
    """
    fixtures = get_fixtures(['distilleries', 'alerts'])

    def test_get_by_collection_nk(self):
        """
        Tests the get_by_natural_key method when the Distillery exists.
        """
        distillery = Distillery.objects.get_by_collection_nk('elasticsearch',
                                                             'test_index',
                                                             'test_mail')
        self.assertEqual(distillery.pk, 6)

    def test_natural_key_exception(self):
        """
        Tests the get_by_collection_nk method when the Distillery does not exist.
        """
        with LogCapture() as log_capture:
            natural_key = ['elasticsearch', 'test_index', 'fake_doctype']
            Distillery.objects.get_by_collection_nk(*natural_key)
            log_capture.check(
                ('warehouses.models',
                 'ERROR',
                 'Collection elasticsearch.test_index.fake_doctype does '
                 'not exist'),
                ('distilleries.models',
                 'ERROR',
                 'Distillery for Collection elasticsearch.test_index.'
                 'fake_doctype does not exist')
            )

    def test_have_alerts(self):
        """
        Tests the have_alerts method.
        """
        assert Distillery.objects.count() > 3
        have_alerts = Distillery.objects.have_alerts()
        self.assertEqual(have_alerts.count(), 3)


class DistilleryTestCaseMixin(object):
    """
    Mixin for testing the Distillery class.
    """
    time = timezone.now()

    data = {
        'text': 'this is an example post',
        'place': None,
        'timestamp_ms': '1424560411595',
        'id': int('123456789'),
        'favorited': False,
        'retweeted': False,
        'geo': None,
        'favorite_count': 0,
        'retweet_count': 0,
        'user': {
            'url': None,
            'protected': False,
            'statuses_count': 101,
            'screen_name': 'JohnSmith76',
            'geo_enabled': False,
            'profile_image_url': 'http://www.example.com/123.jpeg',
            'location': '',
            'id': 9999999,
            'friends_count': 1,
            'name': 'JohnSmith',
            'created_at': 'Mon Mar 04 07:04:44 +0000 2013',
            'id_str': '9999999',
        },
        'created_at': 'Sat Feb 21 23:13:31 +0000 2015',
        'id_str': '123456789',
        'truncated': False,
        'coordinates': None,
        'entities': {
            'media': [
                {
                    'media_url_https': 'https://pbs.twimg.com/media/123.jpg',
                }
            ]
        }
    }

    bottled_data = {
        'content': {
            'link': 'https://twitter.com/JohnSmith76/statuses/123456789',
            'text': 'this is an example post',
            'image': 'https://pbs.twimg.com/media/123.jpg'
        },
        'user': {
            'link': 'https://twitter.com/JohnSmith76/',
            'screen_name': 'JohnSmith76',
            'id': '9999999',
            'name': 'JohnSmith',
            'profile_pic': 'http://www.example.com/123.jpeg'
        },
        'location': None,
        'created_date': 'Sat Feb 21 23:13:31 +0000 2015'
    }

    meta = {
        _DISTILLERY_SETTINGS['DISTILLERY_KEY']: 1,
        _DISTILLERY_SETTINGS['PLATFORM_KEY']: 'twitter',
        _DISTILLERY_SETTINGS['RAW_DATA_KEY']: {
            _DISTILLERY_SETTINGS['DOC_ID_KEY']: '551d54e6f861c95f3123e5f6',
            _DISTILLERY_SETTINGS['BACKEND_KEY']: 'mongodb',
            _DISTILLERY_SETTINGS['WAREHOUSE_KEY']: 'test_database',
            _DISTILLERY_SETTINGS['COLLECTION_KEY']: 'twitter'
        },
        _DISTILLERY_SETTINGS['DATE_KEY']: time,
    }

    backend = 'mongodb'
    database = 'test_database'
    collection = 'test_posts'

    def _create_example_distillery(self):
        """
        Helper method that supplies an example Distillery.
        """
        container = Container.objects.get_by_natural_key('mail')
        collection = Collection.objects.get_by_natural_key(self.backend,
                                                           self.database,
                                                           self.collection)
        return Distillery(container=container, collection=collection)


class DistilleryTestCase(TestCase, DistilleryTestCaseMixin):
    """
    Tests the Distillery class.
    """
    fixtures = get_fixtures(['distilleries', 'funnels', 'tastes'])
    doc = {'foo': 'bar'}
    doc_obj = DocumentObj(
        collection='elasticsearch.cyphon.syslog',
        doc_id='1',
        data=doc
    )

    @classmethod
    def setUpTestData(cls):
        cls.distillery = cls._create_example_distillery(cls)

    def test_add_raw_data_info_for_none(self):
        """
        Tests the _add_raw_data_info method when no Collection name is
        given.
        """
        with LogCapture() as log_capture:
            doc_obj = self.doc_obj
            doc_obj.collection = None
            actual = self.distillery._add_raw_data_info(self.doc, doc_obj)
            expected = self.doc
            log_capture.check(
                ('cyphon.documents',
                 'ERROR',
                 'Info for raw data document None:1 could not be added'),
            )
            self.assertEqual(actual, expected)

    def test_add_raw_data_info_bad_str(self):
        """
        Tests the _add_raw_data_info method for a malformed collection string.
        """
        with LogCapture() as log_capture:
            doc_obj = self.doc_obj
            doc_obj.collection = 'bad_string'
            actual = self.distillery._add_raw_data_info(self.doc, doc_obj)
            expected = self.doc
            log_capture.check(
                ('cyphon.documents',
                 'ERROR',
                 'Info for raw data document bad_string:1 could not be added'),
            )
            self.assertEqual(actual, expected)

    def test_get_backend(self):
        """
        Tests the get_backend method.
        """
        self.assertEqual(self.distillery.get_backend(), 'mongodb')

    def test_get_warehouse_name(self):
        """
        Tests the get_backend_name method.
        """
        self.assertEqual(self.distillery.get_warehouse_name(), 'test_database')

    def test_get_collection(self):
        """
        Tests the get_collection_name method.
        """
        self.assertEqual(self.distillery.get_collection_name(), 'test_posts')

    def test_find(self):
        """
        Tests the find method.
        """
        mock_docs = Mock()
        mock_fieldsets = Mock()
        self.distillery.collection.find = Mock(return_value=mock_docs)

        docs = self.distillery.find(mock_fieldsets, 'AND')

        self.distillery.collection.find.assert_called_once_with(mock_fieldsets,
                                                                'AND', 1,
                                                                _PAGE_SIZE)
        self.assertEqual(docs, mock_docs)

    def test_filter_ids(self):
        """
        Tests the filter_ids method.
        """
        mock_doc_ids = [1, 2]
        test_ids = [1, 2, 3, 4]
        self.distillery.collection.filter_ids = Mock(return_value=mock_doc_ids)

        doc_ids = self.distillery.filter_ids_by_content(
            doc_ids=test_ids,
            value='cat'
        )

        bottled_with_meta = copy.deepcopy(self.bottled_data)
        bottled_with_meta.update(self.meta)
        call_args = self.distillery.collection.filter_ids.call_args[0]

        ids = call_args[0]
        field1 = call_args[1][0]
        field2 = call_args[1][1]
        field3 = call_args[1][2]
        field4 = call_args[1][3]
        value = call_args[2]

        self.assertEqual(ids, test_ids)

        self.assertEqual(field1.field_name, 'body')
        self.assertEqual(field1.field_type, 'TextField')
        self.assertEqual(field1.target_type, 'Keyword')

        self.assertEqual(field2.field_name, 'from')
        self.assertEqual(field2.field_type, 'EmailField')
        self.assertEqual(field2.target_type, 'Account')

        self.assertEqual(field3.field_name, 'priority')
        self.assertEqual(field3.field_type, 'CharField')
        self.assertEqual(field3.target_type, 'Keyword')

        self.assertEqual(field4.field_name, 'subject')
        self.assertEqual(field4.field_type, 'TextField')
        self.assertEqual(field4.target_type, 'Keyword')

        self.assertEqual(value, 'cat')

        self.assertEqual(doc_ids, mock_doc_ids)

    def test_get_sample(self):
        """
        Tests the get_sample method.
        """
        data = {
            '_raw_data': {
                'backend': 'elasticsearch',
                'database': 'test_index',
                'collection': 'test_docs'
            },
            'date': '2015-01-01T12:00:00-05:00',
            'from': 'test@account.com',
            'subject': 'This is a test',
            'body': 'This is only a test.'
        }

        actual = self.distillery.get_sample(data)

        expected = {
            'collection': 'elasticsearch.test_index.test_docs',
            'date': dateutil.parser.parse('2015-01-01T12:00:00-05:00'),
            'author': 'test@account.com',
            'title': 'This is a test',
            'content': 'This is only a test.',
            'location': None
        }

        self.assertEqual(actual, expected)

    def test_get_blind_sample_w_codebk(self):
        """
        Tests the get_blind_sample method for a Distillery with a
        CodeBook.
        """
        data = {'subject': 'test title'}
        sample = {'title': 'test title'}
        distillery = Distillery.objects.get_by_natural_key('mongodb.test_database.test_posts')
        with patch('distilleries.models.Distillery.container') \
                as mock_container:
            mock_container.get_blind_sample = Mock(return_value=sample)
            actual = distillery.get_blind_sample(data)
            mock_container.get_blind_sample.assert_called_once_with(
                data,
                distillery.codebook
            )
            self.assertEqual(actual, sample)

    def test_get_blind_sample_wo_codebk(self):
        """
        Tests the get_blind_sample method for a Distillery without a
        CodeBook.
        """
        data = {'subject': 'test title'}
        sample = {'title': 'test title'}
        with patch('distilleries.models.Distillery.container') \
                as mock_container:
            mock_container.get_sample = Mock(return_value=sample)
            actual = self.distillery.get_blind_sample(data)
            mock_container.get_sample.assert_called_once_with(data)
            self.assertEqual(actual, sample)


class SaveDataTestCase(TransactionTestCase, DistilleryTestCaseMixin):
    """
    Tests the save_data method of Distilleries.
    """
    fixtures = get_fixtures(['distilleries'])

    def setUp(self):
        self.distillery = self._create_example_distillery()

    def test_save_data(self):
        """
        Tests the save_data method.
        """
        mock_doc_id = 1
        self.distillery.collection.insert = Mock(return_value=mock_doc_id)

        doc_obj = DocumentObj(
            data=self.bottled_data,
            doc_id='551d54e6f861c95f3123e5f6',
            collection='mongodb.test_database.twitter',
            platform='twitter'
        )

        with patch('distilleries.models.timezone.now',
                   return_value=self.time):
            doc_id = self.distillery.save_data(doc_obj)

        bottled_with_meta = copy.deepcopy(self.bottled_data)
        bottled_with_meta.update(self.meta)
        self.distillery.collection.insert.assert_called_once_with(bottled_with_meta)
        self.assertEqual(doc_id, mock_doc_id)

# TODO(LH): test labeled doc
