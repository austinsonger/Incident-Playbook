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
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.test import TestCase

# local
import platforms.jira.handlers as jira_module
from responder.actions.models import Action
from tests.fixture_manager import get_fixtures


class ActionsBaseTestCase(TestCase):
    """
    Base class for testing Actions.
    """

    fixtures = get_fixtures(['actions', 'dispatches'])

    def setUp(self):
        self.action = Action.objects.get(pk=1)


class ActionTestCase(ActionsBaseTestCase):
    """
    Tests the Action class.
    """

    def test_str(self):
        """
        Tests the string representation of a Pipe.
        """
        self.assertEqual(str(self.action), 'Jira IssueAPI')

    def test_get_module(self):
        """
        Tests the _get_module method for getting the module for an
        Action's Destination.
        """
        self.assertEqual(self.action._get_module(), jira_module)

    def test_create_request_handler(self):
        """
        Tests the create_request_handler method for getting a request
        handler for an Action.
        """
        mock_user = Mock()
        mock_handler = Mock()
        with patch('platforms.jira.handlers.IssueAPI',
                   return_value=mock_handler) as mock_api:
            kwargs = {
                'user': mock_user,
            }
            result = self.action.create_request_handler(**kwargs)
            mock_api.assert_called_once_with(endpoint=self.action,
                                             user=mock_user)
            self.assertEqual(result, mock_handler)

    def test_save_w_no_descr(self):
        """
        Test the save method of an Action with the Action has no
        description.
        """
        self.assertEqual(self.action.description, None)
        self.action.save()
        self.assertEqual(self.action.description, 'Jira IssueAPI')

    def test_save_w_descr(self):
        """
        Test the save method of an Action with the Action has a
        description.
        """
        self.action.description = 'Create a JIRA Issue'
        self.action.save()
        self.assertEqual(self.action.description, 'Create a JIRA Issue')

    def test_get_dispatch(self):
        """
        Test the get_dispatch method of an Action.
        """
        mock_alert = Mock()
        mock_user = Mock()
        mock_record = Mock()
        mock_handler = Mock()

        mock_handler.run = Mock(return_value=mock_record)
        mock_handler.record = mock_record

        with patch('platforms.jira.handlers.IssueAPI',
                   return_value=mock_handler) as mock_api:
            kwargs = {
                'alert': mock_alert,
                'user': mock_user,
            }
            result = self.action.get_dispatch(**kwargs)
            mock_api.assert_called_once_with(endpoint=self.action,
                                             user=mock_user)
            mock_handler.run.assert_called_once_with(mock_alert)
            self.assertEqual(result, mock_record)
