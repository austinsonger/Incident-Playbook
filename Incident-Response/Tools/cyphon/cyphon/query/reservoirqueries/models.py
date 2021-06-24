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

# standard library
import re

# third party
from django.db import models
from django.conf import settings

# local
from aggregator.pumproom.pumproom import PumpRoom
from aggregator.reservoirs.models import Reservoir
from query.reservoirqueries.reservoirquery import ReservoirQuery
from target.locations.models import Location
from target.searchterms.models import SearchTerm
from target.timeframes.models import TimeFrame


class ReservoirQueryParameters(models.Model):
    """
    Model used for constructing a ReservoirQuery object from form input.
    """
    JOIN_CHOICES = (
        ('AND', 'satisfy both keyword and location conditions'),
        ('OR', 'satisfy either keyword or location conditions')
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True
    )
    reservoirs = models.ManyToManyField(
        Reservoir,
        limit_choices_to={'enabled': True}
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    included_keywords = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Contains at least one of the keywords"
    )
    excluded_keywords = models.CharField(
        blank=True,
        max_length=255,
        verbose_name="Does not contain the keywords"
    )
    locations = models.ManyToManyField(Location, blank=True)
    trm_loc_logic = models.CharField(
        max_length=5,
        choices=JOIN_CHOICES,
        default='AND',
        verbose_name='Query type'
    )

    @staticmethod
    def _parse_keywords(keywords):
        """
        Takes a string of comma-separated or space-separated keywords/phrases
        and returns a list of keywords/phrases.
        """
        keyword_array = [keywords]

        phrases = re.findall('".*?"', keywords)
        words = re.sub('".*?"', ' ', keywords)

        if re.search(',', words):
            keyword_array = words.split(',')
        elif re.search(' ', words):
            keyword_array = words.split(' ')

        keyword_array.extend(phrases)
        return keyword_array

    def _create_terms_by_type(self, keywords, negate=False):
        """
        Takes a string of comma-separated or space-separated keywords/phrases
        and a Boolean indicating whether they should be negated in a text
        search. Returns a list of SearchTerm objects.
        """
        keyword_array = self._parse_keywords(keywords)

        searchterms = []
        for keyword in keyword_array:
            cleaned_keyword = keyword.strip()
            cleaned_keyword = cleaned_keyword.replace('"', '')
            if cleaned_keyword != '':
                term = SearchTerm(term=cleaned_keyword, negate=negate)
                searchterms.append(term)

        return searchterms

    def _create_searchterms(self):
        """
        Takes a string of comma-separated or space-separated keywords/phrases
        and returns a list of SearchTerm objects.
        """
        included_terms = self._create_terms_by_type(self.included_keywords, False)
        excluded_terms = self._create_terms_by_type(self.excluded_keywords, True)

        searchterms = []
        searchterms.extend(included_terms)
        searchterms.extend(excluded_terms)

        return searchterms

    def _create_timeframe(self):
        """
        Returns a TimeFrame object representing the start and end times
        specified in the query parameters.
        """
        timeframe = TimeFrame()
        if self.start_time:
            timeframe.start = self.start_time
        if self.end_time:
            timeframe.end = self.end_time
        return timeframe

    def _create_reservoir_query(self):
        """
        Returns a ReservoirQuery based on the ReservoirQueryParameters.
        """
        return ReservoirQuery(
            locations=self.locations.all(),
            searchterms=self._create_searchterms(),
            timeframe=self._create_timeframe(),
            trm_loc_logic=self.trm_loc_logic
        )

    def _get_reservoirs(self):
        """
        If Reservoirs were specified in the query paramters, returns a QuerySet
        of those Reservoirs. Otherwise, returns a QuerySet of all enabled
        Reservoirs.
        """
        if self.reservoirs:
            return self.reservoirs
        return Reservoir.objects.find_enabled()

    def execute_ad_hoc_search(self):
        """
        Performs an ad hoc search using the ReservoirQueryParameters.
        """
        reservoirs = self._get_reservoirs()

        # ReservoirQuery object created from ReservoirQueryParameters
        query = self._create_reservoir_query()

        pumproom = PumpRoom(
            reservoirs=reservoirs,
            task='ADHOC_SRCH',
            user=self.created_by
        )
        return pumproom.get_results(query)

