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
Defines Context and ContextFilter classes for finding documents related
to a given reference document.
"""

# standard library
from datetime import timedelta
import logging

# third party
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.fieldsets import QueryFieldset
from cyphon.choices import (
    LOGIC_CHOICES,
    MINUTES,
    OPERATOR_CHOICES,
    TIME_UNIT_CHOICES,
)
from distilleries.models import Distillery
from engines.queries import EngineQuery
from engines.sorter import SortParam, Sorter
from utils.choices.choices import get_field_type
from utils.dateutils import dateutils as dt
from utils.parserutils.parserutils import get_dict_value

_LOGGER = logging.getLogger(__name__)


class ContextManager(models.Manager):
    """Manage |Context| objects.

    Adds methods to the default Django model manager.
    """

    def get_by_natural_key(self, name, distillery_name):
        """Get a |Context| by its natural key.

        Allows retrieval of a |Context| by its natural key instead of
        its primary key.

        Parameters
        ----------
        name : str
            The name of the Context.

        backend : str
            The backend associated with the Context's `primary_distillery`.

        warehouse_name : str
            The name of the |Warehouse| associated with the Context's
            `primary_distillery`.

        collection_name : str
            The name of the |Collection| associated with the Context's
            `primary_distillery`.

        Returns
        -------
        |Context|
            The |Context| associated with the natural key.

        """
        try:
            return self.get(name=name,
                            primary_distillery__name=distillery_name)
        except ObjectDoesNotExist:
            _LOGGER.error('%s %s:%s does not exist',
                          self.model.__name__, name, distillery_name)


class Context(models.Model):
    """
    A Context takes a reference document that was distilled by one
    Distillery and returns related documents from another Distillery.

    The Context's optional time_interval defines a time frame in which
    to search for related documents. A Context may also have one or more
    ContextFilters. A ContextFilter filters related documents by a value
    in the reference document.

    Attributes
    ----------
    name : str
        The name of the Context.

    primary_distillery : Distillery
        The Distillery in which the reference documents reside.

    related_distillery : Distillery
        A Distillery that should be searched for documents related to
        documents in the primary_distillery.

    before_time_interval : int
        An int which, when combined with before_time_units, defines a
        time frame in which to search for related documents. Captures
        data generated prior to the data associated with the Alert.

    before_time_unit : str
        The time units for the before_time_interval. Possible values are
        constrained to TIME_UNIT_CHOICES.

    after_time_interval : int
        An int which, when combined with after_time_units, defines a
        time frame in which to search for related documents. Captures
        data generated after the data associated with the Alert.

    after_time_unit : str
        The time units for the before_time_interval. Possible values are
        constrained to TIME_UNIT_CHOICES.

    Notes
    -----

    The Context's optional time_interval is relative to the date
    associated with the reference document.

    If a Context has neither a time_interval nor a ContextFilter, it
    will not attempt to find related data. Instead, search requests
    will return an error message asking the user to define a
    time_interval or ContextFilter.

    """
    name = models.CharField(max_length=60)
    primary_distillery = models.ForeignKey(
        Distillery,
        related_name='contexts',
        related_query_name='context'
    )
    related_distillery = models.ForeignKey(Distillery)
    before_time_interval = models.PositiveIntegerField(null=True, default=0)
    before_time_unit = models.CharField(max_length=3, choices=TIME_UNIT_CHOICES,
                                        null=True, default=MINUTES)
    after_time_interval = models.PositiveIntegerField(null=True, default=0)
    after_time_unit = models.CharField(max_length=3, choices=TIME_UNIT_CHOICES,
                                       null=True, default=MINUTES)
    filter_logic = models.CharField(
        max_length=40,
        choices=LOGIC_CHOICES,
        default='AND'
    )

    objects = ContextManager()

    class Meta:
        unique_together = ['name', 'primary_distillery']
        ordering = ['name', 'primary_distillery', 'related_distillery']

    def __str__(self):
        return self.name

    def clean(self):
        super(Context, self).clean()
        if self._has_time_interval():
            if not self._focal_date_field:
                msg = _('A time frame is specified, but the primary '
                        'distillery\'s Container has no designated date '
                        'field. Please make sure the Container has a Taste '
                        'with a date field.')
                raise ValidationError(msg)
            if not self._related_date_field:
                msg = _('A time frame is specified, but the related '
                        'distillery\'s Container has no designated date '
                        'field. Please make sure the Container has a Taste '
                        'with a date field.')
                raise ValidationError(msg)

    @cached_property
    def _focal_date_field(self):
        """

        """
        return self.primary_distillery.get_date_field()

    @cached_property
    def _related_date_field(self):
        """
        Returns the name of a date field in the related_distillery's
        Container for filtering documents by time. If no such field
        exists, returns the name of the field for storing the date
        on which a distilled document is saved.
        """
        return self.related_distillery.get_searchable_date_field()

    def _has_before_interval(self):
        """
        Returns a Boolean indicating whether the Context contains a
        "before" time interval.
        """
        return bool(self.before_time_interval and self.before_time_unit)

    def _has_after_interval(self):
        """
        Returns a Boolean indicating whether the Context contains an
        "after" time interval.
        """
        return bool(self.after_time_interval and self.after_time_unit)

    def _has_time_interval(self):
        """
        Returns a Boolean indicating whether the Context has a time
        interval.
        """
        return self._has_before_interval() or self._has_after_interval()

    def _get_before_interval_in_seconds(self):
        """
        If the Context has a time_interval and time_unit, returns the
        number of seconds in the Context's time interval. Otherwise,
        returns 0.
        """
        if self._has_before_interval():
            return dt.convert_time_to_seconds(self.before_time_interval,
                                              self.before_time_unit)
        else:
            return 0

    def _get_after_interval_in_seconds(self):
        """
        If the Context has a time_interval and time_unit, returns the
        number of seconds in the Context's time interval. Otherwise,
        returns 0.
        """
        if self._has_after_interval():
            return dt.convert_time_to_seconds(self.after_time_interval,
                                              self.after_time_unit)
        else:
            return 0

    def _get_reference_time(self, data):
        """
        Takes a dictionary of reference data and attempts to return a
        datetime object from the designated date field in the dictionary.
        """
        if self._focal_date_field:
            return self.primary_distillery.get_date(data)

    def _get_end_time(self, data):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery and returns a datetime for the end of a time
        frame for searching related data.
        """
        reference_time = self._get_reference_time(data)
        if reference_time:
            seconds = self._get_after_interval_in_seconds()
            return reference_time + timedelta(seconds=seconds)

    def _get_start_time(self, data):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery. Returns a datetime for the start of a time
        frame for searching related data.
        """
        reference_time = self._get_reference_time(data)
        if reference_time:
            seconds = self._get_before_interval_in_seconds()
            return reference_time - timedelta(seconds=seconds)

    def _create_timeframe_query(self, data):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery. If the Context has a time_interval and
        time_unit, returns a list of fieldset dictionaries for a
        time-frame query. Otherwise, returns an empty list.
        """
        timeframe = []

        if self._has_time_interval():
            start_time = self._get_start_time(data)
            end_time = self._get_end_time(data)

            if start_time:
                timeframe.append(QueryFieldset(
                    field_name=self._related_date_field,
                    field_type='DateTimeField',
                    operator='gt',
                    value=start_time
                ))

            if end_time:
                timeframe.append(QueryFieldset(
                    field_name=self._related_date_field,
                    field_type='DateTimeField',
                    operator='lte',
                    value=end_time
                ))

        if timeframe:
            return EngineQuery(timeframe, 'AND')

    def _create_filter_query(self, data):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery. Returns a list of fieldset dictionaries for
        query terms defined by the Context's ContextFilters. If the
        Context has no ContextFilters, returns an empty list.
        """
        fieldsets = [cfilter.create_fieldset(data) \
                     for cfilter in self.filters.all()]
        if fieldsets:
            return EngineQuery(fieldsets, self.filter_logic)

    def _get_text_fields(self):
        """
        Returns a list of text DataFields associated with the
        primary_distillery's Container.
        """
        return self.related_distillery.get_text_fields()

    def _create_keyword_query(self, keyword):
        """

        """
        keyword_search = []
        if keyword:
            fields = self._get_text_fields()
            for field in fields:
                keyword_search.append(QueryFieldset(
                    field_name=field.field_name,
                    field_type=field.field_type,
                    operator='regex',
                    value=keyword
                ))
        if keyword_search:
            return EngineQuery(keyword_search, 'OR')

    def _get_query(self, data, keyword):
        """

        """
        filter_q = self._create_filter_query(data)
        keyword_q = self._create_keyword_query(keyword)
        timeframe_q = self._create_timeframe_query(data)
        subqueries = [q for q in [filter_q, keyword_q, timeframe_q] if q]
        if subqueries:
            return EngineQuery(subqueries, 'AND')

    def _get_sorter(self):
        """

        """
        sort = SortParam(
            field_name=self._related_date_field,
            field_type='DateTimeField',
            order='DESC',
        )
        return Sorter(sort_list=[sort])

    def _find_related_data(self, data, keyword, page, page_size):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery and an integer specifying the page in a
        paginated result set. Returns a list of data dictionaries for
        related documents that match the Context's time frame and
        ContextFilters. If the Context has neither a time frame nor any
        ContextFilters, returns a dictionary containing an error message.
        """
        query = self._get_query(data, keyword)
        sorter = self._get_sorter()

        if query:
            results = self.related_distillery.find(query, sorter, page, page_size)
            if isinstance(results, dict):
                return results
            else:
                return {'error': 'The query could not be completed. '
                                 'Please increase the timeout setting '
                                 'or try again later.'}
        else:
            return {'error': 'No query parameters available for searching '
                             'related data. Please define a time interval, '
                             'keyword, or filters for the Context.'}

    def _get_reference_data(self, doc_id):
        """
        Takes a document id and returns the matching document from the
        Context's primary_distillery,
        """
        return self.primary_distillery.find_by_id(doc_id)

    def get_primary_distillery_fields(self):
        """
        Returns a list of field names for fields in the
        primary_distillery's Container.
        """
        return self.primary_distillery.get_field_list()

    def get_related_distillery_fields(self):
        """
        Returns a list of field names for fields in the
        related_distillery's Container.
        """
        return self.related_distillery.get_field_list()

    def get_related_data(self, data, keyword=None, page=None, page_size=None):
        """
        Takes a dictionary of data that was distilled by the Context's
        primary_distillery. Returns a dictionary that includes the name of
        the related_distillery and a list of documents from that
        distillery's Collection that match the Context's time frame and
        ContextFilters. E.g.::

            {
                'distillery': 'mongodb.mydatabase.mycollection',
                'results': [
                    {
                        'date': '1463150162',
                        'username': 't-rex',
                        'post': 'I hate pushups'
                    }
                ]
            }

        """
        results = self._find_related_data(data, keyword, page, page_size)
        results['distillery'] = str(self.related_distillery)
        return results

    def get_related_data_by_id(self, doc_id, keyword=None,
                               page=None, page_size=None):
        """
        Takes a document id for a document distilled by the Context's
        primary_distillery. Returns a dictionary that includes the name
        of the related_distillery and a list of relevant documents from
        that distillery. If a document matching the doc_id can't be
        found in the primary_distillery's Collection, returns a dictionary
        containing an error message.
        """
        data = self._get_reference_data(doc_id)
        if data:
            return self.get_related_data(data, keyword, page, page_size)
        else:
            msg = 'The document associated with the id could not be found.'
            return {'error': msg}


class ContextFilterManager(models.Manager):
    """Manage |ContextFilter| objects.

    Adds methods to the default Django model manager.
    """

    # pylint: disable=R0913
    def get_by_natural_key(self, name, distillery_name, value_field,
                           search_field):
        """Get a |ContextFilter| by its natural key.

        Allows retrieval of a |ContextFilter| by its natural key instead
        of its primary key.

        Parameters
        ----------
        name : str
            The name of the |Context| to which the |ContextFilter| belongs.

        backend : str
            The backend associated with the `primary_distillery` of the
            |ContextFilter|'s |Context|.

        warehouse_name : str
            The name of the |Warehouse| associated with the
            `primary_distillery` of the |ContextFilter|'s |Context|.

        collection_name : str
            The name of the |Collection| associated with the
            `primary_distillery` of the |ContextFilter|'s |Context|.

        value_field : str
            The |ContextFilter|'s `value_field`.

        search_field : str
            The |ContextFilter|'s `search_field`.

        Returns
        -------
        |ContextFilter|
            The |ContextFilter| associated with the natural key.

        """
        try:
            filter_key = [name, distillery_name]
            context = Context.objects.get_by_natural_key(*filter_key)
            return self.get(context=context, value_field=value_field,
                            search_field=search_field)
        except ObjectDoesNotExist:
            _LOGGER.error('%s %s:%s (%s -> %s) does not exist',
                          self.model.__name__, name, distillery_name,
                          value_field, search_field)


class ContextFilter(models.Model):
    """
    Defines parameters for constructing a query expression to filter
    data for a Context.

    Attributes
    ----------
    context : Context
        The Context with which the ContextFilter is associated.

    value_field : str
        The name of a Container field in the Context's primary_distillery
        whose value will be used to construct a query expression.

    search_field : str
        The name of a Container field in the Context's related_distillery
        whose value will be compared to that of the value_field.

    operator : str
        The operator that should be used in the query expression.
        Options are constrained to OPERATOR_CHOICES.

    """
    context = models.ForeignKey(Context, related_name='filters',
                                related_query_name='filter')
    value_field = models.CharField(
        max_length=255,
        verbose_name=_('value field in Distillery'),
        help_text=_('The Container field whose value should be used to '
                    'search the field of the Related Distillery.'))
    search_field = models.CharField(
        max_length=255,
        verbose_name=_('search field in Related Distillery'),
        help_text=_('The field of the Related Distillery\'s Container '
                    'that should be used to filter results.'))
    operator = models.CharField(max_length=40, choices=OPERATOR_CHOICES)

    objects = ContextFilterManager()

    class Meta:
        unique_together = ('context', 'value_field', 'search_field')
        ordering = ['search_field', 'value_field']

    def clean(self):
        """
        Overrides Django's default clean method for a Model. Checks
        that the value_field is a field in the Container used by the
        Focal Distillery of the Context. Similarly, checks that the
        search_field is a field in the Container used by the Related
        Distillery of the Context.
        """
        super(ContextFilter, self).clean()
        if not self._value_field_is_valid():
            msg = 'The value field "%s" is not a field in the Container '\
                  'used by the Focal Distillery %s.' \
                  % (self.value_field, self.context.primary_distillery)
            raise ValidationError(_(msg))

        if not self._search_field_is_valid():
            msg = 'The search field "%s" is not a field in the Container '\
                  'used by the Related Distillery %s.' \
                  % (self.search_field, self.context.related_distillery)
            raise ValidationError(_(msg))

    @property
    def operator_text(self):
        """
        Returns a human readable string for the context filter operator.
        """
        for choice in OPERATOR_CHOICES:
            if self.operator == choice[0]:
                return choice[1]

        return self.operator

    def _value_field_is_valid(self):
        """
        Returns a Boolean indicating whether the value_field is a field
        in the Container used by the Focal Distillery of the Context.
        """
        fields = self.context.get_primary_distillery_fields()
        return bool(self.value_field in fields)

    def _search_field_is_valid(self):
        """
        Returns a Boolean indicating whether the search_field is a field
        in the Container used by the Related Distillery of the Context.
        """
        fields = self.context.get_related_distillery_fields()
        return bool(self.search_field in fields)

    def create_fieldset(self, data):
        """
        Takes a dictionary of data that was distilled by the Context's
        Focal Distillery. Returns a QueryFieldset representing a
        query expression for the ContextFilter.
        """
        value = get_dict_value(self.value_field, data)
        field_type = get_field_type(self.search_field)
        return QueryFieldset(
            field_name=self.search_field,
            field_type=field_type,
            operator=self.operator,
            value=value
        )
