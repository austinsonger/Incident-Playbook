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
Tests Alert views.
"""

# third party
from django.conf import settings
from django.test import TestCase

# local
from alerts.models import Comment
from alerts.services import compose_comment_email
from tests.fixture_manager import get_fixtures


class CommentEmailTestCase(TestCase):
    """
    Base class for testing the Alert class.
    """
    fixtures = get_fixtures(['comments'])

    def setUp(self):
        self.comment = Comment.objects.get(pk=1)

    def test_compose_comment_email(self):
        """
        Tests the compose_comment_email function.
        """
        email = compose_comment_email(self.comment,
                                      self.comment.alert.assigned_user)

        self.assertEqual(email.subject, 'John Smith commented on Alert #3')
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to, ['testuser1@testdomain.com'])
        self.assertEqual(email.alternatives, [('<body style="margin: 0; padding: 0; font-family: \'Helvetica Neue\', Helvetica, Arial, sans-serif; color: #333333; font-weight: 300; background-color: #E6E6E6; letter-spacing: 0.6px; font-weight: 300; font-size: 14px;">\n    <table cellpadding="0" cellspacing="0" width="600px" style="margin: 20px auto; max-width: 600px;">\n        <tr>\n            <td style="padding: 25px 35px; line-height: 25px;">   \n                <img src="cid:cyphon-sm.png">\n                <p>John Smith commented on <a href="http://localhost:8000/app/alerts/3" target="_blank">Alert #3</a> (Acme Supply Co).</p>\n                <blockquote style="background: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px;">I have something to say</blockquote>\n                <p style="display: inline;">If the Alert link doesn\'t work, please copy this URL into your browser: <br>http://localhost:8000/app/alerts/3</p>\n            </td>\n        </tr>\n    </table>\n</body>', 'text/html')])
        self.assertEqual(email.mixed_subtype, 'related')
        self.assertEqual(len(email.attachments), 1)
