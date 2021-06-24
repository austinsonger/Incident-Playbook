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
Provides package choices that can be used to limit choices for Labs.
Constructs choices from the names of subpackages in the Labs package.

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


LABS_PACKAGE = get_this_package()

ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
LAB_CHOICES = choices.get_package_choices(ABSOLUTE_PATH)
