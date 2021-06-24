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

# standard library
import importlib

# third party
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    """

    """
    custom_filter_backends = []

    def __init__(self, *args, **kawrgs):
        super(CustomModelViewSet, self).__init__(*args, **kawrgs)
        custom_backends = self._get_custom_backends()
        default_backends = super(CustomModelViewSet, self).filter_backends
        self.filter_backends = list(default_backends) + custom_backends

    def _get_custom_backends(self):
        """

        """
        backends = []
        for class_ref in self.custom_filter_backends:
            backend = self._get_class_from_string(class_ref)
            backends.append(backend)
        return backends

    @staticmethod
    def _get_class_from_string(class_ref):
        """

        """
        try:
            module_name, class_name = class_ref.rsplit('.', 1)
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as error:
            msg = "Could not import '%s'. %s: %s." % \
                  (class_ref, error.__class__.__name__, error)
            raise ImportError(msg)

    def _is_write_request(self):
        """
        Checks to see if the request is protected per user.
        """
        write_requests = ['PATCH', 'PUT', 'DELETE']
        return self.request.method in write_requests
