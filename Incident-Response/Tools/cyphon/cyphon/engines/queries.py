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
Defines base classes for constructing queries.

=============================  ==========================================
Class                          Description
=============================  ==========================================
:class:`~EngineQuery`          Create a query for a data store.
:class:`~EngineQueryFieldset`  Format a |QueryFieldset| for a data store.
=============================  ==========================================

"""

# local
from cyphon.baseclass import BaseClass
from cyphon.fieldsets import QueryFieldset

# map logical operators to those used by the data store
_ENGINE_QUERY_JOINERS = {
    'OR': 'OR',
    'AND': 'AND'
}


class EngineQueryFieldset(BaseClass):
    """
    Format a |QueryFieldset| for a particular data store.

    Parameters
    ----------
    fieldset : |QueryFieldset|
        A |QueryFieldset| providing the basis for a query expression.

    Attributes
    ----------
    field_name : str
        The name of the field being queried.

    field_type : str
        The type of field being queried (e.g., "CharField"). Corresponds
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

    value : `str`, `int`, `float`, `dict`, or `list`
        The value that should be used in the query expression, to be
        compared against the value of the field being queried.

    """

    QUERY_OPERATORS = {
        'eq': NotImplemented,            # equals
        'in': NotImplemented,            # list contains value
        'gt': NotImplemented,            # greater than
        'gte': NotImplemented,           # greater than or equal to
        'lt': NotImplemented,            # less than
        'lte': NotImplemented,           # less than or equal to
        'regex': NotImplemented,         # text contains regex
        'not:eq': NotImplemented,        # does not equal
        'not:in': NotImplemented,        # list does not contain value
        'not:regex': NotImplemented,     # text does not contain regex
        'not:missing': NotImplemented,   # is not null
        'within': NotImplemented         # within polygon(s)
    }
    """|dict|

    Maps the values in |OPERATOR_CHOICES| to the corresponding query
    operators for the Engine.

    Notes
    -----
    Must be overridden in derived classes.

    """

    QUERY_JOINERS = _ENGINE_QUERY_JOINERS
    """`dict`

    Maps the values in |LOGIC_CHOICES| to the corresponding logical
    operators for the Engine.

    Notes
    -----
    Must be overridden in derived classes.

    """

    NEGATE_OPERATOR = NotImplemented
    """`str`

    The Engine's equivalent of a 'NOT' operator. Used for negating a
    |QueryFieldset|.

    Notes
    -----
    Must be overridden in derived classes.

    """

    def __init__(self, fieldset):
        """Initialize an EngineQueryFieldset instance."""
        self.field_name = fieldset.field_name
        self.field_type = fieldset.field_type
        self.raw_value = fieldset.value
        self.raw_operator = fieldset.operator

        operator = self.get_operator(self.raw_operator)
        negate_operator = self.get_negate_operator()
        self.negate = bool(negate_operator in operator)
        self.operator = operator.replace(negate_operator, '')

        # format value once we set self.operator
        self.value = self.format_value()

    def get_operator(self, raw_operator):
        """Return an operator for the query expression.

        Parameters
        ----------
        raw_operator : str
            Corresponds to the value of an option in |OPERATOR_CHOICES|.

        Returns
        -------
        str
            The operator that should be used for building the query
            expression.

        Raises
        ------
        NotImplementedError
            If :const:`~engines.queries.EngineQueryFieldset.QUERY_OPERATORS`
            has not been properly implemented.

        """
        operator = self.QUERY_OPERATORS.get(raw_operator)
        if operator in [None, NotImplemented]:
            undefined_operator = 'QUERY_OPERATORS[\'$s\']' % raw_operator
            return self.raise_attr_not_implemented(undefined_operator)
        else:
            return operator

    def get_joiner(self, raw_joiner):
        """Return a logical operator to join fieldsets.

        Parameters
        ----------
        raw_joiner : str
            The value of an option in |LOGIC_CHOICES|.

        Returns
        -------
        str
            The logical operator that should be used to combine
            fieldsets in the manner specified by the `raw_joiner`
            parameter.

        Raises
        ------
        NotImplementedError
            If :const:`~engines.queries.EngineQueryFieldset.QUERY_JOINERS`
            has not been properly implemented.

        """
        joiner = self.QUERY_JOINERS.get(raw_joiner)
        if joiner in [None, NotImplemented]:
            undefined_joiner = 'QUERY_JOINERS[\'%s\']' % raw_joiner
            return self.raise_attr_not_implemented(undefined_joiner)
        else:
            return joiner

    def get_negate_operator(self):
        """Return an operator to negate a query expression.

        Returns
        -------
        str
            The Engine's equivalent of a 'NOT' operator.

        Raises
        ------
        NotImplementedError
            If :const:`~engines.queries.EngineQueryFieldset.NEGATE_OPERATOR`
            has not been implemented.

        """
        if self.NEGATE_OPERATOR is NotImplemented:
            return self.raise_attr_not_implemented('NEGATE_OPERATOR')
        else:
            return self.NEGATE_OPERATOR

    def format_value(self):
        """Return a value that can be used in the query expression.

        Transforms the `raw_value` attribute into a value that can be
        used in a query expression.

        Returns
        -------
        |str|, |int|, |float|, |dict|, or |list|
            A value that can be used in the query expression.

        Raises
        ------
        NotImplementedError
            If the method has not been implemented.

        Notes
        -----
        This method must be implemented in derived classes.

        """
        return self.raise_method_not_implemented()

    def _polygon_filter(self, polygon_feature):
        """Create a polygon filter.

        Takes a GeoJSON polygon or multipolygon feature and returns
        a query expression for a geofilter. This method must be
        implemented in derived classes for the `_geo_query` method
        to work.
        """
        return self.raise_method_not_implemented()

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
            or_key = self.get_joiner('OR')
            geo_filter = {or_key: []}
            for feature in features:
                poly_filter = self._polygon_filter(feature)
                geo_filter[or_key].append(poly_filter)

            return geo_filter

    @property
    def selector(self):
        """Return a query expression.

        Returns
        -------
        dict
            A query expression based on the |QueryFieldset| used to
            initialize the object instance.

        Raises
        ------
        NotImplementedError
            If the method has not been implemented.

        """
        return self.raise_method_not_implemented()


class EngineQuery(BaseClass):
    """Create a query for a data store.

    Defines search parameters for a |Collection| serviced by an |Engine|
    instance.

    Attributes
    ----------
    subqueries : `list` of `QueryFieldsets` and/or `EngineQueries`
        Any combination of |QueryFieldsets| and child |EngineQueries|
        to be used in constructing a query. Child |EngineQueries| are
        used to construct more complex (nested) query expressions.

    joiner : str
        A logical operator for combining query terms. Corresponds to a
        value in |LOGIC_CHOICES|.

    """

    QUERY_JOINERS = _ENGINE_QUERY_JOINERS
    """|dict|

    Maps the values in |LOGIC_CHOICES| to the corresponding logical
    operators for the Engine.

    Notes
    -----
    Must be overridden in derived classes.

    """

    fieldset_model = NotImplemented
    """|type|

    The |EngineQueryFieldset| subclass used to model fieldsets for the
    Engine.

    Notes
    -----
    Must be overridden in derived classes.

    """

    def __init__(self, subqueries, joiner='AND'):
        """Initialize an EngineQuery instance."""
        self.subqueries = subqueries
        self.joiner = self.get_joiner(joiner)

    def _get_fieldset_model(self):
        """Get the EngineQueryFieldset subclass used for the data store.

        Returns the |EngineQueryFieldset| subclass used to model
        fieldsets for the Engine, if one has been defined. Otherwise,
        raises a NotImplementedError.
        """
        if self.fieldset_model is NotImplemented:
            return self.raise_attr_not_implemented('fieldset_model')
        else:
            return self.fieldset_model

    def _get_selector(self, fieldset):
        """Create a query expression from a fieldset.

        Takes a |QueryFieldset| and returns a query expression.
        """
        fieldset_model = self._get_fieldset_model()
        fieldset_obj = fieldset_model(fieldset)
        return fieldset_obj.selector

    def _get_query(self, query):
        """Create a query expression.

        Takes an |EngineQuery| or |QueryFieldset| and returns a query
        expression. If the `query` argument is an |EngineQuery|,
        recursively examines all its components to form the expression.
        """
        query_phrases = []

        for subquery in query.subqueries:

            # base case
            if isinstance(subquery, QueryFieldset):
                subquery_filter = self._get_selector(subquery)
                query_phrases.append(subquery_filter)

            # recursive case
            elif isinstance(subquery, EngineQuery):
                query_class = type(self)
                classquery = query_class(subquery.subqueries, subquery.joiner)
                subquery_filter = self._get_query(classquery)
                query_phrases.append(subquery_filter)

        return self.join_subqueries(query_phrases, query.joiner)

    def get_joiner(self, raw_joiner):
        """Return a logical operator to join fieldsets.

        Parameters
        ----------
        raw_joiner : str
            Corresponds to the value of an option in |LOGIC_CHOICES|.

        Returns
        -------
        str
            The logical operator that should be used to combine
            fieldsets in the manner specified by the `raw_joiner`
            parameter.

        Raises
        ------
        NotImplementedError
            If :const:`~engines.queries.EngineQuery.QUERY_JOINERS`
            has not been properly implemented.

        """
        joiner = self.QUERY_JOINERS.get(raw_joiner)
        if joiner in [None, NotImplemented]:
            undefined_joiner = 'QUERY_JOINERS[\'%s\']' % raw_joiner
            return self.raise_attr_not_implemented(undefined_joiner)
        else:
            return joiner

    @staticmethod
    def join_subqueries(subqueries, joiner):
        """Return a query expression.

        Parameters
        ----------
        fieldsets : |list| of |QueryFieldsets|
            |QueryFieldsets| for defining a query.

        joiner : str
            A logical operator specifying how multiple query fieldsets
            should be combined. Corresponds to a value in |LOGIC_CHOICES|.

        Raises
        ------
        NotImplementedError
            If the method has not been implemented.

        Notes
        -----
        This method may be overridden in derived classes.

        """
        return {joiner: subqueries}

    @property
    def params(self):
        """Return parameters for a query.

        Returns
        -------
        dict
            A query expression constructed from the object's
        :attr:`~EngineQuery.fieldsets`.

        """
        return self._get_query(self)
