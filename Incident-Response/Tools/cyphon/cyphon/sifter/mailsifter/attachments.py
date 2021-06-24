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
from datetime import datetime
import logging
import mimetypes
import os
import urllib
import uuid

# third party
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import six

_MAILSIFTER_SETTINGS = settings.MAILSIFTER

_LOGGER = logging.getLogger(__name__)


def get_file_name():
    """

    """
    return uuid.uuid4().hex


def get_extension(attachment):
    """

    """
    try:
        filename = attachment.get_filename()
        if filename:
            extension = os.path.splitext(filename)[1]
        else:
            extension = mimetypes.guess_extension(attachment.get_content_type())
        return extension or '.bin'

    except AttributeError:
        return None


def get_raw_directory_path(company=None):
    """

    """
    attachments_folder = _MAILSIFTER_SETTINGS['ATTACHMENTS_FOLDER']

    if company is not None:
        return os.path.join(company.uuid.hex, attachments_folder)
    else:
        return os.path.join(attachments_folder)


def get_directory_path(company=None):
    """

    """
    path = get_raw_directory_path(company)
    if '%' in path:
        return datetime.utcnow().strftime(path)
    else:
        return path


def get_attachment_path(path):
    """

    """
    return os.path.join(settings.MEDIA_ROOT, path)


def get_attachment_url(path):
    """

    """
    base_url = urllib.parse.urljoin(settings.BASE_URL, settings.MEDIA_URL)
    return urllib.parse.urljoin(base_url, path)


def get_file_path(attachment, company=None):
    """

    """
    file_name = get_file_name()
    extension = get_extension(attachment)
    if extension in _MAILSIFTER_SETTINGS['ALLOWED_FILE_EXTENSIONS']:
        dir_path = get_directory_path(company)
        return os.path.join(dir_path, file_name + extension)
    else:
        orig_filename = attachment.get_filename()
        _LOGGER.warning('The attachment %s is not an allowed file type',
                        orig_filename)


def get_attachment_content(attachment):
    """

    """
    payload = attachment.get_payload(decode=True)
    return six.BytesIO(payload).getvalue()


def save_attachment(attachment, company=None):
    """

    """
    file_path = get_file_path(attachment, company)
    if file_path is not None:
        full_path = get_attachment_path(file_path)
        file_content = get_attachment_content(attachment)
        default_storage.save(full_path, ContentFile(file_content))
        return get_attachment_url(file_path)
