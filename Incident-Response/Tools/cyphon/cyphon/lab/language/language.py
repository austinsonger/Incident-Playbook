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
Provides a function for classifying the language of text.

======================  ================================================
Constant                Description
======================  ================================================
:const:`~PROBABILTY`    Level of certainty needed to assign a language.
:const:`~LANGUAGES`     A list of supported languages.
======================  ================================================

======================  ================================================
Function                Description
======================  ================================================
:func:`~get_language`   Classifies the language of text.
======================  ================================================

"""

# third party
from langdetect import detect_langs


PROBABILTY = 0.95
"""|float|

The mininum level of certainty needed to classify the language of text.
"""

LANGUAGES = ['da', 'nl', 'en', 'fi', 'fr', 'de', 'hu', 'it',
             'nb', 'pt', 'ro', 'ru', 'es', 'sv', 'tr']
"""|list| of |str|

ISO 639-1 codes for supported languages. These are languages supported
by MongoDB's text index.
"""


def get_language(text):
    """Classify the language of text.

    Uses Google's language detection algorithm to assign a language to
    a text string.

    Parameters
    ----------
    text :str
        The text to classify.

    Returns
    -------
    str
        The most likely language of the text that meets the
        :const:`~PROBABILTY` threshold, among the list of
        supported :const:`~LANGUAGES`. If no supported language meets
        the threshold, returns the value 'none'.

    Notes
    -----
    When associated with a field called "language", the string "none"
    tells MongoDB's text index to use simple tokenization with no list
    of stop words and no stemming. See http://docs.mongodb.org/manual/reference/text-search-languages/
    for more info.

    """
    results = detect_langs(text)
    for result in results:
        if result.lang in LANGUAGES and result.prob >= PROBABILTY:
            return result.lang
    return 'none'
