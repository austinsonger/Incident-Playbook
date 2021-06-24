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
Tests for the Engine base class.
"""

# third party
from django.test import TestCase

# local
from engines.engine import Engine
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures


class EngineBaseTestCase(TestCase):
    """
    Class for testing the Engine class.
    """

    fixtures = get_fixtures(['distilleries'])

    # schema used for tests:
    # 
    #    [
    #         {
    #             'key': 'user.screen_name',
    #             'type': 'CharField'
    #         },
    #         {
    #             'key': 'content.tags',
    #             'type': 'ListField'
    #         },
    #         {
    #             'key': 'user.active',
    #             'type': 'BooleanField'
    #         },
    #         {
    #             'key': 'created_at',
    #             'type': 'DateTimeField'
    #         },
    #         {
    #             'key': 'user.email',
    #             'type': 'EmailField'
    #         },
    #         {
    #             'key': 'content.rating',
    #             'type': 'FloatField'
    #         },
    #         {
    #             'key': 'user.age',
    #             'type': 'IntegerField'
    #         },
    #         {
    #             'key': 'host',
    #             'type': 'GenericIPAddressField'
    #         },
    #         {
    #             'key': 'location',
    #             'type': 'PointField'
    #         },
    #         {
    #             'key': 'content.link',
    #             'type': 'URLField'
    #         },
    #         {
    #             'key': 'status',
    #             'type': 'ChoiceField'
    #         }
    #     ]

    @staticmethod
    def _get_count(results):
        """
        Takes a results object (such as a list or cursor) and returns the number
        of documents it contains. This method should be implemented in each
        EngineBaseTestCase subclass.
        """
        raise NotImplementedError

    @staticmethod
    def _get_id(results, index):
        """
        Takes an list of results and a list index and returns the documentid
        for that index. This method is used to return document ids from
        different engines. As such, it should be customized in each
        EngineBaseTestCase subclass.
        """
        raise NotImplementedError

    @staticmethod
    def _get_doc(results, index):
        """
        Takes an list of results and a list index and returns the document
        for that index, stripping any additional fields added by the engine.
        This method is used to return documents from different engines in a
        standard format (with just the data from FilterTestCaseMixin.test_docs
        and no additional fields/nesting). As such, it should be customized in
        each EngineBaseTestCase subclass.
        """
        raise NotImplementedError


class EngineTestCase(EngineBaseTestCase):
    """
    Class for testing the Engine class.
    """
    def setUp(self):
        distillery = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_docs')
        self.engine = Engine(distillery.collection)

    def test_find_by_id(self):
        """
        Tests the find_by_id method.
        """
        with self.assertRaises(NotImplementedError):
            self.engine.find_by_id('xyz')

    def test_find(self):
        """
        Tests the find method.
        """
        with self.assertRaises(NotImplementedError):
            self.engine.find({'_id': 'xyz'})

    def test_filter_ids(self):
        """
        Tests the find_by_id method.
        """
        with self.assertRaises(NotImplementedError):
            self.engine.filter_ids(['1', '2'], ['foo', 'bar'], 'foobar')

    def test_insert(self):
        """
        Tests the insert method.
        """
        with self.assertRaises(NotImplementedError):
            self.engine.insert({'_id': 'xyz'})

    def test_remove_by_id(self):
        """
        Tests the remove_by_id method.
        """
        with self.assertRaises(NotImplementedError):
            self.engine.remove_by_id('xyz')


# TODO(LH): add tests for insert with DuplicateKeyError

