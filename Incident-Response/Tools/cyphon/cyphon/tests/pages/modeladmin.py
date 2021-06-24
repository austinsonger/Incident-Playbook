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
from .page import Page


class ModelAdminLocators(object):
    """
    Page class for a ConfigToolAdmin page.
    """
    SUBMIT_BUTTON = (By.NAME, '_save')


class ModelAdminPage(Page):
    """
    Page class for a ModelAdmin page.
    """

    def submit(self):
        """
        Clicks the submit button.
        """
        element = self.driver.find_element(*ModelAdminLocators.SUBMIT_BUTTON)
        element.click()

