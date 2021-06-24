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

TIMEOUT = 5


class PageLocators(object):
    """
    A base class for page locators.
    """
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'input[type="submit"]')


class Page(object):
    """
    Base class to initialize the base page that will be called from all
    pages.
    """

    def __init__(self, driver):
        self.driver = driver
        self.timeout = TIMEOUT

    def scroll_to_top(self):
        """
        Scrolls to the top of the page.
        """
        script = 'window.scrollTo(0, 0);'
        self.driver.execute_script(script)

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the page.
        """
        script = 'window.scrollTo(0, document.body.scrollHeight);'
        self.driver.execute_script(script)

    def submit(self):
        """
        Clicks the submit button.
        """
        element = self.driver.find_element(*PageLocators.SUBMIT_BUTTON)
        element.click()

