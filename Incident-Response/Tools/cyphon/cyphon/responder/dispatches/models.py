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
Defines a Dispatch class.
"""

# third party
from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField
from django.utils.functional import cached_property

# local
from alerts.models import Alert
from ambassador.records.models import Record, RecordManager


class Dispatch(Record):
    """
    A Record of an API call by a Courier.
    """
    alert = models.ForeignKey(
        Alert,
        related_name='dispatches',
        related_query_name='dispatch'
    )
    data = JSONField(blank=True, null=True)

    objects = RecordManager()

    class Meta:
        verbose_name_plural = 'dispatches'

    def __str__(self):
        return 'Dispatch %s' % self.pk

    @cached_property
    def title(self):
        """

        """
        return self.get_title()

    @cached_property
    def issued_by(self):
        """

        """
        return self.get_user()

    @cached_property
    def status_code(self):
        """

        """
        return self.get_status_code()

    @cached_property
    def response_msg(self):
        """

        """
        return self.stamp.notes

    def get_status_code(self):
        """

        """
        return self.stamp.status_code

    get_status_code.short_description = 'status code'

    def get_title(self):
        """

        """
        action = self.get_endpoint()
        return action.title

    get_title.short_description = 'title'

    def get_user(self):
        """

        """
        return self.stamp.user

    get_user.short_description = 'user'

    def finalize(self, cargo):
        """

        """
        # copy cargo.notes to dispatch.stamp.notes
        super(Dispatch, self).finalize(cargo)

        # copy cargo.data to dispatch.data
        self.data = cargo.data
        self.save()
