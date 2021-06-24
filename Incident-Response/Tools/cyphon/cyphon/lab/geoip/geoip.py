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
import ipaddress
import logging
import os

# third party
from django.conf import settings
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

_GEOIP_SETTINGS = settings.GEOIP

_LOGGER = logging.getLogger(__name__)


def get_city_db_path():
    """
    Returns the path for the GeoLite2 city database.
    """
    return os.path.join(_GEOIP_SETTINGS['GEOIP_PATH'],
                        _GEOIP_SETTINGS['CITY_DB'])


def is_public_ip_addr(ip_address):
    """
    Takes an IPv4 or IPv6 address and returns a Boolean indicating
    whether it is public.
    """
    try:
        return not ipaddress.ip_address(ip_address).is_private

    except ValueError:
        _LOGGER.warning('"%s" does not appear to be an IPv4 or IPv6 address.',
                        ip_address)


def get_lng_lat(ip_address):
    """
    Takes an IPv4 or IPv6 address and returns a 2-tuple of (longitude, latitude).
    """
    coord = None

    if ip_address and is_public_ip_addr(ip_address):

        city_db_path = get_city_db_path()
        db_reader = Reader(city_db_path)

        try:
            result = db_reader.city(ip_address)
            coord = (result.location.longitude, result.location.latitude)

        except AddressNotFoundError:
            _LOGGER.warning('The address %s is not in the GeoLite2 database.',
                            ip_address)

        finally:
            db_reader.close()

    return coord
