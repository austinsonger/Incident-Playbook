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
Defines classes and helper functions for constructing Elasticsearch queries.

====================================  =========================================
Class                                 Description
====================================  =========================================
:class:`~ElasticsearchQuery`          Create a query for Elasticsearch.
:class:`~ElasticsearchQueryFieldset`  Format a |QueryFieldset| for
                                      Elasticsearch.
====================================  =========================================

====================================  =========================================
Function                              Description
====================================  =========================================
:func:`~bool_query`                   Create a bool query.
:func:`~id_query`                     Create a query to find a doc by id.
:func:`~ids_and_value_filter`         Create a query for docs matching a value.
:func:`~ids_filter`                   Return a filter for docs using ids.
:func:`~ids_query`                    Create a query to find docs by id.
:func:`~ids_selector`                 Create a query for docs by id.
:func:`~regex_query`                  Create a regexp query.
====================================  =========================================

"""

# standard library
import json
import re

# local
from engines.queries import EngineQuery, EngineQueryFieldset
from .mapper import get_data_type, get_index_types

# map logical operators to those used by Elasticsearch
_ELASTIC_QUERY_JOINERS = {
    'OR': 'should',
    'AND': 'filter'
}


def regex_query(field_name, value):
    """Create a regexp query.

    Constructs an Elasticsearch regexp query that will match documents
    in which the specified value is found somewhere within the content
    of the given field.

    Parameters
    ----------
    field_name : str
        The name of the field to be queried.

    value : str
        A value that should appear somewhere in the field's content.

    Returns
    -------
    dict
        An Elasticsearch regexp query.

    """
    value = re.escape(value)
    return {'regexp': {field_name: '.*%s.*' % value}}


def bool_query(must=None, should=None, must_not=None, filter_expr=None):
    """Create a bool query.

    Parameters
    ----------
    must : |dict|, |list| of |dict|, or |None|
        One or more query clauses that documents must match. For use
        when 'AND' logic is needed to join query terms.

    should : |list| of |dict| or |None|
        A list of query clauses for which documents must match at least
        one. For use when 'OR' logic is needed to join query terms.

    must_not : |dict|, |list| of |dict| or |None|
        One or more query query clauses which documents must not match.
        For use when 'NOT' logic is needed.

    filter_expr : |dict| or |None|
        A query clause that documents must match. For use when 'AND'
        logic is needed to join query terms. Preferred over the `must`
        parameter since we're not using relevance scores and it's more
        efficient.

    Returns
    -------
    dict
        An Elasticsearch bool query.

    """
    query_dict = {}

    if must:
        query_dict.update({'must': must})
    else:
        query_dict.update({'must': {'match_all': {}}})

    if should:
        query_dict.update({'should': should, 'minimum_should_match': 1})

    if must_not:
        query_dict.update({'must_not': must_not})

    if filter_expr:
        query_dict.update(filter_expr)

    return {'bool': query_dict}


def ids_selector(doc_ids):
    """Create a query for documents with the given ids.

    Parameters
    ----------
    doc_id : |list| of |str|
        The document ids to match.

    Returns
    -------
    dict
        A query for documents matching the given `doc_ids`.

    """
    ids = [doc_id for doc_id in doc_ids if doc_id is not None]
    return {'ids': {'values': ids}}


def ids_filter(doc_ids):
    """Create a filter for documents with the given ids.

    Parameters
    ----------
    doc_ids : |list| of |str|
        The document ids to match.

    Returns
    -------
    dict
        A query for documents matching the given `doc_ids`.

    """
    return {'filter': [ids_selector(doc_ids)]}


def ids_query(doc_ids):
    """Create a query for documents with the given ids.

    Parameters
    ----------
    doc_ids : |list| of |str|
        The document ids to match.

    Returns
    -------
    dict
        A query for documents matching the given `doc_ids`.

    """
    return {'query': ids_selector(doc_ids)}


def id_query(doc_id):
    """Create a query for a document with the given id.

    Parameters
    ----------
    doc_id : str
        The document id to match.

    Returns
    -------
    dict
        A query for a document with the given `doc_id`.

    """
    return {'id': doc_id, 'refresh': True, 'ignore': 404}


def ids_and_value_filter(doc_ids, fields, value):
    """Create a query to find documents that contain the given value.

    Constructs a query that will find documents associated with the set
    of `doc_ids` that also contain the given `value` somewhere within
    the content of one of the given `fields`.

    Parameters
    ----------
    doc_ids : |list| of |str|
        The document ids to match.

    fields : |list| of |DataFields|
        |DataFields| indicating the fields in documents that should be
        examined for a matching value.

    value : |str|
        A value used to find matching documents.

    Returns
    -------
    list
        Document ids for which at least one of the specified `fields`
        contains the given `value`.

    """
    mappings = get_index_types(fields)
    full_text_fields = mappings['text']
    exact_text_fields = mappings['keyword']

    exact_text_query = []
    full_text_query = None

    if exact_text_fields:
        for field in exact_text_fields:
            regexp = regex_query(field.field_name, value)
            exact_text_query.append(regexp)

    if full_text_fields:
        analyzed_fields = [field.field_name for field in full_text_fields]
        full_text_query = {
            'multi_match': {
                'query': value,
                'fields': analyzed_fields
            }
        }

    id_filter = ids_filter(doc_ids)

    if exact_text_query and full_text_query:
        should_queries = [full_text_query] + exact_text_query
        query = bool_query(should=should_queries, filter_expr=id_filter)
    elif exact_text_query:
        query = bool_query(should=exact_text_query, filter_expr=id_filter)
    elif full_text_query:
        query = bool_query(must=full_text_query, filter_expr=id_filter)
    else:
        return None
        # TODO(LH): raise exception?

    return {'query': query}


class ElasticsearchQueryFieldset(EngineQueryFieldset):
    """Format a |QueryFieldset| for Elasticsearch.

    Parameters
    ----------
    fieldset : |QueryFieldset|
        A |QueryFieldset| providing the basis for a query expression.

    Attributes
    ----------
    field_name : str
        The name of the field being queried.

    field_type : str
        The type of field being queried (e.g., 'CharField'). Corresponds
        to a value in |FIELD_TYPE_CHOICES|.

    raw_value : str
        The `value` from the |QueryFieldset| used to initialize the
        object instance.

    raw_operator : str
        The `operator` from the |QueryFieldset| used to initialize the
        object instance. Corresponds to a value in |OPERATOR_CHOICES|.

    operator : str
        The engine-specific operator that should be used for building
        the query expression.

    negate : bool
        Indicates whether the `operator` should be negated by applying
        'NOT' logic to the query expression.

    value : |str|, |int|, |float|, |dict|, or |list|
        The value that should be used in the query expression, to be
        compared against the value of the field being queried.

    """

    QUERY_OPERATORS = {
        'eq': 'match',                  # equals
        'in': 'term',                   # list contains value
        'gt': 'gt',                     # greater than
        'gte': 'gte',                   # greater than or equal to
        'lt': 'lt',                     # less than
        'lte': 'lte',                   # less than or equal to
        'regex': 'match',               # text contains regex
        'not:eq': 'not:match',          # does not equal
        'not:in': 'not:term',           # list does not contain value
        'not:regex': 'not:match',       # text does not contain regex
        'not:missing': 'exists',        # is not null
        'within': 'within'              # point is within polygon
    }
    """|dict|

    Maps the values in |OPERATOR_CHOICES| to the corresponding query
    operators in Elasticsearch.
    """

    QUERY_JOINERS = _ELASTIC_QUERY_JOINERS
    """|dict|

    Maps the values in |LOGIC_CHOICES| to the corresponding query
    operators in Elasticsearch.
    """

    NEGATE_OPERATOR = 'not:'
    """|dict|

    The Engine's equivalent of a 'NOT' operator. Used for negating a
    |QueryFieldset|.
    """

    @staticmethod
    def _negate_query(query):
        """Negate a query.

        Takes a dictionary representing a query and applies 'NOT' logic.
        Returns a dictionary representing the negated query.
        """
        # return {'not': query}
        return bool_query(must_not=query)

    def format_value(self):
        """Format a value for a query expression.

        Transforms the `raw_value` attribute into a value that can be
        used in an Elasticsearch query expression.

        Returns
        -------
        |str|, |int|, |float|, |dict|, or |list|
            A value that can be used in the query expression.

        """
        if self.raw_value is not None:
            # if string value, convert to lowercase
            # so it can be compared to indexed terms
            if get_data_type(self.field_type) == 'text':
                return self.raw_value.lower()

            # if location search, convert geojson value back to dictionary
            if self.operator == 'within':
                return json.loads(self.raw_value)

            # otherwise no special formatting is needed
            else:
                return self.raw_value

        else:
            return ''

    def _default_query(self):
        """Create a generic query.

        Returns a generic field query.
        """
        return {self.operator: {self.field_name: self.value}}

    def _match_phrase(self):
        """Match value as a phrase.

        Returns a selector for a match_phrase query.
        """
        return {'match_phrase': {self.field_name: self.value}}

    def _match_term(self):
        """Match value as a term.

        Returns a selector for a term query.
        """
        return {'match': {self.field_name: self.value}}

    def _exists_query(self):
        """Check if a field exists.

        Returns a selector for an exists query.
        """
        return {'exists': {'field': self.field_name}}

    def _range_query(self):
        """Create a range query.

        Returns a selector for an open-ended range query (e.g., "greater
        than", "less than or equal to", etc.).
        """
        return {'range': {self.field_name: {self.operator: self.value}}}

    def _regex_query(self):
        """Create a regex query.

        Returns a selector for matching a field using a regular
        expression.
        """
        return regex_query(self.field_name, self.value)

    def _contains_query(self):
        """Match value as phrase or fragment.

        Returns a list of filters to capture results for either an exact
        phrase or a word fragment.
        """
        regex_filter = [
            self._match_phrase(),
            self._regex_query()
        ]
        if self.negate:
            return bool_query(must_not=regex_filter)
        else:
            return bool_query(should=regex_filter)

    def _eq_query(self):
        """Match the exact value.

        Returns a selector for examining equality, negated when
        appropriate. The exact form of the selector depends on whether
        or not the field is analyzed by Elasticsearch.
        """
        if get_data_type(self.field_type) == 'text':
            query = self._match_phrase()
        else:
            query = self._match_term()

        if self.negate:
            query = self._negate_query(query)

        return bool_query(filter_expr={'filter': query})

    def _polygon_filter(self, polygon_feature):
        """Create a polygon filter.

        Takes a GeoJSON polygon feature and returns a polygon filter.
        """
        geometry = polygon_feature['geometry']

        if geometry['type'] != 'Polygon':  # pragma: no cover
            raise ValueError('Feature is a %s not a Polygon'
                             % geometry['type'])

        return {
            'geo_polygon': {
                self.field_name: {
                    'points': geometry['coordinates'][0]
                },
                # 'validation_method': 'COERCE'
            }
        }

    def _geo_query(self):
        """Create a geofilter.

        If the object's `value` attribute represents a feature collection,
        returns a geofilter based on the feature collection.
        """
        feature_collection = self.value
        features = feature_collection['features']
        if len(features) < 2:
            return self._polygon_filter(features[0])
        else:
            poly_filters = []
            for feature in features:
                poly_filter = self._polygon_filter(feature)
                poly_filters.append(poly_filter)
            return bool_query(should=poly_filters)

    def _get_query(self):
        """Create a base query prior to negation.

        Returns a base selector for use in an Elasticsearch query,
        prior to applying any negation.
        """
        if self.operator == 'exists':
            return self._exists_query()

        elif self.operator == 'within':
            return self._geo_query()

        elif self.operator in ['gt', 'gte', 'lt', 'lte']:
            return self._range_query()

        else:
            return self._default_query()

    def _get_selector(self):
        """Create a query selector with negation if needed.

        Returns a selector for use in an Elasticsearch query, negated
        when appropriate.
        """
        query = self._get_query()
        if self.negate:
            return self._negate_query(query)
        else:
            return query

    @property
    def selector(self):
        """Create a query expression.

        Creates a dictionary suitable for use as a selector in an
        Elasticsearch query.

        Returns
        -------
        dict
            A query expression based on the |QueryFieldset| used to
            initialize the object instance.

        """
        if 'regex' in self.raw_operator:
            return self._contains_query()

        elif 'eq' in self.raw_operator:
            return self._eq_query()

        else:
            return self._get_selector()


class ElasticsearchQuery(EngineQuery):
    """Create a query for Elasticsearch.

    Defines search parameters for querying the index and document type
    serviced by an |ElasticsearchEngine| instance. Uses those
    parameters to format an Elasticsearch query.

    Attributes
    ----------
    subqueries : list of QueryFieldsets and/or EngineQueries
        Any combination of |QueryFieldsets| and child |EngineQueries|
        to be used in constructing a query. Child |EngineQueries| are
        used to construct more complex (nested) query expressions.

    joiner : str
        A logical operator for combining query terms. Corresponds to a
        value in |LOGIC_CHOICES|.

    """

    QUERY_JOINERS = _ELASTIC_QUERY_JOINERS
    """|dict|

    Maps the values in |LOGIC_CHOICES| to the corresponding logical
    operators in Elasticsearch.
    """

    fieldset_model = ElasticsearchQueryFieldset
    """|type|

    The |EngineQueryFieldset| subclass used to model fieldsets for
    Elasticsearch.
    """

    @staticmethod
    def join_subqueries(subqueries, joiner):
        """Return a query expression.

        Parameters
        ----------
        fieldsets : |list| of :class:`~ElasticsearchQueryFieldset`
            :class:`ElasticsearchQueryFieldsets<ElasticsearchQueryFieldset>`
            for defining a query.

        joiner : str
            A logical operator specifying how multiple query fieldsets
            should be combined. Corresponds to a value in |LOGIC_CHOICES|.

        """
        bool_query = {joiner: subqueries}

        if 'should' in bool_query:
            bool_query.update({'minimum_should_match': 1})

        if 'must' not in bool_query:
            bool_query.update({'must': {'match_all': {}}})

        return {'bool': bool_query}

    @property
    def params(self):
        """Return parameters for a query.

        Returns
        -------
        dict
            A query expression based on the parameters of the object
            instance.

        """
        query = self._get_query(self)
        return {'query': query}
