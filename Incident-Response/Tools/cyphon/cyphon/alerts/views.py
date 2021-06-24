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
Provides views for Alerts.
"""

# standard library
import datetime
import json

# third party
from django.db.models import OuterRef
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.utils import timezone
from rest_framework.decorators import list_route
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

# local
from cyphon.choices import ALERT_LEVEL_CHOICES, ALERT_STATUS_CHOICES
from cyphon.views import CustomModelViewSet
from distilleries.models import Distillery
from distilleries.serializers import DistilleryListSerializer
from utils.dbutils.dbutils import count_by_group, SQCount
from .filters import AlertFilter
from .models import Alert, Analysis, Comment
from .serializers import (
    AlertDetailSerializer,
    AlertListSerializer,
    AlertUpdateSerializer,
    AnalysisSerializer,
    RedactedAlertDetailSerializer,
    RedactedAlertListSerializer,
    CommentSerializer,
    CommentDetailSerializer,
)


class AlertPagination(LimitOffsetPagination):
    """
    Pagination class for overriding the default pagination for Alerts.
    """
    default_limit = 20
    max_limit = 100


class AlertViewSet(CustomModelViewSet):
    """
    A simple ViewSet for viewing and editing Alerts.
    """
    queryset = Alert.objects.all()
    filter_class = AlertFilter
    pagination_class = AlertPagination
    serializer_class = AlertDetailSerializer
    custom_filter_backends = ['alerts.filters.AlertFilterBackend']

    MAX_DAYS = 30

    def get_queryset(self):
        """
        Overrides the default method for returning the ViewSet's
        queryset.
        """
        use_redaction = self.request.user.use_redaction
        if use_redaction:
            return Alert.objects.with_codebooks()
        else:
            # ensure queryset is re-evaluated on each request
            return self.queryset.all()

    def partial_update(self, request, pk):
        """
        Performs a patch request to update an alert.
        """
        alert = self.get_object()
        alert_serializer = AlertUpdateSerializer(alert, data=request.data,
                                                 partial=True)
        if alert_serializer.is_valid():
            updated_alert = alert_serializer.save()

            notes = request.data.get('notes')
            if notes:
                Analysis.objects.save_notes(alert=updated_alert, notes=notes)

            detail_serializer = AlertDetailSerializer(
                updated_alert,
                context={'request': request},
            )
            return Response(detail_serializer.data)

        return Response(alert_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Overrides the default method for returning the ViewSet's
        serializer.
        """
        if self.serializer_class is None:  # pragma: no cover
            msg = ("'%s' should either include a `serializer_class` attribute,"
                   " or override the `get_serializer_class()` method."
                   % type(self).__name__)
            raise RuntimeError(msg)

        use_redaction = self.request.user.use_redaction

        if self.action is 'list':
            if use_redaction:
                return RedactedAlertListSerializer
            else:
                return AlertListSerializer
        else:
            if use_redaction:
                return RedactedAlertDetailSerializer
            else:
                return self.serializer_class

    @staticmethod
    def _get_date(days_ago):
        """
        Takes an integer representing a number of days in the past, and
        returns a datetime for midnight localtime of that day.
        """
        try:
            days = int(days_ago)
            localtime = timezone.localtime(timezone.now())
            date_time = localtime - datetime.timedelta(days=days)
            return date_time.replace(hour=0, minute=0,
                                     second=0, microsecond=0)
        except (ValueError, TypeError):
            return None

    def _get_filtered_alerts(self):
        """

        """
        return self.filter_queryset(self.get_queryset())

    def _filter_by_timeframe(self, start_date=None, end_date=None):
        """

        """
        queryset = self._get_filtered_alerts()

        if start_date is not None:
            queryset = queryset.filter(created_date__gte=start_date)

        if end_date is not None:
            queryset = queryset.filter(created_date__lt=end_date)

        return queryset

    def _filter_by_start_date(self, days_ago):
        """

        """
        start_date = self._get_date(days_ago)
        return self._filter_by_timeframe(start_date=start_date)

    @staticmethod
    def _counts_by_field(queryset, field_name, choices):
        """

        """
        counts = count_by_group(
            queryset=queryset,
            column=field_name,
            options=choices
        )
        return counts[field_name]

    def _timeseries(self, days, field_name, choices):
        """

        """
        counts = {'date': []}

        for (value, dummy_text) in choices:
            counts[value] = []

        for day in reversed(range(1, days + 1)):
            start_date = self._get_date(day)
            end_date = self._get_date(day - 1)
            queryset = self._filter_by_timeframe(start_date, end_date)
            date_cnt = self._counts_by_field(
                queryset=queryset,
                field_name=field_name,
                choices=choices
            )
            counts['date'].append(start_date.date())
            for (value, dummy_text) in choices:
                counts[value].append(date_cnt[value])

        return counts

    @staticmethod
    def _handle_missing_days_param():
        """
        Returns a Response containing an error message for a missing
        or improper `days` parameter.
        """
        msg = 'Please provide an integer for the days parameter'
        return Response({'error': msg})

    def _exceeds_max_days(self):
        """
        Returns a Response containing an error message when a `days`
        parameter exceeds the maximum allowed.
        """
        msg = 'A maximum of %s days is permitted' % self.MAX_DAYS
        return Response({'error': msg})

    def _catch_days_param_error(self, days):
        """

        """
        try:
            days = int(days)
            if days > self.MAX_DAYS:
                return self._exceeds_max_days()
        except (TypeError, ValueError):
            return self._handle_missing_days_param()

    def _get_counts(self, request, field_name, choices):
        """

        """
        days = request.query_params.get('days')

        error = self._catch_days_param_error(days)

        if error:
            return error
        else:
            queryset = self._filter_by_start_date(int(days))
            counts = self._counts_by_field(
                queryset=queryset,
                field_name=field_name,
                choices=choices
            )
            return Response(counts)

    @list_route(methods=['get'], url_path='levels')
    def counts_by_level(self, request):
        """
        Provides a REST API endpoint for GET requests for alert counts
        by level.
        """
        return self._get_counts(request, 'level', ALERT_LEVEL_CHOICES)

    @list_route(methods=['get'], url_path='statuses')
    def counts_by_status(self, request):
        """
        Provides a REST API endpoint for GET requests for alert counts
        by status.
        """
        return self._get_counts(request, 'status', ALERT_STATUS_CHOICES)

    @list_route(methods=['get'], url_path='collections')
    def counts_by_collection(self, request):
        """
        Provides a REST API endpoint for GET requests for alert counts
        by Collection.
        """
        days = request.query_params.get('days')
        error = self._catch_days_param_error(days)
        date = self._get_date(days)

        if error:
            return error
        else:
            alerts = Alert.objects.filter(
                created_date__gte=date,
                distillery_id=OuterRef('collection_id'))
            alerts = Alert.objects.filter_by_user(request.user, alerts)
            counts = {
                d.name: d.alert_count
                for d in Distillery.objects.annotate(
                    alert_count=SQCount(alerts))
                if d.alert_count
            }
            return Response(counts)

    @list_route(methods=['get'], url_path='locations')
    def locations(self, request):
        """
        Provides a REST API endpoint for GET requests for alert
        locations.

        WARNING
        -------
        Alerts titles will not be redacted.

        """
        days = request.query_params.get('days')

        error = self._catch_days_param_error(days)

        if error:
            return error
        else:
            queryset = self._filter_by_start_date(int(days))
            location_qs = queryset.filter(location__isnull=False)
            fields = (
                'pk',
                'location',
                'title',
                'level',
                'incidents',
            )
            geojson = serialize('geojson', location_qs, fields=fields)
            return Response(json.loads(geojson))

    @list_route(methods=['get'], url_path='level-timeseries')
    def level_timeseries(self, request):
        """
        Provides a REST API endpoint for GET requests for a timeseries
        of alert counts by level.
        """
        days = request.query_params.get('days')

        error = self._catch_days_param_error(days)

        if error:
            return error
        else:
            counts = self._timeseries(
                days=int(days),
                field_name='level',
                choices=ALERT_LEVEL_CHOICES
            )
            return Response(counts)

    @list_route(methods=['get'], url_path='distilleries')
    def distilleries(self, request):
        """
        Provides a REST API endpoint for GET requests for Distilleries
        associated with Alerts.
        """
        alerts = self._get_filtered_alerts()
        distilleries = Distillery.objects.filter(alerts__in=alerts).distinct()
        page = self.paginate_queryset(distilleries)

        if page is not None:
            serializer = DistilleryListSerializer(page, many=True,
                                                  context={'request': request})
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)


class AnalysisViewSet(CustomModelViewSet):
    """
    Viewset for viewing and editing Alert Analyses.
    """
    queryset = Analysis.objects.all()
    pagination_class = AlertPagination
    serializer_class = AnalysisSerializer
    filter_fields = ['alert', 'alert__assigned_user']

    def get_object(self):
        """
        Gets an object for single object views.
        """
        queryset = self.get_queryset()
        primary_key = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, pk=primary_key)
        self.check_object_permissions(self.request, obj)

        if self._is_write_request() and \
                (obj.alert.assigned_user is None or
                 self.request.user.id != obj.alert.assigned_user.id):
            raise PermissionDenied()

        return obj


class CommentPagination(PageNumberPagination):
    """
    Pagination for comments view.
    """
    page_size = 100


class CommentViewSet(CustomModelViewSet):
    """
    Viewset for viewing and editing Alert Comments.
    """
    queryset = Comment.objects.all().order_by('created_date')
    pagination_class = CommentPagination
    serializer_class = CommentSerializer
    filter_fields = ['alert', 'user']

    def get_serializer_class(self):
        """

        """
        base_serializer_actions = ['create', 'update', 'partial_update']

        if self.action in base_serializer_actions:
            return CommentSerializer

        return CommentDetailSerializer

    def get_object(self):
        """
        Gets an object for single object views.
        """
        queryset = self.get_queryset()
        primary_key = self.kwargs[self.lookup_field]
        obj = get_object_or_404(queryset, pk=primary_key)
        self.check_object_permissions(self.request, obj)
        is_comment_user = self.request.user.id is obj.user.id

        if self._is_write_request() and not is_comment_user:
            raise PermissionDenied()

        return obj
