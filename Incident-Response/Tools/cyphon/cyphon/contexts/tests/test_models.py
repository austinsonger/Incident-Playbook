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
Tests the Context class.
"""

# standard library
from datetime import timedelta
import logging
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
import six
from testfixtures import LogCapture

# local
from cyphon.fieldsets import QueryFieldset
from contexts.models import Context, ContextFilter
from tests.fixture_manager import get_fixtures


class ContextBaseTestCase(TestCase):
    """
    Test case for the Context class.
    """
    fixtures = get_fixtures(['contexts'])

    def setUp(self):
        logging.disable(logging.WARNING)
        self.context_w_filters = Context.objects.get(pk=1)
        self.context_wo_focal_taste = Context.objects.get(pk=2)
        self.context_wo_related_taste = Context.objects.get(pk=3)
        self.context_wo_filters = Context.objects.get(pk=4)
        self.context_wo_time_frame = Context.objects.get(pk=5)

    def tearDown(self):
        logging.disable(logging.NOTSET)


class ContextManagerTestCase(ContextBaseTestCase):
    """
    Tests the ContextManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for an existing Context.
        """
        key = ['context_w_filters', 'mongodb.test_database.test_posts']
        context = Context.objects.get_by_natural_key(*key)
        self.assertEqual(context.pk, 1)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method for a Context that doesn't
        exist.
        """
        with LogCapture() as log_capture:
            key = ['dummy_context', 'mongodb.test_database.test_posts']
            Context.objects.get_by_natural_key(*key)
            expected = ('Context dummy_context:mongodb.test_database.'
                        'test_posts does not exist')
            log_capture.check(
                ('contexts.models', 'ERROR', expected),
            )


class ContextTestCase(ContextBaseTestCase):
    """
    Test case for the Context class.
    """

    def test_str(self):
        """
        Tests the __str__ method for a Context.
        """
        self.assertEqual(str(self.context_w_filters), 'context_w_filters')

    def test_get_before_intrvl_in_secs(self):
        """
        Tests the _get_before_interval_in_seconds method for a Context with
        both a before_time_interval and before_time_unit.
        """
        actual = self.context_w_filters._get_before_interval_in_seconds()
        expected = 300
        self.assertEqual(actual, expected)

    def test_get_before_intrvl_no_time(self):
        """
        Tests the _get_before_interval_in_seconds method for a Context without
        a before_time_interval.
        """
        self.context_w_filters.before_time_interval = None
        actual = self.context_w_filters._get_before_interval_in_seconds()
        expected = 0
        self.assertEqual(actual, expected)

    def test_get_before_intrvl_no_unit(self):
        """
        Tests the _get_before_interval_in_seconds method for a Context without
        a before_time_unit.
        """
        self.context_w_filters.before_time_unit = None
        actual = self.context_w_filters._get_before_interval_in_seconds()
        expected = 0
        self.assertEqual(actual, expected)

    def test_get_end_time_wo_taste(self):
        """
        Tests the _get_end_time method for a Context whose focal
        distillery has a container without a taste.
        """
        data = {'host': 'foo', 'message': 'bar'}
        context = self.context_wo_focal_taste
        assert not hasattr(context.primary_distillery.container, 'taste')
        actual = context._get_end_time(data)
        expected = None
        self.assertEqual(actual, expected)

    def test_get_end_time_w_taste(self):
        """
        Tests the _get_end_time method for a Context whose focal
        distillery has a container with a taste.
        """
        time = timezone.now()
        end_time = time + timedelta(seconds=5)
        data = {'date': time, 'body': 'bar'}
        context = self.context_wo_related_taste
        assert hasattr(context.primary_distillery.container, 'taste')
        self.assertEqual(context._get_end_time(data), end_time)

    def test_get_end_time_wo_date(self):
        """
        Tests the _get_end_time method for a Context whose focal
        distillery has a container with a taste but the date field is
        not present in the data.
        """
        data = {'body': 'bar'}
        context = self.context_wo_related_taste
        assert hasattr(context.primary_distillery.container, 'taste')
        actual = context._get_end_time(data)
        expected = None
        self.assertEqual(actual, expected)

    def test_get_start_time(self):
        """
        Tests the _get_start_time method when _get_before_interval_in_seconds
        returns a value.
        """
        time = timezone.now()
        data = {'date': time, 'body': 'bar'}
        context = self.context_wo_related_taste
        actual = context._get_start_time(data)
        expected = time - timedelta(minutes=10)
        self.assertEqual(actual, expected)

    def test_get_start_wo_before(self):
        """
        Tests the _get_start_time method when before_time_interval is 0.
        """
        time = timezone.now()
        data = {'date': time, 'body': 'bar'}
        context = Context.objects.get(pk=4)
        actual = context._get_start_time(data)
        expected = time
        self.assertEqual(actual, expected)

    def test_get_end_wo_after(self):
        """
        Tests the _get_end_time method when after_time_interval is 0.
        """
        time = timezone.now()
        data = {'created_date': time, 'body': 'bar'}
        context = self.context_w_filters
        context.after_time_interval = 0
        actual = context._get_end_time(data)
        expected = time
        self.assertEqual(actual, expected)

    def test_time_fieldsets_no_taste(self):
        """
        Tests the _create_timeframe_query method when the related_distillery's
        container has no associated taste.
        """
        data = {'body': 'bar'}
        context = self.context_wo_related_taste
        query = context._create_timeframe_query(data)
        self.assertEqual(query, None)

    def test_time_fieldsets_no_intrvl(self):
        """
        Tests the _create_timeframe_query method when the context when
        no time frame is given.
        """
        context = self.context_wo_related_taste
        data = {'body': 'bar'}
        context.before_time_interval = 0
        context.after_time_interval = 0
        query = context._create_timeframe_query(data)
        self.assertEqual(query, None)

    def test_clean_wo_focal_taste_sh(self):
        """
        Tests the clean method when a time frame is specified,
        the primary_distillery has no taste, and the primary_distillery
        is a shell.
        """
        context = self.context_wo_focal_taste
        context.primary_distillery.is_shell = True
        msg = ('A time frame is specified, but the primary '
               'distillery\'s Container has no designated date '
               'field. Please make sure the Container has a Taste '
               'with a date field.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            context.clean()

    def test_clean_wo_focal_date_sh(self):
        """
        Tests the clean method when a time frame is specified,
        the primary_distillery has a taste without a defined date field,
        and the primary_distillery is a shell.
        """
        context = self.context_wo_filters
        context.primary_distillery.taste.datetime = None
        context.primary_distillery.is_shell = True
        msg = ('A time frame is specified, but the primary '
               'distillery\'s Container has no designated date '
               'field. Please make sure the Container has a Taste '
               'with a date field.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            context.clean()

    def test_clean_wo_related_taste_sh(self):
        """
        Tests the clean method when a time frame is specified,
        the related_distillery has no taste, and the related_distillery
        is a shell.
        """
        context = self.context_wo_related_taste
        context.related_distillery.is_shell = True
        msg = ('A time frame is specified, but the related '
               'distillery\'s Container has no designated date '
               'field. Please make sure the Container has a Taste '
               'with a date field.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            context.clean()

    def test_clean_wo_related_date_sh(self):
        """
        Tests the clean method when a time frame is specified,
        the related_distillery has a taste without a defined date field,
        and the related_distillery is a shell.
        """
        context = self.context_w_filters
        context.related_distillery.is_shell = True
        msg = ('A time frame is specified, but the related '
               'distillery\'s Container has no designated date '
               'field. Please make sure the Container has a Taste '
               'with a date field.')
        with six.assertRaisesRegex(self, ValidationError, msg):
            context.clean()

    def test_clean_wo_focal_taste(self):
        """
        Tests the clean method when a time frame is specified and the
        primary_distillery has no taste, but the primary_distillery is not
        a shell.
        """
        context = self.context_wo_focal_taste
        try:
            context.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_clean_wo_related_taste(self):
        """
        Tests the clean method when a time frame is specified and the
        related_distillery has no taste, but the primary_distillery is not
        a shell.
        """
        context = self.context_wo_related_taste
        try:
            context.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_clean_wo_time_frame(self):
        """
        Tests the clean method when the primary_distillery and
        related_distillery have no designated date fields and no time
        frame is specified.
        """
        context = self.context_wo_time_frame
        try:
            context.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_clean_w_time_frame(self):
        """
        Tests the clean method when the primary_distillery and
        related_distillery have designated date fields and a time
        frame is specified.
        """
        context = self.context_w_filters
        try:
            context.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_get_focal_distill_fields(self):
        """
        Tests the get_primary_distillery_fields method.
        """
        actual = self.context_wo_focal_taste.get_primary_distillery_fields()
        expected = ['date_str', 'host', 'message']
        self.assertEqual(actual, expected)

    def test_get_related_distill_fields(self):
        """
        Tests the get_related_distillery_fields method.
        """
        actual = self.context_wo_focal_taste.get_related_distillery_fields()
        expected = ['body', 'date', 'from', 'priority', 'subject']
        self.assertEqual(actual, expected)

    @patch('distilleries.models.Distillery.find')
    def test_get_related_data_timeout(self, mock_find):
        """
        Tests the get_related_data method for a Context when the query
        cannot be completed.
        """
        data = {'host': 'foo', 'message': 'bar'}
        actual = self.context_w_filters.get_related_data(
            data, page=1, page_size=10)
        expected = {
            'distillery': 'elasticsearch.test_index.test_docs',
            'error': ('The query could not be completed. '
                      'Please increase the timeout setting '
                      'or try again later.')
        }
        self.assertEqual(actual, expected)

    @patch('distilleries.models.Distillery.find')
    @patch('contexts.models.Context._create_filter_query', return_value=None)
    @patch('contexts.models.Context._create_timeframe_query', return_value=None)
    def test_get_related_data_wo_params(self, mock_tf, mock_filter, mock_find):
        """
        Tests the get_related_data method for a Context without a defined
        time frame or ContextFilters.
        """
        data = {'host': 'foo', 'message': 'bar'}
        actual = self.context_wo_focal_taste.get_related_data(
            data, page=1, page_size=10)
        expected = {
            'distillery': 'elasticsearch.test_index.test_mail',
            'error': ('No query parameters available for searching '
                      'related data. Please define a time interval, '
                      'keyword, or filters for the Context.')
        }
        mock_find.assert_not_called()
        self.assertEqual(actual, expected)

    def test_get_related_data_wo_filter(self):
        """
        Tests the get_related_data method for a Context with a defined
        time frame but no ContextFilters.
        """
        time = timezone.now()
        data = {'date': time, 'host': 'foo', 'message': 'bar'}
        mock_results = {
            'count': 1,
            'results': [{'foo2': 'bar2'}]
        }
        with patch('distilleries.models.Distillery.find',
                   return_value=mock_results) as mock_find:
            results = self.context_wo_filters.get_related_data(
                data, page=1, page_size=10)
            expected_timeframe = [
                {
                    'operator': 'gt',
                    'field_type': 'DateTimeField',
                    'field_name': 'created_date',
                    'value': time
                },
                {
                    'operator': 'lte',
                    'field_type': 'DateTimeField',
                    'field_name': 'created_date',
                    'value': time + timedelta(minutes=60)
                }
            ]
            expected_results = {
                'distillery': 'mongodb.test_database.test_posts',
                'count': 1,
                'results': [{'foo2': 'bar2'}]
            }
            self.assertEqual(mock_find.call_count, 1)
            query = mock_find.call_args[0][0]
            timeframe = [vars(q) for q in query.subqueries[0].subqueries]
            self.assertEqual(timeframe, expected_timeframe)
            self.assertEqual(query.joiner, 'AND')
            self.assertEqual(query.subqueries[0].joiner, 'AND')
            self.assertEqual(results, expected_results)

    def test_get_related_data_w_keyword(self):
        """
        Tests the get_related_data method for a Context with a defined
        time frame and a keyword but no ContextFilters.
        """
        time = timezone.now()
        data = {'date': time, 'host': 'foo', 'message': 'bar'}
        mock_results = {
            'count': 1,
            'results': [{'foo2': 'bar2'}]
        }
        with patch('distilleries.models.Distillery.find',
                   return_value=mock_results) as mock_find:
            results = self.context_wo_filters.get_related_data(
                data, keyword='foobar', page=1, page_size=10)
            expected_timeframe = [
                {
                    'operator': 'gt',
                    'field_type': 'DateTimeField',
                    'field_name': 'created_date',
                    'value': time
                },
                {
                    'operator': 'lte',
                    'field_type': 'DateTimeField',
                    'field_name': 'created_date',
                    'value': time + timedelta(minutes=60)
                }
            ]
            expected_keyword = [{
                'value': 'foobar',
                'operator': 'regex',
                'field_name': '_metadata.priority',
                'field_type': 'CharField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'content.image',
                'field_type': 'URLField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'content.link',
                'field_type': 'URLField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'content.text',
                'field_type': 'TextField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'content.title',
                'field_type': 'TextField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'content.video',
                'field_type': 'URLField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.email',
                'field_type': 'EmailField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.id',
                'field_type': 'CharField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.link',
                'field_type': 'URLField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.name',
                'field_type': 'CharField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.profile_pic',
                'field_type': 'URLField'
            }, {
                'value': 'foobar',
                'operator': 'regex',
                'field_name': 'user.screen_name',
                'field_type': 'CharField'
            }]

            expected_results = {
                'distillery': 'mongodb.test_database.test_posts',
                'count': 1,
                'results': [{'foo2': 'bar2'}]
            }
            self.assertEqual(mock_find.call_count, 1)
            query = mock_find.call_args[0][0]
            keyword = [vars(q) for q in query.subqueries[0].subqueries]
            timeframe = [vars(q) for q in query.subqueries[1].subqueries]
            self.assertEqual(keyword, expected_keyword)
            self.assertEqual(timeframe, expected_timeframe)
            self.assertEqual(query.joiner, 'AND')
            self.assertEqual(query.subqueries[0].joiner, 'OR')
            self.assertEqual(query.subqueries[1].joiner, 'AND')
            self.assertEqual(results, expected_results)

    def test_get_related_data_w_filters(self):
        """
        Tests the get_related_data method for a Context with a defined
        time frame and ContextFilters.
        """
        time = timezone.now()
        data = {
            'created_date': time,
            'host': 'foo',
            'content': {
                'message': 'bar'
            }
        }
        mock_results = {
            'count': 1,
            'results': [{'foo2': 'bar2'}]
        }
        with patch('distilleries.models.Distillery.find',
                   return_value=mock_results) as mock_find:
            results = self.context_w_filters.get_related_data(
                data, page=1, page_size=10)
            expected_fieldsets = [
                {
                    'field_name': 'content.subject',
                    'field_type': 'TextField',
                    'operator': 'eq',
                    'value': 'bar'
                },
                {
                    'field_name': 'from',
                    'field_type': 'EmailField',
                    'operator': 'eq',
                    'value': 'foo'
                }
            ]
            expected_timeframe = [
                {
                    'field_name': '_saved_date',
                    'field_type': 'DateTimeField',
                    'operator': 'gt',
                    'value': time - timedelta(minutes=5)
                },
                {
                    'field_name': '_saved_date',
                    'field_type': 'DateTimeField',
                    'operator': 'lte',
                    'value': time + timedelta(seconds=10)
                }
            ]
            expected_results = {
                'distillery': 'elasticsearch.test_index.test_docs',
                'count': 1,
                'results': [{'foo2': 'bar2'}]
            }

            self.assertEqual(mock_find.call_count, 1)
            query = mock_find.call_args[0][0]
            fieldsets = [vars(q) for q in query.subqueries[0].subqueries]
            timeframe = [vars(q) for q in query.subqueries[1].subqueries]
            self.assertEqual(fieldsets, expected_fieldsets)
            self.assertEqual(timeframe, expected_timeframe)
            self.assertEqual(query.subqueries[0].joiner, 'AND')
            self.assertEqual(query.subqueries[1].joiner, 'AND')
            self.assertEqual(results, expected_results)

    def test_get_related_data_by_id(self):
        """
        Tests the get_related_data_by_id method.
        """
        doc_id = '1'
        mock_data = {'host': 'foo', 'message': 'bar'}
        mock_results = {
            'count': 1,
            'results': [{'foo2': 'bar2'}]
        }
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=mock_data) as mock_find_by_id:
            with patch('distilleries.models.Distillery.find',
                       return_value=mock_results):
                actual = self.context_w_filters.get_related_data_by_id(
                    doc_id, page=1, page_size=10)
                expected = {
                    'distillery': 'elasticsearch.test_index.test_docs',
                    'count': 1,
                    'results': [{'foo2': 'bar2'}]
                }
                mock_find_by_id.assert_called_once_with(doc_id)
                self.assertEqual(actual, expected)

    @patch('distilleries.models.Distillery.find_by_id', return_value=None)
    @patch('distilleries.models.Distillery.find')
    def test_get_by_id_no_data(self, mock_find, mock_find_by_id):
        """
        Tests the get_related_data_by_id method when the document
        associated with the given doc_id cannot be found.
        """
        doc_id = '1'
        actual = self.context_w_filters.get_related_data_by_id(
            doc_id, page=1, page_size=10)
        expected = {'error': 'The document associated with '
                             'the id could not be found.'}
        mock_find_by_id.assert_called_once_with(doc_id)
        self.assertEqual(actual, expected)


class ContextFilterManagerTestCase(ContextBaseTestCase):
    """
    Tests the ContextFilterManager class.
    """

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method for an existing ContextFilter.
        """
        key = ['context_w_filters', 'mongodb.test_database.test_posts',
               'host', 'from']
        context = ContextFilter.objects.get_by_natural_key(*key)
        self.assertEqual(context.pk, 1)

    @staticmethod
    def test_natural_key_exception():
        """
        Tests the get_by_natural_key method for a ContextFilter that
        doesn't exist.
        """
        with LogCapture() as log_capture:
            key = ['dummy_context', 'mongodb.test_database.test_posts',
                   'host', 'from']
            ContextFilter.objects.get_by_natural_key(*key)
            expected_1 = ('Context dummy_context:mongodb.test_database.'
                          'test_posts does not exist')
            expected_2 = ('ContextFilter dummy_context:mongodb.test_database.'
                          'test_posts (host -> from) does not exist')
            log_capture.check(
                ('contexts.models', 'ERROR', expected_1),
                ('contexts.models', 'ERROR', expected_2)
            )


class ContextFilterTestCase(ContextBaseTestCase):
    """
    Test case for the ContextFilter class.
    """

    def test_invalid_value_field(self):
        """
        Tests the clean() method of a ContextFilter when the value_field
        is invalid.
        """
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='host',
            operator='eq',
            search_field='from'
        )
        msg = 'The value field "host" is not a field in the Container used '\
              'by the Focal Distillery mongodb.test_database.test_posts.'
        with six.assertRaisesRegex(self, ValidationError, msg):
            context_filter.clean()

    def test_invalid_search_field(self):
        """
        Tests the clean() method of a ContextFilter when the
        search_field is invalid.
        """
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='user.email',
            operator='eq',
            search_field='host'
        )
        msg = 'The search field "host" is not a field in the Container used '\
              'by the Related Distillery elasticsearch.test_index.test_docs.'
        with six.assertRaisesRegex(self, ValidationError, msg):
            context_filter.clean()

    def test_valid_filter(self):
        """
        Tests the clean() method of a ContextFilter when the value_field
        and search_field are valid.
        """
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='user.email',
            operator='regex',
            search_field='user.email'
        )
        try:
            context_filter.clean()
        except ValidationError:
            self.fail('A ValidationError was raised unexpectedly')

    def test_create_fieldset(self):
        """
        Tests the create_fieldset method of a ContextFilter.
        """
        data = {'host': 'foo', 'message': 'bar'}
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='host',
            operator='eq',
            search_field='from'
        )
        fieldset = context_filter.create_fieldset(data)

        self.assertEqual(type(fieldset), QueryFieldset)
        self.assertEqual(fieldset.field_name, 'from')
        self.assertEqual(fieldset.field_type, 'EmailField')
        self.assertEqual(fieldset.operator, 'eq')
        self.assertEqual(fieldset.value, 'foo')

    def test_operator_text(self):
        """
        Tests that the property 'operator_text' returns a human readable
        version of operator.
        """
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='host',
            operator='eq',
            search_field='from'
        )
        self.assertEqual(context_filter.operator_text, 'equals')

    def test_failed_operator_text(self):
        """
        Tests that the operator value will be returned if it cannot find
        a match in the operator choices.
        """
        context_filter = ContextFilter(
            context=self.context_w_filters,
            value_field='host',
            operator='meh',
            search_field='from'
        )
        self.assertEqual(context_filter.operator_text, 'meh')
