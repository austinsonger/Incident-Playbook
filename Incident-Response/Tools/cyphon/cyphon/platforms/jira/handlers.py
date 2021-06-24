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
Defines classes for JIRA actions.
"""

# standard library
import urllib

# third party
from django.conf import settings
import jira

# local
from ambassador.transport import Cargo
from responder.carrier import Carrier

_JIRA_SETTINGS = settings.JIRA


class JiraHandler(Carrier):
    """
    Base class for interacting with JIRA APIs.
    """

    def __init__(self, *args, **kwargs):
        super(JiraHandler, self).__init__(*args, **kwargs)
        self.server = _JIRA_SETTINGS['SERVER']
        self.authed_jira = self._authenticate()

    def _get_oauth_dict(self):
        """
        Returns a dictionary of credentials for JIRA authentication.
        """
        consumer_key = self.get_key()
        key_cert_data = self.get_key_cert()
        access_token = self.get_access_token()
        access_token_secret = self.get_access_token_secret()

        return {
            'access_token': access_token,
            'access_token_secret': access_token_secret,
            'consumer_key': consumer_key,
            'key_cert': key_cert_data
        }

    def _authenticate(self):
        """
        Method for authenticating with a Twitter API.
        """
        oauth_dict = self._get_oauth_dict()
        return jira.JIRA(server=self.server, oauth=oauth_dict)


class IssueAPI(JiraHandler):
    """
    Class for accessing the JIRA Isssue API.
    """

    def __init__(self, *args, **kwargs):
        super(IssueAPI, self).__init__(*args, **kwargs)
        self._issue_type = _JIRA_SETTINGS['ISSUE_TYPE']
        self._project_key = _JIRA_SETTINGS['PROJECT_KEY']
        self._custom_fields = _JIRA_SETTINGS['CUSTOM_FIELDS']
        self._jira_user = self._get_jira_user()

    def _get_jira_user(self):
        """
        Attempts to return a JIRA user Resource associated with the
        current user. Returns None if unsuccessful.
        """
        if self.user is not None:
            users = self.authed_jira.search_users(self.user.email)
            if len(users) == 1:
                return users[0]

    @staticmethod
    def _format_code_block(text):
        """
        Takes a string and returns it with a styled code block that can
        be read by JIRA. Style rules are defined by the STYLE_PARAMS
        setting of Cyphon's JIRA configuration.
        """
        param_dict = _JIRA_SETTINGS['STYLE_PARAMS']
        sorted_params = sorted(param_dict.items())  # makes testing easier
        param_list = ['='.join([key, val]) for (key, val) in sorted_params]
        param_str = '|'.join(param_list)
        return '\n'.join(['{code:' + param_str + '}', text, '{code' + '}'])

    def _format_full_descr(self, alert):
        """
        Takes an Alert and formats it for the description field of a
        JIRA issue.
        """
        include_empty = _JIRA_SETTINGS['INCLUDE_EMPTY_FIELDS']
        include_comments = _JIRA_SETTINGS['INCLUDE_ALERT_COMMENTS']
        summary = alert.summary(include_empty=include_empty,
                                include_comments=include_comments)
        return self._format_code_block(summary)

    def _format_description(self, alert):
        """
        Takes an Alert and formats it for the description field of a
        JIRA issue.
        """
        full_descr = _JIRA_SETTINGS['INCLUDE_FULL_DESCRIPTION']
        if full_descr:
            return self._format_full_descr(alert)
        elif alert.notes:
            return alert.notes
        else:
            return ''

    @staticmethod
    def _format_summary(alert):
        """
        Takes an Alert and formats its title for the summary field of a
        JIRA issue.
        """
        if alert.title:
            return alert.title.replace('\n', ' ').strip()
        else:
            return 'Cyphon alert'

    @staticmethod
    def _get_priority_name(alert):
        """
        Takes an Alert and returns the name to use for the priority
        field of the JIRA issue.
        """
        priorities = _JIRA_SETTINGS['PRIORITIES']
        default_level = _JIRA_SETTINGS['DEFAULT_PRIORITY']
        return priorities.get(alert.level, default_level)

    def _format_issue(self, alert):
        """
        Takes an Alert and returns a dictionary of fields to create a
        JIRA issue.
        """
        issue_description = self._format_description(alert)
        summary = self._format_summary(alert)
        priority_name = self._get_priority_name(alert)

        fields = {
            'project': {
                'key': _JIRA_SETTINGS['PROJECT_KEY']
            },
            'summary': summary,
            'description': issue_description,
            'issuetype': {
                'name': _JIRA_SETTINGS['ISSUE_TYPE']
            },
            'priority': {'name': priority_name},
        }

        fields.update(_JIRA_SETTINGS['CUSTOM_FIELDS'])

        if self._jira_user is not None:
            fields['reporter'] = {'name': self._jira_user.name}

        return fields

    def _get_issue_url(self, issue):
        """
        Takes a JIRA issue Resource and returns a URL for the issue.
        """
        base_url = urllib.parse.urljoin(self.server, 'browse/')
        return urllib.parse.urljoin(base_url, issue.raw['key'])

    def _format_results(self, issue):
        """
        Takes a JIRA issue Resource and returns a dictionary of fields
        for referencing the issue.
        """
        data = issue.raw
        return {
            'key': data['key'],
            'issue_id': data['id'],
            'created': data['fields']['created'],
            'url': self._get_issue_url(issue),
        }

    def _add_comment(self, issue, body):
        """
        Takes an Alert, creates a JIRA issue, and returns the JIRA issue
        Resource.
        """
        kwargs = {
            'issue': issue,
            'body': body,
        }

        visibility = _JIRA_SETTINGS.get('COMMENT_VISIBILITY')
        if visibility:
            kwargs.update({'visibility': visibility})

        self.authed_jira.add_comment(**kwargs)

    def _create_issue(self, alert):
        """
        Takes an Alert, creates a JIRA issue, and returns the JIRA issue
        Resource.
        """
        issue_dict = self._format_issue(alert)
        issue = self.authed_jira.create_issue(fields=issue_dict)

        if _JIRA_SETTINGS['INCLUDE_ALERT_LINK']:
            self._add_comment(issue=issue, body=alert.link)

        return issue

    def process_request(self, obj):
        """Create a JIRA issue for an Alert.

        Parameters
        ----------
        obj : |Alert|
            The |Alert| used to create the JIRA Issue.

        Returns
        -------
        |Cargo|
            The results of the API call to JIRA.

        """
        try:
            issue = self._create_issue(obj)
            status_code = '200'
            data = self._format_results(issue)
            notes = None
        except jira.exceptions.JIRAError as error:
            status_code = str(error.status_code)
            data = None
            notes = error.text

        return Cargo(status_code=status_code, data=data, notes=notes)
