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
[`source`_]

Cyphon Celery tasks.

.. _source: ../_modules/cyphon/tasks.html

"""

# third party
from django.apps import apps
from django.db import close_old_connections

# local
from cyphon.celeryapp import app
from aggregator.filters.services import execute_filter_queries


@app.task(name='tasks.get_new_mail')
def get_new_mail():
    """
    Checks mail for all Mailboxes.
    """
    mailbox_model = apps.get_model(app_label='django_mailbox',
                                   model_name='mailbox')
    mailboxes = mailbox_model.objects.all()

    for mailbox in mailboxes:
        mailbox.get_new_mail()

    close_old_connections()


@app.task(name='tasks.run_health_check')
def run_health_check():
    """
    Gathers all active Monitors and updates their status.
    """
    monitor_model = apps.get_model(app_label='monitors', model_name='monitor')
    monitors = monitor_model.objects.find_enabled()

    for monitor in monitors:
        monitor.update_status()

    close_old_connections()


@app.task(name='tasks.run_bkgd_search')
def run_bkgd_search():
    """
    Runs background queries.
    """
    execute_filter_queries()
    close_old_connections()
