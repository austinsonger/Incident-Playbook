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
from django.conf import settings as conf
from django.db import models
from django.utils.functional import cached_property

# local
from aggregator.pipes.models import Pipe
from cyphon.documents import DocumentObj
from sifter.chutes.models import Chute, ChuteManager
from sifter.datasifter.datasieves.models import DataSieve
from sifter.datasifter.datamungers.models import DataMunger


class DataChuteManager(ChuteManager):
    """
    Adds methods to the default model manager.
    """

    settings = conf.DATASIFTER

    def find_by_endpoint(self, endpoint):
        """
        Returns a QuerySet object containing only enabled Chutes
        for the gievn endpoint.
        """
        enabled_chutes = super(DataChuteManager, self).find_enabled()
        return enabled_chutes.filter(endpoint=endpoint)


class DataChute(Chute):
    """

    """
    sieve = models.ForeignKey(
        DataSieve,
        null=True,
        blank=True,
        default=None,
        related_name='chutes',
        related_query_name='chute'
    )
    munger = models.ForeignKey(DataMunger)
    endpoint = models.ForeignKey(Pipe)

    objects = DataChuteManager()

    @cached_property
    def _platform_name(self):
        """

        """
        return self.endpoint.platform.name

    def bulk_process(self, data):
        """

        """
        for doc in data:
            doc_obj = DocumentObj(data=doc)
            self.process(doc_obj)

    def process(self, doc_obj):
        """
        Overrides the parent method to add platform info to the data.
        """
        doc_obj.platform = self._platform_name
        return super(DataChute, self).process(doc_obj)
