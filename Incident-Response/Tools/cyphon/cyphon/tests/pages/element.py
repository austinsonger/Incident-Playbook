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

# standard library
import socket
import time

# third party
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 1

SLEEP = 0.5


class HtmlElement(object):
    """
    Base element class.
    """

    def __init__(self, locator=''):
        self.locator = locator
        self.timeout = TIMEOUT


class StyledElement(HtmlElement):
    """
    Represents an HTML element that is located by CSS selector.
    """

    def __get__(self, obj, owner):
        """
        Gets the text of the specified object.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.locator))
        )
        return element.get_attribute('innerHTML')


class NamedElement(HtmlElement):
    """
    Represents an HTML input element that is located by name.
    """

    def __get__(self, obj, owner):
        """
        Gets the text of the specified object.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.locator))
        )
        return element.get_attribute('value')


class TextInputElement(NamedElement):
    """
    Represents an HTML input element that is located by name.
    """

    def __set__(self, obj, value):
        """
        Sets the text to the value supplied.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.locator))
        )
        element.clear()
        element.send_keys(value)


class SelectElement(HtmlElement):
    """
    Represents an HTML select element that is located by name. Selections
    set and retrve

    """

    def __get__(self, obj, owner):
        """
        Gets the text of the specified object.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.locator))
        )
        select = Select(element)
        return select.first_selected_option.text

    def __set__(self, obj, value):
        """
        Sets the select element to the value supplied.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.locator))
        )
        for option in element.find_elements_by_tag_name('option'):
            if option.text == value:
                option.click()
                break


class LinkElement(HtmlElement):
    """
    Represents a link element that is located by ID.
    """

    def __get__(self, obj, owner):
        """
        Gets the text of the specified object.
        """
        driver = obj.driver
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, self.locator))
        )
        return element.get_attribute('href')


class AutocompleteElement(HtmlElement):
    """

    """

    def __init__(self, driver, *args, **kwargs):
        super(AutocompleteElement, self).__init__(*args, **kwargs)
        self.driver = driver
        self.path = '//span[@data-input-id="id_%s-autocomplete"]' % self.locator
        self.name = self.locator + '-autocomplete'

    def click(self):
        """

        """
        element = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.name))
        )
        element.click()

    def delete(self):
        """

        """
        btn_path = '//span[@id="id_%s-deck"]//span[@class="remove"]' \
                   % self.locator
        element = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, btn_path))
        )
        element.click()

    def _get_option(self, value):
        """

        """
        option_path = '%s/span[@data-value="%s"]' % (self.path, value)
        return WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, option_path))
        )

    def exists(self, value):
        """
        Takes an index of an inline form and the name of a target_field, and
        returns a Boolean indicating whether the option exists.
        """
        try:
            self._get_option(value)
            return True
        except NoSuchElementException:
            return False

    def select(self, value):
        """

        """
        self.click()
        time.sleep(SLEEP)
        option = self._get_option(value)
        option.click()

    def count(self):
        """

        """
        time.sleep(SLEEP)
        self.click()
        time.sleep(SLEEP)  # wait for server response
        option_path = self.path + '/span[@data-value]'
        try:
            WebDriverWait(self.driver, TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, option_path))
            )
            options = self.driver.find_elements_by_xpath(option_path)
            return len(options)
        except (TimeoutException, socket.timeout):
            return 0

    def get_value(self):
        """
        Gets the current value of the autocomplete.
        """
        element = WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((By.NAME, self.locator))
        )
        return element.get_attribute('value')
