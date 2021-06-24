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
Tests Alert model methods.
"""

# standard library
import datetime
import logging
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

# local
from alerts.models import Alert, Comment
from companies.models import Company
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures
from tests.mock import patch_find_by_id
from watchdogs.models import Watchdog


NOW_DATE = timezone.now()

RAW_DATA = {
    'backend': 'elasticsearch',
    'database': 'test_index',
    'collection': 'test_docs',
}

DOC_W_DATE = {
    '_raw_data': RAW_DATA,
    'date': str(NOW_DATE),
    'from': 'me@example.com',
    'subject': 'Welcome to Acme Supply Co',
    'body': 'example text',
}

DOC_W_BAD_DATE = {
    '_raw_data': RAW_DATA,
    'date': 'whenever',
    'from': 'me@example.com',
    'subject': 'Thanks from Acme Supply Co',
    'body': 'example text',
}

DOC_WO_DATE = {
    '_raw_data': RAW_DATA,
    'from': 'me@example.com',
    'subject': 'Sale at Acme Supply Co',
    'body': 'example text',
}

DOC_W_TIMESTAMP = {
    '_raw_data': RAW_DATA,
    'date': '1444316990',
    'from': 'me@example.com',
    'subject': 'mock doc with timestamp',
    'body': 'example text',
}

DOC_W_DATE_OBJ = {
    '_raw_data': RAW_DATA,
    'date': NOW_DATE,
    'from': 'me@example.com',
    'subject': 'mock doc with datetime obj',
    'body': 'example text',
}


class AlertModelTestCase(TestCase):
    """
    Base class for testing the Alert class.
    """
    fixtures = get_fixtures(['alerts', 'comments'])

    @property
    def distillery(self):
        """
        Edit distillery so that it has a Company with a Codebook.
        """
        distillery = Distillery.objects.get_by_natural_key(
            'elasticsearch.test_index.test_mail')
        distillery.company = Company.objects.get(pk=1)
        distillery.save()
        return distillery

    @property
    def watchdog(self):
        return Watchdog.objects.get(pk=1)

    def _get_alert(self):
        """
        Returns a fresh instance of an Alert to access cached properties.
        """
        if self.alert.pk:
            return Alert.objects.get(pk=self.alert.pk)
        else:
            return self.alert

    def setUp(self):
        self.alert = Alert(
            level='HIGH',
            status=0,
            distillery=self.distillery,
            doc_id=1,
            alarm=self.watchdog
        )

        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)


class AlertCompanyTestCase(AlertModelTestCase):
    """
    Tests the company property.
    """

    def test_with_company(self):
        """
        Tests the company property when the Alert's Distillery has a
        company.
        """
        alert = Alert.objects.get(pk=4)
        company = Company.objects.get(pk=1)
        self.assertEqual(alert.company, company)

    def test_without_company(self):
        """
        Tests the company property when the Alert's Distillery has no
        company.
        """
        alert = Alert.objects.get(pk=1)
        self.assertEqual(alert.company, None)

    def test_without_distillery(self):
        """
        Tests the company property when the Alert has no Distillery.
        """
        alert = Alert.objects.get(pk=7)
        self.assertEqual(alert.company, None)


class AlertMuzzleHashTestCase(AlertModelTestCase):
    """
    Tests the save method with respect to an Alert's muzzle_hash.
    """

    def test_duplicate_alert(self):
        """
        Checks that duplicate muzzle hashes are not generated when Alert
        levels are changed.
        """
        new_alert = Alert.objects.get(pk=1)
        new_alert.pk = None
        new_alert.level = 'MEDIUM'
        new_alert.save()

        # create a potential duplicate alert
        old_alert = Alert.objects.get(pk=1)
        old_alert.level = 'MEDIUM'
        try:
            old_alert.save()
        except IntegrityError:
            self.fail('Alert raised IntergrityError unexpectedly')


class AlertContentDateTestCase(AlertModelTestCase):
    """
    Tests the save method with respect to an Alert's content_date.
    """

    @patch_find_by_id(DOC_W_DATE)
    def test_update_alert(self):
        """
        Tests the save method for an Alert that already exists in the database.
        """
        alert = Alert.objects.get(pk=1)
        before_date = alert.content_date
        alert.save()
        after_date = alert.content_date
        self.assertEqual(before_date, after_date)

    @patch_find_by_id(DOC_W_DATE)
    def test_save_alert_w_date_str(self):
        """
        Tests the save method of an Alert when the teaser data for the
        original document includes a datetime string.
        """
        self.alert.data = None
        self.alert.save()
        actual = self.alert.content_date
        expected = NOW_DATE
        self.assertEqual(actual, expected)

    @patch_find_by_id(DOC_W_TIMESTAMP)
    def test_save_alert_w_timestamp(self):
        """
        Tests the save method of an Alert when the teaser data for the
        original document includes a date that's a timestamp string.
        """
        self.alert.data = None
        self.alert.save()
        utc = datetime.timezone.utc
        actual = self.alert.content_date
        expected = datetime.datetime.fromtimestamp(1444316990, tz=utc)
        self.assertEqual(actual, expected)

    @patch_find_by_id(DOC_W_DATE_OBJ)
    def test_save_alert_w_date_obj(self):
        """
        Tests the save method of an Alert when the teaser data for the
        original document includes a date that's a datetime object.
        """
        self.alert.save()
        saved_date = self.alert.content_date
        origin_date = NOW_DATE
        timedelta = origin_date - saved_date
        actual = timedelta.total_seconds()
        expected = 0
        self.assertAlmostEqual(actual, expected, places=2)

    @patch_find_by_id(DOC_W_BAD_DATE)
    def test_save_alert_w_bad_date(self):
        """
        Tests the save method of an Alert when the date for the orginal
        document is not parsible.
        """
        self.alert.save()
        actual = self.alert.content_date
        expected = None
        self.assertEqual(actual, expected)

    @patch_find_by_id(DOC_WO_DATE)
    def test_save_alert_wo_date(self):
        """
        Tests the save method of an Alert when no date for the orginal
        document is available.
        """
        self.alert.save()
        actual = self.alert.content_date
        expected = None
        self.assertEqual(actual, expected)


class AlertTitleTestCase(AlertModelTestCase):
    """
    Tests the save method with respect to an Alert's title.
    """

    def setUp(self):
        super(AlertTitleTestCase, self).setUp()
        self.max_length = Alert._meta.get_field('title').max_length

    def tearDown(self):
        super(AlertTitleTestCase, self).tearDown()
        Alert._meta.get_field('title').max_length = self.max_length

    @patch_find_by_id(DOC_W_DATE)
    def test_update_alert_same_title(self):
        """
        Tests the save method for an Alert that already exists in the
        database and currently has a title, and the title of the
        original document has not changed.
        """
        self.alert.save()

        # get fresh instance for cached_properties
        updated_alert = Alert.objects.get(pk=self.alert.pk)
        updated_alert.save()
        actual = updated_alert.title
        expected = DOC_W_DATE['subject']
        self.assertEqual(actual, expected)

    def test_update_alert_missing_title(self):
        """
        Tests the save method for an Alert that already exists in the
        database and currently has a title, but the original document
        can no longer be found.
        """
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=DOC_W_DATE):
            self.alert.save()
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=None):
            # get fresh instance for cached_properties
            updated_alert = Alert.objects.get(pk=self.alert.pk)
            updated_alert.save()
            actual = updated_alert.title
            expected = DOC_W_DATE['subject']
            self.assertEqual(actual, expected)

    @patch_find_by_id(None)
    def test_alert_has_no_doc(self):
        """
        Tests the save method of a new Alert when the orginal document
        is not available.
        """
        self.alert.save()
        actual = self.alert.title
        expected = None
        self.assertEqual(actual, expected)

    @patch_find_by_id({'subject': ''})
    def test_alert_has_no_title(self):
        """
        Tests the save method of a new Alert when the title for the
        orginal document is an empty string.
        """
        self.alert.save()
        actual = self.alert.title
        expected = ''
        self.assertEqual(actual, expected)

    @patch_find_by_id({'subject': None})
    def test_alert_title_is_none(self):
        """
        Tests the save method of a new Alert when the title for the
        orginal document is None.
        """
        self.alert.save()
        actual = None
        expected = self.alert.title
        self.assertEqual(actual, expected)

    @patch_find_by_id({'subject': '0123456789'})
    def test_alert_title_over_limit(self):
        """
        Tests the save method of a new Alert when the title for the
        orginal document exceeds the character limit setting.
        """
        Alert._meta.get_field('title').max_length = 9
        self.alert.save()
        actual = self.alert.title
        expected = '012345678'
        self.assertEqual(actual, expected)

    @patch_find_by_id({'subject': '0123456789'})
    def test_alert_title_at_limit(self):
        """
        Tests the save method of a new Alert when the title for the
        orginal document is at the character limit setting.
        """
        Alert._meta.get_field('title').max_length = 10
        self.alert.save()
        actual = self.alert.title
        expected = '0123456789'
        self.assertEqual(actual, expected)

    @patch_find_by_id({'subject': '0123456789'})
    def test_alert_title_under_limit(self):
        """
        Tests the save method of a new Alert when the title for the
        orginal document is under the character limit setting.
        """
        Alert._meta.get_field('title').max_length = 11
        self.alert.save()
        actual = self.alert.title
        expected = '0123456789'
        self.assertEqual(actual, expected)


class AlertSavedDataTestCase(AlertModelTestCase):
    """
    Tests the saved_data property of an Alert.
    """

    def test_data_without_distillery(self):
        """
        Tests the saved_data property when the Alert has no Distillery.
        """
        self.alert.distillery = None
        self.assertEqual(self.alert.saved_data, {})

    @patch_find_by_id(None)
    def test_data_without_match(self):
        """
        Tests the saved_data property when the doc_id is not associated with a
        matching document.
        """
        actual = self.alert.saved_data
        expected = {}
        self.assertEqual(actual, expected)

    @patch_find_by_id(DOC_W_DATE)
    def test_data_with_match(self):
        """
        Tests the saved_data property when the doc_id is associated with a matching
        document.
        """
        actual = self.alert.saved_data
        expected = DOC_W_DATE
        self.assertEqual(actual, expected)

    @patch_find_by_id(DOC_W_DATE)
    def test_disable_searching_setting(self):
        with self.settings(ALERTS={'DISABLE_COLLECTION_SEARCH': True}):
            actual = self.alert.saved_data
            expected = {}
            self.assertEqual(actual, expected)


class GetDataStrTestCase(AlertModelTestCase):
    """
    Tests the get_data_str method of an Alert.
    """

    def test_get_data_str_with_match(self):
        """
        Tests the get_data_str method when the doc_id is associated with
        a matching document.
        """
        self.alert.data = DOC_W_DATE
        actual = self.alert.get_data_str()
        expected = \
"""{
    "_raw_data": {
        "backend": "elasticsearch",
        "collection": "test_docs",
        "database": "test_index"
    },
    "body": "example text",
    "date": "%s",
    "from": "me@example.com",
    "subject": "Welcome to Acme Supply Co"
}""" % str(NOW_DATE)
        self.assertEqual(actual, expected)

    def test_get_data_str_without_match(self):
        """
        Tests the get_data_str method when the doc_id is not associated
        with a matching document.
        """
        self.alert.data = {}
        actual = self.alert.get_data_str()
        expected = '{}'
        self.assertEqual(actual, expected)


class AlertTidyDataTestCase(AlertModelTestCase):
    """
    Tests the tidy_data property of an Alert.
    """

    def test_tidy_data_wo_distillery(self):
        """
        Tests the tidy_data property when the Alert has no Distillery.
        """
        self.alert.distillery = None
        self.assertEqual(self.alert.tidy_data, self.alert.data)

    def test_tidy_data_w_distillery(self):
        """
        Tests the tidy_data property when the Alert has no Distillery.
        """
        alert = Alert.objects.get(pk=4)
        self.assertEqual(alert.tidy_data,
                         {'content': {'link': 'url', 'text': 'foobar'}})


class AddIncidentTestCase(AlertModelTestCase):
    """
    Tests the add_incident method of an Alert.
    """

    @patch_find_by_id
    def test_add_incident(self):
        """
        Tests the add_incident method.
        """
        alert = Alert.objects.get(pk=1)
        old_incidents = alert.incidents
        alert.add_incident()
        alert_updated = Alert.objects.get(pk=1)
        self.assertEqual(alert_updated.incidents, old_incidents + 1)


class AlertTeaserTestCase(AlertModelTestCase):
    """
    Tests the teaser property of an Alert.
    """

    def test_teaser_with_data(self):
        """
        Tests the teaser property when the doc_id is associated with a
        matching document.
        """
        self.alert.data = DOC_W_DATE
        actual = self.alert.teaser
        expected = {
            'collection': 'elasticsearch.test_index.test_docs',
            'date': NOW_DATE,
            'author': DOC_W_DATE['from'],
            'title': 'Welcome to Acme Supply Co',
            'content': DOC_W_DATE['body'],
            'location': None
        }
        self.assertEqual(actual, expected)

    def test_teaser_without_distillery(self):
        """
        Tests the teaser property when the doc_id is not associated with a
        matching document.
        """
        self.alert.distillery = None
        self.assertEqual(self.alert.teaser, {})

    def test_teaser_without_data(self):
        """
        Tests the teaser property when the doc_id is not associated with a
        matching document.
        """
        self.alert.data = {}
        actual = self.alert.teaser
        expected = {
            'author': None,
            'content': None,
            'date': None,
            'location': None,
            'collection': None,
            'title': None
        }
        self.assertEqual(actual, expected)


class AlertStrTestCase(AlertModelTestCase):
    """
    Tests the __str__ method of an Alert.
    """

    @patch_find_by_id(DOC_W_DATE)
    def test_str_with_title(self):
        """
        Tests the string method when teaser data exists.
        """
        alert = self.alert
        alert.save()
        actual = str(alert)
        expected = 'PK %s: %s' % (alert.pk,
                                  DOC_W_DATE['subject'])
        self.assertEqual(actual, expected)

    @patch_find_by_id(None)
    def test_str_without_title(self):
        """
        Tests the string method when teaser data does not exist.
        """
        alert = self.alert
        alert.save()
        actual = str(alert)
        expected = 'PK %s' % alert.pk
        self.assertEqual(actual, expected)

    @patch_find_by_id(None)
    def test_str_without_title_or_pk(self):
        """
        Tests the string method when teaser data does not exist and the
        Alert has not yet been saved.
        """
        alert = self.alert
        actual = str(alert)
        expected = 'Alert object'
        self.assertEqual(actual, expected)


class GetCodeBookTestCase(AlertModelTestCase):
    """
    Tests the _get_codebook method of an Alert.
    """

    def test_get_codebook(self):
        """
        Tests the _get_codebook method when the Alert has a Distillery
        and the Distillery has a CodeBook.
        """
        codebook = self.alert._get_codebook()
        self.assertEqual(codebook.company.pk, 1)

    def test_no_distillery(self):
        """
        Tests the _get_codebook method when the Alert's Distillery does
        not have a CodeBook.
        """
        self.alert.distillery = None
        actual = self.alert._get_codebook()
        expected = None
        self.assertEqual(actual, expected)

    def test_no_codebook(self):
        """
        Tests the _get_codebook method when the Alert is not associated
        with a Distillery.
        """
        self.alert.distillery.codebook = None
        actual = self.alert._get_codebook()
        expected = None
        self.assertEqual(actual, expected)


class DisplayTitleTestCase(AlertModelTestCase):
    """
    Tests the display_title and redacted_title methods of an Alert.
    """

    @patch_find_by_id(DOC_W_DATE)
    def setUp(self):
        super(DisplayTitleTestCase, self).setUp()
        self.alert.save()

    @patch_find_by_id(None)
    def test_no_title(self):
        """
        Tests the display_title method when no title is available.
        """
        self.alert.title = None
        actual = self.alert.display_title()
        expected = 'No title available'
        self.assertEqual(actual, expected)

    def test_no_distillery(self):
        """
        Tests the display_title method when the Alert has no Distillery.
        """
        self.alert.distillery = None
        actual = self.alert.display_title()
        expected = DOC_W_DATE['subject']
        self.assertEqual(actual, expected)

    def test_no_codebook(self):
        """
        Tests the redacted_title method when no CodeBook is available.
        """
        self.alert.distillery.codebook = None
        actual = self.alert.redacted_title()
        expected = 'Welcome to Acme Supply Co'
        self.assertEqual(actual, expected)

    @patch('alerts.models.settings')
    def test_codenames_disabled(self, mock_settings):
        """
        Tests the redacted_title method when the Alert has a Distillery
        and a Codebook.
        """
        mock_settings.CODENAME_PREFIX = '**'
        mock_settings.CODENAME_SUFFIX = '**'
        actual = self.alert.redacted_title()
        expected = 'Welcome to **PEAK**'
        self.assertEqual(actual, expected)

    @patch('alerts.models.settings')
    def test_codenames_enabled(self, mock_settings):
        """
        Tests the redacted_title method when CodeNames are enabled
        for the current user.
        """
        mock_settings.CODENAME_PREFIX = '**'
        mock_settings.CODENAME_SUFFIX = '**'
        actual = self.alert.redacted_title()
        expected = 'Welcome to **PEAK**'
        self.assertEqual(actual, expected)


class AssociatedTagsTestCase(TestCase):
    """
    Tests the associated_tags property of an Alert.
    """

    fixtures = get_fixtures(['alerts', 'comments', 'tags'])

    def test_alert_w_comments(self):
        """

        """
        alert = Alert.objects.get(pk=3)
        tags = alert.associated_tags
        self.assertEqual(tags.count(), 4)
        self.assertTrue(tags.filter(name='bird').exists())
        self.assertTrue(tags.filter(name='cat').exists())
        self.assertTrue(tags.filter(name='dog').exists())
        self.assertTrue(tags.filter(name='turtle').exists())


class AlertSummaryWithCommentsTestCase(AlertModelTestCase):
    """
    Tests the summary_with_comments method.
    """

    def test_summary_with_comments(self):
        """

        """
        self.maxDiff = None
        mock_doc = {
            '_raw_data': {
                'backend': 'elasticsearch',
                'collection': 'test_docs',
                'database': 'test_index'
            },
            'date': '2016-08-19 14:11:43.162196+00:00',
            'from': 'me@example.com',
            'subject': 'Welcome to Acme Supply Co',
            'body': 'example text'
        }
        alert = Alert.objects.get(pk=3)
        alert.data = mock_doc
        actual = alert.summary(include_comments=True)
        expected = \
"""Alert ID:     3
Title:        Acme Supply Co
Level:        MEDIUM
Incidents:    1
Created date: 2015-03-01 02:46:24.468404+00:00

Collection:   mongodb.test_database.test_posts
Document ID:  3
Source Data:  
{
    "body": "example text",
    "date": "2016-08-19 14:11:43.162196+00:00",
    "from": "me@example.com",
    "subject": "Welcome to Acme Supply Co"
}

Notes:        
Some example notes.

-----

John Smith commented at 2015-03-01 02:41:24.468404+00:00:
I have something to say

Jack Miller commented at 2015-03-01 02:42:24.468404+00:00:
I have something to say about what you have to say"""

        self.assertEqual(actual, expected)


class CommentTestCase(TestCase):
    """
    Tests the Comment model methods.
    """
    fixtures = get_fixtures(['comments'])

    def setUp(self):
        self.comment = Comment.objects.get(pk=1)

    def test_get_all_comments(self):
        """
        Tests the get_all_comments method.
        """
        results = self.comment.get_all_comments()
        self.assertEqual(len(results), 2)

    def test_get_alert_assignee(self):
        """
        Tests the get_alert_assignee method.
        """
        user_model = get_user_model()
        actual = self.comment.get_alert_assignee()
        expected = user_model.objects.get(pk=1)
        self.assertEqual(actual, expected)

    def test_get_other_contributors(self):
        """
        Tests the get_other_contributors method.
        """
        contributors = self.comment.get_other_contributors()
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].pk, 2)

        comment = Comment.objects.get(pk=2)
        contributors = comment.get_other_contributors()
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0].pk, 1)

    def test_summary(self):
        """
        Tests the summary method.
        """
        comment = Comment.objects.get(pk=1)
        actual = comment.summary()
        expected = ('John Smith commented at 2015-03-01 02:41:24.468404+00:00:\n'
                    'I have something to say')
        self.assertEqual(actual, expected)
