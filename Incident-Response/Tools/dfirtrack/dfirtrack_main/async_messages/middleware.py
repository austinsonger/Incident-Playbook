from django.contrib import messages
from dfirtrack_main.async_messages import get_messages


def async_messages_middleware(get_response):

    def middleware(request):

        """ add code here to be executed for each request before the view (and later middleware) are called """

        # call the view
        response = get_response(request)

        """ add code here to be executed for each request/response after the view is called """

        # check the request for session attribute, user and authentication
        if hasattr(request, 'session') and hasattr(request, 'user') and request.user.is_authenticated:

            # get messages from cache
            msgs = get_messages(request.user)

            # if there were messages found in the cache
            if msgs:
                # iterate over messages
                for msg, level in msgs:
                    # add message to django's default messages framework to show them with next response
                    messages.add_message(request, level, msg)

        return response

    return middleware
