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

# local
from sifter.chutes.models import Chute, ChuteManager
from sifter.mailsifter.mailmungers.models import MailMunger
from sifter.mailsifter.mailsieves.models import MailSieve


class MailChuteManager(ChuteManager):
    """
    Adds methods to the default model manager.
    """

    settings = conf.MAILSIFTER


class MailChute(Chute):
    """

    """
    sieve = models.ForeignKey(
        MailSieve,
        null=True,
        blank=True,
        default=None,
        related_name='chutes',
        related_query_name='chute'
    )
    munger = models.ForeignKey(MailMunger)

    objects = MailChuteManager()
