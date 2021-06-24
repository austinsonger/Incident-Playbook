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
from constance import config
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# local
from .conf import CYCLOPS_JS_URL, CYCLOPS_CSS_URL, CYCLOPS_VERSION

DEVELOPMENT_ENABLED = settings.CYCLOPS.get('DEVELOPMENT_ENABLED', False)
DEVELOPMENT_URL = settings.CYCLOPS.get(
    'DEVELOPMENT_URL', 'http://localhost:8080/')
API_TIMEOUT = settings.CYCLOPS.get('API_TIMEOUT', 30000)

CSS_URL = (
    '{}cyclops.css'.format(DEVELOPMENT_URL)
    if DEVELOPMENT_ENABLED
    else CYCLOPS_CSS_URL
)
JS_URL = (
    '{}cyclops.js'.format(DEVELOPMENT_URL)
    if DEVELOPMENT_ENABLED
    else CYCLOPS_JS_URL
)


@login_required(login_url='/login/')
def application(request):
    """Return an HTML template for Cyclops.

    Returns an HTML template for Cyclops with the necessary variables and
    resources to make it run.

    Parameters
    ----------
    request : :class:`~django.http.HttpRequest`

    Returns
    -------
    :class:`~django.http.HttpResponse`

    """
    api_timeout = settings.CYCLOPS.get('API_TIMEOUT', 30000)

    return render(request, 'cyclops/app.html', {
        'notifications_enabled': config.PUSH_NOTIFICATIONS_ENABLED,
        'mapbox_access_token': settings.CYCLOPS['MAPBOX_ACCESS_TOKEN'],
        'cyclops_version': CYCLOPS_VERSION,
        'cyphon_version': request.cyphon_version,
        'css_url': CSS_URL,
        'js_url': JS_URL,
        'api_timeout': api_timeout,
    })


def manifest(request):
    """Return the manifest.json necessary for push notifications.

    Parameters
    ----------
    request : :class:`~django.http.HttpRequest`

    Returns
    -------
    :class:`~django.http.JsonResponse`

    """
    return JsonResponse({
        'gcm_sender_id': settings.NOTIFICATIONS['GCM_SENDER_ID'],
        'manifest_version': 2,
        'name': 'Cyphon Push Notifications',
        'version': '0.2',
    })
