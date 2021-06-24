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
from functools import wraps

# third party
from django import db
from django.apps import apps


LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)


def require_lock(model_ref, lock_mode):
    """Decorator for PostgreSQL's table-level lock functionality.

    Parameters
    ----------
    model_ref : |Model|, |tuple|, or |list|
        Model or tuple/list of App label and Model name

    lock_mode : str
        The

    Example
    -------
    .. code-block:: python

       @transaction.atomic
       @require_lock(MyModel, 'ACCESS EXCLUSIVE')
       def myview(request):
            ...

    See also
    --------
    PostgreSQL's LOCK Documentation:
    http://www.postgresql.org/docs/8.3/interactive/sql-lock.html

    """
    def _decorator(func):
        @wraps(func)  # preserve name and docstring of wrapped function
        def _call(*args, **kwargs):
            if isinstance(model_ref, (tuple, list)):
                model = apps.get_model(*model_ref)
            else:
                model = model_ref

            if lock_mode not in LOCK_MODES:
                err_msg = '%s is not a PostgreSQL supported lock mode.' \
                          % lock_mode
                raise ValueError(err_msg)

            cursor = db.connection.cursor()
            cursor.execute(
                'LOCK TABLE %s IN %s MODE' % (model._meta.db_table, lock_mode)
            )
            return func(*args, **kwargs)
        return _call
    return _decorator


def close_old_connections(func):
    """

    """
    @wraps(func)  # preserve name and docstring of wrapped function
    def _decorator(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        finally:
            db.close_old_connections()
        return result
    return _decorator


def close_connection(func):
    """

    """
    @wraps(func)  # preserve name and docstring of wrapped function
    def _decorator(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
        finally:
            db.connection.close()
        return result
    return _decorator
