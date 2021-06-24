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

# third party
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q

# local
from alerts.models import Alert
from alerts.serializers import AlertDetailSerializer
from distilleries.models import Distillery
from utils.dbutils.dbutils import join_query
from .search_results import DEFAULT_PAGE_SIZE, SearchResults

ALERT_SEARCH_VIEW_NAME = 'search_alerts'


class AlertSearchResults(SearchResults):
    """

    """
    VIEW_NAME = 'search_alerts'
    OPERATOR_CONVERSIONS = {
        'regex': 'icontains',
        'eq': '',
        'not:eq': '',
    }
    NEGATIVE_QUERY_FLAGS = ['not:eq']

    def __init__(self, query, page=1, page_size=DEFAULT_PAGE_SIZE,
                 after=None, before=None):
        """Find alerts that match a SearchQuery.

        Parameters
        ----------
        query : query.search.search_query.SearchQuery

        """
        super(AlertSearchResults, self).__init__(
            self.VIEW_NAME, query, page, page_size,
            after=after, before=before)
        self.results = []

        queryset = self._get_alert_search_queryset(
            query, after=after, before=before)

        if queryset:
            self.results = self._get_results_page(
                queryset, page, page_size)
            self.count = queryset.count()

    @staticmethod
    def _serialize_alert_object(alert, request):
        """Return a JSON serializable representation of an Alert.

        Parameters
        ----------
        alert : Alert
            Alert object to serialize.

        request : django.http.HttpRequest
            Request from the view that wants the serializable data.

        Returns
        -------
        dict

        """
        return AlertDetailSerializer(alert, context={'request': request}).data

    @staticmethod
    def _get_keyword_search_query(keyword, text_fields):
        """ Create a search query for searching by keyword.

        Parameters
        ----------
        keyword : string
        text_fields : list of DataField

        Returns
        -------
        Q
        """
        queries = [
            Q(title__icontains=keyword),
            Q(analysis__notes__icontains=keyword),
            Q(comments__content__icontains=keyword)]

        for field in text_fields:
            underscored_field = field.replace('.', '__')
            query_field = 'data__{}__icontains'.format(underscored_field)
            queries.append(Q(**{query_field: keyword}))

        return join_query(queries, 'OR')

    @staticmethod
    def _get_keyword_list_search_query(keywords, distilleries):
        """Create a search query that searches alerts for keywords.

        Parameters
        ----------
        keywords : list of str
            Keywords to search for.

        distilleries: list of distilleries.models.Distillery

        Returns
        -------
        Q

        """
        if not keywords:
            return Q()

        text_fields = AlertSearchResults._get_shared_text_fields(distilleries)
        queries = [
            AlertSearchResults._get_keyword_search_query(keyword, text_fields)
            for keyword in keywords]

        if len(queries) == 1:
            return queries[0]

        return join_query(queries, 'AND')

    @staticmethod
    def _convert_fieldset_operator(fieldset_operator):
        """Converts a Fieldset operator to the django filter equivalent.

        Parameters
        ----------
        fieldset_operator: str

        Returns
        -------
        str
        """

        return (
            AlertSearchResults.OPERATOR_CONVERSIONS[fieldset_operator]
            or fieldset_operator)

    @staticmethod
    def _format_fieldset_operator(fieldset_operator):
        conversion = AlertSearchResults._convert_fieldset_operator(
            fieldset_operator)

        return '__{}'.format(conversion) if conversion else ''

    @staticmethod
    def _create_field_query(field_parameter):
        field_name = field_parameter.field_name
        fieldset_operator = field_parameter.operator.fieldset_operator
        parsed_value = field_parameter.value.parsed_value
        query_field = 'data__{}{}'.format(
            field_name.replace('.', '__'),
            AlertSearchResults._format_fieldset_operator(fieldset_operator))
        query = Q(**{query_field: parsed_value})

        return (
            ~query
            if fieldset_operator in AlertSearchResults.NEGATIVE_QUERY_FLAGS
            else query)

    @staticmethod
    def _get_field_search_query(field_parameters):
        """

        Parameters
        ----------
        field_parameters : list of query.search.field_search_parameter.FieldSearchParameter

        Returns
        -------
        Q
        """
        if not field_parameters:
            return Q()

        queries = []

        for parameter in field_parameters:
            if not parameter.is_valid():
                continue

            if not parameter.operator.fieldset_operator:
                continue

            query = AlertSearchResults._create_field_query(parameter)
            queries.append(query)

        return join_query(queries, 'AND') if queries else Q()

    @staticmethod
    def _get_shared_text_fields(distilleries):
        """Gets the shared text fields from a list of distilleries.

        Parameters
        ----------
        distilleries : list of Distillery

        Returns
        -------
        list of DataFields
        """
        grouped_text_fields = [
            distillery.get_text_fields() for distillery in distilleries]
        text_fields = [
            text_field for grouped_text_field in grouped_text_fields
            for text_field in grouped_text_field]
        field_names = [field.field_name for field in text_fields]

        return list(set(field_names))

    @staticmethod
    def _get_alert_search_queryset(query, after=None, before=None):
        """Return the queryset of alerts matching particular keywords.

        Parameters
        ----------
        query : query.search.search_query.SearchQuery
            Keywords to search for.

        after: datetime

        before: datetime

        Returns
        -------
        django.db.models.query.QuerySet

        """
        alert_qs = Alert.objects.filter_by_user(query.user)
        distillery_qs = None

        if not query.user.is_staff:
            distillery_qs = Distillery.objects.filter(
                company=query.user.company)

        if query.distilleries.count():
            distillery_qs = query.distilleries

        if distillery_qs:
            alert_qs = alert_qs.filter(distillery__in=distillery_qs)
        else:
            distillery_qs = Distillery.objects.all()

        if after:
            alert_qs = alert_qs.filter(created_date__gte=after)
        if before:
            alert_qs = alert_qs.filter(created_date__lte=before)

        keyword_query = AlertSearchResults._get_keyword_list_search_query(
            query.keywords, distillery_qs)
        field_query = AlertSearchResults._get_field_search_query(
            query.field_parameters)
        alert_qs = alert_qs.filter(
            join_query([keyword_query, field_query], 'AND'))

        return alert_qs

    @staticmethod
    def _serialize_alert_queryset(queryset, request):
        """Create a JSON serializable representation of the alert queryset.

        Parameters
        ----------
        queryset : django.db.models.query.QuerySet
            Alert queryset.

        request : django.http.HttpRequest
            Request from the view making the request.

        Returns
        -------
        list of dict

        """
        return [
            AlertSearchResults._serialize_alert_object(alert, request)
            for alert in queryset
        ]

    @staticmethod
    def _get_results_page(queryset, page, page_size):
        """

        """
        paginator = Paginator(queryset, page_size)

        try:
            return paginator.page(page)
        except EmptyPage:
            return []

    def as_dict(self, request):
        """Return a JSON serializable representation of this object.

        Parameters
        ----------
        request : :class:`~django.http.HttpRequest`

        Returns
        -------
        |dict|

        """
        parent_dict = super(AlertSearchResults, self).as_dict(request)

        parent_dict['results'] = self._serialize_alert_queryset(
            self.results, request)

        return parent_dict
