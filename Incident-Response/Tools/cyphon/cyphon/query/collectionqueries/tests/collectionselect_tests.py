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

# local
from tests.functional_tests import FunctionalTest


class CollectionSelectPageTest(FunctionalTest):
    """
    Functional tests for the Collection select page.
    """

    def test_can_access_collectselect(self):
        """
        Test for accessing the page to select a Collection.
        """
        self.webdriver.get('http://localhost:8000/collections/')
        self.assertIn('Cyphon Collections', self.webdriver.title)

    def test_select_posts(self):
        """
        Tests Collection selection for the cyphon.posts Collection.
        """
        self.webdriver.get('http://localhost:8000/collections/')
        self.webdriver.find_element_by_xpath(
            "//select[@id='id_collection']/option[2]"
        ).click()
        self.webdriver.find_element_by_id('id_collection_form').submit()
        self.assertIn('/collections/mongodb/cyphon/posts/query',
                      self.webdriver.current_url)

    def test_select_mail(self):
        """
        Tests Collection selection for the cyphon.accts Collection.
        """
        self.webdriver.get('http://localhost:8000/collections/')
        self.webdriver.find_element_by_xpath(
            "//select[@id='id_collection']/option[3]"
        ).click()
        self.webdriver.find_element_by_id('id_collection_form').submit()
        self.assertIn('/collections/mongodb/cyphon/mail/query',
                      self.webdriver.current_url)
