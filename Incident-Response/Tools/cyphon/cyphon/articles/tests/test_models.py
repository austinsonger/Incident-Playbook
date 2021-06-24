# -*- coding: utf-8 -*-
# Copyright 2017 ControlScan.
#
# This file is part of Cyphon Engine.
#
# Cyphon Engine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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

# third party
from django.test import TestCase
from testfixtures import LogCapture

# local
from articles.models import Article
from tags.models import Tag, Topic
from tests.fixture_manager import get_fixtures


class ArticleManagerTestCase(TestCase):
    """
    Test cases for the ArticleManager class.
    """
    fixtures = get_fixtures(['tags'])

    def test_get_by_natural_key(self):
        """
        Tests the get_by_natural_key method.
        """
        article = Article.objects.get_by_natural_key('Birds')
        self.assertEqual(article.pk, 1)

    def test_natural_key_exception(self):
        """
        Tests the get_by_natural_key method when the Article does not exist.
        """
        with LogCapture() as log_capture:
            Article.objects.get_by_natural_key('Foobar')
            log_capture.check(
                ('articles.models',
                 'ERROR',
                 'Article "Foobar" does not exist'),
            )


class ArticleTestCase(TestCase):
    """
    Test cases for the Article class.
    """
    fixtures = get_fixtures(['tags'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        article = Article.objects.get(pk=1)
        self.assertEqual(str(article), 'Birds')

    def test_topics(self):
        """
        Tests the topics property.
        """
        article = Article.objects.get(pk=1)
        topic = Topic.objects.get(name='Animals')
        Tag.objects.create(name='falcon', topic=topic, article=article)
        self.assertEqual(article.topics.count(), 1)
        self.assertEqual(article.topics[0], topic)
