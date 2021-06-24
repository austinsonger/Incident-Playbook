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
Provides constants for locating |Engine| subclasses.

[`source`_]

=========================  ================================================
Constant                   Description
=========================  ================================================
:const:`~ENGINES_PACKAGE`  The name of this package.
:const:`~ENGINE_MODULE`    Name for modules containing |Engine| subclasses.
:const:`~CURRENT_PATH`     Path containing `engines` subpackages.
:const:`~BACKEND_CHOICES`  Choices for data stores (e.g., Elasticsearch).
=========================  ================================================

.. _source: ../_modules/engines/registry.html

"""

# standard library
import os

# local
from utils.choices import choices


def _get_this_package():
    """Get the name of this package.

    Returns the name of the package in which this module resides.
    """
    current_path = os.path.dirname(__file__)
    return os.path.basename(current_path)


ENGINES_PACKAGE = _get_this_package()
"""|str|

The name of this package, which contains subpackages for specific
backends.
"""

ENGINE_MODULE = 'engine'
"""|str|

Standard name for a module in an `engines` subpackage that contains an
|Engine| sublclass used to interact with a data store.
"""

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
"""|str|

Path containing `engines` subpackages for particular backends.
"""

BACKEND_CHOICES = choices.get_package_choices(CURRENT_PATH)
"""|tuple| of |tuple|

Backend choices, based on `engines` subpackages. Each item provides a
(value, label) choice for a package, which can be used in a `choices`
argument for a CharField in a Django Model, e.g.::

    (
        ('elasticsearch', 'elasticsearch'),
        ('mongodb', 'mongodb'),
    )

"""
