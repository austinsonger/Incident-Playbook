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
Tests the JiraHandler and IssueAPI classes.
"""

# standard library
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch

# third party
from django.contrib.auth import get_user_model
from django.test import TestCase
from jira.exceptions import JIRAError

# local
from tests.fixture_manager import get_fixtures
from alerts.models import Alert
from platforms.jira.handlers import JiraHandler, IssueAPI
from responder.actions.models import Action

USER_MODEL = get_user_model()


class JiraBaseTestCase(TestCase):
    """
    Base class for testing the JIRA handler classes.
    """

    def setUp(self):
        self.endpoint = Action.objects.get(pk=1)
        self.user = USER_MODEL.objects.get(pk=2)
        self.mock_data = {
            'host': 'foo',
            'message': 'bar',
        }
        self.mock_cert = 'mock_cert'
        self.mock_jira_user_1 = Mock()
        self.mock_jira_user_2 = Mock()
        self.mock_jira_user_1.name = 'Bob'
        self.mock_issue = Mock()
        self.mock_issue.raw = {
            'key': 'FOO-5',
            'id': 11,
            'fields': {
                'created': 'now'
            },
            'self': 'https://jira.example.com/11'
        }
        self.mock_auth = Mock()
        self.mock_auth.search_users = Mock(return_value=[self.mock_jira_user_1])
        self.mock_auth.create_issue = Mock(return_value=self.mock_issue)
        self.mock_settings = {
            'SERVER': 'https://jira.example.com',
            'PROJECT_KEY': 'SOC',
            'ISSUE_TYPE': 'Incident',
            'CUSTOM_FIELDS': {
                'customfield_10200': {'value': 'Unknown'},
                'customfield_10201': {'value': 'Unassigned'},
            },
            'PRIORITIES': {
                'CRITICAL': 'Critical',
                'HIGH': 'High',
                'MEDIUM': 'Medium',
                'LOW': 'Low',
                'INFO': 'Low'
            },
            'DEFAULT_PRIORITY': 'Medium',
            'STYLE_PARAMS': {
                'title': 'Test Alert',
                'titleBGColor': '#dcdcdc',
                'bgColor': '#f5f5f5',
            },
            'INCLUDE_FULL_DESCRIPTION': True,
            'INCLUDE_EMPTY_FIELDS': True,
            'INCLUDE_ALERT_COMMENTS': True,
            'INCLUDE_ALERT_LINK': True,
            'COMMENT_VISIBILITY': {'type': 'role', 'value': 'Service Desk Team'},
        }

class JiraHandlerTestCase(JiraBaseTestCase):
    """
    Base class for testing the JiraHandler class.
    """
    fixtures = get_fixtures(['couriers'])

    def test_authenticate(self):
        """
        Tests that the __init__ method creates an authenticated JIRA
        client using the appropriate credentials.
        """
        oauth_dict = {
            'access_token': 'exampleaccesstoken2',
            'access_token_secret': 'exampleaccesstokensecret2',
            'consumer_key': 'examplekey2',
            'key_cert': self.mock_cert
        }
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth) as mock_jira:
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    jira_handler = JiraHandler(endpoint=self.endpoint,
                                               user=self.user)
                    actual = jira_handler.authed_jira
                    expected = self.mock_auth
                    mock_jira.assert_called_once_with(
                        server=self.mock_settings['SERVER'],
                        oauth=oauth_dict
                    )
                    self.assertEqual(actual, expected)


class IssueAPITestCase(JiraBaseTestCase):
    """
    Base class for testing the IssueAPI class.
    """
    fixtures = get_fixtures(['couriers', 'alerts', 'comments'])

    def setUp(self):
        super(IssueAPITestCase, self).setUp()

        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    self.handler_w_user = IssueAPI(endpoint=self.endpoint,
                                                   user=self.user)
                    self.handler_wo_user = IssueAPI(endpoint=self.endpoint)

    def test_get_jira_user_w_user(self):
        """
        Tests the _get_jira_user method when JIRA returns one and only
        one matching user.
        """
        actual = self.handler_w_user._get_jira_user()
        expected = self.mock_jira_user_1
        self.assertEqual(actual, expected)

    def test_get_jira_user_multi(self):
        """
        Tests the _get_jira_user method when JIRA returns more than one
        matching user.
        """
        self.mock_auth.search_users = Mock(return_value=[self.mock_jira_user_1,
                                                         self.mock_jira_user_2])
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    handler_w_user = IssueAPI(endpoint=self.endpoint,
                                              user=self.user)
                    actual = handler_w_user._get_jira_user()
                    expected = None
                    self.assertEqual(actual, expected)

    def test_get_jira_user_wo_user(self):
        """
        Tests the _get_jira_user method when the APIhanlder has no user.
        """
        actual = self.handler_wo_user._get_jira_user()
        expected = None
        self.assertEqual(actual, expected)

    def test_format_code_block(self):
        """
        Tests the _format_code_block method.
        """
        text = 'Test text.'
        actual = self.handler_wo_user._format_code_block(text)
        expected = """\
{code:bgColor=#f5f5f5|title=Cyphon Alert|titleBGColor=#dcdcdc}
Test text.
{code}"""
        self.assertEqual(actual, expected)

    def test_format_full_description(self):
        """
        Tests the _format_description method when a full description
        is used and empty fields are included.
        """
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    handler_w_user = IssueAPI(endpoint=self.endpoint,
                                              user=self.user)
                    alert = Alert.objects.get(pk=2)
                    alert.data = self.mock_data
                    actual = handler_w_user._format_description(alert)
                    expected = """\
{code:bgColor=#f5f5f5|title=Test Alert|titleBGColor=#dcdcdc}
Alert ID:     2
Title:        Threat Alert
Level:        HIGH
Incidents:    1
Created date: 2015-03-01 02:41:24.468404+00:00

Collection:   mongodb.test_database.test_posts
Document ID:  2
Source Data:  
{
    "host": "foo",
    "message": "bar"
}

Notes:        
None

-----

John Smith commented at 2015-03-01 02:43:24.468404+00:00:
This alert isn't this important
{code}"""
                    self.assertEqual(actual, expected)

    def test_format_descr_w_exclude(self):
        """
        Tests the _format_description method when a full description
        is used and empty fields are excluded.
        """
        self.mock_settings['INCLUDE_EMPTY_FIELDS'] = False
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    handler_w_user = IssueAPI(endpoint=self.endpoint,
                                              user=self.user)
                    alert = Alert.objects.get(pk=2)
                    alert.data = self.mock_data
                    actual = handler_w_user._format_description(alert)
                    expected = """\
{code:bgColor=#f5f5f5|title=Test Alert|titleBGColor=#dcdcdc}
Alert ID:     2
Title:        Threat Alert
Level:        HIGH
Incidents:    1
Created date: 2015-03-01 02:41:24.468404+00:00

Collection:   mongodb.test_database.test_posts
Document ID:  2
Source Data:  
{
    "host": "foo",
    "message": "bar"
}

-----

John Smith commented at 2015-03-01 02:43:24.468404+00:00:
This alert isn't this important
{code}"""
        self.assertEqual(actual, expected)

    def test_format_descr_w_notes(self):
        """
        Tests the _format_description method when the alert has notes.
        """
        self.mock_settings['INCLUDE_FULL_DESCRIPTION'] = False
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    handler_w_user = IssueAPI(endpoint=self.endpoint,
                                              user=self.user)
                    alert = Alert.objects.get(pk=3)
                    actual = handler_w_user._format_description(alert)
                    expected = 'Some example notes.'
        self.assertEqual(actual, expected)

    def test_format_descr_wo_notes(self):
        """
        Tests the _format_description method when the alert has no notes.
        """
        self.mock_settings['INCLUDE_FULL_DESCRIPTION'] = False
        with patch('ambassador.transport.Transport.get_key_cert',
                   return_value=self.mock_cert):
            with patch('platforms.jira.handlers.jira.JIRA',
                       return_value=self.mock_auth):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    handler_w_user = IssueAPI(endpoint=self.endpoint,
                                              user=self.user)
                    alert = Alert.objects.get(pk=2)
                    actual = handler_w_user._format_description(alert)
                    expected = ''
        self.assertEqual(actual, expected)

    def test_get_priority_name(self):
        """
        Tests the _get_priority_name method.
        """
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            alert = Alert.objects.get(pk=2)
            actual = self.handler_w_user._get_priority_name(alert)
            expected = 'High'
            self.assertEqual(actual, expected)

    def test_get_priority_name_default(self):
        """
        Tests the _get_priority_name method when the alert.level is not
        in the JIRA settings.
        """
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            alert = Alert.objects.get(pk=2)
            alert.level = 'FOOBAR'
            actual = self.handler_w_user._get_priority_name(alert)
            expected = 'Medium'
            self.assertEqual(actual, expected)

    def test_format_issue(self):
        """
        Tests the _format_issue method.
        """
        mock_descr = 'foobar'
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            with patch('platforms.jira.handlers.IssueAPI._format_description',
                       return_value=mock_descr):
                with patch.dict('platforms.jira.handlers.settings.JIRA',
                                self.mock_settings):
                    alert = Alert.objects.get(pk=2)
                    alert.title = 'Threat\nAlert\n'  # check newlines are removed
                    actual = self.handler_w_user._format_issue(alert)
                    expected = {
                        'customfield_10200': {
                            'value': 'Unknown'
                        },
                        'customfield_10201': {
                            'value': 'Unassigned'
                        },
                        'description': mock_descr,
                        'issuetype': {
                            'name': 'Incident'
                        },
                        'priority': {
                            'name': 'High'
                        },
                        'project': {
                            'key': 'SOC'
                        },
                        'reporter': {
                            'name': 'Bob'
                        },
                        'summary': 'Threat Alert'
                    }

                    self.assertEqual(actual, expected)

    def test_format_results(self):
        """
        Tests the _format_results method.
        """
        actual = self.handler_w_user._format_results(self.mock_issue)
        expected = {
            'key': 'FOO-5',
            'issue_id': 11,
            'created': 'now',
            'url': 'https://jira.example.com/browse/FOO-5',
        }
        self.assertEqual(actual, expected)

    def test_create_issue(self):
        """
        Tests the _create_issue method.
        """
        mock_dict = {}
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            with patch('platforms.jira.handlers.IssueAPI._format_issue',
                       return_value=mock_dict) as mock_format:
                alert = Alert.objects.get(pk=2)
                actual = self.handler_w_user._create_issue(alert)
                expected = self.mock_issue
                self.assertEqual(actual, expected)
                mock_format.assert_called_once_with(alert)
                self.mock_auth.create_issue.assert_called_once_with(fields=mock_dict)

    def test_process_request(self):
        """
        Tests the process_request method for a successful request.
        """
        mock_dict = {}
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            with patch('platforms.jira.handlers.IssueAPI._format_issue',
                       return_value=mock_dict) as mock_format:
                alert = Alert.objects.get(pk=2)
                cargo = self.handler_w_user.process_request(alert)
                expected_data = {
                    'key': 'FOO-5',
                    'issue_id': 11,
                    'created': 'now',
                    'url': 'https://jira.example.com/browse/FOO-5',
                }
                mock_format.assert_called_once_with(alert)
                self.assertEqual(cargo.status_code, '200')
                self.assertEqual(cargo.data, expected_data)
                self.assertEqual(cargo.notes, None)

    def test_process_request_w_error(self):
        """
        Tests the process_request method when a JIRA error is thrown.
        """
        error_text = 'an error occurred'
        status_code = 400
        jira_error = JIRAError(status_code=status_code, text=error_text)
        self.mock_auth.create_issue = Mock(side_effect=jira_error)
        with patch('distilleries.models.Distillery.find_by_id',
                   return_value=self.mock_data):
            alert = Alert.objects.get(pk=2)
            cargo = self.handler_w_user.process_request(alert)
            self.assertEqual(cargo.status_code, str(status_code))
            self.assertEqual(cargo.data, [])
            self.assertEqual(cargo.notes, error_text)

