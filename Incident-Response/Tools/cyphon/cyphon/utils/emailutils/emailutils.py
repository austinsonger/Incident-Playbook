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
from email.mime.image import MIMEImage
import os

# third party
from constance import config


def emails_enabled():
    """Return a Boolean indicating whether email notifcations are enabled.

    Returns the Constance configuration for email notifcations if it
    exists. Otherwise, returns True.
    """
    if hasattr(config, 'EMAIL_NOTIFICATIONS_ENABLED'):
        return config.EMAIL_NOTIFICATIONS_ENABLED
    else:
        return True


def embed_image(message, dir_path, file_name):
    """Attach an image to an email.

    Parameters
    ----------
    message : |Message|
        The email message to which the image will be attached.

    dir_path : |str|
        The path for the directory containing the image file.

    file_name : |str|
        The name of the image file.

    """
    message.mixed_subtype = 'related'
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'rb') as image_file:
        image = MIMEImage(image_file.read())
    image.add_header('Content-ID', '<{}>'.format(file_name))
    message.attach(image)
    return message
