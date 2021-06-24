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
Methods that handle signals necessary for push notifications.
"""

# standard library
import logging
import requests

# third party
from constance import config
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from alerts.models import Alert

_NOTIFICATION_SETTINGS = settings.NOTIFICATIONS

_PUSH_NOTIFICATION_URL = 'https://android.googleapis.com/gcm/send'

_PUSH_NOTIFICATION_REQUEST_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + _NOTIFICATION_SETTINGS['PUSH_NOTIFICATION_KEY']
}

_LOGGER = logging.getLogger(__name__)


def get_registration_ids(alert):
    """
    Takes an Alert and returns a list of push notification ids for users
    who should be notified.
    """
    user_model = get_user_model()
    queryset = Alert.objects.filter(pk=alert.pk)
    registration_ids = []
    for user in user_model.objects.all():
        can_view = Alert.objects.filter_by_user(user, queryset)

        if can_view and user.push_notification_id:
            registration_ids.append(user.push_notification_id)

    return registration_ids


def send_push_notifications(alert):
    """
    Sends push notifications to all the users that registered for them.
    """
    registration_ids = get_registration_ids(alert)

    if registration_ids:
        data = {'registration_ids': registration_ids}

        try:
            push_request = requests.post(
                _PUSH_NOTIFICATION_URL,
                headers=_PUSH_NOTIFICATION_REQUEST_HEADERS,
                json=data
            )

            if push_request.status_code != 200:
                _LOGGER.error('Could not send push notifications. '
                              'Received error from Chrome server: %s',
                              push_request.text)
            else:
                _LOGGER.info('Push notifications sent successfully')

        except requests.exceptions.SSLError:
            _LOGGER.error('Could not send push notifications. '
                          'SSL certificate verification failed. ')


@receiver(post_save, sender=Alert)
def handle_alert_post_save_signal(sender, instance, created, **kwargs):
    """
    Handles the Alert models post_save signal.
    """
    if created and config.PUSH_NOTIFICATIONS_ENABLED:

        if not _NOTIFICATION_SETTINGS['PUSH_NOTIFICATION_KEY']:
            _LOGGER.error('Could not send push notifications. '
                          'No PUSH_NOTIFICATION_KEY was provided')
        else:
            ignored_levels = _NOTIFICATION_SETTINGS['IGNORED_ALERT_LEVELS']
            if instance.level not in ignored_levels:
                send_push_notifications(instance)
