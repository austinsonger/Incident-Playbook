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
import os

# third party
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader

# local
from utils.emailutils import emailutils


_SUBJECT_TEMPLATE = 'alerts/comment_notification_subject.txt',
_TEXT_TEMPLATE = 'alerts/comment_notification_text_email.txt',
_HTML_TEMPLATE = 'alerts/comment_notification_html_email.html'

_LOGO_DIR = os.path.join(settings.PROJ_DIR, 'cyphon/static/images/')
_LOGO_FILE = 'cyphon-sm.png'


def compose_comment_email(comment, user):
    """Email a comment notification to a user.

    Parameters
    ----------
    comment : |Comment|
        The |Comment| to notify the user about.

    user : |AppUser|
        The |AppUser| who should receive the email notification.

    Returns
    -------
    :class:`django.core.mail.message.EmailMultiAlternatives`

    """
    context = {
        'comment': comment,
        'image': _LOGO_FILE,
    }

    subject = loader.render_to_string(_SUBJECT_TEMPLATE, context)

    # email subject must not contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(_TEXT_TEMPLATE, context)

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        to=[user.email],
        from_email=settings.DEFAULT_FROM_EMAIL
    )

    # attach html
    html_email = loader.render_to_string(_HTML_TEMPLATE, context)
    email_message.attach_alternative(html_email, 'text/html')

    # embed logo
    email_message = emailutils.embed_image(
        message=email_message,
        dir_path=_LOGO_DIR,
        file_name=_LOGO_FILE
    )
    return email_message
