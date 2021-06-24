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
Defines a |Cargo| class and a |Transport| base class.

Note
----
The |Transport| class is the basis for the |Carrier| and |Faucet|
classes.

"""

# standard library
import logging

# third party
from django.utils.functional import cached_property

# local
from ambassador.exceptions import EmissaryDoesNotExist
from ambassador.stamps.models import Stamp
from cyphon.baseclass import BaseClass
from cyphon.transaction import close_old_connections

LOGGER = logging.getLogger(__name__)


class Cargo(object):
    """
    Holds the result of an API request.

    Attributes
    ----------
    status_code : str, optional
        The HTTP status code received in response to the API request.

    data : dict, optional
        Data of interest recieved in response to the API call.

    notes : str, optional
        Notes about the API response, such as an error message.

    """

    def __init__(self, status_code=None, data=None, notes=None):
        self.status_code = status_code
        self.data = data or []
        self.notes = notes


class Transport(BaseClass):
    """
    Sends a request to an API and processes the result.

    Attributes
    ----------
    endpoint : Endpoint
        The |Endpoint| for the API endpoint where requests will be sent.

    user : AppUser
        The |AppUser| making the API requests to the `endpoint`.

    cargo : `None` or `Cargo`
        The results of the API call. This will be |None| when the
        |Transport| is initialized. It will be a |Cargo| object when the
        response from the API is received.

    record : `None` or `Record`
        A record of the API call. This will be |None| when the
        |Transport| is initialized. It will be a |Record| when the API
        request is made.

    """

    def __init__(self, endpoint, user=None):
        self.endpoint = endpoint
        self.user = user
        self.cargo = None
        self.record = None

    def _get_emissary_type(self):
        """
        Returns the type of Emissary associated with teh Endpoint, such
        as a Courier or Plumber.
        """
        endpoint_model = type(self.endpoint)
        emissary_field = endpoint_model._meta.get_field('emissary')
        return emissary_field.related_model

    @cached_property
    def emissary(self):
        """
        |Emissary|: The |Emissary| that will be used to access the API endpoint.
        """
        emissary_model = self._get_emissary_type()
        emissaries = emissary_model.objects.find_any(self.endpoint, self.user)
        if emissaries:
            return emissaries.order_by('pk').first()
        else:
            user_str = self.user or 'an anonymous user'
            raise EmissaryDoesNotExist('No %s exists to handle the request to '
                                       '%s by %s' % (emissary_model.__name__,
                                                     self.endpoint, user_str))

    @cached_property
    def passport(self):
        """
        The |Passport| that will be used to access the API endpoint.
        """
        return self.emissary.passport

    def _emissary_enabled(self):
        """
        Returns a Boolean indicating whether the Emissary can be used
        for an API request to the Transport's Endpoint.
        """
        if self.emissary:
            return self.emissary.enabled(endpoint=self.endpoint)
        else:
            return False

    def _stamp_passport(self):
        """
        Creates a Stamp associated with the Transport's Endpoint,
        Passport, and AppUser. Saves it to the database and returns the
        saved object.
        """
        return Stamp.objects.create(
            endpoint=self.endpoint,
            passport=self.passport,
            user=self.user
        )

    def get_key(self):
        """Get the consumer/client/developer key used to authenticate requests.

        Returns
        -------
        |str|
            The consumer/client/developer key used to authenticate requests.

        """
        return self.passport.key

    def get_key_cert(self):
        """Get the certificate for authenticating requests.

        Returns
        -------
        |str|
            The certificate used to authenticate requests.

        """
        key_cert = self.passport.file
        key_cert_data = None
        try:
            key_cert.open()
            key_cert_data = key_cert.read()
        finally:
            key_cert.close()
        return key_cert_data

    def get_secret(self):
        """Get the client/consumer secret used to authenticate requests.

        Returns
        -------
        |str|
            The client/consumer secret used to authenticate requests.

        """
        return self.passport.secret

    def get_access_token(self):
        """Get the access token used for OAuth authentication.

        Returns
        -------
        |str|
            The access token used for OAuth authentication.

        """
        return self.passport.access_token

    def get_access_token_secret(self):
        """Get the access token secret used for OAuth authentication.

        Returns
        -------
        |str|
            The access token secret used for OAuth authentication.

        """
        return self.passport.access_token_secret

    def create_record(self, stamp, obj):
        """Create a |Record| of the API call.

        Parameters
        ----------
        stamp : |Stamp|
            A |Stamp| containing details of the API request.

        obj : |object|
            An object related to the API request, such as an |Alert| or
            |dict| of query parameters. The type of object is determined
            in derived classes.

        Note
        ----
        This method needs to be implemented in derived classes.

        """
        raise self.raise_method_not_implemented()

    def ensure_cargo(self):
        """Supply the Transport with Cargo if it has none.

        Returns
        -------
        self

        """
        if self.cargo is None:
            self.cargo = Cargo(
                notes=('An error occurred while fetching data. '
                       'Please contact your Site Administrator.')
            )
        return self

    def process_request(self, obj):
        """Submit a request to the API and return the results.

        Parameters
        ----------
        obj : |object|
            The object used to create the API request, such as an
            |Alert| or |ReservoirQuery|. The type of object is
            determined in derived classes.

        Returns
        -------
        |Cargo|
            The results of the API call packaged as a |Cargo| object.

        Note
        ----
        This method needs to be implemented in derived classes so it can
        be customized for specific APIs.

        """
        raise self.raise_method_not_implemented()

    def prepare(self, obj):
        """Create a |Record| for an the API call prior to issuing the call.

        If the value of the |Transport|'s :attr:`~Transport.record` is
        |None|, creates a |Record| of the API call and updates the
        |Transport|'s :attr:`~Transport.record` with it.

        Parameters
        ----------
        obj : |object|
            The object used to create the API request, such as an
            |Alert| or |ReservoirQuery|. The type of object is
            determined in derived classes.

        Returns
        -------
        |Transport|
            self

        Note
        ----
        This method separates the creation of a |Record| from the
        :meth:`~Transport.start` method which actually calls the API.
        In cases where we wish to call the API within a daemon thread,
        this makes it possible to get a preliminary |Record| of the
        request prior to issuing the API call through a background
        process.

        However, this means care should be taken to always call
        :meth:`~Transport.prepare` just prior to calling
        :meth:`~Transport.start`, to ensure a |Record| of the API
        request is created.

        """
        if self._emissary_enabled():

            # create a Record if one does not already exist
            if self.record is None:
                stamp = self._stamp_passport()
                self.record = self.create_record(stamp=stamp, obj=obj)
        else:
            LOGGER.error('Emissary is not enabled')

        return self

    @close_old_connections
    def start(self, obj):
        """Issue the API call and update the |Transport|'s
        :attr:`~Transport.cargo` with the result.

        Parameters
        ----------
        obj : |object|
            The object used to create the API request, such as an
            |Alert| or |ReservoirQuery|. The type of object is
            determined in derived classes.

        Returns
        -------
        |Transport|
            self

        Warning
        -------
        The :meth:`~Transport.prepare` method should always be called
        prior to calling :meth:`~Transport.start`.

        """
        self.cargo = self.process_request(obj)
        return self

    @close_old_connections
    def stop(self):
        """Update the |Transport|'s :attr:`~Transport.record` with
        information about the API response.

        Returns
        -------
        |Transport|
            self

        Raises
        ------
        :obj:`~AssertionError`
            If either the |Transport|'s :attr:`~Transport.record`
            or :attr:`~Transport.cargo` is |None|.

        Warning
        -------
        The :meth:`~Transport.prepare` and :meth:`~Transport.start`
        methods must be called prior to calling :meth:`~Transport.stop`.

        """
        if self.record is None or self.cargo is None:  # pragma: no cover
            msg = ('The prepare() and start() methods must be called first')
            raise RuntimeError(msg)

        self.record.finalize(self.cargo)
        return self

    def run(self, obj):
        """Issue an API call and update the |Transport|'s
        :attr:`~Transport.record` and :attr:`~Transport.cargo`
        with the result.

        Parameters
        ----------
        obj : |object|
            The object used to create the API request, such as an
            |Alert| or |ReservoirQuery|. The type of object is
            determined in derived classes.

        Returns
        -------
        |Transport|
            self

        Note
        ----
        The :meth:`~Transport.run` method bundles together the
        :meth:`~Transport.prepare`, :meth:`~Transport.start`, and
        :meth:`~Transport.stop` methods. It can be used for convienence
        in cases where there is no need to access the |Transport|'s
        :attr:`~Transport.record` prior to the API call's return.

        """
        self.prepare(obj)
        self.start(obj)
        self.stop()
        return self
