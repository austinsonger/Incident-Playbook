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
Tests views for Articles.
"""

# third party
from rest_framework import status

# local
from articles.models import Article
from tags.models import Tag, Topic
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class ArticlesAPITestCase(CyphonAPITestCase):
    """
    Base class for testing REST API endpoints for Bottles and related objects.
    """
    fixtures = get_fixtures(['tags'])

    model_url = 'articles/'

    def test_get_articles(self):
        """
        Tests the Articles list REST API endpoint.
        """
        response = self.get_api_response()
        data = response.json()
        actual = data['results'][0]
        expected = {
            'id': 1,
            'title': 'Birds',
            'url': 'http://testserver/api/v1/articles/1/'
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(actual, expected)

    def test_get_article(self):
        """
        Tests the Article detail REST API endpoint.
        """
        article = Article.objects.get(pk=1)
        topic = Topic.objects.get(name='Animals')
        Tag.objects.create(id=5, name='falcon', topic=topic, article=article)
        response = self.get_api_response('1/')
        actual = response.json()
        expected = {
            'id': 1,
            'title': 'Birds',
            'content': 'All about birds.',
            'topics': [
                {
                    'id': 1,
                    'name': 'Animals',
                    'url': 'http://testserver/api/v1/topics/1/'
                }
            ],
            'tags': [
                {
                    'id': 1,
                    'name': 'bird'
                }, {
                    'id': 5,
                    'name': 'falcon'
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual, expected)
