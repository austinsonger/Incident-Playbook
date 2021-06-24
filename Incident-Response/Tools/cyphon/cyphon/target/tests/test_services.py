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
Tests the services of the targets package
"""

# standard library
import datetime

# third party
from django.test import TestCase


class CreateTargetsTestCase(TestCase):
    """
    Tests the create_targets method
    """

    def setUp(self):
        self.test_data_pass = {
            "followees" : [
                {
                    "nickname": "bob",
                },
            ],
            "locations": [
                {
                    "name": "This Polygon",
                    "geom": {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [
                                        6.6796875,
                                        13.581920900545844
                                    ],
                                    [
                                        6.6796875,
                                        18.646245142670608
                                    ],
                                    [
                                        15.8203125,
                                        18.646245142670608
                                    ],
                                    [
                                        15.8203125,
                                        13.581920900545844
                                    ],
                                    [
                                        6.6796875,
                                        13.581920900545844
                                    ]
                                ]
                            ]
                        }
                    }
                },
                {
                    "name": "This Point",
                    "geom": {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                73.125,
                                49.724479188713005
                            ]
                        },
                    },
                },
            ],
            "searchterms": [
                {
                    "term": "Search for me",
                    "negate": True,
                },
            ],
            "timeframes": [
                {
                    "start": datetime.datetime(2008, 11, 22, 19, 53, 42),
                }
            ],
        }

        self.test_data_fail = {

        }