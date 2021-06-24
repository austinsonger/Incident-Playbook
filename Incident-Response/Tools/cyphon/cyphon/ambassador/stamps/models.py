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
Defines a Visa class for the documenting API calls.
"""

# third party
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# local
from ambassador.passports.models import Passport


class Stamp(models.Model):
    """
    Stores a record of an API request and its response.

    Attributes
    ----------
    content_type : ContentType
        The |ContentType| of the model representing the API endpoint.
        This can be either an |Action| or a |Pipe|.

    object_id : int
        A positive |int| representing the Object Id of the `endpoint`.

    endpoint : `Action` or `Pipe`
        An |Action| or |Pipe| representing an API endpoint.

    passport : Passport
        A |Passport| used to access the API endpoint.

    user : `AppUser` or `None`
        The |AppUser| who initiated the call to the API endpoint.

    job_start : datetime
        A |datetime| representing when the request to the API was made.
        The default is the current time.

    job_end : `datetime` or `None`
        A |datetime| when the response from the API was recieved. In the
        case of a streaming API, indicates when the stream was closed.

    status_code : `str` or `None`
        The HTTP status code for the API response (e.g., '200').

    notes : `str` or `None`
        Additional information about the API response, such as an error
        message.

    """
    _ACTION = models.Q(app_label='actions', model='action')
    _PIPE = models.Q(app_label='pipes', model='pipe')
    _CONTENT_TYPES = _ACTION | _PIPE

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=_CONTENT_TYPES,
        verbose_name=_('endpoint type')
    )
    object_id = models.PositiveIntegerField(verbose_name=_('endpoint id'))
    endpoint = GenericForeignKey()
    passport = models.ForeignKey(
        Passport,
        related_name='stamps',
        related_query_name='stamp'
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    job_start = models.DateTimeField(default=timezone.now)
    job_end = models.DateTimeField(null=True, blank=True)
    status_code = models.CharField(max_length=3, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return 'PK %s: %s (%s) %s' % (self.pk, self.endpoint, self.status_code,
                                      self.job_start)

    def finalize(self, status_code=None, notes=None):
        """Update the |Stamp| with status_code and notes about the API response.

        Parameters
        ----------
        status_code : |str| or |None|
            The HTTP status code (e.g., '200') for the API response.

        notes : |str| or |None|
            Notes about the API response, such as an error message.

        Returns
        -------
        self : |Stamp|

        """
        self.job_end = timezone.now()
        if status_code is not None:
            self.status_code = status_code
        if notes is not None:
            self.notes = notes
        self.save()
        return self

    def is_obsolete(self):
        """
        Returns a Boolean indicating whether a more recent call has been
        made to the same endpoint with the same credentials.
        """
        last_success = Stamp.objects.filter(
            passport=self.passport,
            object_id=self.object_id,
            content_type=self.content_type).first()
        return self != last_success

