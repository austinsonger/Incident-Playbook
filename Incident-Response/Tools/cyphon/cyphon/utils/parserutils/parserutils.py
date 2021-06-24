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
Provides parsing helper functions.
"""

# standard library
from copy import deepcopy
import logging
import os
import re

# third party
from bson import ObjectId
from bs4 import BeautifulSoup

LOGGER = logging.getLogger(__name__)


def html_to_text(html):
    """Strip HTML tags from a string.

    Parameters
    ----------
    html : |str|
        Text containing HTML tags.

    Returns
    -------
    |str|
        Text without HTML tags. The string is indented according to
        where tags were nested, but blank lines are removed.

    Example
    -------
    >>> html = ('<html><head></head><body><p>Hi!<br>Here is the '
    >>>         '<a href="https://www.python.org">link</a> you wanted.</p></html>')
    >>> html_to_text(html)
           Hi!
           Here is the
            link
           you wanted.

    """
    html_parser = 'html5lib'
    soup = BeautifulSoup(html, html_parser)
    pretty_html = soup.prettify()
    pretty_soup = BeautifulSoup(pretty_html, html_parser)
    text = pretty_soup.get_text()
    lines = [s for s in text.splitlines() if not re.search(r'^\s*$', s)]
    return os.linesep.join(lines)


def get_dict_value(field_name, doc):
    """Return the value of a dictionary item.

    Parameters
    ----------
    field_name : |str|

    doc : |dict|
        A data dictionary.

    Returns
    -------
    any type
        The value associated with the given `field_name` from the `doc`.

    Note
    ----
    For a nested dictionary, use dot notation in the `field_name`
    (e.g., 'parentkey.childkey'). You may also reference an array value
    by its index (e.g., 'tags[0]').

    Examples
    --------
    >>> get_value('a.b.c', {'a': {'b': {'c': 100}}})
    100

    >>> doc = {'a': {'b': [{'c': [100, [15, 20]]}, {'d': 40}], 'e': 10}}
    >>> field = 'a.b[0].c[1][1]'
    >>> get_dict_value(field, doc)
    20

    """

    def get_array_value(doc, key):
        """
        Takes a dictionary (doc) and a string (key) representing a dictionary
        key and one or more array indexes, e.g. "location[0][1]". Returns the
        corresponding value from the dictionary.
        """
        # split key at the start of array values, e.g. 'loc[0]' -> ['loc', '0]']
        key_parts = key.split('[')

        # get the name of the parent field, e.g. "loc"
        key = key_parts.pop(0)

        # get the dictionary value, which is the first array
        array = doc[key]

        while len(key_parts) > 0:

            index = key_parts.pop(0)

            # remove trailing bracket from index value
            index = index.replace(']', '')

            # need to convert the string to an integer to use it as an index
            index = int(index)

            value = array[index]

            # step into the next array
            array = value

        return value

    if isinstance(field_name, str):

        doc_copy = deepcopy(doc)

        # parse the string into a list of keys
        keys = field_name.split('.')
        value = ''

        try:
            while len(keys) > 0:

                if isinstance(doc_copy, dict):

                    key = keys.pop(0)

                    # remove any leading or trailing whitespaces
                    key.strip()

                    # check if the key includes an array index (e.g., 'location[0]')
                    if '[' in key:
                        value = get_array_value(doc_copy, key)
                    else:
                        value = doc_copy[key]

                    doc_copy = value

                else:
                    return doc_copy

        except KeyError:
            # log this error so user knows to correct field_name
            # LOGGER.warning('The field_name "%s" cannot be found in the document %s.',
            #                field_name, str(doc)[:160])
            return None

        return value


def merge_dict(target, addition):
    """Merge additional keys into a target dictionary.

    Parameters
    ----------
    target : dict
        The dict to mutate.

    addition : dict
        The dict containing keys to merge into the `target` dict.

    Returns
    -------
    dict

    """
    for key in addition:
        if key in target and isinstance(target[key], dict) \
                and isinstance(addition[key], dict):
            merge_dict(target[key], addition[key])
        else:
            target[key] = addition[key]


def abridge_dict(schema, data):
    """Abridge a data document to only include specified fields.

    Parameters
    ----------
    schema : |list| of |DataFields|
        The fields that should be included in the abridged dict.

    data : dict
        The dictionary to be tidied.

    """
    abridged_dict = {}
    for field in schema:
        value = get_dict_value(field.field_name, data)
        if value:
            keys = field.field_name.split('.')
            val = {keys.pop(-1): value}
            while len(keys):
                val = {keys.pop(-1): val}
            merge_dict(abridged_dict, val)
    return abridged_dict


def divide_into_groups(items, max_group_size):
    """Divide a list of items into a list of smaller lists.

    Parameters
    ----------
    items : |list|
        The items to divide into groups.

    max_group_size : |int|
        The maximum number of items per group.

    Returns
    -------
    |list| of |list|
        A list of lists dividing the items into groups not exceeding the
        maximum group size.

    Examples
    --------
    >>> divide_into_groups(['a', 'b', 'c', 'd', 'e'], 2)
    [['a', 'b'], ['c', 'd'], ['e']]

    >>> divide_into_groups(['a', 'b', 'c', 'd', 'e'], 6)
    [['a', 'b', 'c', 'd', 'e']]

    >>> divide_into_groups(['a', 'b', 'c', 'd', 'e'], 0)
    [[]]

    """
    if max_group_size <= 0:
        raise ValueError('maximum group size must be greater than 0')

    items_copy = deepcopy(items)
    groups = []

    while len(items_copy) > 0:

        # size of current group is either max number of items or
        # number of remaining items, whichever is smaller
        group_size = min(len(items_copy), max_group_size)

        # save the items for the current group
        new_group = items_copy[:group_size]
        groups.append(new_group)

        # remove the items from the list
        del items_copy[:group_size]

    return groups


def extract_substring(string, left, right, right_to_left=False):
    """Return a substring from a string.

    Parameters
    ----------
    string : |str|
        A string to be parsed.
    left : |str|
        A character representing the left bound of a target substring.
    right : |str|
        A character representing the right bound of a target substring.
    right_to_left : |bool|, optional
        Whether the `string` should be searched from right to left.

    Returns
    -------
    |str|
        The substring between the specified bounds.

    Examples
    --------
    >>> extract_substring('dup key : { "123" }', ':', '}')
    ' { "123" '

    >>> extract_substring('$_id_1', '$', '_', True)
    '_id'

    """
    if right_to_left:
        l_index = string.rfind(left) + len(left)
        r_index = string.rfind(right)
    else:
        l_index = string.find(left) + len(left)
        r_index = string.find(right)

    return string[l_index:r_index]


def string_to_bool(value):
    """Recast a str representation of a Boolean to bool.

    Parameters
    ----------
    value : |str|
        The value to convert (e.g., 'false').

    Returns
    -------
    |bool|
        The Boolean value of `value`.

    Notes
    -----
    If `value` is not 'true', 'True', 'false', or 'False', the function
    simply converts the string to its Boolean value.

    Examples
    --------
    >>> string_to_bool('true')
    True

    >>> string_to_bool('False')
    False

    >>> string_to_bool('0')
    True

    >>> string_to_bool(0)
    False

    """
    if value in ['true', 'True']:
        return True
    elif value in ['false', 'False']:
        return False
    else:
        return bool(value)


def restore_type(field_type, value):
    """Recast a string value as a given type.

    Parameters
    ----------
    field_type : {'BooleanField', 'CharField', 'FloatField', 'IntegerField'}
        A model field type.

    value : |str|
        The value to recast.

    Returns
    -------
    |bool|, |float|, |int|, or |str|
        The value recast to the specified type.

    Examples
    --------
    >>> restore_type('BooleanField', 'false')
    False

    >>> restore_type('CharField', '0')
    '0'

    >>> restore_type('FloatField', '1.2')
    1.2

    >>> restore_type('IntegerField', '1')
    1

    """
    field_types = {
        'BooleanField': string_to_bool,
        'CharField': str,
        'FloatField': float,
        'IntegerField': int,
    }
    return_val = lambda x: x
    recast = field_types.get(field_type, return_val)
    return recast(value)


def restore_type_from_str(string):
    """Restore a value to its inferred type.

    Parameters
    ----------
    string : str
        A |str| representation of a string, ObjectId, integer, or null
        value.

    Returns
    -------
    |str|, |ObjectId|, |int|, or |None|

    Examples
    --------
    >>> restore_type('"123"')
    '123'

    >>> restore_type("ObjectId('123')")
    ObjectId('123')

    >>> restore_type('123')
    123

    >>> restore_type('_123')
    '_123'

    >>> restore_type('null')
    None

    """
    if string[0] == '"':
        return string.replace('"', '')
    elif string[0] == "'":
        return string.replace("'", '')
    elif re.match('ObjectId', string):
        match = re.match(r'ObjectId\(\'(?P<id>.*)\'\)', string)
        return ObjectId(match.group('id'))
    elif string == 'null':
        return None
    else:
        try:
            return int(string)
        except ValueError:
            return string


def get_dup_key_val(errmsg):
    """Return the duplicate key referenced in an error message.

    Parameters
    ----------
    errmsg : |str|
        A pymongo `DuplicateKeyError` message.

    Returns
    -------
    |dict|
        The key(s) and value(s) of the duplicate key.

    Example
    -------
    >>> errmsg = ('insertDocument :: caused by :: 11000 E11000 duplicate '
    >>>           'key error collection: cyphon.posts index: '
    >>>           '_platform_1_doc_id_1 dup key: { : twitter", : '
    >>>           '"ObjectId(\'5543769ef861c942838c7ee9\') }')
    >>> get_dup_key_val(errmsg)
    {'_platform': 'twitter', '_doc_id': ObjectId('5543769ef861c942838c7ee9')}
    """
    msg = errmsg.split(' dup key: { ')
    key = extract_substring(msg[0], 'index: ', '_', 'right').strip()
    val = extract_substring(msg[1], ':', '}').strip()

    # parse compound indexes
    keys = re.split(r'_[0-9]+_', key)
    values = val.split(', : ')

    if len(keys) != len(values):  # pragma: no cover
        raise ValueError('cannot match index keys with values')

    key_val = {}

    for index, value in enumerate(values):
        key_val[keys[index]] = restore_type_from_str(values[index])

    return key_val


def format_fields(field_data, include_empty=True):
    """Format field labels and values.

    Parameters
    ----------
    field_data : |list| of |tuple|
       2-tuples of field labels and values.

    include_empty : |bool|, optional
        Whether fields whose values are |None| or an empty |str| should
        be included in the formatted fields.

    Returns
    -------
    str
        Formatted field labels and values.

    Examples
    --------
    >>> field_data = [('Name', 'Jane'), ('Age', 30), ('DOB', None)]
    >>> format_fields(field_data, include_empty=True)
    Name: Jane
    Age:  30
    DOB:  None

    >>> field_data = [('Name', 'Jane'), ('Age', 30), ('DOB', None)]
    >>> format_fields(field_data, include_empty=False)
    Name: Jane
    Age:  30

    """
    max_label = 0
    for (label, value) in field_data:
        label_length = len(label)
        if label_length > max_label:
            max_label = label_length

    fields = []
    for (label, value) in field_data:
        empty = str(value).strip() in ['', 'None']
        if not empty or include_empty:
            label_length = len(label.strip())
            extra_spaces = ' ' * (max_label - label_length)
            label_sep = ':' + extra_spaces + ' '
            joined_field = label_sep.join([label, str(value)])
            fields.append(joined_field)

    return '\n'.join(fields)
