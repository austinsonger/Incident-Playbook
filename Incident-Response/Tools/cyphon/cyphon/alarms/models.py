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
Defines an Alarm base class.
"""

# third party
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from alerts.models import Alert
from cyphon.baseclass import BaseClass
from cyphon.models import GetByNameManager, FindEnabledMixin
from cyphon.transaction import close_old_connections


class AlarmManager(GetByNameManager, FindEnabledMixin, BaseClass):
    """
    Adds methods to the default model manager.
    """

    def find_relevant(self, distillery):
        """Find appropriate Alarms to inspect a document.

        This method should be overridden in derived classes.

        Parameters
        ----------
        doc_obj : |Distillery|
            The |Distillery| associated with the document.

        Raises
        ------
        NotImplementedError

        """
        self.raise_method_not_implemented()

    @close_old_connections
    def process(self, doc_obj):
        """Inspect a document with Alarms.

        Parameters
        ----------
        doc_obj : |DocumentObj|
            The document that Alarms should inspect.

        Returns
        -------
        None

        """
        alarms = self.find_relevant(doc_obj.distillery)
        for alarm in alarms:
            alarm.process(doc_obj)


class Alarm(models.Model, BaseClass):
    """
    Defines a class for inspecting data produced by a Distillery. Used
    to create Alerts when appropriate.

    Attributes
    ----------
    name : str
        A |str| representing the name of the Watchdog.

    enabled : bool
        A |bool| indicating whether the Watchdog is active.

    groups : `QuerySet` of `Groups`
        |Groups| to which the generated Alerts should be visible.

    """
    name = models.CharField(max_length=255, unique=True)
    enabled = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_('Only show Alerts to Users in these Groups. '
                    'If no Groups are selected, Alerts will be visible '
                    'to all Groups.')
    )
    alerts = GenericRelation(
        Alert,
        content_type_field='alarm_type',
        object_id_field='alarm_id',
        related_query_name='%(class)s'
    )

    class Meta(object):
        """Metadata options."""

        abstract = True
        ordering = ['name']

    def process(self, doc_obj):
        """Inspect a document and generate an Alert if appropriate.

        This method should be overridden in derived classes.

        Parameters
        ----------
        doc_obj : |DocumentObj|
            The document that Alarms should inspect.

        Raises
        ------
        NotImplementedError

        """
        self.raise_method_not_implemented()
