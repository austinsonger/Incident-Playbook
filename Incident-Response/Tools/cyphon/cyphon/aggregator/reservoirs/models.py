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
Handles settings for which social media platforms are enabled.
Also handles settings for which Pipes (APIs) are used for which purpose
(ad hoc search vs. background stream, etc.).
"""

# third party
from django.db import models

# local
from ambassador.platforms.models import Platform, PlatformManager
from cyphon.choices import SEARCH_TASK_CHOICES


class ReservoirManager(PlatformManager):
    """
    Adds methods to the default model manager.
    """

    def find_pipes(self, task):
        """
        (str) -> set

        Takes a gateway task and returns a set of pipes assigned to that task.
        Only returns pipes from platforms that are enabled.
        """
        enabled_platforms = self.find_enabled()
        pipes = set([])
        for platform in enabled_platforms:
            pipe = platform.get_pipe(task)
            if pipe:
                pipes.add(pipe)
        return pipes


class Reservoir(Platform):
    """
    Determines whether a platform is enabled for use. The platform
    corresponds to a subpackage in the Platforms package. A Reservoir's
    primary key is the name of the subpackage associated with the
    Reservoir (e.g., 'twitter').
    """
    objects = ReservoirManager()

    def get_gateway(self, task):
        """
        Returns the gateway for a given task, or None if the gateway
        doesn't exist.
        """
        try:
            return Gateway.objects.get(reservoir=self, task=task)
        except Gateway.DoesNotExist:
            return None

    def get_pipe(self, task):
        """
        Takes the primary key (name) of a SearchTask and returns the
        Pipe for that task, if one exists. Otherwise, returns None.
        """
        gateway = self.get_gateway(task)
        if gateway and gateway.pipe:
            return gateway.pipe
        else:
            return None


class Gateway(models.Model):
    """
    Specifies the Pipe (API) that is used for a particular task, e.g., ad hoc
    searches, "streaming" background searches, or finding the user id for an
    account. In many cases, the same API may be used for more than one task.
    """
    reservoir = models.ForeignKey(Reservoir)
    task = models.CharField(max_length=20, choices=SEARCH_TASK_CHOICES)
    pipe = models.ForeignKey('pipes.Pipe', null=True, blank=True,
                             limit_choices_to={'reservoir': reservoir})

    class Meta:
        """
        Metadata options.
        """
        unique_together = ('reservoir', 'task')

