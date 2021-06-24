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
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView, TemplateView
from rest_framework.routers import DefaultRouter
import rest_framework_jwt.views as rest_views
# from rest_framework_docs.views import DRFDocsView

# local
from alerts.views import AlertViewSet, AnalysisViewSet, CommentViewSet
from appusers.views import AppUserViewSet
from articles.views import ArticleViewSet
from categories.views import CategoryViewSet
from contexts.views import ContextViewSet, ContextFilterViewSet
from cyclops.views import application, manifest
from bottler.bottles.views import BottleViewSet, BottleFieldViewSet
from bottler.containers.views import ContainerViewSet
from bottler.labels.views import LabelFieldViewSet, LabelViewSet
from bottler.tastes.views import TasteViewSet
from distilleries.views import DistilleryViewSet
from monitors.views import MonitorViewSet
from query.collectionqueries.views import (
    CollectionQueryViewSet,
    QueryFieldsetViewSet,
)
from responder.actions.views import ActionViewSet
from responder.destinations.views import DestinationViewSet
from responder.dispatches.views import DispatchViewSet
from tags.views import TagViewSet, TopicViewSet
from warehouses.views import WarehouseViewSet, CollectionViewSet


urlpatterns = [
    # url(r'^$', 'dashboard.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

# CYCLOPS
if settings.CYCLOPS['ENABLED']:
    urlpatterns += [
        url(
            r'^login/$',
            auth_views.login,
            {'template_name': 'cyclops/login.html'},
            name='login'
        ),
        url(
            r'^logout/',
            auth_views.logout,
            {'next_page': 'login'},
            name='logout'
        ),
        url(r'^manifest.json$', manifest, name='manifest.json'),
        url(r'^sw.js$', TemplateView.as_view(
            template_name="cyclops/sw.js",
            content_type='application/javascript',
        ), name='service_worker'),
        url(r'^app/', application, name='cyclops'),
        url(r'^$', RedirectView.as_view(url='app/')),
    ]
else:
    urlpatterns += [url(r'^$', RedirectView.as_view(url='admin/'))]

# REST API
router = DefaultRouter()

router.register(r'actions', ActionViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'analyses', AnalysisViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'bottles', BottleViewSet)
router.register(r'bottlefields', BottleFieldViewSet)
router.register(r'collectionqueries', CollectionQueryViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'containers', ContainerViewSet)
router.register(r'contexts', ContextViewSet)
router.register(r'contextfilters', ContextFilterViewSet)
router.register(r'destinations', DestinationViewSet)
router.register(r'distilleries', DistilleryViewSet)
router.register(r'dispatches', DispatchViewSet)
router.register(r'queryfieldsets', QueryFieldsetViewSet)
router.register(r'labels', LabelViewSet)
router.register(r'labelfields', LabelFieldViewSet)
router.register(r'monitors', MonitorViewSet)
router.register(r'tags', TagViewSet)
router.register(r'tastes', TasteViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'users', AppUserViewSet)
router.register(r'warehouses', WarehouseViewSet)

# The API URLs are determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns += [
    url(r'^admin/password_reset/$', auth_views.password_reset,
        name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),

    # REST API documenation
    url(r'^docs/', include('rest_framework_docs.urls')),
    # url(r'^docs/', DRFDocsView.as_view(drf_router=router), name='drfdocs'),
    # TODO(LH): use DRFDocsView once DRF Docs does next release

    # REST API
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/search/', include('query.search.urls')),
    url(r'^api/v1/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/notifications/', include('notifications.urls')),
    url(r'^api/v1/api-token-auth/', rest_views.obtain_jwt_token),
    url(r'^api/v1/api-token-verify/', rest_views.verify_jwt_token),
    url(r'^api/v1/api-token-refresh/', rest_views.refresh_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Cyphon'
