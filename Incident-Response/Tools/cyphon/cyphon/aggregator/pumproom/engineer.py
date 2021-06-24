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
Defines a Engineer class for formatting a query to conform to API limits.
"""

# standard library
from copy import deepcopy

# local
from utils.parserutils import parserutils


class Engineer(object):
    """
    Examines API limits (Specs) for a Pipe and ensures that a query conforms
    to those limits. May refactor the original query into a set of queries
    if necessary.

    Attributes:
        _query: a ReservoirQuery object
        _specs: a Specs object

    """

    def __init__(self, query, specs):
        self._query = query
        self._specs = specs

    def _get_spec(self, name):
        """
        Takes the name of a Specs attribute and returns its value.
        Returns None if the attribute does not exist.
        """
        return getattr(self._specs, name, None)

    def _get_query_trm_loc_logic(self):
        """

        """
        return self._query.trm_loc_logic

    def _remove_negated_terms(self):
        """

        """
        return self._query.remove_negated_terms()

    def _convert_all_shapes_to_boxes(self):
        """

        """
        return self._query.convert_all_shapes_to_boxes()

    def _convert_all_shapes_to_radiuses(self):
        """

        """
        return self._query.convert_all_shapes_to_radiuses()

    def _factor_locations_by_radius(self, radius_km):
        """

        """
        return self._query.factor_locations_by_radius(radius_km)

    def _transform_phrases(self):
        """

        """
        return self._query.transform_phrases()

    # TODO(LH): save the query for a filter so we don't have to refactor
    #   locations every time a background search is run

    def _format_locations(self):
        """
        Formats the query Locations to conform to Specs for search area size
        and shape.
        """
        location_format = self._get_spec('location_format')

        if location_format == 'box':
            self._convert_all_shapes_to_boxes()

        elif location_format == 'radius':
            self._convert_all_shapes_to_radiuses()
            radius_km = self._get_spec('radius_limit_km')
            self._factor_locations_by_radius(radius_km)

        else:
            raise AttributeError('Invalid location format "%s"' % location_format)

    def _handle_negation(self):
        """
        If the API does not allow terms to be excluded from query results (e.g.,
        with a "NOT" operator), removes any negated search terms from the query.
        """
        allows_negation = self._get_spec('NOT_operator')

        if not allows_negation:
            self._remove_negated_terms()

    def _handle_phrases(self):
        """
        If the API does not accepts phrases, reformats any phrases so that a
        query is performed on each word of a phrase, as well as on the tag for
        the phrase (i.e., no spaces between words).
        """
        accepts_phrases = self._get_spec('accepts_phrases')

        if not accepts_phrases:
            self._transform_phrases()

    # TODO(LH): need a better way to handle excluded terms in factored queries,
    #   so that each negated term is included in each subquery; also need to
    #   make sure that no query consists only of negated search terms (i.e.,
    #   no included search terms, locations, or accounts)

    def _preprocess_components(self):
        """
        Formats locations and phrases so they can be handled by the API.
        """
        # convert locations into the proper format
        self._format_locations()

        # removed negated terms if the API lacks a "NOT" operator
        self._handle_negation()

        # break up phrases if needed
        self._handle_phrases()

    def get_num_searchterms(self, query):
        """
        Takes a ReservoirQuery and returns the number of search terms in
        the query, according to how the API counts terms (i.e., whether logical
        operators or Accounts count toward the total number of search terms).
        Depending on the query and the API, this may be greater than the number
        of SearchTerms in the query.
        """
        # first count the actual SearchTerms in the query
        total_terms = len(query.searchterms)

        # determine whether followees (Accnts) count toward the search term limit
        handled_together = self._get_spec('combine_trm_fol')

        if handled_together:

            # count accounts as search terms
            total_terms += len(query.accounts)

        # determine whether query operators count toward the search term limit
        includes_operators = self._get_spec('combine_trm_opr')

        if includes_operators:

            # get the default logic for combining terms ("AND" or "OR")
            default_logic = self._get_spec('trm_trm_logic')

            if default_logic == 'AND':

                # make sure we have a way to combine search terms with "OR"
                if self._get_spec('OR_operator'):

                    # add the number of "OR" operators we'll need to join terms
                    total_terms += total_terms - 1

        return total_terms

    def _exceeds_searchterms_limit(self, query):
        """
        Takes a ReservoirQuery and return a Boolean indicating whether
        the query exceeds the Specs for maximum number of search terms allowed.
        """
        # get the total number of search terms allowed
        searchterms_limit = self._get_spec('searchterms_limit')
        total_terms = self.get_num_searchterms(query)

        return total_terms > searchterms_limit

    @staticmethod
    def _separate_terms(query):
        """
        Takes a ReservoirQuery and returns a list of queries, each
        containing one SearchTerm from the orginal query.
        """
        if len(query.searchterms) > 1:

            new_queries = []

            for term in query.searchterms:
                new_query = deepcopy(query)
                new_query.terms = [term]
                new_queries.append(new_query)

            return new_queries

        else:
            return [query]

    def _handle_trm_trm_logic(self, queries):
        """
        Takes a list of ReservoirQueries and determines the need to break
        up the queries in order to obtain a union of results for each SearchTerm in a
        query (i.e., by joining SearchTerms with an "OR" operator). If the API
        doesn't provide a means of joining SearchTerms with "OR", the method breaks up
        each query into multiple queries with only one SearchTerm per query, and
        returns the processed queries as a list. Otherwise, returns the orignal
        queries.
        """
        # get the Pipe's default logic for combining terms ("AND" or "OR")
        default_logic = self._get_spec('trm_trm_logic')

        if default_logic == 'OR' or self._get_spec('OR_operator'):
            return queries

        else:
            new_queries = []

            for query in queries:
                sep_queries = self._separate_terms(query)
                new_queries.extend(sep_queries)

            return new_queries

    @staticmethod
    def _separate_locations_and_terms(query):
        """
        Takes a ReservoirQuery and divides it into two queries: one that
        contains Locations but not SearchTerms, and one that contains SearchTerms but not
        Locations. Returns the two new ReservoirMediaQueries as a list.
        """
        # create a copy of the query without SearchTerms
        locations_query = deepcopy(query)
        locations_query.searchterms = []

        # create a copy of the query without Locations
        terms_query = deepcopy(query)
        terms_query.locations = []

        return [locations_query, terms_query]

    def _handle_trm_loc_logic(self, queries):
        """
        Takes a list of ReservoirMediaQueries and determines the need to place
        Locations and SearchTerms in seperate queries before sending to the API. If
        Locations need to be handled separately from SearchTerms, puts each in its own
        query and returns the processed queries as a list. Otherwise, returns
        original queries.
        """
        # we assume that each query in the queries argument was derived from the
        # original query (self._query) and therefore uses the same trm_loc_logic
        query_logic = self._get_query_trm_loc_logic()

        default_logic = self._get_spec('trm_loc_logic')

        # check if terms and locations can be combined in a query with "OR"
        has_or_logic = self._get_spec('combine_trm_loc') \
                       and self._get_spec('OR_operator')

        # If query_logic == 'OR' and 'OR' logic is not allowed, we need to
        # split each query up before sending it to the API.
        if query_logic == 'OR' and default_logic == 'AND' and not has_or_logic:
            new_queries = []

            for query in queries:
                sep_queries = self._separate_locations_and_terms(query)
                new_queries.extend(sep_queries)

            return new_queries

        else:
            return queries

    @staticmethod
    def _separate_accounts_and_terms(query):
        """
        Takes a ReservoirQuery and divides it into two queries: one that
        contains Accounts but not SearchTerms, and one that contains SearchTerms but not
        Accounts. Returns the two new ReservoirMediaQueries as a list.
        """
        # create a copy of the query without terms
        accounts_query = deepcopy(query)
        accounts_query.searchterms = []

        # create a copy of the query without accounts
        terms_query = deepcopy(query)
        terms_query.accounts = []

        return [accounts_query, terms_query]

    def _handle_trm_fol_logic(self, queries):
        """
        Takes a list of ReservoirMediaQueries and determines the need to place
        Accounts and SearchTerms in seperate queries before sending to the API. If
        Accounts need to be handled separately from SearchTerms, puts each in its own
        query and returns the processed queries as a list. Otherwise, returns
        the original queries.
        """
        # get the Pipe's default logic for combining terms ("AND" or "OR")
        default_logic = self._get_spec('trm_fol_logic')

        # check if terms and accounts are combined in a query
        can_combine = self._get_spec('combine_trm_fol')

        if default_logic == 'OR' or (self._get_spec('OR_operator') and \
        can_combine):
            return queries

        else:
            new_queries = []

            for query in queries:
                separated_queries = self._separate_accounts_and_terms(query)
                new_queries.extend(separated_queries)

            return new_queries

    def _separate_components(self):
        """
        Takes the current ReservoirQuery and, where needed, breaks it
        into smaller queries to allow "OR" queries in cases where the API only
        allows "AND" queries. For example, if a query is for "cat OR dog" and
        the API only allows the query "cat AND dog", the method will break the
        orginal query into two separate queries: one for "cat" and one for
        "dog", which together will produce the same results as "cat OR dog".
        Returns the result as a list of ReservoirMediaQueries.
        """
        new_queries = [self._query]

        # Media query can use either "SearchTerm OR Location" or "SearchTerm AND Location"
        # logic. In the case of a "SearchTerm OR Location" query, we need to split up
        # SearchTerms and Locations if the API only takes "SearchTerm AND Location" queries.
        new_queries = self._handle_trm_loc_logic(new_queries)

        # media query uses "SearchTerm OR Account", so we need to break these up if
        # the API uses "SearchTerm AND Account" logic
        new_queries = self._handle_trm_fol_logic(new_queries)

        # media query uses "SearchTerm OR SearchTerm", so we need to break these up if
        # the API uses "SearchTerm AND SearchTerm" logic
        new_queries = self._handle_trm_trm_logic(new_queries)

        return new_queries

    def _handle_combined_trm_fol_limit(self, queries):
        """
        Takes a list of ReservoirMediaQueries and, for each query, determines
        the need to query Accounts separately from SearchTerms. If the API handles
        Accounts and SearchTerms together (by treating usernames like keywords), and a
        query exceeds the API's limit for search terms, breaks up the query so
        that Accounts are queried separately from SearchTerms. Returns the processed
        queries as a list.
        """
        # determine whether followees count toward the search term limit
        handled_together = self._get_spec('combine_trm_fol')

        if handled_together:

            new_queries = []

            for query in queries:
                if query.accounts and query.searchterms \
                and self._exceeds_searchterms_limit(query):
                    sep_queries = self._separate_accounts_and_terms(query)
                    new_queries.extend(sep_queries)
                else:
                    new_queries.append(query)

            return new_queries

        else:
            return queries

    @staticmethod
    def _factor_queries_by_component(queries, component, limit):
        """
        Takes a list of ReservoirMediaQueries, a string representing the name
        of a query component/attribute (e.g., 'locations'), and an integer
        representing the API limit on the number of items for that attribute.
        Returns a list of queries that break up the orginal queries by the given
        component so than none of the new queries exceed the API limit for that
        component.
        """
        if limit == None:
            limit = float('inf')

        new_queries = []

        for query in queries:

            # get the items in the query component (e.g., query.locations)
            items = getattr(query, component)

            if len(items) > limit:

                # divide the items into groups no larger than the limit
                groups = parserutils.divide_into_groups(items, limit)

                # create a new query for each group
                for group in groups:
                    new_query = deepcopy(query)
                    setattr(new_query, component, group)
                    new_queries.append(new_query)
            else:
                new_queries.append(query)

        return new_queries

    def _get_adjusted_searchterms_limit(self):
        """
        Determines whether the search terms limit needs to be adjusted downward
        to take into account inclusion of 'OR' operators between terms. If so,
        returns the adjusted limit. Otherwise, returns the unadjusted limit.
        """
        limit = self._get_spec('searchterms_limit')
        includes_operators = self._get_spec('combine_trm_opr')
        needs_operators = (self._get_spec('trm_trm_logic') == 'AND')
        has_operator = self._get_spec('OR_operator')

        if includes_operators and needs_operators and has_operator and limit > 1:

            # return half the limit, rounded down to the enarest integer
            limit = limit // 2

        return limit

    def _factor_by_searchterms(self, queries):
        """
        Takes a list of ReservoirMediaQueries and returns a list of queries
        that, if necessary, breaks up the orginal queries by the searchterms
        attribute to ensure that no query exceeds the API limit for number of
        terms.
        """
        limit = self._get_adjusted_searchterms_limit()
        return self._factor_queries_by_component(queries, 'searchterms', limit)

    def _factor_by_accounts(self, queries):
        """
        Takes a list of ReservoirMediaQueries and returns a list of queries
        that, if necessary, breaks up the orginal queries by the accounts
        attribute to ensure that no query exceeds the API limit for number of
        accounts.
        """
        limit = self._get_spec('followees_limit')
        return self._factor_queries_by_component(queries, 'accounts', limit)

    def _factor_by_locations(self, queries):
        """
        Takes a list of ReservoirMediaQueries and returns a list of queries
        that, if necessary, breaks up the orginal queries by the locations
        attribute to ensure that no query exceeds the API limit for number of
        locations.
        """
        limit = self._get_spec('locations_limit')
        return self._factor_queries_by_component(queries, 'locations', limit)

    def _factor_components(self, queries):
        """
        Takes a list of ReservoirQueries and returns a list of ReservoirQueries
        that, if necessary, breaks up the orginal queries by accounts, locations,
        and/or search terms to ensure that no query exceeds the API limit for
        any of these arguments.
        """
        new_queries = self._factor_by_accounts(queries)
        new_queries = self._factor_by_searchterms(new_queries)
        new_queries = self._factor_by_locations(new_queries)
        return new_queries

    def factor_query(self):
        """
        Takes a ReservoirQuery and factors them into a list of ReservoirQueries
        for a particular API.
        """
        # format Locations and SearchTerms so that they can be handled by the API
        self._preprocess_components()

        # split up components where the API doesn't allow "OR" queries
        new_queries = self._separate_components()

        # split up Accounts and SearchTerms if they share the same API limit
        new_queries = self._handle_combined_trm_fol_limit(new_queries)

        # break up each component (Accounts, Locations, SearchTerms) so that none
        # exceed their respective API limit
        new_queries = self._factor_components(new_queries)

        return new_queries

    def get_accounts(self):
        """
        Returns the list of Accounts associated with the query.
        """
        return self._query.accounts

    def get_locations(self):
        """
        Returns the list of Locations associated with the query.
        """
        return self._query.locations

    def get_searchterms(self):
        """
        Returns the list of SearchTerms associated with the query.
        """
        return self._query.searchterms
