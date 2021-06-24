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
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from cyphon.models import GetByNameManager
from sifter.datasifter.datasieves.models import DataSieve


class Inspection(models.Model):
    """

    Attributes:
        name: a string representing the name of the Inspection
        steps: one or more InspectionSteps associated with the Inspection
    """
    name = models.CharField(max_length=255, unique=True)

    objects = GetByNameManager()

    def __str__(self):
        return self.name

    def get_result(self, data):
        """

        Notes
        -----
        This method should have the same name as the corresponding
        method in a LabProcedure.

        """
        steps = self.steps.all()
        for step in steps:
            if step.is_match(data):
                return step.result_value
        return None


class InspectionStep(models.Model):
    """
    Defines a step in an Inspection.

    Attributes:
        inspection: the Inspection associated with the InspectionStep
        sieve: a DataSieve for examining data
        result_value: a value to be returned if the datasieve returns True for
            the data examined
        rank: an integer representing the order of the step in an Inspection;
            steps are performed in ascending order (the lowest rank first)

    """
    inspection = models.ForeignKey(
        Inspection,
        related_name='steps',
        related_query_name='step',
        verbose_name=_('Inspection'),
        help_text=_('The Inspection in which this step is included.')
    )
    sieve = models.ForeignKey(
        DataSieve,
        related_name='inspection_steps',
        related_query_name='inspection_step',
        help_text=_('The DataSieve used to inspect the data during this step.')
    )
    result_value = models.CharField(
        max_length=255,
        help_text=_('The value to be returned if the DataSieve returns True '
                    'for the data examined.')
    )
    rank = models.IntegerField(
        default=0,
        help_text=_('An integer representing the order of this step in the '
                    'Inspection. Steps are performed in ascending order, '
                    'with the lowest number examined first.')
    )

    objects = GetByNameManager()

    class Meta(object):
        """Metadata options."""

        ordering = ['rank']
        unique_together = [('inspection', 'sieve'), ('inspection', 'rank')]

    def __str__(self):
        return '%s <- %s (rank: %s)' % (self.sieve, self.result_value, self.rank)

    def is_match(self, data):
        return self.sieve.is_match(data)
