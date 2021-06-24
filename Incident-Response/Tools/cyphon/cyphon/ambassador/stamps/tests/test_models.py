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
Tests the Stamp class.
"""

# third party
from django.test import TestCase

# local
from ambassador.stamps.models import Stamp
from tests.fixture_manager import get_fixtures


class StampTestCase(TestCase):
    """
    Class for Stamp test cases.
    """
    fixtures = get_fixtures(['stamps'])

    def setUp(self):
        self.stamp1 = Stamp.objects.get(pk=1)
        self.stamp2 = Stamp.objects.get(pk=2)

    def test_is_obsolete_false(self):
        """
        Tests the is_obsolete method when the stamp is associated with
        the latest call.
        """
        self.assertFalse(self.stamp1.is_obsolete())
        self.assertFalse(self.stamp2.is_obsolete())

    def test_is_obsolete_true(self):
        """
        Tests the is_obsolete method when the stamp is not associated
        with the latest call.
        """
        self.stamp1.passport = self.stamp2.passport
        self.stamp1.save()
        self.assertTrue(self.stamp1.is_obsolete())

