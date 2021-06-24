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
import email.utils as email_utils
from email.header import decode_header
import logging
import os

# third party
import bleach
from django.conf import settings

# local
from utils.parserutils.parserutils import html_to_text

_MAILSIFTER_SETTINGS = settings.MAILSIFTER
_CONTENT_PREFERENCES = _MAILSIFTER_SETTINGS['EMAIL_CONTENT_PREFERENCES']

_LOGGER = logging.getLogger(__name__)


def get_content(email, content_types=_CONTENT_PREFERENCES, remove_tags=True):
    """
    Takes an email Message object and a Boolean indicating whether
    HTML tags should be removed. Returns a string of the most
    preferred content. If no matches are found, returns None.
    """
    for content_type in content_types:
        for part in email.walk():
            if part.get_content_type() == content_type:
                payload = part.get_payload(decode=True)
                if remove_tags and content_type == 'text/html':
                    return html_to_text(payload)
                else:
                    return payload


def get_date(email):
    """
    Takes an email Message object and attempts to parse a date according
    to the rules in RFC 2822. If successful, returns a string of the
    datetime in UTC and in ISO 8601 format. Otherwise, returns None.
    """
    date_str = email.get('Date', '')
    try:
        email_datetime = email_utils.parsedate_to_datetime(date_str)
        return email_datetime.isoformat()
    except TypeError:
        _LOGGER.warning('Email date for %s could not be parsed.',
                       email.get('Message-ID'))


def format_address(address):
    """

    """
    return "'%s' %s" % (address[0], address[1])


def get_from(email):
    """
    Takes an email Message object and returns the 'from' email address.
    """
    address = email.get('From')
    parsed_addr = email_utils.parseaddr(address)
    return format_address(parsed_addr)


def get_to(email):
    """
    Takes an email Message object and returns the 'to' email address(es).
    """
    addresses = email.get_all('To', [])
    parsed_addresses = email_utils.getaddresses(addresses)
    return ', '.join([format_address(addr) for addr in parsed_addresses])


def get_subject(email):
    """
    Takes an email Message object and returns the Subject as a string,
    decoding base64-encoded subject lines as necessary.
    """
    subject = email.get('Subject', '')
    result = decode_header(subject)
    subject = result[0][0]
    if isinstance(subject, str):
        return subject
    else:
        return subject.decode('unicode_escape')


def get_attachment(email_part):
    """Return the file path of an email attachment.

    Parameters
    ----------
    email_part : Message
        Part of a multipart email |Message| object.

    Returns
    -------
    |str| or |None|
        The file path to the attachment associated with the email part,
        if one exists and is an allowed file type. Otherwise, returns
        |None|.

    """
    if not email_part.is_multipart() \
            and 'attachment' in email_part.get('Content-Disposition', ''):
        content_type = email_part.get_content_type()
        _, extension = os.path.splitext(email_part.get_filename())
        if content_type in _MAILSIFTER_SETTINGS['ALLOWED_EMAIL_ATTACHMENTS'] \
                or extension in _MAILSIFTER_SETTINGS['ALLOWED_FILE_EXTENSIONS']:
            return email_part


def get_attachments(email):
    """Return a list of file paths for attachments from an email.

    Parameters
    ----------
    email : Message
        An email |Message| object.

    Returns
    -------
    |list| of |str|
        A |list| of file paths to email attachments. If the email has no
        attachments, returns an empty |list|.

    """
    attachments = []
    for part in email.walk():
        attachment = get_attachment(part)
        if attachment is not None:
            attachments.append(attachment)
    return attachments


def get_first_attachment(email):
    """Return the file path of the first attachment from an email.

    Parameters
    ----------
    email : Message
        An email |Message| object.

    Returns
    -------
    |str| or |None|
        The file path to the first attachment in the email, if one
        exists and is an allowed file type. Otherwise, returns |None|.

    """
    for part in email.walk():
        attachment = get_attachment(part)
        if attachment is not None:
            return attachment


def get_email_value(field_name, email):
    """
    Takes the name of an email field and an email Message object and
    returns the value of the field from the Message object.
    """
    field_functions = {
        'Content': get_content,
        'Date': get_date,
        'From': get_from,
        'To': get_to,
        'Subject': get_subject,
        'Attachment': get_first_attachment,
        'Attachments': get_attachments
    }

    if field_name in field_functions:
        value = field_functions[field_name](email)
    else:
        value = email.get(field_name, '')

    if isinstance(value, bytes):
        value = value.decode('utf-8')

    if isinstance(value, str):
        try:
            # strip any tags that aren't on the whitelist
            return bleach.clean(value, strip=True)
        except UnicodeDecodeError:
            _LOGGER.error('An error was encountered while parsing the %s '
                          'field of an email.', field_name)
            return 'The %s of this email could not be displayed due to an error.' \
                   % field_name
    else:
        return value
