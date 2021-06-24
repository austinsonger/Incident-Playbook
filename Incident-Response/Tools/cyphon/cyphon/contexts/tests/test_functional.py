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
Functional tests for the Contexts app.
"""

# local
from distilleries.models import Distillery
from tests.fixture_manager import get_fixtures
from tests.functional_tests import ModelPreviewFunctionalTest
from .pages import ContextPage, ContextFilterPage


class ContextFunctionalTest(ModelPreviewFunctionalTest):
    """
    Base class for testing admin pages in the Contexts app.
    """
    fixtures = get_fixtures(['contexts'])

    def setUp(self):
        super(ContextFunctionalTest, self).setUp()
        self.page = ContextPage(self.driver)
        self.syslog = Distillery.objects.get_by_natural_key('elasticsearch.test_time_series.test_syslogs')
        self.mail = Distillery.objects.get_by_natural_key('elasticsearch.test_index.test_mail')


class AddContextFunctionalTest(ContextFunctionalTest):
    """
    Tests the Add Context admin page.
    """
    url = '/admin/contexts/context/add/'

    def test_filtering_and_autocomplete(self):
        """
        Tests the behavior of the select and input elements.
        """
        self.page.scroll_to_bottom()

        # make sure field options are filtered
        self.assertEqual(self.page.search_field_0.count(), 0)
        self.assertEqual(self.page.operator_0.count(), 0)
        self.assertEqual(self.page.value_field_0.count(), 0)

        self.page.primary_distillery = 'elasticsearch.test_time_series.test_syslogs'
        self.page.related_distillery = 'elasticsearch.test_index.test_mail'

        self.assertEqual(self.page.search_field_0.count(), 5)
        self.assertEqual(self.page.value_field_0.count(), 3)
        self.page.search_field_0.select('from')
        self.assertEqual(self.page.operator_0.count(), 2)


class EditContextFunctionalTest(ContextFunctionalTest):
    """
    Tests the Edit Context admin page.
    """
    url = '/admin/contexts/context/1/'

    def test_restore_values(self):
        """
        Tests that saved values are restored for autocomplete fields.
        """
        self.assertEqual(self.page.search_field_0.get_value(), 'from')
        self.assertEqual(self.page.operator_0.get_value(), 'eq')
        self.assertEqual(self.page.value_field_0.get_value(), 'host')

        self.assertEqual(self.page.search_field_1.get_value(), 'subject')
        self.assertEqual(self.page.operator_1.get_value(), 'eq')
        self.assertEqual(self.page.value_field_1.get_value(), 'message')


class AddContextFilterFunctionalTest(ContextFunctionalTest):
    """
    Tests the Add Context admin page.
    """
    url = '/admin/contexts/contextfilter/add/'

    def setUp(self):
        super(AddContextFilterFunctionalTest, self).setUp()
        self.page = ContextFilterPage(self.driver)

    def test_filtering_and_autocomplete(self):
        """
        Tests the behavior of the select and input elements.
        """
        # make sure field options are filtered
        # but be careful of order to make sure lower fields aren't
        # covered by upper field's autocomplete options
        self.assertEqual(self.page.value_field.count(), 0)
        self.assertEqual(self.page.operator.count(), 0)
        self.assertEqual(self.page.search_field.count(), 0)

        self.page.context = 'context_w_filters'
        self.assertEqual(self.page.value_field.count(), 15)
        self.assertEqual(self.page.search_field.count(), 18)

        self.page.search_field.select('content.title')
        self.assertEqual(self.page.operator.count(), 3)


class EditContextFunctionalTest(ContextFunctionalTest):
    """
    Tests the Edit Context admin page.
    """
    url = '/admin/contexts/contextfilter/1/'

    def setUp(self):
        super(EditContextFunctionalTest, self).setUp()
        self.page = ContextFilterPage(self.driver)

    def test_restore_values(self):
        """
        Tests that saved values are restored for autocomplete fields.
        """
        self.assertEqual(self.page.search_field.get_value(), 'from')
        self.assertEqual(self.page.operator.get_value(), 'eq')
        self.assertEqual(self.page.value_field.get_value(), 'host')

