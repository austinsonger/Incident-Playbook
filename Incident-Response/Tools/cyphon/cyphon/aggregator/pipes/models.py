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
Defines a class for a data platform's API. Stores information on
an API's rate limits and parameter limits. Also stores information on
how to access the specific class needed to handle a query to the API.
"""

# standard library
import logging

# third party
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from aggregator.reservoirs.models import Reservoir
from ambassador.endpoints.models import Endpoint, EndpointManager
from cyphon.choices import LOCATION_FORMAT_CHOICES, LOGIC_CHOICES

LOGGER = logging.getLogger(__name__)


class Pipe(Endpoint):
    """
    Specifies the module and |Faucet| class that should be used to
    access an API endpoint of a |Reservoir|, such as Twitter.

    A |Pipe| can have a |PipeSpecSheet| that details information on the
    API's parameter limits.

    Since a |Reservoir| may be accessed using more than one API (e.g.,
    Twitter Search API vs. Twitter Public API), |Pipes| have a
    many-to-one relationship with |Reservoirs|.

    Attributes
    ----------
    platform : |Reservoir|
        The data platform which the API endpoint accesses.

    """
    platform = models.ForeignKey(Reservoir)

    objects = EndpointManager()

    class Meta:
        """
        Metadata options.
        """
        unique_together = ('platform', 'api_class')

    def get_specsheet(self):
        """
        Returns the Specs for the Pipe if it has them.
        """
        if hasattr(self, 'specsheet'):
            return self.specsheet


class PipeSpecSheet(models.Model):
    """
    Contains info on search parameter formats and limits.

    Attributes:
        pipe: the ForeignKey for the Pipe with which the SpecSheet is associated
        streaming: a Boolean indicating whether the API endpoint is for streaming
        searchterms_limit: the maximum number of search terms allowed in a query
        followees_limit: the maximum number of user accounts that can be
            included in a query
        locations_limit: the maximum number of locations that can be searched
            in a query
        location_format: whether the API takes a location as a bounding box or
            a search radius
        radius_limit_km: the maximum radius of a search area accepted,
            in kilometers
        combine_trm_dt: a Boolean indicating whether timeframes count toward
            the search term limit; if true, start datetime and end datetime each
            count as a search term
        combine_trm_fol: a Boolean indicating whether search terms and followees
            share the same parameter space and therefore the same limit;
            if true, also indicates than terms and followees can be joined with
            an "OR" operator if one is available
        combine_trm_loc: a Boolean indicating whether search terms and locations
            share the same parameter space and therefore the same limit;
            if true, also indicates than terms and locations can be joined with
            an "OR" operator if one is available
        combine_trm_opr: a Boolean indicating whether logical operators count
            toward the search term limit
        accepts_phrases: whether the API accepts phrases (if False,
            only takes keywords)
        trm_trm_logic: a logical "AND" or "OR" operator indicating how multiple
            terms are evaluated in a query (i.e., with an intersection vs.
            a union of results)
        trm_fol_logic: a logical "AND" or "OR" operator indicating how terms and
            followees are evaluated in a query (i.e., with an intersection vs.
            a union of results)
        trm_loc_logic: a logical "AND" or "OR" operator indicating how terms and
            locations are evaluated in a query (i.e., with an intersection vs.
            a union of results)
        OR_operator: a string that the API uses as an "OR" operator; can be used
            to join arguments in the search terms parameter space
        NOT_operator: a string that the API uses as a "NOT" operator

        #TODO(LH): add validator that makes sure logic fields have values if limits are > 1
    """
    pipe = models.OneToOneField(
        Pipe,
        primary_key=True,
        related_name='specsheet'
    )

    streaming = models.BooleanField(default=False)
    searchterms_limit = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Search-term limit'),
        help_text=_('Maximum number of search terms in a query.')
    )
    followees_limit = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Followee limit'),
        help_text=_('Maximum number of user accounts in a query.')
    )
    locations_limit = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Location limit'),
        help_text=_('Maximum number of user accounts in a query.')
    )
    location_format = models.CharField(
        max_length=6,
        choices=LOCATION_FORMAT_CHOICES
    )
    radius_limit_km = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_('Radius limit in km'),
        help_text=_('Maximum radius of a search area in kilometers')
    )
    combine_trm_dt = models.BooleanField(
        default=False,
        verbose_name=_('Time frames count toward search-term limit')
    )
    combine_trm_fol = models.BooleanField(
        default=False,
        verbose_name=_('Followees count toward search-term limit')
    )
    combine_trm_loc = models.BooleanField(
        default=False,
        verbose_name=_('Locations count toward search-term limit')
    )
    combine_trm_opr = models.BooleanField(
        default=False,
        verbose_name=_('Logical operators count toward search-term limit')
    )
    accepts_phrases = models.BooleanField(default=True)
    trm_trm_logic = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        choices=LOGIC_CHOICES,
        verbose_name=_('Term-Term logic'),
        help_text=_('Operator used to combine search terms.')
    )
    trm_fol_logic = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        choices=LOGIC_CHOICES,
        verbose_name=_('Term-Followee logic'),
        help_text=_('Operator used to combine search terms and followees.')
    )
    trm_loc_logic = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        choices=LOGIC_CHOICES,
        verbose_name=_('Term-Location logic'),
        help_text=_('Operator used to combine search terms and locations.')
    )
    OR_operator = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_('String used for an "OR" operator, if applicable.')
    )
    NOT_operator = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text=_('String used for a "NOT" operator, if applicable.')
    )

    def __str__(self):
        return str(self.pipe)
