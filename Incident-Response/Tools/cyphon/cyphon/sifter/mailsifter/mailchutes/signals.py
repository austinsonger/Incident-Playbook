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
Defines a signal receiver for incoming emails.
"""

# third party
from django.conf import settings
from django.dispatch import receiver
from django_mailbox.signals import message_received

# local
from cyphon.documents import DocumentObj
from .models import MailChute

_MAILSIFTER_SETTINGS = settings.MAILSIFTER


@receiver(message_received)
def handle_message(sender, message, **args):
    """
    Takes a signal sender and a Django Mailbox Message and processes
    the message.
    """
    # get the Python email.message.Message object
    email = message.get_email_object()

    doc_obj = DocumentObj(
        data=email,
        doc_id=email['Message-ID'],
        collection=_MAILSIFTER_SETTINGS['MAIL_COLLECTION'],
    )

    # process the email through enabled MailChutes
    MailChute.objects.process(doc_obj)
