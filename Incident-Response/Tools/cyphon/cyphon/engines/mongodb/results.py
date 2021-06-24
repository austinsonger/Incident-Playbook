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
Defines helper fuctions for formatting MongoDB query results.

==============================  ============================================
Function                        Description
==============================  ============================================
:func:`~get_count`              Get the number of matching docs.
:func:`~get_doc_ids`            Get the ids of matching docs.
:func:`~get_results`            Get docs from a search result.
:func:`~get_results_and_count`  Get docs and doc count from a search result.
==============================  ============================================

"""

# third party
from pymongo.cursor import Cursor


def _convert_obj_ids_to_strings(data):
    """Convert ObjectIds to hexadecimal strings.

    Takes a dictionary or a list of dictionaries of MongoDB BSON
    documents. Transforms their ObjectIds into strings so the documents
    are JSON serializable and the doc ids are easily accessed.
    """
    if isinstance(data, list):
        for doc in data:
            doc['_id'] = str(doc['_id'])
    elif isinstance(data, dict):
        data['_id'] = str(data['_id'])

    return data


def get_count(data):
    """Get the number of documents in a MongoDB search result.

    Parameters
    ----------
    data : `~pymongo.cursor.Cursor`
        A MongoDB search result.

    Returns
    -------
    int
        The total number of documents matching the search criteria.

    """
    if isinstance(data, Cursor):
        return data.count()


def get_results(data):
    """Get documents from a MongoDB search result.

    Transforms MongoDB BSON documents into JSON serializable documents.
    This process converts the ObjectIds into hexadecimal strings.

    Parameters
    ----------
    data : `~pymongo.cursor.Cursor`
        A MongoDB search result.

    Returns
    -------
    |list| of |dict|
        A list of JSON serializable documents.

    """
    if isinstance(data, Cursor):
        data = list(data)
    return _convert_obj_ids_to_strings(data)


def get_results_and_count(data):
    """Get the documents and document count from a search result.

    Parameters
    ----------
    data : `~pymongo.cursor.Cursor`
        A MongoDB search result.

    Returns
    -------
    dict
        A dictionary with keys 'count' and 'results'. The 'count' value
        is the total number of documents matching the search criteria.
        The 'results' value is a list of documents from the search
        result, with the ObjectIds converted to hexadecimal strings.

    """
    count = get_count(data)
    results = get_results(data)
    return {
        'count': count,
        'results': results,
    }


def get_doc_ids(results):
    """Get the ids of documents contained in a MongoDB search result.

    Parameters
    ----------
    results : `~pymongo.cursor.Cursor`
        A MongoDB search result.

    Returns
    -------
    |list| of |str|
        Hexadecimal ids of documents contained in the search result.

    """
    docs = get_results(results)
    return [doc['_id'] for doc in docs]
