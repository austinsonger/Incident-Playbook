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
Functional tests for the Cyphon QueryBuilder.
"""

# third party
from selenium.common.exceptions import ElementNotVisibleException

# local
from tests.functional_tests import FunctionalTest


class CollectionQueryPageTest(FunctionalTest):
    """
    Functional tests for the database query page. Ensures that the
    DataField options correspond to the Collection specified in the URL.
    """

    def _get_field_options(self):
        """
        Helper function that gets the datafield selectbox of the second
        form in the formset.
        """
        return self.webdriver.find_elements_by_css_selector(
            '#id_form-1-operator option')

    def _choose_field(self, option):
        """
        Helper function that selects the specified field in the datafield
        selectbox of the second form in the formset.
        """
        return self.webdriver.find_element_by_xpath(
            "//select[@id='id_form-1-datafield']/option[@value='"+option+"']"
        ).click()

    def _check_option(self, option):
        """
        Helper function that checks that the operator selectbox contains the
        specified option value. Uses the second form in the formset. Takes an
        option value, and returns true if one and only one option with the
        specified value exists.
        """
        elem = self.webdriver.find_elements_by_xpath(
            "//select[@id='id_form-1-operator']/option[@value='"+option+"']"
        )
        return len(elem) == 1

    def test_can_access_posts_page(self):
        """
        Test for accessing the page for the cyohon.posts Warehouse.
        """
        url = 'http://localhost:8000/collections/mongodb/cyphon/posts/query'
        self.webdriver.get(url)
        options = self.webdriver.find_elements_by_css_selector(
            '#id_form-0-datafield option')
        self.assertIn('Cyphon Database Query', self.webdriver.title)
        self.assertEqual(len(options), 12)

    def test_can_access_mail_page(self):
        """
        Test for accessing the page for the cyohon.mail Warehouse.
        """
        url = 'http://localhost:8000/collections/mongodb/cyphon/mail/query'
        self.webdriver.get(url)
        options = self.webdriver.find_elements_by_css_selector(
            '#id_form-0-datafield option')
        self.assertIn('Cyphon Database Query', self.webdriver.title)
        self.assertEqual(len(options), 5)

    def test_can_add_form(self):
        """
        Test for ability to add a form to the formset.
        """
        url = 'http://localhost:8000/collections/mongodb/cyphon/posts/query'
        self.webdriver.get(url)
        old_options = self.webdriver.find_elements_by_css_selector('#id_formset .filter')

        # click the 'Add Filter' button
        add_filter = self.webdriver.find_element_by_id('id_add_filter')
        add_filter.click()

        new_options = self.webdriver.find_elements_by_css_selector('#id_formset .filter')

        self.assertEqual(len(new_options), len(old_options) + 1)

        num_forms = self.webdriver.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(num_forms.get_attribute('value'), str(len(new_options)))

    def test_can_remove_form(self):
        """
        Test for ability to remove a form from the formset.
        """
        url = 'http://localhost:8000/collections/mongodb/cyphon/posts/query'
        self.webdriver.get(url)

        add_filter = self.webdriver.find_element_by_id('id_add_filter')
        remove_filter = self.webdriver.find_element_by_id('id_remove_filter')
        joiner = self.webdriver.find_element_by_id('id_joiner')

        filters = self.webdriver.find_elements_by_css_selector('#id_formset .filter')
        self.assertEqual(len(filters), 1)

        num_forms = self.webdriver.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(num_forms.get_attribute('value'), '1')

        with self.assertRaises(ElementNotVisibleException):
            remove_filter.click()

        with self.assertRaises(ElementNotVisibleException):
            joiner.click()

        add_filter.click()
        add_filter.click()

        filters = self.webdriver.find_elements_by_css_selector('#id_formset .filter')
        self.assertEqual(len(filters), 3)

        num_forms = self.webdriver.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(num_forms.get_attribute('value'), '3')

        remove_filter.click()
        remove_filter.click()

        filters = self.webdriver.find_elements_by_css_selector('#id_formset .filter')
        self.assertEqual(len(filters), 1)

        num_forms = self.webdriver.find_element_by_id('id_form-TOTAL_FORMS')
        self.assertEqual(num_forms.get_attribute('value'), '1')

        with self.assertRaises(ElementNotVisibleException):
            remove_filter.click()

        with self.assertRaises(ElementNotVisibleException):
            joiner.click()

    def test_dynamic_query_options(self):
        """
        Test for the creation of correct query options based on the selected
        datafield.
        """
        url = 'http://localhost:8000/collections/mongodb/cyphon/test_docs/query'
        self.webdriver.get(url)

        # add a new form by clicking 'Add More'
        add_filter = self.webdriver.find_element_by_id('id_add_filter')
        add_filter.click()

        # use the new form so we can be sure the behaviors bind to new elements
        self.assertEqual(len(self._get_field_options()), 18)

        self._choose_field('platform:ChoiceField')
        self.assertTrue(self._check_option('$eq'))
        self.assertTrue(self._check_option('$ne'))
        self.assertEqual(len(self._get_field_options()), 2)

        self._choose_field('likes:IntegerField')
        self.assertTrue(self._check_option('$gt'))
        self.assertEqual(len(self._get_field_options()), 6)

        self._choose_field('content.link:URLField')
        self.assertTrue(self._check_option('$regex'))
        self.assertEqual(len(self._get_field_options()), 3)

        self._choose_field('created_date:DateTimeField')
        self.assertTrue(self._check_option('$gte'))
        self.assertFalse(self._check_option('$gt'))
        self.assertEqual(len(self._get_field_options()), 2)

        self._choose_field('content.text:CharField')
        self.assertTrue(self._check_option('$regex'))
        self.assertEqual(len(self._get_field_options()), 3)

        self._choose_field('tags:ListField')
        self.assertTrue(self._check_option('$nin'))
        self.assertEqual(len(self._get_field_options()), 2)

        self._choose_field('email:EmailField')
        self.assertTrue(self._check_option('$regex'))
        self.assertEqual(len(self._get_field_options()), 3)

        self._choose_field('verified:BooleanField')
        self.assertTrue(self._check_option('$ne'))
        self.assertEqual(len(self._get_field_options()), 2)

        self._choose_field('ip_address:IPAddressField')
        self.assertTrue(self._check_option('$regex'))
        self.assertEqual(len(self._get_field_options()), 3)

    def test_datetime_widget(self):
        """
        Tests that the datetimepicker appears in the input box if a
        DateTimeField has been selected.
        """

        url = 'http://localhost:8000/collections/mongodb/cyphon/posts/query'
        self.webdriver.get(url)

        # add a new form by clicking 'Add More'
        add_filter = self.webdriver.find_element_by_id('id_add_filter')
        add_filter.click()

        picker = self.webdriver.find_elements_by_css_selector('.datetimepicker')

        self.assertEqual(len(picker), 0)

        self._choose_field('created_date:DateTimeField')

        input_field = self.webdriver.find_element_by_id('id_form-1-value')
        input_field.click()

        picker = self.webdriver.find_elements_by_css_selector('.datetimepicker')

        self.assertEqual(len(picker), 1)
        picker[0].click()
