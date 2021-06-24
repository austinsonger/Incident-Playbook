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
Settings for the Cyclops package.
"""

CYCLOPS_AWS_BUCKET_URL = 'https://s3.amazonaws.com/cyclops-public'

CYCLOPS_VERSION = '0.5.4'
"""str

Version number of Cyclops to use.
"""

CYCLOPS_JS_URL = (
    '{0}/{1}/cyclops.js'.format(
        CYCLOPS_AWS_BUCKET_URL, CYCLOPS_VERSION))
"""str

CDN URL of the cyclops JS file. Contains the main application.
"""

CYCLOPS_CSS_URL = (
    '{0}/{1}/cyclops.css'.format(
        CYCLOPS_AWS_BUCKET_URL, CYCLOPS_VERSION))
"""str

CDN URL of the cyclops CSS file. Contains all the styling.
"""
