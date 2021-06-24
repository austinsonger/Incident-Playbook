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

# local
from cyphon.models import GetByNameManager
from sifter.mungers.models import Munger
from sifter.mailsifter.mailcondensers.models import MailCondenser


class MailMunger(Munger):
    """
    Attributes:
        name : str

        distillery : Distillery

        condenser: MailCondenser
            a MailCondenser used to distill the message into the chosen
            Bottle

    """
    condenser = models.ForeignKey(MailCondenser)

    objects = GetByNameManager()

    def _get_company(self):
        """

        """
        return self.distillery.company

    def _process_data(self, data):
        """
        Takes a dictionary of data (e.g., of a social media post) and a
        Condenser. Returns a dictionary that distills the data
        using the crosswalk defined by the Condenser.
        """
        company = self._get_company()
        return self.condenser.process(data=data, company=company)
