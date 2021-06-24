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
from bottler.bottles.models import BottleField


class CondenserTestCaseMixin(object):
    """

    """

    def test_field_is_in_bottle_true(self):
        """
        Tests the field_is_in_bottle method for a BottleField that is
        in the DataCondenser's Bottle.
        """
        field = BottleField.objects.get_by_natural_key('user')
        actual = self.condenser.field_is_in_bottle(field)
        self.assertEqual(actual, True)

    def test_field_is_in_bottle_false(self):
        """
        Tests the field_is_in_bottle method for a BottleField that is
        not in the DataCondenser's Bottle.
        """
        field = BottleField.objects.get_by_natural_key('subject')
        actual = self.condenser.field_is_in_bottle(field)
        self.assertEqual(actual, False)


class FittingTestCaseMixin(object):
    """

    """

    def test_is_parser_for_parser(self):
        """
        Tests the is_parser method for a Fitting that's a Parser.
        """
        self.assertTrue(self.parser_fitting.is_parser())

    def test_is_parser_for_condenser(self):
        """
        Tests the is_parser method for a Fitting that's a Condenser.
        """
        self.assertFalse(self.condenser_fitting.is_parser())

    def test_is_condenser_for_condenser(self):
        """
        Tests the is_condenser method for a Fitting that's a Condenser.
        """
        self.assertTrue(self.condenser_fitting.is_condenser())

    def test_is_condenser_for_parser(self):
        """
        Tests the is_condenser method for a Fitting that's a Parser.
        """
        self.assertFalse(self.parser_fitting.is_condenser())

