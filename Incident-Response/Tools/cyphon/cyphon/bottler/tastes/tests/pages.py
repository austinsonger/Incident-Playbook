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

# local
from tests.pages.element import AutocompleteElement, SelectElement
from tests.pages.modeladmin import ModelAdminPage


class TastePage(ModelAdminPage):
    """
    Page class for a Taste admin page.
    """
    container = SelectElement('container')

    def __init__(self, *args, **kwargs):
        """

        """
        super(TastePage, self).__init__(*args, **kwargs)
        self.datetime = AutocompleteElement(self.driver, 'datetime')
        self.location = AutocompleteElement(self.driver, 'location')
        self.content = AutocompleteElement(self.driver, 'content')
        self.title = AutocompleteElement(self.driver, 'title')
        self.author = AutocompleteElement(self.driver, 'author')


class InlineTastePage(ModelAdminPage):
    """
    Page class for a Fitting admin page.
    """
    bottle = SelectElement('bottle')
    label = SelectElement('label')

    def __init__(self, *args, **kwargs):
        """

        """
        super(InlineTastePage, self).__init__(*args, **kwargs)
        self.datetime = AutocompleteElement(self.driver, 'taste-0-datetime')
        self.location = AutocompleteElement(self.driver, 'taste-0-location')
        self.content = AutocompleteElement(self.driver, 'taste-0-content')
        self.title = AutocompleteElement(self.driver, 'taste-0-title')
        self.author = AutocompleteElement(self.driver, 'taste-0-author')
