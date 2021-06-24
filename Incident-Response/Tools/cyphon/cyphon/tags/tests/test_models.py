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
Tests the Tag class and related classes.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from testfixtures import LogCapture

# local
from alerts.models import Alert
from bottler.containers.models import Container
from tags.models import DataTagger, Tag, TagRelation, Topic
from tests.fixture_manager import get_fixtures


class TopicTestCase(TestCase):
    """
    Base class for testing the Topic class.
    """
    fixtures = get_fixtures(['tags'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        topic = Topic.objects.get(pk=1)
        self.assertEqual(str(topic), 'Animals')


class TagManagerTestCase(TransactionTestCase):
    """
    Test cases for the TagManager class.
    """
    fixtures = get_fixtures(['tags'])

    text = 'This is some text about pied piper and cats and dogs.'

    def setUp(self):
        self.alert = Alert.objects.get(pk=2)

    def test_get_tokens(self):
        """
        Tests that strings with plural words generate tokens that
        include the singular form.
        """
        text = 'this is some text about wild cats.'
        tokens = Tag.objects._get_tokens(text)
        self.assertTrue('cat' in tokens)
        self.assertTrue('cats' in tokens)

    def test_process_default_qs(self):
        """
        Tests the process method with the default queryset.
        """
        self.assertEquals(len(self.alert.associated_tags), 0)
        Tag.objects.process(value=self.text, obj=self.alert)
        self.assertEquals(len(self.alert.associated_tags), 2)

    def test_process_filtered_qs(self):
        """
        Tests the process method with the a filtered queryset.
        """
        topic = Topic.objects.get(name='Names')
        queryset = Tag.objects.filter(topic=topic)
        self.assertEquals(len(self.alert.associated_tags), 0)
        Tag.objects.process(value=self.text, obj=self.alert, queryset=queryset)
        self.assertEquals(len(self.alert.associated_tags), 0)


class TagTestCase(TestCase):
    """
    Base class for testing the Tag class.
    """
    fixtures = get_fixtures(['tags'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        tag = Tag.objects.get_by_natural_key('Animals', 'cat')
        self.assertEqual(str(tag), 'cat')

    def test_assign_tag(self):
        """
        Tests the assign_tag method.
        """
        tag = Tag.objects.get(pk=3)
        alert = Alert.objects.get(pk=1)
        tag_relation = tag.assign_tag(alert)
        self.assertEqual(tag_relation.tagged_object, alert)


class TagRelationTestCase(TestCase):
    """
    Base class for testing the TagRelation class.
    """
    fixtures = get_fixtures(['tags'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        tag_relation = TagRelation.objects.get(pk=1)
        self.assertEqual(str(tag_relation), 'cat <Alert: PK 1: Acme Supply Co>')


class DataTaggerManagerTestCase(TransactionTestCase):
    """
    Test cases for the DataTaggerManager class.
    """

    fixtures = get_fixtures(['datataggers'])

    def setUp(self):
        self.alert = Alert.objects.get(pk=2)

    def test_process(self):
        """
        Tests the process method.
        """
        enabled_count = DataTagger.objects.find_enabled().count()
        assert enabled_count < DataTagger.objects.count()

        with patch('tags.models.DataTagger.process') as mock_process:
            DataTagger.objects.process(self.alert)
            self.assertEqual(mock_process.call_count, enabled_count)

        self.assertEquals(len(self.alert.associated_tags), 0)
        DataTagger.objects.process(self.alert)
        self.assertEquals(len(self.alert.associated_tags), 2)


class DataTaggerTestCase(TestCase):
    """
    Base class for testing the DataTagger class.
    """
    fixtures = get_fixtures(['datataggers'])

    def setUp(self):
        self.alert = Alert.objects.get(pk=2)
        self.container = Container.objects.get_by_natural_key('post')
        self.datatagger = DataTagger.objects.get(pk=1)


class DataTaggerTransactionTestCase(TransactionTestCase):
    """
    Base class for testing the DataTagger class.
    """
    fixtures = get_fixtures(['datataggers'])

    def setUp(self):
        self.alert = Alert.objects.get(pk=2)
        self.container = Container.objects.get_by_natural_key('post')
        self.datatagger = DataTagger.objects.get(pk=1)



class GetValueTestCase(DataTaggerTestCase):
    """
    Test cases for the _get_value method of the DataTagger class.
    """

    def test_string(self):
        """
        Tests that a lowercase string is returned if a value is found.
        """
        datatagger = DataTagger(
            container=self.container,
            field_name='content.text'
        )
        actual = datatagger._get_value(self.alert)
        expected = 'this is some text about wild cats.'
        self.assertEqual(actual, expected)

    def test_non_string(self):
        """
        Tests that None is returned if the field does not exist in the
        Alert data.
        """
        datatagger = DataTagger(
            container=self.container,
            field_name='foobar'
        )
        actual = datatagger._get_value(self.alert)
        expected = None
        self.assertEqual(actual, expected)


class CreateTagTestCase(DataTaggerTestCase):
    """
    Test cases for the _create_tag method the DataTagger class.
    """

    @patch('django.db.models.Manager.get_or_create',
           side_effect=ValidationError('error msg'))
    def test_validation_error(self, mock_create):
        """
        Test case for when a VlaidatioNError is raised.
        """
        with LogCapture() as log_capture:
            self.datatagger._create_tag('pied piper')
            log_capture.check(
                ('tags.models',
                 'ERROR',
                 'An error occurred while creating a new tag "pied piper": '
                 '[\'error msg\']'),
            )

    def test_duplicate(self):
        """
        Test case for when the Tag already exists.
        """
        topic = Topic.objects.get_by_natural_key('Names')
        new_tag = Tag.objects.create(name='pied piper', topic=topic)
        result = self.datatagger._create_tag('pied piper')
        self.assertEqual(result.pk, new_tag.pk)

    def test_new_tag(self):
        """
        Test case for when the Tag does not already exist.
        """
        self.assertFalse(Tag.objects.filter(name='piedpiper').exists())
        self.datatagger._create_tag('piedpiper')
        self.assertTrue(Tag.objects.filter(name='piedpiper').exists())


class GetTagTestCase(DataTaggerTestCase):
    """
    Test cases for the _get_tag method the DataTagger class.
    """

    def test_tag_exists(self):
        """
        Test case for when the Tag already exists.
        """
        datatagger = DataTagger.objects.get(pk=3)
        actual = datatagger._get_tag('cat')
        expected = Tag.objects.get_by_natural_key(topic_name='Animals',
                                                  tag_name='cat')
        self.assertEqual(actual, expected)

    def test_no_tag_create_tag_true(self):
        """
        Test case for when the Tag does not already exist and
        create_tags is True.
        """
        self.assertFalse(Tag.objects.filter(name='newtag').exists())
        actual = self.datatagger._get_tag('newtag')
        expected = Tag.objects.get_by_natural_key(topic_name='Names',
                                                  tag_name='newtag')
        self.assertEqual(actual, expected)

    def test_no_tag_create_tag_false(self):
        """
        Test case for when the Tag does not already exist and
        create_tags is False.
        """
        datatagger = DataTagger.objects.get(pk=2)
        actual = datatagger._get_tag('newtag')
        expected = None
        self.assertEqual(actual, expected)
        self.assertFalse(Tag.objects.filter(name='newtag').exists())


class TagExactMatchTestCase(DataTaggerTestCase):
    """
    Test cases for the _tag_exact_match method the DataTagger class.
    """

    def test_tag_exists(self):
        """
        Test case for when an appropriate Tag exists or is created.
        """
        self.assertFalse(Tag.objects.filter(name='piedpiper').exists())
        self.datatagger._tag_exact_match(self.alert, 'piedpiper')
        actual = self.alert.associated_tags[0]
        expected = Tag.objects.get(name='piedpiper')
        self.assertEqual(actual, expected)

    def test_tag_does_not_exist(self):
        """
        Test case for when an appropriate Tag does not exist.
        """
        self.datatagger.create_tags = False
        self.datatagger._tag_exact_match(self.alert, 'piedpiper')
        self.assertEqual(len(self.alert.associated_tags), 0)
        self.assertFalse(Tag.objects.filter(name='pied piper').exists())


class TagPartialMatchTestCase(DataTaggerTransactionTestCase):
    """
    Test cases for the _tag_partial_match method the DataTagger class.
    """

    def test_single_token_tag(self):
        """
        Test case for Tags containing a single token.
        """
        datatagger = DataTagger.objects.get(pk=3)
        datatagger._tag_partial_match(self.alert,
                                      'this is some text about wild cats.')
        actual = self.alert.associated_tags[0]
        expected = Tag.objects.get(name='cat')
        self.assertEqual(actual, expected)

    def test_multi_token_tag(self):
        """
        Test case for Tags containing omultiple tokens.
        """
        datatagger = DataTagger.objects.get(pk=3)
        topic = Topic.objects.get_by_natural_key('Animals')
        Tag.objects.create(name='wild cats', topic=topic)
        datatagger._tag_partial_match(self.alert,
                                      'this is some text about wild cats.')
        tags = self.alert.associated_tags
        cat_tag = Tag.objects.get(name='cat')
        wild_cat_tags = Tag.objects.get(name='wild cats')
        self.assertTrue(cat_tag in tags)
        self.assertTrue(wild_cat_tags in tags)

    def test_no_tags(self):
        """
        Test case when the string matches no Tags.
        """
        datatagger = DataTagger.objects.get(pk=2)
        datatagger._tag_partial_match(self.alert, 'pied piper')
        self.assertEqual(len(self.alert.associated_tags), 0)


class ProcessTestCase(DataTaggerTransactionTestCase):
    """
    Test cases for the process method of the DataTagger class.
    """

    def test_exact_match_true(self):
        """
        Test case for when exact_match is True.
        """
        self.datatagger.process(self.alert)
        actual = self.alert.associated_tags[0]
        expected = Tag.objects.get(name='piedpiper')
        self.assertEqual(actual, expected)

    def test_exact_match_false(self):
        """
        Test case for when exact_match is False.
        """
        datatagger = DataTagger.objects.get(pk=3)
        datatagger.process(self.alert)
        actual = self.alert.associated_tags[0]
        expected = Tag.objects.get(name='cat')
        self.assertEqual(actual, expected)
