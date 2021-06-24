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
A collection of methods to operate on all the different target packages.
"""

# standard library
import importlib


def create_targets(data):
    """
    Takes a dictionary of data and creates target objects from it. Each
    key in the dictionary must align to an attribute of the target object
    it's trying to create.
    """
    target_objects = {}

    for key, value in data.iteritems():
        try:
            target = importlib.import_module(key)
        except ImportError as error:
            raise error
        else:
            target_objects[key] = create_target_object(target, value)

    return target_objects


def create_target_object(object_package, data_list):
    """
    Creates a list of target objects given the target object package
    and a list of dictionaries whose keys map to the objects attributes.
    """
    targets = []

    for data in data_list:
        serializer = object_package.serializers.ObjectSerializer(data)
        if serializer.is_valid():
            targets.append(serializer.save())
        else:
            return

    return targets
