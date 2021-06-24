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
Views for push notifications.
"""

# third party
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# local
from alerts.models import Alert
from .serializers import SubscribeSerializer

LEVEL_IMAGES = {
    'CRITICAL': '/assets/img/cyphon-push-notification-critical.png',
    'HIGH': '/assets/img/cyphon-push-notification-high.png',
    'MEDIUM': '/assets/img/cyphon-push-notification-medium.png',
    'LOW': '/assets/img/cyphon-push-notification-low.png',
    'INFO': '/assets/img/cyphon-push-notification-info.png'
}


class SubscribeView(APIView):
    """
    View that allows a user to subscribe to push notifications
    """
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        """
        Subscribes a user to push notifications
        """
        serializer = SubscribeSerializer(data=request.data)

        if serializer.is_valid() and request.user.is_authenticated:
            user = request.user
            user.push_notification_id = serializer.data['registration_id']
            try:
                user.save()
                return Response(status.HTTP_202_ACCEPTED)
            except IntegrityError:
                return Response(serializer.errors, status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class NotificationView(APIView):
    """
    View that allows a user to get notification data relavent to them.
    """
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        """
        Creates and returns a notification object for push notifications.
        """
        registration_id = request.query_params.get('registration_id')

        # If there was no registration id sent with the request, return a
        # 400 error.
        if not registration_id:
            return Response({
                'errors': ['registration_id parameter was not given']
            }, status=status.HTTP_400_BAD_REQUEST)

        user_model = get_user_model()

        # Check if there is a user with the registration id. If there isn't,
        # return a 400 error.
        try:
            user = user_model.objects.get(push_notification_id=registration_id)
        except ObjectDoesNotExist:
            return Response({
                'errors': ['registration_id is not valid']
            }, status=status.HTTP_400_BAD_REQUEST)

        new_alerts = Alert.objects.filter(status='NEW')
        alerts_for_user = Alert.objects.filter_by_user(user, new_alerts)
        alert = alerts_for_user.first()

        # If there is no alert classified as new, return a 404 error.
        if not alert:
            return Response({
                'errors': ['alert object not present']
            }, status=status.HTTP_404_NOT_FOUND)

        notification = {
            'title': '{}: {}'.format(alert.level, alert.distillery),
            'tag': 'cyphon-alert-{}'.format(alert.id),
            'message': alert.title,
            'icon': LEVEL_IMAGES[alert.level]
        }

        return Response(notification)
