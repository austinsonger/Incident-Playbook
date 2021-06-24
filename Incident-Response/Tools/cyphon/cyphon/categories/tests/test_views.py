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
Tests for Categories REST API.
"""

# third party
from rest_framework import status

# local
from categories.models import Category
from tests.api_tests import CyphonAPITestCase
from tests.fixture_manager import get_fixtures


class CategoryViewTestCase(CyphonAPITestCase):
    """
    Class for testing Category API views.
    """

    fixtures = get_fixtures(['categories'])
    model_url = 'categories/'

    def test_get_category(self):
        """
        Tests getting a single category object by its id.
        """
        response = self.get_api_response('1/')
        category = Category.objects.get(pk=1)
        result = {'id': category.id, 'name': category.name}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, result)

    def test_get_categories(self):
        """
        Tests retrieving a list of categories.
        """
        response = self.get_api_response()
        count = Category.objects.all().count()
        categories = Category.objects.all()
        results = []

        for category in categories:
            results.append({'id': category.id, 'name': category.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] > 0)
        self.assertEqual(response.data['count'], count)
        self.assertEqual(response.data['results'], results)
