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
Defines a |Platform| base class. Handles settings for which third-party
platforms are enabled.

Note
----
The |Platform| class is the basis for the |Destination| and |Reservoir|
classes.

"""

# third party
from django.db import models

# local
from cyphon.models import GetByNameManager, FindEnabledMixin
from platforms.registry import PLATFORM_CHOICES


class PlatformManager(GetByNameManager, FindEnabledMixin):
    """
    Adds methods to the default model manager.
    """
    pass


class Platform(models.Model):
    """
    Determines whether a third-party platform (such as Twitter) is
    enabled for use. A |Platform| corresponds to a subpackage in the
    :doc:`/modules/platforms` package.

    Attributes
    ----------
    name : str
        The name of the :doc:`/modules/platforms` subpackage for
        accessing a third-party API (e.g., 'twitter').

    enabled : bool
        Whether the |Platform| is available for use.

    """
    name = models.CharField(max_length=16, unique=True,
                            choices=PLATFORM_CHOICES)
    enabled = models.BooleanField(default=True)

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name
