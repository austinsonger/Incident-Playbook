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
Defines a |Passport| class for storing authentication information for
a third-party API.
"""

# third party
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from utils.validators.validators import key_file_validator

_KEYS_DIR = settings.KEYS_DIR
_KEYS_STORAGE = FileSystemStorage(location=_KEYS_DIR)


class Passport(models.Model):
    """
    Provides a generalized set of credentials used by APIs to
    authenticate a user or app. Different APIs may make use of different
    fields in the Passport model.

    Attributes
    ----------
    name : str
        An identifier for the |Passport|.

    key : `str` or `None`
        The consumer/client/developer key used to authenticate requests.

    file : `str` or `None`
        Path to a file for a public or private key, depending on the
        needs of the API authenticator. Acceptable extensions are
        defined by :const:`~KEY_FILE_TYPES`.

    secret : `str` or `None`
        A client/consumer secret used to authenticate requests.

    access_token : `str` or `None`
        An access token used for OAuth authentication.

    access_token_secret : `str` or `None`
        An access token secret used for OAuth authentication.

    public : bool
        Whether the |Passport| can be used by any user.

    users : AppUsers
        Specific |AppUsers| who are allowed to use the Passport.

    """

    KEY_FILE_TYPES = ['.pem', '.pub']
    """
    A |list| of acceptable extensions for a :attr:`Passport.file`.
    """

    name = models.CharField(max_length=40, unique=True)
    key = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        null=True,
        blank=True,
        storage=_KEYS_STORAGE,
        validators=[key_file_validator]
    )
    secret = models.CharField(max_length=255, null=True, blank=True)
    access_token = models.CharField(max_length=255, blank=True)
    access_token_secret = models.CharField(max_length=255, blank=True)
    public = models.BooleanField(
        default=False,
        help_text=_('Make available to all registered Users.')
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='passports',
        related_query_name='passport',
        blank=True,
        help_text=_('If not Public, restrict use to these Users.')
    )

    objects = GetByNameManager()

    def __str__(self):
        return self.name

    def get_call_count(self, start_time):
        """Get the number of times the |Passport| has been used since start_time.

        Parameters
        ----------
        start_time : |datetime|
            The start of the time frame in which calls should be counted.

        Returns
        -------
        int
            The number of |Stamps| associated with the |Passport| that
            have a :attr:`~ambassador.stamps.models.Stamp.job_start`
            greater or equal to `start_time`. This represents the number
            of API calls made with the |Passport| in that time.

        """
        return self.stamps.filter(job_start__gte=start_time).count()
