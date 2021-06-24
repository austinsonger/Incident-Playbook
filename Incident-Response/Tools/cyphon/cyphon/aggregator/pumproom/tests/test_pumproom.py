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
Tests the PumpRoom class.
"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# local
from aggregator.pumproom.tests.test_pump import BKGD_SRCH, PumpBaseTestCase
from aggregator.pumproom.pumproom import PumpRoom
from aggregator.reservoirs.models import Reservoir


class PumpRoomSingleTestCase(PumpBaseTestCase):
    """
    Tests the get_results method for the PumpRoom class.
    """

    def test_no_reservoir(self):
        """
        Tests the get_results method for a Reservoir that doesn't exist.
        """
        reservoirs = Reservoir.objects.filter(name='not_there')
        pumproom = PumpRoom(reservoirs=reservoirs, task=BKGD_SRCH)
        results = pumproom.get_results(self.query)
        self.assertEqual(results, [])


# must create separate class because of closed db connection
class PumpRoomMultiTestCase(PumpBaseTestCase):
    """
    Tests the get_results method for the PumpRoom class.
    """

    def test_multiple_reservoirs(self):
        """
        Tests the get_results method for multiple Reservoirs.
        """
        reservoirs = Reservoir.objects.filter(name__in=['twitter', 'instagram'])

        mock_results = [1, 2]
        with patch('aggregator.pumproom.pump.Pump.start',
                   side_effect=mock_results):
            pumproom = PumpRoom(reservoirs=reservoirs, task=BKGD_SRCH)
            results = pumproom.get_results(self.query)
            self.assertEqual(results, mock_results)
