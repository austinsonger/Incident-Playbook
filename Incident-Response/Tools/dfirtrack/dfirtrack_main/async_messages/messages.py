from django.contrib.messages import constants
from . import message_user

"""
Mimic the django.contrib.messages API
"""


def debug(user, message):
    """
    Adds a message with the ``DEBUG`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.DEBUG)


def info(user, message):
    """
    Adds a message with the ``INFO`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.INFO)


def success(user, message):
    """
    Adds a message with the ``SUCCESS`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.SUCCESS)


def warning(user, message):
    """
    Adds a message with the ``WARNING`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.WARNING)


def error(user, message):
    """
    Adds a message with the ``ERROR`` level.

    :param user: User instance
    :param message: Message to show
    """
    message_user(user, message, constants.ERROR)
