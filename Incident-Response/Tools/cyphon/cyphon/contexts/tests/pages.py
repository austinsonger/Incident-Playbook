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

"""

# third party
from selenium.webdriver.common.by import By

# local
from tests.pages.element import (
    AutocompleteElement,
    SelectElement,
    TextInputElement,
)
from tests.pages.modeladmin import ModelAdminPage


class ContextFilterPage(ModelAdminPage):
    """
    Page class for a ContextFilter admin page.
    """
    context = SelectElement('context')

    def __init__(self, *args, **kwargs):
        super(ContextFilterPage, self).__init__(*args, **kwargs)
        self.search_field = AutocompleteElement(self.driver, 'search_field')
        self.operator = AutocompleteElement(self.driver, 'operator')
        self.value_field = AutocompleteElement(self.driver, 'value_field')


class ContextPageLocators(object):
    """
    A base class for page locators.
    """
    ADD_FILTER = (By.CSS_SELECTOR, '.grp-add-handler')
    REMOVE_FILTER = (By.CSS_SELECTOR, '.grp-remove-handler')
    DELETE_FILTER_0 = (By.CSS_SELECTOR, '#filters0 .grp-delete-handler')


class ContextPage(ModelAdminPage):
    """
    Page class for a Context admin page.
    """
    name = TextInputElement('name')
    primary_distillery = SelectElement('primary_distillery')
    related_distillery = SelectElement('related_distillery')

    def __init__(self, driver):
        super(ContextPage, self).__init__(driver)
        self.search_field_0 = AutocompleteElement(self.driver,
                                                  'filters-0-search_field')
        self.operator_0 = AutocompleteElement(self.driver,
                                              'filters-0-operator')
        self.value_field_0 = AutocompleteElement(self.driver,
                                                 'filters-0-value_field')

        self.search_field_1 = AutocompleteElement(self.driver,
                                                  'filters-1-search_field')
        self.operator_1 = AutocompleteElement(self.driver,
                                              'filters-1-operator')
        self.value_field_1 = AutocompleteElement(self.driver,
                                                 'filters-1-value_field')

    def add_filter(self):
        """
        Clicks the 'add filter' button.
        """
        element = self.driver.find_element(*ContextPageLocators.ADD_FILTER)
        element.click()

    def remove_fitting(self):
        """
        Clicks the 'remove filter' button.
        """
        element = self.driver.find_element(*ContextPageLocators.REMOVE_FILTER)
        element.click()

    def delete_fitting(self):
        """
        Deletes the first inline filter.
        """
        element = self.driver.find_element(*ContextPageLocators.DELETE_FILTER_0)
        element.click()
