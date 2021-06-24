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
import logging
import os.path
from unittest import TestCase, skipIf
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

# third party
from geoip2.errors import AddressNotFoundError
from testfixtures import LogCapture

# local
from lab.geoip import geoip

_LOGGER = logging.getLogger(__name__)


if os.path.isfile(geoip.get_city_db_path()):
    NOT_INSTALLED = False

else:
    NOT_INSTALLED = True
    _LOGGER.warning('GeoLite2 database is not installed. '
                    'GeoIP tests will be skipped.')


@skipIf(NOT_INSTALLED, 'GeoLite2 database is not installed')
class GeoIPTestCase(TestCase):
    """
    Tests the get_lng_lat function.
    """

    def test_known_ip(self):
        """
        Test case for a known IP address.
        """
        actual = geoip.get_lng_lat('128.101.101.101')
        expected = (-93.2166, 44.9759)
        self.assertEqual(actual, expected)

    def test_no_ip(self):
        """
        Test case for no IP address.
        """
        self.assertEqual(geoip.get_lng_lat(None), None)

    def test_private_ip(self):
        """
        Test case for a private IP address.
        """
        self.assertEqual(geoip.get_lng_lat('10.195.193.80'), None)

    def test_invalid_ip(self):
        """
        Test case for an invalid IP address.
        """
        with LogCapture() as log_capture:
            self.assertEqual(geoip.get_lng_lat('abc'), None)
            log_capture.check(
                ('lab.geoip.geoip', 'WARNING',
                 '"abc" does not appear to be an IPv4 or IPv6 address.')
            )

    @patch('lab.geoip.geoip.Reader.city', side_effect=AddressNotFoundError())
    def test_unknown_ip(self, mock_reader):
        """
        Test case for an unknown IP address.
        """
        with LogCapture() as log_capture:
            self.assertEqual(geoip.get_lng_lat('99.99.99.99'), None)
            log_capture.check(
                ('lab.geoip.geoip', 'WARNING',
                 'The address 99.99.99.99 is not in the GeoLite2 database.')
            )
