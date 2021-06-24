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

# standard library
import re

# local
from distilleries.models import Distillery
from .search_parameter import SearchParameter, SearchParameterType


class DistilleryFilterParameter(SearchParameter):
    """
    Class representing a search query parameter that wants to filter
    the distilleries it searches through.

    Attributes
    ----------
    filter : str
        String representation of distilleries to filter.

    distilleries : django.db.models.query.QuerySet
        Matching distillery objects.

    """

    FILTER_REGEX = re.compile(r'^@source=\"(?P<filter>.+)\"$')
    """RegExp

    Regex used to get the distillery filter value from the parameter string.
    """

    INVALID_PARAMETER = 'Invalid parameter string.'
    """str

    Errors message explaining that the given parameter string is invalid.
    """

    FILTER_VALUE_IS_EMPTY = 'Distillery filter value is empty.'
    """str

    Error message explaining that the string value to filter distilleries
    with is an empty string.
    """

    NO_MATCHING_DISTILLERIES = 'There were no matching distilleries for `{}`.'
    """str

    Error message explaining that the distillery filter returned
    no distilleries.
    """

    def __init__(self, index, parameter, user):
        """Constructor for DistilleryFilterParameter.

        Parameters
        ----------
        index : int
            Index of this search parameter in the search query string.
        parameter : str
            String representation of this parameter.
        user : appusers.models.AppUser
        """
        super(DistilleryFilterParameter, self).__init__(
            index,
            parameter,
            SearchParameterType.DISTILLERY,
        )
        self.filter = self._get_filter(parameter)

        if not self.is_valid():
            return

        self.distilleries = self._get_distilleries(self.filter, user)

    def _get_filter(self, parameter):
        """Return the distillery filter value from the parameter string.

        If parameter or distillery filter value is invalid, it also adds
        those errors to the parameter.

        Parameters
        ----------
        parameter : str
            String representation of this parameter.

        Returns
        -------
        str
            String representation of the distilleries to filter.

        """
        match_object = DistilleryFilterParameter.FILTER_REGEX.match(parameter)

        if match_object is None:
            self._add_error(DistilleryFilterParameter.INVALID_PARAMETER)
            return ''

        distillery_filter = match_object.group('filter')

        if distillery_filter is None:
            self._add_error(DistilleryFilterParameter.FILTER_VALUE_IS_EMPTY)
            return ''

        return distillery_filter

    def _get_distilleries(self, name, user):
        """Return the distillery objects related to warehouse/collection names.

        If a related distillery cannot be found, adds a
        NO_MATCHING_DISTILLERIES error to the parameter.

        Parameters
        ----------
        name : str
            Distillery name to get related distilleries with.

        user: appusers.models.AppUser

        Returns
        -------
        list of Distillery
            Distilleries related to the given warehouse/collection names.

        """
        distillery_qs = Distillery.objects.filter(name__icontains=name)

        if not user.is_staff:
            distillery_qs = distillery_qs.filter(company=user.company)

        if not distillery_qs.count():
            self._add_error(
                DistilleryFilterParameter.NO_MATCHING_DISTILLERIES.format(name))

        return distillery_qs

    def as_dict(self):
        """Return a JSON serializable representation of this object.

        Returns
        -------
        dict

        """
        info = super(DistilleryFilterParameter, self).as_dict()
        distillery_names = [
            distillery.name
            for distillery
            in self.distilleries
        ]
        info.update({
            'filter': self.filter,
            'distilleries': distillery_names,
        })

        return info
