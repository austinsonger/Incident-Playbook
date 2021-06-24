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
Tests the datetime module.
"""

# standard library
import datetime
from unittest import TestCase

# local
from utils.dateutils import dateutils as dt


class TestConversionsToMinutes(TestCase):
    """
    Tests conversions to minutes. 
    """

    def test_convert_hours_to_days(self):
        """
        Tests conversion from hours to minutes.
        """
        self.assertEqual(dt.convert_hours_to_days(0), 0)
        self.assertEqual(dt.convert_hours_to_days(12), 0.5)
        self.assertEqual(dt.convert_hours_to_days(24), 1)
        self.assertEqual(dt.convert_hours_to_days(36), 1.5)

    def test_convert_hours_to_minutes(self):
        """
        Tests conversion from hours to minutes.
        """
        self.assertEqual(dt.convert_hours_to_minutes(0), 0)
        self.assertEqual(dt.convert_hours_to_minutes(0.00050), 0.03)
        self.assertEqual(dt.convert_hours_to_minutes(1), 60)
        self.assertEqual(dt.convert_hours_to_minutes(24), 1440)

    def test_convert_hours_to_seconds(self):
        """
        Tests conversion from hours to seconds.
        """
        self.assertEqual(dt.convert_hours_to_seconds(0), 0)
        self.assertEqual(dt.convert_hours_to_seconds(0.5), 1800)
        self.assertEqual(dt.convert_hours_to_seconds(1), 3600)
        self.assertEqual(dt.convert_hours_to_seconds(24), 86400)

    def test_convert_days_to_minutes(self):
        """
        Tests conversion from days to minutes.
        """
        self.assertEqual(dt.convert_days_to_minutes(0), 0)
        self.assertEqual(dt.convert_days_to_minutes(0.5), 720)
        self.assertEqual(dt.convert_days_to_minutes(1), 1440)

    def test_convert_days_to_seconds(self):
        """
        Tests conversion from days to seconds.
        """
        self.assertEqual(dt.convert_days_to_seconds(0), 0)
        self.assertEqual(dt.convert_days_to_seconds(0.5), 43200)
        self.assertEqual(dt.convert_days_to_seconds(1), 86400)

    def test_convert_seconds_to_minutes(self):
        """
        Tests conversion from seconds to minutes.
        """
        self.assertEqual(dt.convert_seconds_to_minutes(0), 0)
        self.assertEqual(dt.convert_seconds_to_minutes(30), 0.5)
        self.assertEqual(dt.convert_seconds_to_minutes(60), 1)

    def test_convert_minutes_to_seconds(self):
        """
        Tests conversion from minutes to seconds.
        """
        self.assertEqual(dt.convert_minutes_to_seconds(0), 0)
        self.assertEqual(dt.convert_minutes_to_seconds(0.005), 0.3)
        self.assertEqual(dt.convert_minutes_to_seconds(1.5), 90)

    def test_convert_minutes_to_hours(self):
        """
        Tests conversion from minutes to hours.
        """
        self.assertEqual(dt.convert_minutes_to_hours(0), 0)
        self.assertEqual(dt.convert_minutes_to_hours(30), 0.5)
        self.assertEqual(dt.convert_minutes_to_hours(60), 1)

    def test_convert_minutes_to_days(self):
        """
        Tests conversion from minutes to days.
        """
        self.assertEqual(dt.convert_minutes_to_days(0), 0)
        self.assertEqual(dt.convert_minutes_to_days(360), 0.25)
        self.assertEqual(dt.convert_minutes_to_days(1440), 1)

    def test_convert_seconds_to_minutes(self):
        """
        Tests conversion from seconds to minutes.
        """
        self.assertEqual(dt.convert_seconds_to_minutes(0), 0)
        self.assertEqual(dt.convert_seconds_to_minutes(30), 0.5)
        self.assertEqual(dt.convert_seconds_to_minutes(60), 1)

    def test_convert_seconds_to_hours(self):
        """
        Tests conversion from seconds to hours.
        """
        self.assertEqual(dt.convert_seconds_to_hours(0), 0)
        self.assertEqual(dt.convert_seconds_to_hours(1800), 0.5)
        self.assertEqual(dt.convert_seconds_to_hours(3600), 1)

    def test_convert_seconds_to_days(self):
        """
        Tests conversion from seconds to days.
        """
        self.assertEqual(dt.convert_seconds_to_days(0), 0)
        self.assertEqual(dt.convert_seconds_to_days(21600), 0.25)
        self.assertEqual(dt.convert_seconds_to_days(86400), 1)


class ConvertToWholeMinutesTestCase(TestCase):
    """
    Tests the convert_time_to_whole_minutes function.
    """

    def test_convert_secs_to_whole_mins(self):
        """
        Tests conversion of seconds to whole minutes.
        """
        self.assertEqual(dt.convert_time_to_whole_minutes(0, dt.SECONDS), 0)
        self.assertEqual(dt.convert_time_to_whole_minutes(0.1, dt.SECONDS), 1)
        self.assertEqual(dt.convert_time_to_whole_minutes(30, dt.SECONDS), 1)
        self.assertEqual(dt.convert_time_to_whole_minutes(60, dt.SECONDS), 1)
        self.assertEqual(dt.convert_time_to_whole_minutes(61, dt.SECONDS), 2)

    def test_convert_mins_to_whole_mins(self):
        """
        Tests conversion of minutes to whole minutes.
        """
        self.assertEqual(dt.convert_time_to_whole_minutes(0, dt.MINUTES), 0)
        self.assertEqual(dt.convert_time_to_whole_minutes(0.5, dt.MINUTES), 1)
        self.assertEqual(dt.convert_time_to_whole_minutes(60, dt.MINUTES), 60)
        self.assertEqual(dt.convert_time_to_whole_minutes(60.1, dt.MINUTES), 61)

    def test_convert_hrs_to_whole_mins(self):
        """
        Tests conversion of hours to whole minutes.
        """
        self.assertEqual(dt.convert_time_to_whole_minutes(0, dt.HOURS), 0)
        self.assertEqual(dt.convert_time_to_whole_minutes(0.31, dt.HOURS), 19)
        self.assertEqual(dt.convert_time_to_whole_minutes(1, dt.HOURS), 60)
        self.assertEqual(dt.convert_time_to_whole_minutes(24, dt.HOURS), 1440)

    def test_convert_days_to_whole_mins(self):
        """
        Tests conversion of days to whole minutes.
        """
        self.assertEqual(dt.convert_time_to_whole_minutes(0, dt.DAYS), 0)
        self.assertEqual(dt.convert_time_to_whole_minutes(0.33, dt.DAYS), 476)
        self.assertEqual(dt.convert_time_to_whole_minutes(1, dt.DAYS), 1440)
        self.assertEqual(dt.convert_time_to_whole_minutes(30, dt.DAYS), 43200)


class ConvertToWholeMinutesTestCase(TestCase):
    """
    Tests the convert_time_to_seconds function.
    """

    def test_convert_secs_to_secs(self):
        """
        Tests conversion of seconds to seconds.
        """
        self.assertEqual(dt.convert_time_to_seconds(0, dt.SECONDS), 0)
        self.assertEqual(dt.convert_time_to_seconds(0.1, dt.SECONDS), 0.1)
        self.assertEqual(dt.convert_time_to_seconds(30, dt.SECONDS), 30)
        self.assertEqual(dt.convert_time_to_seconds(60, dt.SECONDS), 60)
        self.assertEqual(dt.convert_time_to_seconds(61, dt.SECONDS), 61)

    def test_convert_mins_to_secs(self):
        """
        Tests conversion of minutes to seconds.
        """
        self.assertEqual(dt.convert_time_to_seconds(0, dt.MINUTES), 0)
        self.assertEqual(dt.convert_time_to_seconds(0.5, dt.MINUTES), 30)
        self.assertEqual(dt.convert_time_to_seconds(60, dt.MINUTES), 3600)
        self.assertEqual(dt.convert_time_to_seconds(60.1, dt.MINUTES), 3606)

    def test_convert_hrs_to_secs(self):
        """
        Tests conversion of hours to seconds.
        """
        self.assertEqual(dt.convert_time_to_seconds(0, dt.HOURS), 0)
        self.assertEqual(dt.convert_time_to_seconds(0.31, dt.HOURS), 1116)
        self.assertEqual(dt.convert_time_to_seconds(1, dt.HOURS), 3600)
        self.assertEqual(dt.convert_time_to_seconds(24, dt.HOURS), 86400)

    def test_convert_days_to_secs(self):
        """
        Tests conversion of days to seconds.
        """
        self.assertEqual(dt.convert_time_to_seconds(0, dt.DAYS), 0)
        self.assertEqual(dt.convert_time_to_seconds(0.33, dt.DAYS), 28512)
        self.assertEqual(dt.convert_time_to_seconds(1, dt.DAYS), 86400)
        self.assertEqual(dt.convert_time_to_seconds(30, dt.DAYS), 2592000)


class ConvertSecondsTestCase(TestCase):
    """
    Tests the convert_seconds function.
    """

    def test_convert_seconds(self):
        """
        Tests convert_seconds function.
        """
        self.assertEqual(dt.convert_seconds(30), '30 s')
        self.assertEqual(dt.convert_seconds(60), '1 m')
        self.assertEqual(dt.convert_seconds(3599), '59 m')
        self.assertEqual(dt.convert_seconds(3600), '1 h')
        self.assertEqual(dt.convert_seconds(86399), '23 h')
        self.assertEqual(dt.convert_seconds(86400), '1 d')


class GetYearMonthDayTestCase(TestCase):
    """
    Tests the get_year_month_day function.
    """

    def test_date(self):
        """
        Tests the get_year_month_day function with a Date object.
        """
        date = datetime.date(2015, 4, 2)
        self.assertTrue(dt.get_year_month_day(date), '2015-04-02')

    def test_datetime(self):
        """
        Tests the get_year_month_day function with a Datetime object.
        """
        date = datetime.datetime(2015, 4, 2)
        self.assertTrue(dt.get_year_month_day(date), '2015-04-02')



class ParseDateTestCase(TestCase):
    """
    Tests the parse_date function.
    """

    def test_email_date(self):
        """
        Tests the parse_date function for a date from an email.
        """
        date = 'Tue, 8 Sep 2015 16:08:59 -0400'
        actual = dt.parse_date(date)
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual), '2015-09-08 16:08:59-04:00')

    def test_no_tz(self):
        """
        Tests the parse_date function for a timezone naive date.
        """
        date = 'Tue, 8 Sep 2015 16:08:59'
        actual = dt.parse_date(date)
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual), '2015-09-08 16:08:59+00:00')

    def test_timestamp(self):
        """
        Tests the parse_date function for a timestamp string.
        """
        actual = dt.parse_date('1444316990')
        self.assertTrue(isinstance(actual, datetime.datetime))
        self.assertEqual(str(actual), '2015-10-08 15:09:50+00:00')

    def test_bad_string(self):
        """
        Tests the parse_date function for a non-date string.
        """
        self.assertEqual(dt.parse_date('foobar'), None)

    def test_datetime(self):
        """
        Tests the parse_date function with a datetime object.
        """
        date = datetime.datetime.now()
        self.assertTrue(dt.parse_date(date), date)

    def test_nonstring_nondate(self):
        """
        Tests the parse_date function for non-string/non-datetime
        inputs.
        """
        self.assertEqual(dt.parse_date(100), None)
        self.assertEqual(dt.parse_date(100.0), None)

    def test_twitter_date(self):
        """
        Tests the parse_date function for date from a tweet.
        """
        date_str = 'Wed Sep 21 23:55:07 +0000 2016'
        actual = dt.parse_date(date_str)
        self.assertEqual(actual.year, 2016)
        self.assertEqual(actual.month, 9)
        self.assertEqual(actual.day, 21)   


class FormatDateTestCase(TestCase):
    """
    Tests the format_date function.
    """

    def test_year_without_century(self):
        """
        Tests the format_date function for %y.
        """
        date_str = '08-16-88'
        date_format = '%m-%d-%y'
        actual = dt.format_date(date_str, date_format)
        self.assertEqual(actual.year, 1988)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 16)

    def test_year_with_century(self):
        """
        Tests the format_date function for %Y.
        """
        date_str = '1988-08-16'
        date_format = '%Y-%m-%d'
        actual = dt.format_date(date_str, date_format)
        self.assertEqual(actual.year, 1988)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 16)

    def test_locale_datetime(self):
        """
        Tests the format_date function for %c.
        """
        date_str = 'Tue Aug 16 21:30:00 1988'
        date_format = '%c'
        actual = dt.format_date(date_str, date_format)
        self.assertEqual(actual.year, 1988)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 16)

    def test_locale_date(self):
        """
        Tests the format_date function for %x.
        """
        date_str = '08/16/88'
        date_format = '%x'
        actual = dt.format_date(date_str, date_format)
        self.assertEqual(actual.year, 1988)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 16)
        self.assertEqual(str(actual.tzinfo), 'UTC')

    def test_no_year(self):
        """
        Tests the format_date function for a date without a year.
        """
        date_str = 'Aug 16 20:16:38'
        date_format = '%b %d %X'
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        actual = dt.format_date(date_str, date_format)
        self.assertEqual(actual.year, utc_now.year)
        self.assertEqual(actual.month, 8)
        self.assertEqual(actual.day, 16)     

