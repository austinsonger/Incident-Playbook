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

# third party
from django.apps import AppConfig
from django.conf import settings
from django.db import close_old_connections
from django.db.utils import ProgrammingError

_IN_TESTING_MODE = settings.TEST


class StreamsConfig(AppConfig):
    """

    """
    name = 'aggregator.streams'
    verbose_name = 'Streams'

    def ready(self):
        """

        """
        from .models import Stream

        if not _IN_TESTING_MODE:
            try:
                Stream.objects.close_all()
                close_old_connections()
            except ProgrammingError:  # if migrations have not been run
                pass
