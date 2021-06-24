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
Creates a MongoDB client instance for use in other modules.

========================  ===========================
Constant                  Description
========================  ===========================
:const:`~MONGODB_CLIENT`  MongoDB client.
:const:`~TIMEOUT`         Request timeout in seconds.
========================  ===========================

"""

# third party
from django.conf import settings
import pymongo

_MONGODB_SETTINGS = settings.MONGODB

TIMEOUT = _MONGODB_SETTINGS['TIMEOUT']
"""|int|

Request timeout in seconds.
"""

MONGODB_CLIENT = pymongo.MongoClient(_MONGODB_SETTINGS['HOST'],
                                     serverSelectionTimeoutMS=TIMEOUT)
""":class:`~pymongo.MongoClient`

Client for a MongoDB instance.
"""
