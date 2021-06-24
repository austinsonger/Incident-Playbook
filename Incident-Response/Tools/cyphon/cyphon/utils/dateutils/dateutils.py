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
Utility functions for dates and times. Provides a suite of functions
for manipulating dates and times. Defines a set of constants to be used for
defining time units.
"""
from __future__ import division

# standard library
import math
import datetime
import logging

# third party
import dateutil.parser
import pytz

# constants used for selectbox choices throughout the site
SECONDS = 's'
MINUTES = 'm'
HOURS = 'h'
DAYS = 'd'

LOGGER = logging.getLogger(__name__)

UTC_TZ = pytz.timezone('UTC')


def convert_hours_to_days(hours):
    """
    (int or float) -> float

    Takes time in hours and returns time in days.
    """
    return hours / 24.0


def convert_hours_to_minutes(hours):
    """
    (int or float) -> float

    Takes time in hours and returns time in minutes.
    """
    return hours * 60.0


def convert_hours_to_seconds(hours):
    """
    (int or float) -> float

    Takes time in hours and returns time in seconds.
    """
    return convert_hours_to_minutes(hours) * 60.0


def convert_days_to_minutes(days):
    """
    (int or float) -> float

    Takes time in days and returns time in minutes.
    """
    hours = days * 24.0
    return convert_hours_to_minutes(hours)


def convert_days_to_seconds(days):
    """
    (int or float) -> float

    Takes time in days and returns time in seconds.
    """
    return convert_days_to_minutes(days) * 60.0


def convert_minutes_to_seconds(seconds):
    """
    (int or float) -> float

    Takes time in seconds and returns time in minutes.
    """
    return seconds * 60.0


def convert_minutes_to_hours(minutes):
    """
    (int or float) -> float

    Takes time in minutes and returns time in hours.
    """
    return minutes / 60.0


def convert_minutes_to_days(minutes):
    """
    (int or float) -> float

    Takes time in minutes and returns time in days.
    """
    return convert_minutes_to_hours(minutes) / 24.0


def convert_seconds_to_minutes(seconds):
    """
    (int or float) -> float

    Takes time in seconds and returns time in minutes.
    """
    return seconds / 60.0


def convert_seconds_to_hours(seconds):
    """
    (int or float) -> float

    Takes time in seconds and returns time in hours.
    """
    minutes = convert_seconds_to_minutes(seconds)
    return convert_minutes_to_hours(minutes)


def convert_seconds_to_days(seconds):
    """
    (int or float) -> float

    Takes time in hours and returns time in seconds.
    """
    hours = convert_seconds_to_hours(seconds)
    return convert_hours_to_days(hours)


def convert_time_to_whole_minutes(time, unit):
    """
    (int or float, str) -> int

    Takes a time in hours, minutes, or seconds, and the time unit. The unit must
    match a string defined by a constant (SECONDS, MINUTES, HOURS, or DAYS).
    The function returns the ceiling of the time in minutes.
    """
    conversions = {
        SECONDS: convert_seconds_to_minutes(time),
        MINUTES: time,
        HOURS: convert_hours_to_minutes(time),
        DAYS: convert_days_to_minutes(time)
    }

    minutes = conversions[unit]

    return math.ceil(minutes)


def convert_time_to_seconds(time, unit):
    """
    (int or float, str) -> int

    Takes a time in hours, minutes, or seconds, and the time unit. The unit must
    match a string defined by a constant (SECONDS, MINUTES, HOURS, or DAYS).
    The function returns the ceiling of the time in seconds.
    """
    conversions = {
        SECONDS: time,
        MINUTES: convert_minutes_to_seconds(time),
        HOURS: convert_hours_to_seconds(time),
        DAYS: convert_days_to_seconds(time)
    }

    return conversions[unit]


def convert_seconds(seconds):
    """
    (int or float) -> str

    Takes a time in seconds and returns a string that rounds the time
    down to the most appropriate time unit.
    """
    if seconds < 60:
        return str(math.floor(seconds)) + ' s'
    elif 60 <= seconds < 3600:
        minutes = math.floor(convert_seconds_to_minutes(seconds))
        return str(minutes) + ' m'
    elif 3600 <= seconds < 86400:
        hours = math.floor(convert_seconds_to_hours(seconds))
        return str(hours) + ' h'
    else:
        days = math.floor(convert_seconds_to_days(seconds))
        return str(days) + ' d'


def get_year_month_day(date):
    """
    Takes a Date or a Datetime and returns a string in the form year-month-day
    (e.g., "2010-12-27").
    """
    new_date = datetime.date(date.year, date.month, date.day)
    return new_date.isoformat()


def ensure_tz_aware(date):
    """

    """
    if not date.tzinfo:
        date = date.replace(tzinfo=UTC_TZ)
    return date


def parse_date(date):
    """
    Takes a string and attempts to parse it as a date. If successful,
    returns a datetime object based on the string. Otherwise,
    returns None.
    """
    if isinstance(date, datetime.datetime):  # just in case...
        return date
    elif isinstance(date, str):
        try:
            parsed_date = dateutil.parser.parse(date)
            return ensure_tz_aware(parsed_date)
        except ValueError:
            try:
                return datetime.datetime.fromtimestamp(float(date), tz=UTC_TZ)
            except ValueError:
                return None
    else:
        return None


def format_date(date_string, date_format):
    """

    """
    formatted_date = datetime.datetime.strptime(date_string, date_format)

    year_directives = ['%y', '%Y', '%c', '%x']
    contains_year = any(directive in date_format for directive in year_directives)

    if not contains_year:
        utc_now = datetime.datetime.now(tz=UTC_TZ)
        formatted_date = formatted_date.replace(year=utc_now.year)

    return ensure_tz_aware(formatted_date)


def date_from_str(date_string, date_format=None):
    """

    """
    fail_msg = ('Could not parse the date string. '
                'Please check the date format')

    success_msg = ('Could not parse the date string using the given format, '
                   'so a different parser was used. Please check the date '
                   'format')

    if date_format:
        try:
            date = format_date(date_string, date_format)
        except ValueError as error:
            date = parse_date(date_string)
            if date:
                LOGGER.warning('%s: %s', success_msg, error)
            else:
                LOGGER.error('%s: %s', fail_msg, error)
    else:
        date = parse_date(date_string)
        if not date:
            LOGGER.error(fail_msg)

    return date
