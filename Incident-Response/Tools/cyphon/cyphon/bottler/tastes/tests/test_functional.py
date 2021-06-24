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
Functional tests for the Tastes app.
"""

# local
from tests.fixture_manager import get_fixtures
from tests.functional_tests import ModelAdminFunctionalTest
from .pages import TastePage, InlineTastePage


class TasteFunctionalTest(ModelAdminFunctionalTest):
    """

    """
    url = '/admin/tastes/taste/add/'

    fixtures = get_fixtures(['containers'])

    def setUp(self):
        super(TasteFunctionalTest, self).setUp()
        self.page = TastePage(self.driver)

    def test_taste(self):
        """
        Tests autocompleted choices on the Taste admin page.
        """
        self.page.scroll_to_bottom()

        self.assertEqual(self.page.datetime.count(), 0)
        self.assertEqual(self.page.location.count(), 0)
        self.assertEqual(self.page.content.count(), 0)
        self.assertEqual(self.page.title.count(), 0)
        self.assertEqual(self.page.author.count(), 0)

        self.page.container = 'labeled_post'

        self.assertEqual(self.page.datetime.count(), 1)
        self.assertEqual(self.page.location.count(), 2)
        self.assertEqual(self.page.content.count(), 12)
        self.assertEqual(self.page.title.count(), 12)
        self.assertEqual(self.page.author.count(), 12)

        self.page.container = 'mail'

        self.assertEqual(self.page.datetime.count(), 1)
        self.assertEqual(self.page.location.count(), 0)
        self.assertEqual(self.page.content.count(), 4)
        self.assertEqual(self.page.title.count(), 4)
        self.assertEqual(self.page.author.count(), 4)


class InlineTasteFunctionalTest(ModelAdminFunctionalTest):
    """
    Tests autocompleted choices on the Taste inline admin form.
    """
    url = '/admin/containers/container/add/'

    fixtures = get_fixtures(['containers'])

    def setUp(self):
        super(InlineTasteFunctionalTest, self).setUp()
        self.page = InlineTastePage(self.driver)

    def test_inline_taste(self):
        """

        """
        self.page.scroll_to_bottom()

        self.assertEqual(self.page.datetime.count(), 0)
        self.assertEqual(self.page.location.count(), 0)
        self.assertEqual(self.page.content.count(), 0)
        self.assertEqual(self.page.title.count(), 0)
        self.assertEqual(self.page.author.count(), 0)

        self.page.scroll_to_top()
        self.page.bottle = 'post'
        self.page.scroll_to_bottom()

        self.assertEqual(self.page.datetime.count(), 1)
        self.assertEqual(self.page.location.count(), 1)
        self.assertEqual(self.page.content.count(), 11)
        self.assertEqual(self.page.title.count(), 11)
        self.assertEqual(self.page.author.count(), 11)

        self.page.scroll_to_top()
        self.page.label = 'mail'
        self.page.scroll_to_bottom()

        self.assertEqual(self.page.datetime.count(), 1)
        self.assertEqual(self.page.location.count(), 2)
        self.assertEqual(self.page.content.count(), 12)
        self.assertEqual(self.page.title.count(), 12)
        self.assertEqual(self.page.author.count(), 12)
