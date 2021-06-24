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
Functional tests for the Containers app.
"""

# local
from tests.fixture_manager import get_fixtures
from tests.functional_tests import ModelPreviewFunctionalTest


class ContainerFunctionalTest(ModelPreviewFunctionalTest):
    """
    Base class for testing admin pages in the Containers app.
    """
    fixtures = get_fixtures(['containers', 'tastes'])

    url = '/admin/containers/container/2/change/'

    def test_change_form(self):
        """
        Tests the Container change form. Makes sure that the dictionary in
        the preview field is indented properly.
        """
        actual = self.page.preview
        expected = (
            '{'
            '<br>'
            '    "_metadata": {'
            '<br>'
            '        "priority": "CharField (Keyword)",'
            '<br>'
            '        "source_ip_location": "PointField (Location)"'
            '<br>'
            '    },'
            '<br>'
            '    "content": {'
            '<br>'
            '        "image": "URLField",'
            '<br>'
            '        "link": "URLField",'
            '<br>'
            '        "text": "TextField (Keyword)",'
            '<br>'
            '        "title": "TextField (Keyword)",'
            '<br>'
            '        "video": "URLField"'
            '<br>'
            '    },'
            '<br>'
            '    "created_date": "DateTimeField (DateTime)",'
            '<br>'
            '    "location": "PointField (Location)",'
            '<br>'
            '    "user": {'
            '<br>'
            '        "email": "EmailField (Account)",'
            '<br>'
            '        "id": "CharField",'
            '<br>'
            '        "link": "URLField",'
            '<br>'
            '        "name": "CharField (Account)",'
            '<br>'
            '        "profile_pic": "URLField",'
            '<br>'
            '        "screen_name": "CharField (Account)"'
            '<br>'
            '    }'
            '<br>'
            '}'
        )
        self.assertEqual(actual, expected)

