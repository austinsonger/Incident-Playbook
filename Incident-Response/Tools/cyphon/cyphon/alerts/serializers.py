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
Serializers for Alerts.
"""

# third party
from rest_framework import serializers

# local
from cyphon.choices import ALERT_LEVEL_CHOICES
from appusers.serializers import AppUserSerializer
from distilleries.serializers import (
    DistilleryDetailSerializer,
    DistilleryListSerializer,
)
from tags.serializers import TagDetailSerializer
from responder.dispatches.serializers import DispatchSerializer
from .models import Alert, Analysis, Comment


class AnalysisSerializer(serializers.ModelSerializer):
    """
    Base serializer for the Analysis class.
    """

    class Meta(object):
        """Metadata options."""

        model = Analysis
        fields = (
            'alert',
            'created_date',
            'last_updated',
            'notes',
        )


class CommentSerializer(serializers.ModelSerializer):
    """
    Base serializer for the Comment class.
    """

    class Meta(object):
        """Metadata options."""

        model = Comment
        fields = (
            'id',
            'alert',
            'user',
            'created_date',
            'content',
        )


class CommentDetailSerializer(CommentSerializer):
    """
    Extended Comment serializer that shows the user object.
    """
    user = AppUserSerializer()


class AlertListSerializer(serializers.ModelSerializer):
    """
    Serializer for Alert list views.
    """
    assigned_user = AppUserSerializer()
    distillery = DistilleryListSerializer()
    title = serializers.CharField(source='display_title')

    class Meta(object):
        """Metadata options."""

        model = Alert
        depth = 1
        fields = (
            'id',
            'assigned_user',
            'content_date',
            'created_date',
            'distillery',
            'incidents',
            'level',
            'outcome',
            'status',
            'title',
            'url',
        )


class RedactedAlertListSerializer(AlertListSerializer):
    """
    Redacted serializer for Alert list views.
    """
    title = serializers.CharField(source='redacted_title')


class AlertUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used to update an Alert Model.
    """
    level = serializers.ChoiceField(
        required=False,
        choices=ALERT_LEVEL_CHOICES,
    )
    notes = serializers.CharField(source='analysis__notes')

    class Meta(object):
        """Metadata options."""

        model = Alert
        fields = (
            'assigned_user',
            'outcome',
            'status',
            'level',
            'notes',
        )


class AlertDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Alert detail views.
    """
    assigned_user = AppUserSerializer()
    comments = CommentDetailSerializer(many=True)
    data = serializers.JSONField(source='tidy_data')
    dispatches = DispatchSerializer(many=True)
    distillery = DistilleryDetailSerializer()
    location = serializers.JSONField(source='coordinates')
    tags = TagDetailSerializer(source='associated_tags', many=True)
    title = serializers.CharField(source='display_title')

    class Meta(object):
        """Metadata options."""

        model = Alert
        depth = 2
        fields = (
            'id',
            'assigned_user',
            'comments',
            'content_date',
            'created_date',
            'data',
            'dispatches',
            'distillery',
            'doc_id',
            'incidents',
            'level',
            'link',
            'location',
            'notes',
            'outcome',
            'status',
            'tags',
            'title',
            'url',
        )


class RedactedAlertDetailSerializer(AlertDetailSerializer):
    """
    Redacted serializer for Alert detail views.
    """
    title = serializers.CharField(source='redacted_title')
