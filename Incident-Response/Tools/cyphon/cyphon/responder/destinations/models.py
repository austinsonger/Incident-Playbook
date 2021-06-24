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
Defines a Destination class to determine platforms are enabled for responders.
"""

# local
from ambassador.platforms.models import Platform, PlatformManager


class Destination(Platform):
    """
    Determines whether a platform is enabled for use as a Destination.
    The platform corresponds to a subpackage in the Platforms package.
    A Destination's primary key is the name of the subpackage associated
    with the Destination (e.g., 'twitter').
    """
    objects = PlatformManager()

    # def __str__(self):
    #     return self.platform

