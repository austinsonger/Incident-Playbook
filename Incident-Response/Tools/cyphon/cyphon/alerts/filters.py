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
Defines AlertFilter, CommentFilter, and CommentFilterBackend classes.
"""

# standard library
import logging
# from threading import Thread

# third party
from django.db.models import Q
from django_filters.rest_framework import filters as django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend

# from rest_framework.filters import BaseFilterBackend

# local
from appusers.models import AppUser
from categories.models import Category
from cyphon.choices import ALERT_LEVEL_CHOICES, ALERT_STATUS_CHOICES
from distilleries.models import Distillery
from tags.models import Tag
from utils.dbutils.dbutils import join_query
from warehouses.models import Warehouse
from .models import Alert

LOGGER = logging.getLogger(__name__)


class AlertFilter(FilterSet):
    """
    Filters Alerts.
    """

    def __init__(self, *args, **kwargs):
        super(AlertFilter, self).__init__(*args, **kwargs)

        # add a blank choice to ChoiceFilter options
        for (dummy_name, field) in self.filters.items():
            if type(field) is django_filters.ChoiceFilter:
                field.choices = tuple([('', '---------'), ] +
                                      list(field.choices))

    collection = django_filters.ModelMultipleChoiceFilter(
        name='distillery',
        label='Collections',
        queryset=Distillery.objects.have_alerts()
    )
    warehouse = django_filters.ModelMultipleChoiceFilter(
        name='distillery__collection__warehouse',
        label='Warehouses',
        queryset=Warehouse.objects.all()
    )
    after = django_filters.DateTimeFilter(
        name='created_date',
        lookup_expr='gt'
    )
    before = django_filters.DateTimeFilter(
        name='created_date',
        lookup_expr='lte'
    )
    level = django_filters.MultipleChoiceFilter(choices=ALERT_LEVEL_CHOICES)
    status = django_filters.MultipleChoiceFilter(choices=ALERT_STATUS_CHOICES)
    assigned_user = django_filters.ModelChoiceFilter(
        name='assigned_user',
        queryset=AppUser.objects.all()
    )
    content = django_filters.CharFilter(
        name='data',
        label='Content',
        method='filter_by_content'
    )
    categories = django_filters.ModelMultipleChoiceFilter(
        name='distillery__categories',
        label='Collection categories',
        queryset=Category.objects.all()
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        name='tag_relations__tags',
        label='tags',
        queryset=Tag.objects.all(),
        method='filter_by_tags'
    )

    class Meta:
        model = Alert

        # List content field last so it will have fewer Alerts to
        # filter. The content filter requires a query to the Distillery
        # associated with the Alert. It's best to filter out as many
        # records as possible before constructing that query.
        fields = ['collection', 'after', 'before', 'level', 'status',
                  'assigned_user', 'content']

    @staticmethod
    def _get_data_query(distillery, value):
        """

        """
        text_fields = distillery.get_text_fields()
        field_names = [field.field_name for field in text_fields]
        field_keys = [name.replace('.', '__') for name in field_names]
        queries = []

        for key in field_keys:
            query_exp = 'data__%s' % key
            kwarg = {query_exp: value}
            queries.append(Q(**kwarg))

        field_query = join_query(queries, 'OR')
        return Q(distillery=distillery) & field_query

    @staticmethod
    def _get_title_query(value):
        """

        """
        return Q(title__icontains=value)

    def _filter_by_value(self, queryset, value):
        """

        """
        distilleries = Distillery.objects.filter(alerts__in=queryset).distinct()

        if distilleries:
            queries = [self._get_data_query(distillery, value) \
                       for distillery in distilleries]
            data_query = join_query(queries, 'OR')
            title_query = self._get_title_query(value)
            return queryset.filter(title_query | data_query)
        else:
            return queryset.none()

    # @timeit
    def filter_by_content(self, queryset, name, value):
        """
        Takes a QuerySet of Alerts and a string value. Returns a filtered
        QuerySet of Alerts whose data includes the given value.
        """
        if not value:
            return queryset

        try:
            return self._filter_by_value(queryset, value)

        except ValueError:
            LOGGER.error('An error occurred while filtering Alerts')
            return queryset

    @staticmethod
    def filter_by_tags(queryset, name, value):
        """Filter |Alerts| by their associated |Tags|.

        Parameters
        ----------
        queryset : |QuerySet| of |Alerts|

        name : str

        value : |QuerySet| of |Tags|

        Returns
        -------
        |QuerySet| of |Alerts|

        """
        if not value:
            return queryset

        try:
            alert_q = Q(tag_relations__tag__in=value)
            analysis_q = Q(analysis__tag_relations__tag__in=value)
            comment_q = Q(comments__tag_relations__tag__in=value)
            return queryset.filter(alert_q | analysis_q | comment_q).distinct()

        except (TypeError, ValueError):
            LOGGER.error('An error occurred while filtering Alerts')
            return queryset


class AlertFilterBackend(DjangoFilterBackend):
    """
    Provides a filter backend to only show |Alerts| that are either
    associated with at least one of a given user's |Group| or are not
    associated with any |Group|.
    """

    def filter_queryset(self, request, queryset, view):
        """Return a filtered queryset.

        Implements `custom filtering`_.

        Parameters
        ----------
        request : Request
             A `Request`_ for a resource.

        queryset : QuerySet
            A |QuerySet| to be filtered.

        view : ModelViewSet
            A `ModelViewSet`_.

        Returns
        -------
        QuerySet
            A |QuerySet| filtered to only show |Alerts| that are either
            associated with at least one of a given user's |Group| or
            are not associated with any |Group|.

        """
        user = request.user
        return Alert.objects.filter_by_user(user, queryset)
