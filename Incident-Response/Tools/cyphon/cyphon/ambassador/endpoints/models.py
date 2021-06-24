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
Defines the |Endpoint| base class. An |Endpoint| represents an API
endpoint. It stores information about the API handler used to submit
requests to the endpoint.

Note
----
The |Endpoint| class is the basis for the |Action| and |Pipe| classes.

"""

# standard library
import importlib
import logging

# third party
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

# local
from platforms.registry import PLATFORMS_PACKAGE, HANDLERS_MODULE
from utils.validators.validators import IDENTIFIER_VALIDATOR

LOGGER = logging.getLogger(__name__)


class EndpointManager(models.Manager):
    """
    Adds methods to the default model manager.
    """

    def get_by_natural_key(self, platform, api_class):
        """Allow retrieval of an |Endpoint| by its natural key.

        Parameters
        ----------
        platform : str
            The primary key of the |Platform| associated with the
            |Endpoint|.

        api_class : str
            The |Endpoint|'s :attr:`~ambassador.endpoints.models.Endpoint.api_class`.

        Returns
        -------
        |Endpoint|
            The |Endpoint| associated with the `platform` and `api_class`.

        """
        try:
            return self.get(platform__name=platform, api_class=api_class)
        except ObjectDoesNotExist:
            LOGGER.error('%s for "%s %s" does not exist',
                         self.model.__name__, platform, api_class)

    def get_id_from_natural_key(self, natural_key):
        """Get an |Endpoint|'s primary key.

        Parameters
        ----------
        natural_key : |list| of |str|
            A |list| containing the primary key of the |Platform|
            associated with the |Endpoint| and the |Endpoint|'s
            :attr:`~ambassador.endpoints.models.Endpoint.api_class`..

        Returns
        -------
        int
            The |Endpoint|'s primary key.

        """
        handler = self.get_by_natural_key(*natural_key)
        return handler.pk


class Endpoint(models.Model):
    """
    Specifies the module and |Transport| class that should be used to
    access an API endpoint of a |Platform|, such as Twitter or JIRA.
    An |Endpoint| can create a |Transport| object instance for handling
    a request to the endpoint.

    Since a |Platform| may be accessed through more than one API (e.g.,
    Twitter Search API vs. Twitter Public API), |Endpoints| have a
    many-to-one relationship with |Platforms|.

    Attributes
    ----------
    api_module : str
        The name of the module that will handle the API request
        (i.e., the name of the Python file without the extension,
        e.g., 'handlers').

    api_class : str
        The name of the class that will handle the API request
        (e.g., 'SearchAPI').

    visa_required : bool
        Whether requests to the API endpoint are rate limited.
        If |True|, an |Emissary| must have a |Visa| to access the
        |Endpoint|. The |Visa| defines the rate limit that should
        apply to the |Emissary|'s |Passport| (API key).

    Note
    ----
    The `platform` attribute is defined in |Endpoint| subclasses,
    such as the |Action| and |Pipe| classes.

    """
    api_module = models.CharField(
        max_length=32,
        validators=[IDENTIFIER_VALIDATOR],
        default=HANDLERS_MODULE,
        help_text=_('The module that will handle the API request.')
    )
    api_class = models.CharField(
        max_length=32,
        validators=[IDENTIFIER_VALIDATOR],
        help_text=_('The class that will handle the API request.')
    )
    visa_required = models.BooleanField(
        default=False,
        help_text=_('Whether API calls are restricted by a Visa.')
    )

    class Meta:
        abstract = True

    def __str__(self):
        api = self.api_class
        platform = str(self.platform).title()
        return '%s %s' % (platform, api)

    def _get_module(self):
        """
        Returns the module for handling the API.
        """
        # e.g., 'platforms.twitter.handler'
        module_full_name = '%s.%s.%s' % (PLATFORMS_PACKAGE,
                                         self.platform.name,
                                         self.api_module)

        # load the module (will raise ImportError if module cannot be loaded)
        module = importlib.import_module(module_full_name)

        return module

    def create_request_handler(self, user, params=None):
        """Create a handler to send a request to an API enpoint.

        Returns
        -------
        |Transport|
            A |Transport| subclass that will send the request to the API
            endpoint and process the result.

        """
        class_name = self.api_class
        module = self._get_module()

        # get the API class (will raise AttributeError if class cannot be found)
        api = getattr(module, class_name)

        # create an instance of the class
        params = params or {}
        request_handler = api(endpoint=self, user=user, **params)

        return request_handler
