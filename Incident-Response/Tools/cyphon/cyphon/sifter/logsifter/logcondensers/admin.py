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
Defines a ModelAdmin subclasses for LogParsers, LogCondensers, and
LogFittings, and registers them with Django Admin.
"""

# third party
from django.contrib import admin

# local
from parsers.admin import ParserAdmin
from sifter.condensers.admin import (
    FittingInLineAdmin,
    FittingAdmin,
    CondenserAdmin
)
from .models import LogParser, LogCondenser, LogFitting
from .forms import (
    LogFittingInlineForm,
    LogFittingForm,
    LogCondenserForm,
    LogParserForm
)


class LogParserAdmin(ParserAdmin):
    """
    Customizes admin pages for LogParsers.
    """
    model = LogParser
    form = LogParserForm


class LogFittingInLineAdmin(FittingInLineAdmin):
    """
    Customizes admin inline tables for DataFittings.
    """
    model = LogFitting
    form = LogFittingInlineForm


class LogFittingAdmin(FittingAdmin):
    """
    Customizes admin pages for DataFittings.
    """
    form = LogFittingForm


class LogCondenserAdmin(CondenserAdmin):
    """
    Customizes admin pages for DataCondensers.
    """
    inlines = [LogFittingInLineAdmin, ]
    form = LogCondenserForm


admin.site.register(LogParser, LogParserAdmin)
admin.site.register(LogCondenser, LogCondenserAdmin)
admin.site.register(LogFitting, LogFittingAdmin)
