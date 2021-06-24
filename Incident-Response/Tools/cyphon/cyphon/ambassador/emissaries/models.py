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
Defines an |Emissary| base class for interacting with third-party APIs.

Note
----
The |Emissary| class is the basis for the |Courier| and |Plumber|
classes.

"""

# standard library
import datetime

# third party
from django.db import models
from django.utils import timezone

# local
from ambassador.passports.models import Passport
from ambassador.visas.models import Visa
from cyphon.models import SelectRelatedManager, GetByNameMixin


class EmissaryManager(SelectRelatedManager, GetByNameMixin):
    """
    Adds methods to the default model manager.
    """

    def find_public(self, endpoint):
        """Get |Emissaries| that are available to all users.

        Parameters
        ----------
        endpoint : |Endpoint|
            An |Endpoint| used to find related |Emissaries|.

        Returns
        -------
        |QuerySet|
            A |QuerySet| containing |Emissaries| available to all
            |AppUsers|.

        """
        return self.filter(
            passport__public=True,
            endpoints=endpoint
        )

    def find_private(self, endpoint, user):
        """Find |Emissaries| that are assigned to the given user.

        Parameters
        ----------
        endpoint : |Endpoint|
            An |Endpoint| used to find related |Emissaries|.

        user : |AppUser|
            The |AppUser| used to find available |Emissaries|.

        Returns
        -------
        |QuerySet|
            A |QuerySet| containing |Emissaries| available to the `user`
            that have a |Passport| that is not
            :attr:`~ambassador.passports.models.Passport.public`.

        """
        return self.filter(
            passport__public=False,
            endpoints=endpoint,
            passport__users=user
        )

    def find_any(self, endpoint, user=None):
        """Find any |Emissary| that can be used for the API call.

        Parameters
        ----------
        endpoint : |Endpoint|
            An |Endpoint| used to find related |Emissaries|.

        user : |AppUser| or |None|, optional
            The |AppUser| used to find available |Emissaries|.

        Returns
        -------
        |QuerySet|
            A |QuerySet| containing |Emissaries| that are compatible
            with the `endpoint` and `user`.

        Note
        ----
        If `user` is |None| or the |AppUser| has no |Emissaries|
        assigned to them, only |Emissaries| with a
        :attr:`~ambassador.passports.models.Passport.public` |Passport|
        will be returned.

        """
        private_emissaries = self.find_private(endpoint, user)
        if private_emissaries:
            return private_emissaries
        else:
            return self.find_public(endpoint)


class Emissary(models.Model):
    """
    Provides access to one or more API enpdoints.

    Attributes
    ----------
    name : str
        The identifier for the |Emissary|.

    passport : Passport
        The |Passport| used by the |Emissary| to access the |Emissary|'s
        `endpoints`. (See note.)

    visa : Visa
        The |Visa| used to define a rate limit for the |Emissary| when
        accessing any of the |Emissary|'s `endpoints`.

    Note
    ----
    The `endpoints` attribute is defined in |Emissary| subclasses,
    such as the |Courier| and |Plumber| classes.

    """
    name = models.CharField(max_length=40, unique=True)
    passport = models.ForeignKey(Passport, null=True)
    visa = models.ForeignKey(Visa, blank=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('passport', 'visa')

    def __str__(self):
        return self.name

    def _get_call_count(self, start_time):
        """
        Takes a datetime and returns an int of the number of calls
        recorded since that time.
        """
        return self.passport.get_call_count(start_time)

    def _get_allowed_calls(self):
        """
        Returns the number of calls allowed in a request interval.
        """
        return self.visa.calls

    def _get_time_interval_in_minutes(self):
        """
        Returns the number of minutes in a request interval.
        """
        return self.visa.get_request_interval_in_minutes()

    def _get_interval_start_time(self):
        """
        Returns a datetime for the start of the current rate limit
        interval.
        """
        current_time = timezone.now()
        minutes = self._get_time_interval_in_minutes()
        time_delta = datetime.timedelta(minutes=minutes)
        return current_time - time_delta

    def _has_endpoint(self, endpoint):
        """
        Takes an Endpoint and returns a Boolean indicating whether it
        is associated with the Emissary.
        """
        return self.endpoints.filter(pk=endpoint.pk).exists()

    def _has_valid_visa(self):
        """
        Returns a Boolean indiacting whether the Emissary has a valid
        Visa.
        """
        if self.visa is not None:
            return self.visa_is_valid()
        else:
            return False

    def _can_access_endpoint(self, endpoint):
        """
        Takes an Endpoint and returns a Boolean indicating whether the
        Emissary ia allowed to access it.
        """
        if endpoint.visa_required:
            return self._has_valid_visa()
        else:
            return True

    def call_count(self):
        """Get the number of calls made in the current rate limit
        interval.

        Returns
        -------
        |int|
            The number of calls made during the current rate limit
            interval.

        """
        start_time = self._get_interval_start_time()
        return self._get_call_count(start_time)

    def remaining_calls(self):
        """Get the number of calls that can be made in the current
        interval.

        Returns
        -------
        |int|
            The number of additional calls that can be made in the
            current request interval.

        """
        if self.visa is None:  # pragma: no cover
            raise RuntimeError('No Visa exists.')
        calls_allowed = self._get_allowed_calls()
        calls_made = self.call_count()
        return calls_allowed - calls_made

    def visa_is_valid(self):
        """Return |True| if the |Emissary| has not reached its |Visa|'s
        limit.

        Returns
        -------
        bool
            Whether the |Emissary| can make additional calls in the
            current rate limit interval.

        """
        if self.visa is None:  # pragma: no cover
            raise RuntimeError('No Visa exists.')
        return self.remaining_calls() > 0

    def enabled(self, endpoint):
        """Return |True| if the |Emissary| can make API calls to the
        endpoint.

        Parameters
        ----------
        endpoint : |Endpoint|
            The |Endpoint| to be accessed by the |Emissary|.

        Returns
        -------
        |bool|
            Whether the |Emissary| can make API calls to the `endpoint`.

        Note
        ----
        This method will return |False| if any of the following applies
        to the |Emissary|:

            - it is not associated with the `endpoint`
            - it lacks a |Visa| and the `endpoint` requires a |Visa|
            - it has exceeded the rate limit defined by its |Visa|

        """
        if self._has_endpoint(endpoint):
            return self._can_access_endpoint(endpoint)
        else:
            return False

    def calculate_query_time_in_minutes(self, query_cnt):
        """Get the number of minutes required to execute the queries.

        Parameters
        ----------
        query_cnt : |int|
            The number of queries that need to be performed.

        Returns
        -------
        |float|
            The number of minutes required to fulfill all the queries
            based on the |Emissary|'s |Visa|.

        """
        remaining_calls = self._get_remaining_calls()
        balance = remaining_calls - query_cnt

        if balance < 0:
            allowed_calls = self.get_allowed_calls()
            needed_calls = abs(balance)

            # get the floor of the number of intervals needed to fulfill
            # all the requests; we use the floor because we assume we
            # will make the next batch of requests as soon as a new
            # interval starts, rather than spreading them out over the
            # interval - so we don't count time from the last interval
            num_intervals = needed_calls // allowed_calls
            extra_time = num_intervals * self.get_time_interval_in_minutes()
            time_left_in_current_intrvl = self.get_time_remaining_in_minutes()
            return time_left_in_current_intrvl + extra_time
        else:
            return 0

