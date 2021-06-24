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
Provides platform choices that can be used to limit choices for
Reservoirs and Destinations. Constructs choices from the names of
subpackages in the platforms package.

Also establishes constants for certain package and module names. These
are used to import modules needed to handle queries to specific APIs.
"""

# standard library
import os

# local
from utils.choices import choices


def get_this_package():
    """
    Returns the name of the package in which this module resides.
    """
    current_path = os.path.dirname(__file__)
    return os.path.basename(current_path)


# The name of this package, which contains subpackages for specific social media
# platforms.
PLATFORMS_PACKAGE = get_this_package()

# Packages for social media platforms that can be chosen as a Reservoir.
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
PLATFORM_CHOICES = choices.get_package_choices(ABSOLUTE_PATH)

# Standard name for a module in a platform package that handles
# queries to APIs. These modules contain the classes associated with
# Endpoints.
HANDLERS_MODULE = 'handlers'

