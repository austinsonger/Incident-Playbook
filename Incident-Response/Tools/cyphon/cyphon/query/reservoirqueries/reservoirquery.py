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
Defines a ReservoirQuery class for passing media queries to Pipes.
"""

# standard library
import json

# third party
from django.core import serializers


class ReservoirQuery(object):
    """
    Specifies search criteria for searching social media posts from a particular
    platform.

    Attributes:
        accounts: a list of Account objects associated with a particular
            social media platform (Reservoir)
        locations: a list of Location objects
        searchterms: a list of SearchTerm objects
        timeframe: a TimeFrame object
        trm_loc_logic: a logical "AND" or "OR" operator indicating how terms and
            locations are evaluated in a query (i.e., with an intersection vs.
            a union of results)
    """

    def __init__(self, accounts=None, locations=None, searchterms=None,
                 timeframe=None, trm_loc_logic='OR'):
        if accounts == None:
            self.accounts = []
        else:
            self.accounts = accounts

        if locations == None:
            self.locations = []
        else:
            self.locations = locations

        if searchterms == None:
            self.searchterms = []
        else:
            self.searchterms = searchterms

        self.timeframe = timeframe
        self.trm_loc_logic = trm_loc_logic

    def __str__(self):
        return '%s Accounts, %s Locations, %s Search SearchTerms ' % \
            (len(self.accounts), len(self.locations), len(self.searchterms))

    @property
    def included_terms(self):
        """
        Returns SearchTerms that searched text should contain.
        """
        included_terms = []

        for term in self.searchterms:
            if not term.negate:
                included_terms.append(term)

        return included_terms

    @property
    def excluded_terms(self):
        """
        Returns SearchTerms that searched text should not contain.
        """
        excluded_terms = []

        for term in self.searchterms:
            if term.negate:
                excluded_terms.append(term)

        return excluded_terms

    @staticmethod
    def _model_obj_to_dict(model_instance):
        """
        Takes an instance of a Django model and returns a dictionary in which
        the keys are the fields of the model instance and the values are the
        model instance's values for those fields.
        """
        if model_instance:
            json_data = serializers.serialize('json', [model_instance])
            data = json.loads(json_data)
            return data[0]['fields']
        else:
            return {}

    def _model_objs_to_dict(self, model_instances):
        """
        Takes a list of Django model instances and returns list of dictionaries
        representing each model instance. In each dictionary, the keys are the
        fields of the model instance and the values are the model instance's
        values for those fields.
        """
        dict_list = []
        for model_instance in model_instances:
            dict_list.append(self._model_obj_to_dict(model_instance))
        return dict_list

    def to_dict(self):
        """
        Returns a dictionary representation of the ReservoirQuery.
        """
        return {
            'accounts': self._model_objs_to_dict(self.accounts),
            'locations': self._model_objs_to_dict(self.locations),
            'searchterms': self._model_objs_to_dict(self.searchterms),
            'timeframe': self._model_obj_to_dict(self.timeframe),
            'trm_loc_logic': self.trm_loc_logic
        }

    def to_json(self):
        """
        Returns a pretty-printed JSON string of the ReservoirQuery,
        sorted by key.
        """
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)

    def remove_negated_terms(self):
        """
        Removes any negated terms from the list of SearchTerms.
        """
        self.searchterms = self.included_terms
        return self

    def filter_accounts(self, reservoir):
        """
        Takes a Reservoir and filters the list of Accounts to only
        include Accounts associated with the given Reservoir.
        """
        accounts = []

        for account in self.accounts:
            if account.platform == reservoir:
                accounts.append(account)

        self.accounts = accounts

        return self

    def convert_all_shapes_to_boxes(self):
        """
        Transforms Locations into their bounding boxes.
        """
        self.locations = [loc.get_bbox() for loc in self.locations]
        return self

    def convert_all_shapes_to_radiuses(self):
        """
        Transforms Locations into radiuses.
        """
        self.locations = [loc.get_radius() for loc in self.locations]
        return self

    def factor_locations_by_radius(self, radius_km):
        """
        Transforms Locations into Locations with radiuses not exceeding the
        given radius, which together cover the same total area.
        """
        all_locations = []

        for location in self.locations:
            radiuses = radius_km is not None and location.radius_km is not None
            if radiuses and location.radius_km > radius_km:
                new_locations = location.factor_by_radius_km(radius_km)
                all_locations.extend(new_locations)
            else:
                all_locations.append(location)

        self.locations = all_locations

        return self

    def add_searchterm(self, new_term):
        """
        Takes a SearchTerm object and adds the SearchTerm to the
        ReservoirQuery's searchterms if the value for the SearchTerm.term
        property is not a duplicate.
        """
        dup = False

        for searchterm in self.searchterms:
            if new_term.term == searchterm.term:
                dup = True
                break

        if dup == False:
            self.searchterms.append(new_term)

        return self

    def transform_phrases(self):
        """
        Transforms SearchTerms that are phrases so that they can be processed by
        Pipes that cannot handle phrases. Each SearchTerm that is a phrase is
        tranformed into new SearchTerms in which each word of the phrase is
        queried individually as well as combined as a single tag (i.e., no
        spaces between the words).
        """
        old_searchterms = self.searchterms
        self.searchterms = []

        for searchterm in old_searchterms:

            if searchterm.is_phrase():
                new_searchterms = searchterm.create_terms_from_phrase()

                for new_searchterm in new_searchterms:
                    self.add_searchterm(new_searchterm)
            else:
                self.add_searchterm(searchterm)

        return self

    def wrap_phrases_in_quotes(self):
        """
        For SearchTerms that are phrases, wraps phrases in quotation marks.
        """
        old_searchterms = self.searchterms
        self.searchterms = []

        for searchterm in old_searchterms:
            if searchterm.is_phrase():
                searchterm.wrap_in_quotes()
            self.add_searchterm(searchterm)

        return self


