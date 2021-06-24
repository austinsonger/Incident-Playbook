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
Tests the Company class.
"""

# standard library
from django.test import TestCase

# local
from companies.models import Company
from tests.fixture_manager import get_fixtures


class CompanyTestCase(TestCase):
    """
    Base class for testing the CodeBook class and related classes.
    """
    fixtures = get_fixtures(['companies'])

    def test_str(self):
        """
        Tests the __str__ method.
        """
        company = Company.objects.get(pk=1)
        self.assertEqual(str(company), 'Acme')

