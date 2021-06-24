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
from django.contrib import admin

# local
from sifter.sieves.admin import (
    FieldRuleAdmin,
    SieveNodeInLineAdmin,
    SieveNodeAdmin,
    SieveAdmin
)
from . import models


class MailRuleAdmin(FieldRuleAdmin):
    """
    Customizes admin inline tables for MailSieveNodes.
    """
    pass


class MailSieveNodeInLineAdmin(SieveNodeInLineAdmin):
    """
    Customizes admin inline tables for MailSieveNodes.
    """
    model = models.MailSieveNode


class MailSieveAdmin(SieveAdmin):
    """
    Customizes admin pages for MailSieves.
    """
    inlines = [MailSieveNodeInLineAdmin, ]


admin.site.register(models.MailRule, MailRuleAdmin)
admin.site.register(models.MailSieve, MailSieveAdmin)
admin.site.register(models.MailSieveNode, SieveNodeAdmin)
