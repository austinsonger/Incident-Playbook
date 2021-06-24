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
Provides helper functions for gathering fixtures for Django TestCases.
"""

# standard library
import logging
import os.path

# third party
from django.conf import settings

FIXTURES_DIR = 'tests/fixtures/'
FILE_EXTENSION = '.json'

LOGGER = logging.getLogger(__name__)

# dictionary of fixture files and their direct dependencies
FIXTURE_DEPENDENCIES = {
    'actions': ['destinations'],
    'alerts': ['distilleries', 'watchdogs', 'users'],
    'articles': [],
    'bottles': [],
    'categories': [],
    'codebooks': ['companies'],
    'comments': ['alerts', 'users'],
    'companies': [],
    'containers': ['bottles', 'labels'],
    'contexts': ['distilleries'],
    'couriers': ['passports', 'visas', 'actions', 'users'],
    'datachutes': ['datamungers', 'datasieves', 'pipes'],
    'datacondensers': ['bottles'],
    'datamungers': ['datacondensers', 'distilleries'],
    'datasieves': [],
    'datataggers': ['containers', 'tags'],
    'destinations': [],
    'dispatches': ['alerts', 'stamps'],
    'distilleries': ['categories', 'containers', 'companies',
                     'codebooks', 'tastes', 'warehouses'],
    'filters': ['followees', 'locations', 'searchterms'],
    'followees': ['reservoirs'],
    'funnels': ['bottles', 'datacondensers', 'pipes'],
    'gateways': ['reservoirs', 'pipes'],
    'groups': [],
    'invoices': ['stamps'],
    'inspections': [],
    'labels': ['inspections', 'procedures'],
    'locations': ['users'],
    'logchutes': ['logmungers', 'logsieves'],
    'logcondensers': ['bottles'],
    'logmungers': ['logcondensers', 'distilleries'],
    'logsieves': [],
    'mailchutes': ['mailmungers', 'mailsieves'],
    'mailcondensers': ['bottles'],
    'mailmungers': ['mailcondensers', 'distilleries'],
    'mailsieves': [],
    'monitors': ['distilleries', 'groups'],
    'parameters': ['locations', 'users'],
    'passports': ['users'],
    'pipes': ['reservoirs'],
    'plumbers': ['passports', 'visas', 'pipes', 'users'],
    'procedures': [],
    'records': ['plumbers'],
    'reservoirs': [],
    'samples': ['pipes'],
    'searchterms': [],
    'stamps': ['passports', 'pipes', 'actions', 'users'],
    'streams': ['invoices'],
    'tags': ['alerts', 'comments', 'articles'],
    'tastes': ['containers'],
    'timeframes': [],
    'warehouses': [],
    'watchdogs': ['categories', 'groups'],
    'users': ['companies', 'groups'],
    'visas': []
}


def get_dependencies(dependencies):
    """
    Takes a list of fixture file names (without their extension) and
    returns a list of file names for the fixtures and their dependencies.
    (This list may contain duplicates.)
    """
    fixture_list = []
    for dependency in dependencies:
        fixture_list.append(dependency)
        child_dependencies = FIXTURE_DEPENDENCIES.get(dependency, [])
        if child_dependencies != []:
            new_list = get_dependencies(child_dependencies)
            fixture_list = new_list + fixture_list
    return fixture_list


def get_fixtures(dependencies):
    """
    Takes a list of fixture file names (without their .json extension)
    and returns a list of fixture files containing all those fixtures
    and all their dependencies. This list can be assigned to the
    fixtures property of a Django TestCase. raises an AssertionError
    if any of the files are missing.
    """
    assert isinstance(dependencies, list), 'Dependencies must be a list'

    fixtures = []
    for fixture in get_dependencies(dependencies):
        file_name = FIXTURES_DIR + fixture + FILE_EXTENSION
        if file_name not in fixtures:
            exists = os.path.isfile(os.path.join(settings.BASE_DIR, file_name))
            if not exists:
                LOGGER.error('Fixture file %s is missing', file_name)
            fixtures.append(file_name)

    return fixtures
