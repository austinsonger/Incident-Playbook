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
Defines views for |Distilleries| using the Django REST framework.

==============================  ===========================================
Class                           Description
==============================  ===========================================
:class:`~ArticlePagination`     Pagination for |Article| views.
:class:`~ArticleViewSet`        `ReadOnlyModelViewSet`_ for |Article|.
==============================  ===========================================

"""

# third party
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

# local
from .models import Article
from .serializers import ArticleDetailSerializer, ArticleListSerializer


class ArticlePagination(PageNumberPagination):
    """Pagination for |Article| views.

    Paginates |Articles| using Django REST framework's
    `PageNumberPagination`_.
    """

    page_size = 50


class ArticleViewSet(viewsets.ModelViewSet):
    """REST API views for Articles."""

    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    pagination_class = ArticlePagination

    def get_serializer_class(self):
        """
        Overrides the default method for returning the ViewSet's
        serializer.
        """
        if self.serializer_class is None:  # pragma: no cover
            msg = ("'%s' should either include a `serializer_class` attribute,"
                   " or override the `get_serializer_class()` method."
                   % type(self).__name__)
            raise RuntimeError(msg)

        if self.action == 'list':
            return ArticleListSerializer
        else:
            return self.serializer_class
