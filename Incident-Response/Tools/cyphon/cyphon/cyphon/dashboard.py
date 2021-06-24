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
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py:
    GRAPPELLI_INDEX_DASHBOARD = 'cyphon.dashboard.CustomIndexDashboard'
"""

# third party
from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CyphonIndexDashboard(Dashboard):
    """
    Custom index dashboard.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(modules.ModelList(
            _('Shaping Data'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'bottler.bottles.models.BottleField',
                'bottler.bottles.models.Bottle',
                'bottler.labels.models.LabelField',
                'bottler.labels.models.Label',
                'bottler.containers.models.Container',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Filtering Data'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'target.followees.models.Followee',
                'target.locations.models.Location',
                'target.searchterms.models.SearchTerm',
                'aggregator.filters.models.Filter',
            ),
        ))

        self.children.append(modules.Group(
            _('Sifting Data'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            children=[
                modules.ModelList(
                    _('Logs'),
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.logsifter.logsieves.models.LogRule',
                        'sifter.logsifter.logsieves.models.LogSieve',
                        'sifter.logsifter.logmungers.models.LogMunger',
                        'sifter.logsifter.logchutes.models.LogChute',
                    ),
                ),
                modules.ModelList(
                    _('Email'),
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.mailsifter.mailsieves.models.MailRule',
                        'sifter.mailsifter.mailsieves.models.MailSieve',
                        'sifter.mailsifter.mailmungers.models.MailMunger',
                        'sifter.mailsifter.mailchutes.models.MailChute',
                    ),
                ),
                modules.ModelList(
                    _('JSON Data'),
                    column=1,
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.datasifter.datasieves.models.DataRule',
                        'sifter.datasifter.datasieves.models.DataSieve',
                        'sifter.datasifter.datamungers.models.DataMunger',
                        'sifter.datasifter.datachutes.models.DataChute',
                    ),
                ),
            ]
        ))

        self.children.append(modules.Group(
            _('Condensing Data'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            children=[
                modules.ModelList(
                    _('Logs'),
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.logsifter.logcondensers.models.LogParser',
                        'sifter.logsifter.logcondensers.models.LogCondenser',
                    ),
                ),
                modules.ModelList(
                    _('Email'),
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.mailsifter.mailcondensers.models.MailParser',
                        'sifter.mailsifter.mailcondensers.models.MailCondenser',
                    ),
                ),
                modules.ModelList(
                    _('JSON Data'),
                    css_classes=('grp-collapse grp-closed',),
                    models=(
                        'sifter.datasifter.datacondensers.models.DataParser',
                        'sifter.datasifter.datacondensers.models.DataCondenser',
                    ),
                ),
            ]
        ))

        self.children.append(modules.ModelList(
            _('Enhancing Data'),
            column=1,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'inspections.models.InspectionStep',
                'inspections.models.Inspection',
                'lab.procedures.models.Procedure',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Storing Data'),
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'warehouses.models.Warehouse',
                'warehouses.models.Collection',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Distilling Data'),
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'categories.models.Category',
                'distilleries.models.Distillery',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Investigating Data'),
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'contexts.models.Context',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Tagging Data'),
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'tags.models.DataTagger',
                'articles.models.Article',
                'tags.models.Topic',
                'tags.models.Tag',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Configuring Alerts'),
            column=1,
            css_classes=('grp-collapse grp-closed',),
            models=(
                'monitors.models.Monitor',
                'watchdogs.models.Watchdog',
                'watchdogs.models.Muzzle',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Manage Alerts'),
            column=2,
            collapsible=False,
            models=(
                'alerts.models.Alert',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Manage Mail'),
            column=2,
            collapsible=False,
            models=(
                'django_mailbox.models.Mailbox',
                'django_mailbox.models.Message',
                'django_mailbox.models.MessageAttachment',
            ),
        ))

        self.children.append(modules.ModelList(
            _('People and Permissions'),
            column=2,
            collapsible=False,
            models=(
                'appusers.models.AppUser',
                'django.contrib.auth.models.Group',
            ),
        ))

        self.children.append(modules.ModelList(
            _('Records'),
            column=2,
            collapsible=False,
            models=(
                'responder.dispatches.models.Dispatch',
                'aggregator.invoices.models.Invoice',
                'ambassador.stamps.models.Stamp',
                'aggregator.streams.models.Stream',
            ),
        ))

        self.children.append(modules.Group(
            _('App Configurations'),
            column=2,
            collapsible=True,
            css_classes=('grp-collapse grp-closed',),
            children=[
                modules.ModelList(
                    _('Passports & Visas'),
                    css_classes=('grp-collapse grp-open',),
                    models=(
                        'ambassador.passports.models.Passport',
                        'ambassador.visas.models.Visa',
                    ),
                ),
                modules.ModelList(
                    _('Alert Response'),
                    css_classes=('grp-collapse grp-open',),
                    models=(
                        'responder.actions.models.Action',
                        'responder.couriers.models.Courier',
                        'responder.destinations.models.Destination',
                    ),
                ),
                modules.ModelList(
                    _('Data Collection'),
                    css_classes=('grp-collapse grp-open',),
                    models=(
                        'aggregator.pipes.models.Pipe',
                        'aggregator.plumbers.models.Plumber',
                        'aggregator.reservoirs.models.Reservoir',
                    ),
                ),
                modules.ModelList(
                    _('Data Enhancement'),
                    css_classes=('grp-collapse grp-open',),
                    models=(
                        'lab.procedures.models.Protocol',
                    ),
                ),
                modules.ModelList(
                    _('Notifications'),
                    css_classes=('grp-collapse grp-open',),
                    models=(
                        'constance.*',
                    ),
                ),
            ]
        ))

        # self.children.append(modules.AppList(
        #     _('App Configurations'),
        #     collapsible=True,
        #     column=2,
        #     css_classes=('grp-collapse grp-closed',),
        #     exclude=(
        #         'django.contrib.*',
        #         'alerts.*',
        #         'appusers.*',
        #         'django_mailbox.models.Message*'
        #     ),
        # ))

        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            column=3,
            collapsible=False,
            limit=3,
        ))

        self.children.append(modules.LinkList(
            _('Support'),
            column=3,
            children=[
                {
                    'title': _('Cyphon Documentation'),
                    'url': 'https://cyphon.readthedocs.io/',
                    'external': True,
                },
            ]
        ))

        self.children.append(modules.Feed(
            _('Latest Cyphon News'),
            feed_url='https://www.cyphon.io/blog?format=rss&utm_source=admin',
            column=3,
            limit=3,
        ))
