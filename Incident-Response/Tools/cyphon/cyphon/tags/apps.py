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
Configures the :ref:`Tags<tags>` app.

============================  ===============================
Class                         Description
============================  ===============================
:class:`~TagsConfig`          |AppConfig| for |Tags|.
============================  ===============================

"""

# third party
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TagsConfig(AppConfig):
    """|AppConfig| for |Tags|."""

    name = 'tags'
    verbose_name = _('Tags')

    def ready(self):
        """Override the default :meth:`~django.apps.AppConfig.ready` method.

        Registers :mod:`~tags.signals` used in the app.
        """
        import tags.signals  # noqa: F401
