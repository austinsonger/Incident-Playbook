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
Tests for the locking database tables.
"""

# standard library
from unittest import TestCase
try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

# third party
from django.db import transaction
import six

# local
from cyphon.transaction import require_lock
from alerts.models import Alert


class RequireLockTest(TestCase):
    """
    Tests the require_lock wrapper.
    """
    model = Alert

    def test_access_lock(self):
        """
        Tests the require_lock wrapper for a valid lock mode.
        """
        lock = 'ACCESS EXCLUSIVE'

        @transaction.atomic
        @require_lock(self.model, lock)
        def dummy_func():
            """A dummy function to test the wrapper."""
            pass

        command = 'LOCK TABLE %s IN %s MODE' % (self.model._meta.db_table, lock)

        mock_cursor = MagicMock()

        with patch('cyphon.transaction.db.connection.cursor',
                   return_value=mock_cursor):
            dummy_func()
            mock_cursor.execute.assert_called_once_with(command)


    def test_bad_mode(self):
        """
        Tests the require_lock wrapper for an invalid lock mode.
        """
        lock = 'BAD MODE'

        @transaction.atomic
        @require_lock(self.model, lock)
        def dummy_func():
            """A dummy function to test the wrapper."""
            pass

        msg = '%s is not a PostgreSQL supported lock mode.' % lock
        with six.assertRaisesRegex(self, ValueError, msg):
            dummy_func()

