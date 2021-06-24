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
Defines a DashboardPage and its elements.
"""

# local
from tests.pages.page import Page
from tests.pages.element import StyledElement


class DashboardPage(Page):
    """
    Page class for the admin dashboard.
    """
    module_1 = StyledElement('div[id="module_1"] h2')
    module_2 = StyledElement('div[id="module_2"] h2')
    module_3 = StyledElement('div[id="module_3"] h2')
    module_4 = StyledElement('div[id="module_4"] h2')
    module_5 = StyledElement('div[id="module_5"] h2')
    module_6 = StyledElement('div[id="module_6"] h2')
    module_7 = StyledElement('div[id="module_7"] h2')
    module_8 = StyledElement('div[id="module_8"] h2')
    module_9 = StyledElement('div[id="module_9"] h2')
    module_10 = StyledElement('div[id="module_10"] h2')
    module_11 = StyledElement('div[id="module_11"] h2')
    module_12 = StyledElement('div[id="module_12"] h2')
    module_13 = StyledElement('div[id="module_13"] h2')
    module_14 = StyledElement('div[id="module_14"] h2')
    module_15 = StyledElement('div[id="module_15"] h2')
    module_16 = StyledElement('div[id="module_16"] h2')
    module_17 = StyledElement('div[id="module_17"] h2')
