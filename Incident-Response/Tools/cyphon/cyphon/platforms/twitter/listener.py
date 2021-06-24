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
Defines a custom listener for a Twitter Stream.
"""

# standard
import json
import logging

# third party
from django.conf import settings
from tweepy.streaming import StreamListener

LOGGER = logging.getLogger(__name__)

DATA_LIMIT = float('inf')
TEST_LIMIT = 10     # number of tweets to save while running tests

# if running tests, use test limit
if settings.TEST:
    LIMIT = TEST_LIMIT
else:
    LIMIT = DATA_LIMIT


class CustomStreamListener(StreamListener):
    """
    A listener handles tweets as they are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, faucet):
        super(CustomStreamListener, self).__init__()
        self.faucet = faucet
        self.status_code = None
        self.notes = None
        self.data_count = 0
        self.saved_data_count = 0

    def _process_response(self, data):
        """
        Takes data received from a Twitter Stream and saves it using the
        CustomStreamListener's api_handler. If the DATA_LIMIT has been reached,
        return False to stop the stream. Otherwise returns the doc_id of the
        distilled data.
        """
        self.status_code = '200'
        self.faucet.load_cargo([data])
        self.faucet.process_results()
        self.saved_data_count += 1

        # disconnect the stream if another stream has been started
        if self.faucet.is_obsolete():
            return False
        else:
            # disconnect the stream if enough data has been gathered
            return self.saved_data_count < LIMIT

    def on_data(self, raw_data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        try:
            data = json.loads(raw_data)
            self.data_count += 1

            if 'in_reply_to_status_id' in data:
                return self.on_status(data)
            elif 'delete' in data:
                delete = data['delete']['status']
                return self.on_delete(delete['id'], delete['user_id'])
            elif 'event' in data:
                return self.on_event(data)
            elif 'direct_message' in data:
                return self.on_direct_message(data)
            elif 'friends' in data:
                return self.on_friends(data['friends'])
            elif 'limit' in data:
                return self.on_limit(data['limit']['track'])
            elif 'disconnect' in data:
                return self.on_disconnect(data['disconnect'])
            elif 'warning' in data:
                return self.on_warning(data['warning'])
            else:
                LOGGER.error("Unknown message type: " + str(raw_data))

        except TypeError as error:
            LOGGER.error('The message could not be loaded: %s', error)

    @staticmethod
    def keep_alive():
        """Called when a keep-alive arrived"""
        return True

    def on_status(self, status):
        """Called when a new status arrives"""
        return self._process_response(status)

    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        msg = 'An error occurred with the Twitter stream: %s' % exception
        self.notes = msg
        LOGGER.error(msg)
        return False

    @staticmethod
    def on_delete(status_id, user_id):
        """Called when a delete notice arrives for a status"""

        #TODO(LH): handle deleted tweets
        LOGGER.warning('User %s has deleted the tweet %s', user_id, status_id)
        return True

    def on_event(self, status):
        """Called when a new event arrives"""
        return self._process_response(status)

    def on_direct_message(self, status):
        """Called when a new direct message arrives"""
        return self._process_response(status)

    @staticmethod
    def on_friends(friends):
        """Called when a friends list arrives.

        friends is a list that contains user_id
        """
        return True

    @staticmethod
    def on_limit(track):
        """Called when a limitation notice arrives"""
        LOGGER.warning('Twitter limitation notice: %s', track)
        return True

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        msg = 'An error occurred with the Twitter stream'
        self.notes = msg
        self.status_code = status_code
        LOGGER.error('%s: %s', msg, status_code)
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        msg = 'The Twitter stream has timed out.'
        self.notes = msg
        LOGGER.error(msg)
        return False

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice

        Disconnect codes are listed here:
        https://dev.twitter.com/docs/streaming-apis/messages#Disconnect_messages_disconnect
        """
        msg = 'The Twitter stream has been disconnected: %s' % notice
        self.notes = msg
        LOGGER.error(msg)
        return False

    @staticmethod
    def on_warning(notice):
        """Called when a disconnection warning message arrives"""
        LOGGER.warning('Twitter disconnection warning: %s', notice)
        return True
