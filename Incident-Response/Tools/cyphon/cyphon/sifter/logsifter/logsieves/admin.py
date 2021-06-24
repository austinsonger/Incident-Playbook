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
    RuleAdmin,
    SieveNodeInLineAdmin,
    SieveNodeAdmin,
    SieveAdmin
)
from .forms import LogRuleForm
from .models import LogRule, LogSieve, LogSieveNode


class LogRuleAdmin(RuleAdmin):
    """
    Customizes admin inline tables for LogSieveNodes.
    """
    form = LogRuleForm


class LogSieveNodeInLineAdmin(SieveNodeInLineAdmin):
    """
    Customizes admin inline tables for LogSieveNodes.
    """
    model = LogSieveNode


class LogSieveAdmin(SieveAdmin):
    """
    Customizes admin pages for DataSieves.
    """
    inlines = [LogSieveNodeInLineAdmin, ]


admin.site.register(LogRule, LogRuleAdmin)
admin.site.register(LogSieve, LogSieveAdmin)
admin.site.register(LogSieveNode, SieveNodeAdmin)

