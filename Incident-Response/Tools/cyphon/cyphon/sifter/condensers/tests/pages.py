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
    LinkElement,
    TextInputElement,
)
from tests.pages.modeladmin import ModelAdminPage
from tests.pages.configtool import ConfigToolPage
from tests.pages.generic import GenericRelationMixin


class FittingPage(ModelAdminPage, GenericRelationMixin):
    """
    Page class for a Fitting admin page.
    """
    condenser = SelectElement('condenser')

    def __init__(self, *args, **kwargs):
        super(FittingPage, self).__init__(*args, **kwargs)
        self.target_field = AutocompleteElement(self.driver, 'target_field')


class CondenserPageLocators(object):
    """
    A base class for page locators.
    """
    ADD_FITTING = (By.CSS_SELECTOR, '.grp-add-handler')
    REMOVE_FITTING = (By.CSS_SELECTOR, '.grp-remove-handler')
    DELETE_FITTING_0 = (By.CSS_SELECTOR, '#fittings0 .grp-delete-handler')


class CondenserPage(ConfigToolPage):
    """
    Page class for a Condenser admin page.
    """
    name = TextInputElement('name')
    bottle = SelectElement('bottle')

    content_type_0 = SelectElement('fittings-0-content_type')
    object_id_0 = TextInputElement('fittings-0-object_id')
    lookup_0 = LinkElement('lookup_id_fittings-0-object_id')

    content_type_1 = SelectElement('fittings-1-content_type')
    object_id_1 = TextInputElement('fittings-1-object_id')
    lookup_1 = LinkElement('lookup_id_fittings-1-object_id')

    def __init__(self, driver):
        super(CondenserPage, self).__init__(driver)
        self.target_field_0 = AutocompleteElement(self.driver,
                                                  'fittings-0-target_field')
        self.target_field_1 = AutocompleteElement(self.driver,
                                                  'fittings-1-target_field')

    def add_fitting(self):
        """
        Clicks the 'add fitting' button.
        """
        element = self.driver.find_element(*CondenserPageLocators.ADD_FITTING)
        element.click()

    def remove_fitting(self):
        """
        Clicks the 'remove fitting' button.
        """
        self.scroll_to_bottom()
        element = self.driver.find_element(*CondenserPageLocators.REMOVE_FITTING)
        element.click()

    def delete_fitting(self):
        """
        Deletes the first inline fitting.
        """
        self.scroll_to_bottom()
        element = self.driver.find_element(*CondenserPageLocators.DELETE_FITTING_0)
        element.click()
