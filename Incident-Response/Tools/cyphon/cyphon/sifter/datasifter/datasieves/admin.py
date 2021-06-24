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
from .models import DataRule, DataSieve, DataSieveNode


class DataRuleAdmin(FieldRuleAdmin):
    """
    Customizes admin inline tables for LogSieveNodes.
    """
    pass


class DataSieveNodeInLineAdmin(SieveNodeInLineAdmin):
    """
    Customizes admin inline tables for DataSieveNodes.
    """
    model = DataSieveNode


class DataSieveAdmin(SieveAdmin):
    """
    Customizes admin pages for DataSieves.
    """
    inlines = [DataSieveNodeInLineAdmin, ]


admin.site.register(DataRule, DataRuleAdmin)
admin.site.register(DataSieve, DataSieveAdmin)
admin.site.register(DataSieveNode, SieveNodeAdmin)

