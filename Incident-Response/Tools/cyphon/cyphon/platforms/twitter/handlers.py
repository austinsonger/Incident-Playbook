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
Defines classes for Twitter searches.
"""

# standard library
import datetime
import logging

# third party
import tweepy

# local
from platforms.twitter.listener import CustomStreamListener
from aggregator.pumproom.faucet import Faucet
from ambassador.transport import Cargo
from utils.dateutils import dateutils as dt

_LOGGER = logging.getLogger(__name__)


class TwitterHandler(Faucet):
    """
    Base class for interacting with Twitter APIs.
    """

    def authenticate(self):
        """
        Method for authenticating with a Twitter API.
        """
        consumer_key = self.get_key()
        consumer_secret = self.get_secret()
        access_token = self.get_access_token()
        access_token_secret = self.get_access_token_secret()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth.set_access_token(access_token, access_token_secret)

        return auth


class SearchAPI(TwitterHandler):
    """
    Class for accessing the Twitter Search API.
    """

    @staticmethod
    def _format_timeframe(timeframe):
        """
        Takes a TimeFrame object and returns a string that formats the
        start and end of the TimeFrame for a Twitter Search API request.
        """
        dates = []

        start = timeframe.start
        end = timeframe.end

        if start:
            dates.append('since:' + dt.get_year_month_day(start))

        if end:

            # round up to the next day so we include the end date
            delta = datetime.timedelta(days=1)
            end += delta
            dates.append('until:' + dt.get_year_month_day(end))

        return u' '.join(dates)

    @staticmethod
    def _join_terms(terms):
        """
        Takes a list of strings (terms). If there are multiple strings,
        joins them with an "OR" operator for use with the Twitter Search
        API, and returns them as a single string. Otherwise, returns the
        single term as a string.
        """
        if len(terms) > 1:
            operator_str = ' OR '
            joined_terms = operator_str.join(terms)
            terms_str = '(' + joined_terms + ')'
        else:
            terms_str = terms[0]

        return terms_str

    def _format_searchterms(self, searchterms):
        """
        Takes a list of SearchTerm objects and returns a string of
        comma-separated values that format the SearchTerms for a Twitter
        Search API request.
        """
        included_terms = []
        excluded_terms = []
        all_terms = []

        for searchterm in searchterms:
            if searchterm.is_phrase():
                searchterm.wrap_in_quotes()

            if searchterm.negate:
                excluded_terms.append('-' + searchterm.term)
            else:
                included_terms.append(searchterm.term)

        if len(included_terms) > 0:
            included_terms_str = self._join_terms(included_terms)
            all_terms.append(included_terms_str)

        if len(excluded_terms) > 0:
            excluded_terms_str = (' ').join(excluded_terms)
            all_terms.append(excluded_terms_str)

        if len(all_terms) > 1:
            return u' '.join(all_terms)
        else:
            return u''.join(all_terms)

    def _format_accounts(self, accounts):
        """
        Takes a list of Account objects and returns a string of
        comma-separated values that format the Accounts for a Twitter
        Search API request.
        """
        accts = []

        for accounts in accounts:
            accts.append('@' + accounts.username)

        if len(accts) > 1:
            return self._join_terms(accts)
        else:
            return u''.join(accts)

    def _format_q_param(self, query):
        """
        Takes a list of SearchTerms and Accounts and returns a query
        string of terms for the q parameter of a Twitter Search API
        request.
        """
        query_str = []

        if query.searchterms:
            terms = self._format_searchterms(query.searchterms)
            query_str.append(terms)

        if query.accounts:
            accts = self._format_accounts(query.accounts)
            query_str.append(accts)

        if query.timeframe:
            dates = self._format_timeframe(query.timeframe)
            query_str.append(dates)

        return u' '.join(query_str)

    @staticmethod
    def _format_geocode_param(location):
        """
        Takes a circular Location object and returns a query string for
        the location parameter of a Twitter Search API request.

        The parameter value is specified by "latitide,longitude,radius",
        where radius units must be specified as either "mi" (miles) or
        "km" (kilometers), e.g., "37.781157,-122.398720,1mi".
        """
        coords = location.geom.tuple

        if len(coords) != 2:  # pragma: no cover
            raise ValueError('Location must be a point')

        return '%s,%s,%skm' % (location.geom.tuple[1],
                               location.geom.tuple[0],
                               location.radius_km)

    def _format_query(self, query):
        """
        Takes a ReservoirQuery object and constructs a dictionary of
        keyword arguments to use with the Twitter API.
        """
        kwargs = {
            'q': self._format_q_param(query),
            'result_type': 'recent'
        }

        if query.locations:
            location = query.locations[0]
            kwargs['geocode_param'] = self._format_geocode_param(location)

        return kwargs

    def _get_statuses(self, query):
        """
        Takes a ReservoirQuery object and returns a tweepy Cursor of search
        results.
        """
        formatted_query = self._format_query(query)
        auth = self.authenticate()
        api = tweepy.API(auth)
        return tweepy.Cursor(api.search, **formatted_query)

    def process_request(self, obj):
        """Convert a ReservoirQuery into an API request and get the response.

        Parameters
        ----------
        obj : |ReservoirQuery|

        Returns
        -------
        |Cargo|

        """
        try:
            # TODO(LH): handle rate limit
            cursor = self._get_statuses(obj)
            data = [status._json for status in cursor.items()]
            status_code = 200
        except tweepy.TweepError as error:
            data = []
            status_code = error.api_code

        return Cargo(status_code=status_code, data=data)


class PublicStreamsAPI(TwitterHandler):
    """
    Class for accessing the Twitter Streaming API.
    """

    @staticmethod
    def _format_followees_param(accounts):
        """
        Takes a list of Account objects and returns a list of user IDs,
        indicating the users whose Tweets should be delivered on the
        stream.
        """
        accts = []

        for account in accounts:
            accts.append(str(account.user_id))

        return accts

    @staticmethod
    def _format_locations_param(locations):
        """
        Takes a list of Location objects and returns a list of
        longitude,latitude pairs specifying a set of bounding boxes to
        filter tweets, e.g., [-122.75,36.8,-121.75,37.8,-74,40,-73,41].
        Only geolocated tweets falling within the requested bounding
        boxes will be included; unlike the Search API, the user's
        location field is not used to filter tweets.
        """
        locs = []

        for location in locations:
            polygon = location.bbox
            extent = list(polygon.extent)
            locs.extend(extent)

        return locs

    @staticmethod
    def _format_searchterms_param(searchterms):
        """
        Takes a list of SearchTerm objects and returns a list of phrases
        which will be used to determine what Tweets will be delivered on
        the stream.
        """
        terms = []

        for searchterm in searchterms:
            if searchterm.is_phrase():
                searchterm.wrap_in_quotes()
            if not searchterm.negate:
                terms.append(searchterm.term)

        return terms

    def _format_query(self, query):
        """
        Takes a ReservoirQuery object and constructs a dictionary of
        Twitter keyword arguments to use with the Twitter API.
        """
        kwargs = {}

        if query.accounts:
            kwargs['follow'] = self._format_followees_param(query.accounts)
        if query.locations:
            kwargs['locations'] = self._format_locations_param(query.locations)
        if query.searchterms:
            kwargs['track'] = self._format_searchterms_param(query.searchterms)

        return kwargs

    def process_request(self, obj):
        """
        Method for processing a query with the Twitter Public Streams
        API.
        """
        auth = self.authenticate()
        listener = CustomStreamListener(faucet=self)
        stream = tweepy.Stream(auth, listener)
        kwargs = self._format_query(obj)
        stream.filter(**kwargs)

        _LOGGER.info('Received %s objects from Twitter and saved %s of them',
                     stream.listener.data_count,
                     stream.listener.saved_data_count)

        return Cargo(status_code=listener.status_code, notes=listener.notes)
