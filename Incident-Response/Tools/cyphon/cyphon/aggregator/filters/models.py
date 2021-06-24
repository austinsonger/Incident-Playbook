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
Defines a class for a search filter, which can refer to a |Followee|,
|Location|, or |SearchTerm|.
"""

# third party
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

# local
from cyphon.models import FindEnabledMixin
from query.reservoirqueries.models import ReservoirQuery
from target.followees.models import Followee
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame


class FilterManager(models.Manager, FindEnabledMixin):
    """
    Adds methods to the default model manager.
    """

    @staticmethod
    def _get_followee_accounts(followees):
        """
        Takes a list of |Followees| and returns a list of |Accounts|
        associated with the |Followees|.
        """
        accounts = []

        for followee in followees:
            accts = list(followee.accounts.all())
            accounts.extend(accts)

        return accounts

    def _find_enabled_filters_by_type(self, content_type):
        """
        Takes a |ContentType| and returns a |QuerySet| of |Filters|
        associated with that |ContentType|.
        """
        enabled_filters = self.find_enabled()
        return enabled_filters.filter(content_type=content_type)

    def _get_targets_by_type(self):
        """
        Gets Filters grouped by the class of their filter_object.
        Returns a dict mapping target model types (e.g. Account,
        Location, or SearchTerm) to a QuerySet of Filters
        associated with those models.
        """
        targets = (Followee, Location, SearchTerm)
        content_types = ContentType.objects.get_for_models(*targets)
        targets = {}

        for key in content_types:
            content_type = content_types[key]
            filters = self._find_enabled_filters_by_type(content_type)
            target_list = [obj.filter_object for obj in filters]
            targets[key] = target_list

        return targets

    def _get_oldest_time_last_used(self):
        """
        Returns a datetime for the oldest time an enabled Filter
        was last used.
        """
        default_queryset = self.get_queryset()
        enabled_filters = default_queryset.filter(enabled=True)
        aggregation = enabled_filters.aggregate(models.Min('last_used'))
        return aggregation['last_used__min']

    def _create_timeframe(self):
        """
        Returns a TimeFrame with no end value and a start value
        of the oldest time an enabled Filter was last used.
        """
        oldest_time = self._get_oldest_time_last_used()
        return TimeFrame(start=oldest_time)

    def update_enabled_filters(self):
        """Update the :attr:`~filters.models.Filter.last_used` field of
        enabled |Filters|.

        Returns
        -------
        None

        """
        current_time = timezone.now()
        self.find_enabled().update(last_used=current_time)

    def create_reservoir_query(self):
        """Create a |ReservoirQuery| object using all enabled |Filters|.

        Returns
        -------
        ReservoirQuery
            A |ReservoirQuery| that uses all enabled |Filters|.

        """
        # convert QuerySets to lists
        targets = self._get_targets_by_type()
        followees = targets[Followee]
        locations = targets[Location]
        searchterms = targets[SearchTerm]

        timeframe = self._create_timeframe()

        accounts = self._get_followee_accounts(followees)

        query = ReservoirQuery(
            accounts=accounts,
            locations=locations,
            searchterms=searchterms,
            timeframe=timeframe,
            trm_loc_logic='OR'
        )

        return query


class Filter(models.Model):
    """
    Represents a search parameter used in ongoing background searches.

    A |Filter| is a search parameter used for "streaming" background
    searches of |Reservoirs|. A |Filter| can represent a |Followee|,
    |Location|, or |SearchTerm|.

    A |Filter| keeps track of the date it was created, the date
    it was last used, and whether it is currently enabled.

    Attributes
    ----------
    id : int
        The primary key of the |Filter|.

    content_type : ContentType
        The |ContentType| of the :attr:`~Filter.filter_object`. Used to
        define a generic relation.

    object_id : int
        The primary key of the :attr:`~Filter.filter_object`. Used to
        define a generic relation.

    filter_object : Followee, Location, or SearchTerm
        The object defining the search parameter.

    date_created : datetime
        A |datetime| for when the |Filter| was created.

    last_used : datetime
        A |datetime| for when the |Filter| was last used in a query.

    enabled : bool
        ``True`` if the |Filter| should be included in background
        searches. ``False`` otherwise.

    Notes
    -----
    Because data for |Followees|, |Locations|, and |SearchTerms|
    are modeled differently and are therefore stored in different
    tables, a |Filter| stores the reference to this object in the
    :attr:`~Filter.filter_object` field as a |GenericForeignKey|.

    See also
    --------
    For further background, see Django's documentation on
    `Generic Relations`_.

    """

    # get the models that can serve as filters
    _FOLLOWEE = models.Q(app_label='followees', model='followee')
    _LOCATION = models.Q(app_label='locations', model='location')
    _SEARCHTERM = models.Q(app_label='searchterms', model='searchterm')
    _FILTERS = _FOLLOWEE | _LOCATION | _SEARCHTERM

    content_type = models.ForeignKey(ContentType, limit_choices_to=_FILTERS)
    object_id = models.PositiveIntegerField()
    filter_object = GenericForeignKey()
    date_created = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    objects = FilterManager()

    def __str__(self):
        return "%s (%s)" % (self.filter_object, self.filter_type)

    @property
    def filter_type(self):
        """
        |str|: the lowercase name of the model for the type
        of filter, which can be either a |Followee|, |Location|,
        or |SearchTerm|.
        """
        return self.content_type.model

