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
Tests the TwitterSearch class.
"""

# standard library
import logging

# third party
from django.conf import settings

# local
from ambassador.passports.models import Passport

_TWITTER_SETTINGS = settings.TWITTER

_LOGGER = logging.getLogger(__name__)


def _credentials_exist():
    """
    Return a Boolean indicating whether Twitter authentication
    credentials exist.
    """
    for (dummy_key, val) in _TWITTER_SETTINGS.items():
        if not val:
            return False
    return True


if not _credentials_exist():
    TWITTER_TESTS_ENABLED = False
    _LOGGER.warning('Twitter authentication credentials are missing, '
                    'so Twitter API tests will be skipped.')
else:
    TWITTER_TESTS_ENABLED = True


class TwitterPassportMixin(object):
    """
    Supplies valid credentials to a Passport used in Twitter API tests.
    """

    @staticmethod
    def _update_passport():
        """
        Supplies valid credentials to a Passport used in tests.
        """
        passport = Passport.objects.get(pk=4)
        passport.key = _TWITTER_SETTINGS['KEY']
        passport.secret = _TWITTER_SETTINGS['SECRET']
        passport.access_token = _TWITTER_SETTINGS['ACCESS_TOKEN']
        passport.access_token_secret = _TWITTER_SETTINGS['ACCESS_TOKEN_SECRET']
        passport.save()
