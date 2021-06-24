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

# third party
from django.utils.deprecation import MiddlewareMixin

VERSION = '1.6.3'
"""str

Current Cyphon version.
"""


class VersionMiddleware(MiddlewareMixin):
    """Middleware that adds version information to response headers."""

    VERSION_HEADER = 'Cyphon-Version'
    """|str|

    Name of the header that contains the Cyphon version number.
    """

    def process_response(self, request, response):
        """Add the current Cyphon version to an HTTP response header.

        Parameters
        ----------
        request : :class:`~django.core.handlers.wsgi.WSGIRequest`

        response : :class:`~django.template.response.TemplateResponse`

        Returns
        -------
        response : :class:`~django.template.response.TemplateResponse`
            The reponse containing the Cyphon version header.

        """
        response[self.VERSION_HEADER] = VERSION

        return response

    def process_request(self, request):
        """Set the Cyphon version in a WSGIRequest.

        Parameters
        ----------
        request : :class:`~django.core.handlers.wsgi.WSGIRequest`

        Returns
        -------
        None

        """
        request.cyphon_version = VERSION
