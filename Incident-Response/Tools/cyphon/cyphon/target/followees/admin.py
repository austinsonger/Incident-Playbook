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
from target.followees.models import Followee, LegalName, Account


class AccountInLineAdmin(admin.TabularInline):
    """
    Inline admin for Accounts.
    """
    model = Account
    classes = ('grp-open', )
    inline_classes = ('grp-open', )


class LegalNameInLineAdmin(admin.StackedInline):
    """
    Inline admin for LegalNames.
    """
    model = LegalName
    classes = ('grp-open', )
    inline_classes = ('grp-open', )
    max_num = 1


class AccountAdmin(admin.ModelAdmin):
    pass


class FolloweeAdmin(admin.ModelAdmin):
    inlines = [LegalNameInLineAdmin, AccountInLineAdmin, ]


class LegalNameAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Followee, FolloweeAdmin)
admin.site.register(LegalName, LegalNameAdmin)
