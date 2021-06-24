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

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.search, name=views.SEARCH_VIEW_NAME),
    url(r'^alerts/$', views.search_alerts, name=views.ALERT_SEARCH_VIEW_NAME),
    url(r'^distilleries/$', views.search_distilleries,
        name=views.DISTILLERIES_SEARCH_VIEW_NAME),
    url(r'^distilleries/(?P<pk>[0-9]+)/$', views.search_distillery,
        name=views.DISTILLERY_SEARCH_VIEW_NAME),
]
