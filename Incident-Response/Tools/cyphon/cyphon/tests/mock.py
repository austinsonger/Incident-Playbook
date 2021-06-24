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
Provides decorators for frequently used patches.

"""

# standard library
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

DEFAULT = object()


def _get_return_value(data):
    """
    Takes a dict, None, or DEFAULT object. If `data` is the DEFAULT
    object, returns a default dictionary. Otherwise, simply returns
    the value of the `data` parameter.
    """
    if data is DEFAULT:
        return {'subject': 'test'}
    else:
        return data


def patch_find_by_id(data=DEFAULT):
    """
    Mocks the :meth:`~distilleries.models.Distillery.find_by_id`
    method of a |Distillery|.

    Attributes
    ----------
    data: dict, None, or DEFAULT object
        The data that should be returned by the mocked method.

    Returns
    -------
    |dict| or |None|

    """

    def _decorator(func):
        def _call(*args, **kwargs):
            doc = _get_return_value(data)
            with patch('distilleries.models.Distillery.find_by_id',
                       return_value=doc):
                return func(*args, **kwargs)
        return _call
    return _decorator


def patch_find(data=DEFAULT):
    """
    Mocks the :meth:`~distilleries.models.Distillery.find`
    method of a |Distillery|.

    Attributes
    ----------
    data: dict, None, or DEFAULT object
        The data that should be returned by the mocked method.

    Returns
    -------
    |dict| or |None|

    """
    def _decorator(func):
        def _call(*args, **kwargs):
            doc = _get_return_value(data)
            with patch('distilleries.models.Distillery.find',
                       return_value=doc):
                return func(*args, **kwargs)
        return _call
    return _decorator
