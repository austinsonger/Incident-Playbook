from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django_q.tasks import async_task
from dfirtrack_main.async_messages import message_user
from dfirtrack_main.forms import TagCreatorForm
from dfirtrack_main.logger.default_logger import debug_logger, info_logger
from dfirtrack_main.models import Tag, System


@login_required(login_url="/login")
def tag_creator(request):
    """ function to create many tags for many systems at once (helper function to call the real function) """

    # form was valid to post
    if request.method == 'POST':

        # get objects from request object
        request_post = request.POST
        request_user = request.user

        # show immediate message for user
        messages.success(request, 'Tag creator started')

        # call async function
        async_task(
            "dfirtrack_main.creator.tag_creator.tag_creator_async",
            request_post,
            request_user,
        )

        # return directly to tag list
        return redirect(reverse('tag_list'))

    # show empty form
    else:
        form = TagCreatorForm()

        # call logger
        debug_logger(str(request.user), ' TAG_CREATOR_ENTERED')

    return render(request, 'dfirtrack_main/tag/tag_creator.html', {'form': form})

def tag_creator_async(request_post, request_user):
    """ function to create many tags for many systems at once """

    # call logger
    debug_logger(str(request_user), ' TAG_CREATOR_START')

    # extract tags (list results from request object via multiple choice field)
    tags = request_post.getlist('tag')

    # extract systems (list results from request object via multiple choice field)
    systems = request_post.getlist('system')

    # set tags_created_counter (needed for messages)
    tags_created_counter = 0

    # set system_tags_created_counter (needed for messages)
    system_tags_created_counter = 0

    # iterate over systems
    for system_id in systems:

        # autoincrement counter
        system_tags_created_counter  += 1

        # iterate over tags
        for tag_id in tags:

            # create form with request data
            form = TagCreatorForm(request_post)

            # create relation
            if form.is_valid():

                """ object creation """

                # get objects
                system = System.objects.get(system_id=system_id)
                tag = Tag.objects.get(tag_id=tag_id)

                # add tag to system
                system.tag.add(tag)

                """ object counter / log """

                # autoincrement counter
                tags_created_counter  += 1

                # call logger
                system.logger( str(request_user), ' TAG_CREATOR_EXECUTED')

    """ finish tag importer """

    # call final message
    message_user(
        request_user,
        f'{tags_created_counter} tags created for {system_tags_created_counter} systems.',
        constants.SUCCESS
    )

    # call logger
    info_logger(
        str(request_user),
        f' TAG_CREATOR_STATUS'
        f' tags_created:{tags_created_counter}'
        f'|systems_affected:{system_tags_created_counter}'
    )

    # call logger
    debug_logger(str(request_user), ' TAG_CREATOR_END')
