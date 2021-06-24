from django.core.cache import cache
from django.contrib.messages import constants


def message_user(user, message, level=constants.INFO):
    """
    Send a message to a particular user.

    :param user: User instance
    :param message: Message to show
    :param level: Message level
    """
    # We store a list of messages in the cache so we can have multiple messages
    # queued up for a user.
    user_key = _user_key(user)
    messages = cache.get(user_key) or []
    messages.append((message, level))
    cache.set(user_key, messages)


def message_users(users, message, level=constants.INFO):
    """
    Send a message to a group of users.

    :param users: Users queryset
    :param message: Message to show
    :param level: Message level
    """
    for user in users:
        message_user(user, message, level)


def get_messages(user):
    """
    Fetch messages for given user.  Returns None if no such message exists.

    :param user: User instance
    """
    key = _user_key(user)
    result = cache.get(key)
    if result:
        cache.delete(key)
        return result
    return None


def _user_key(user):
    return '_async_message_%d' % user.pk
