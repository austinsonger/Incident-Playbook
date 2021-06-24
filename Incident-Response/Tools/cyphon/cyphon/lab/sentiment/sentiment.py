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
Provides functions for analyzing the sentiment of text.

======================  ================================================
Function                Description
======================  ================================================
:func:`~clean_text`     Removes links and special characters from text.
:func:`~get_polarity`   Gets the degree of polarity of text.
:func:`~get_sentiment`  Classifies the sentiment of text.
======================  ================================================

"""

# standard library
import re

# third party
from textblob import TextBlob


def clean_text(text):
    """Remove HTML links and special characters from text.

    Parameters
    ----------
    text : str
        The text to clean.

    Returns
    -------
    str
        The cleaned text.

    """
    regex = r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)'
    cleaned_text = re.sub(regex, ' ', text)
    return ' '.join(cleaned_text.split())


def get_polarity(text):
    """Get the degree of polarity of text.

    Parameters
    ----------
    text : str
        The text to analyze.

    Returns
    -------
    float
        The polarity of the text.

    """
    cleaned_text = clean_text(text)
    analysis = TextBlob(cleaned_text)
    return analysis.sentiment.polarity


def get_sentiment(text):
    """Classify the sentiment of text.

    Parameters
    ----------
    text : str
        The text to analyze.

    Returns
    -------
    str
        The sentiment of the text, which can be either 'positive',
        'neutral', or 'negative'.

    """
    polarity = get_polarity(text)
    if polarity > 0:
        return 'positive'
    elif polarity == 0:
        return 'neutral'
    else:
        return 'negative'
