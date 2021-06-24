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
Defines helper fuctions for formatting Elasticsearch query results.

==============================  =============================================
Function                        Description
==============================  =============================================
:func:`~get_count`              Get the number of matching docs.
:func:`~get_doc_ids`            Get the ids of matching docs.
:func:`~get_doc_info`           Get the index, doc_type, and id of a doc.
:func:`~get_found_docs`         Get docs from a multi-get request.
:func:`~get_hits`               Get docs from a search result.
:func:`~get_results_and_count`  Get docs and doc count from a search result.
:func:`~get_source`             Get `_source` fields with added `_id` fields.
:func:`~get_source_with_id`     Get a doc's `_source` field with its `_id`.
==============================  =============================================

"""


def get_count(results):
    """Get the number of documents in an Elasticsearch search result.

    Parameters
    ----------
    results : dict
        An Elasticsearch search result.

    Returns
    -------
    int
        The total number of documents matching the search criteria.

    """
    return results['hits']['total']


def get_hits(results):
    """Return a list of documents from an Elasticsearch search result.

    Parameters
    ----------
    results : dict
        An Elasticsearch search result.

    Returns
    -------
    |list| of |dict|
        The list of documents in the search result.

    """
    return results['hits']['hits']


def get_doc_info(result):
    """Get the index, doc_type, and id associated with a document.

    Parameters
    ----------
    result : dict
        A document from an Elasticsearch search result.

    Returns
    -------
    dict
        A dictionary with keys 'index', 'doc_type', and 'id',
        containing the name of the index in which the document resides,
        the doc_type of the document, and its id.

    """
    return {
        'index': result['_index'],
        'doc_type': result['_type'],
        'id': result['_id']
    }


def get_doc_ids(results):
    """Get the ids of documents contained in a search result.

    Parameters
    ----------
    results : dict
        An Elasticsearch search result.

    Returns
    -------
    |list| of |str|
        A list of ids of the documents contained in the search result.

    """
    return [hit['_id'] for hit in get_hits(results)]


def get_source_with_id(result):
    """Return a document's `_source` field with its `_id` added.

    Parameters
    ----------
    result : dict
        A document from a set of Elasticsearch search results.

    Returns
    -------
    dict
        The document's `_source` field updated with the doc's `_id`.

    """
    result['_source'].update({'_id': result['_id']})
    return result['_source']


def get_source(results):
    """Get the documents contained in a search result.

    Extracts documents from an Elasticsearch search result, adds the
    document id to each document, and returns the list of documents.

    Parameters
    ----------
    results : dict
        An Elasticsearch search result.

    Returns
    -------
    |list| of |dict|
        The documents from the search result, with the doc ids added.

    """
    return [get_source_with_id(hit) for hit in get_hits(results)]


def get_found_docs(results):
    """Get the documents found through a multi-get request.

    This method weeds out failed matches from an mget result set.

    Parameters
    ----------
    results : dict
         An Elasticsearch mget (find by id) result.

    Returns
    -------
    |list| of |dict|
        The documents found by the mget request, with the doc ids added.

    """
    docs = results['docs']
    matched_docs = []
    for doc in docs:
        if doc.get('found'):
            formatted_doc = get_source_with_id(doc)
            matched_docs.append(formatted_doc)
    return matched_docs


def get_results_and_count(data):
    """Get the documents and document count from a search result.

    Parameters
    ----------
    data : dict
        An Elasticsearch search result.

    Returns
    -------
    dict
        A dictionary with keys 'count' and 'results'. The 'count' value
        is the total number of documents matching the search criteria.
        The 'results' value is a list of documents from the search
        result, with the doc ids added to each document.

    """
    count = get_count(data)
    results = get_source(data)
    return {
        'count': count,
        'results': results,
    }
