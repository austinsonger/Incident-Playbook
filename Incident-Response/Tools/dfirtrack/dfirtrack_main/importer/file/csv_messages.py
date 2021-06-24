from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.messages import constants
from dfirtrack_main.async_messages import message_users


def final_messages(systems_created_counter, systems_updated_counter, systems_skipped_counter, systems_multiple_counter, systems_multiple_list, request):
    """ final messages if function was called from 'system_instant' and 'system_upload' """

    # call final messages
    if systems_created_counter > 0:
        if systems_created_counter  == 1:
            messages.success(request, f'{systems_created_counter} system was created.')
        else:
            messages.success(request, f'{systems_created_counter} systems were created.')
    if systems_updated_counter > 0:
        if systems_updated_counter  == 1:
            messages.success(request, f'{systems_updated_counter} system was updated.')
        else:
            messages.success(request, f'{systems_updated_counter} systems were updated.')
    if systems_skipped_counter > 0:
        if systems_skipped_counter  == 1:
            messages.success(request, f'{systems_skipped_counter} system was skipped.')
        else:
            messages.success(request, f'{systems_skipped_counter} systems were skipped.')
    if systems_multiple_counter > 0:
        if systems_multiple_counter  == 1:
            messages.warning(request, f'{systems_multiple_counter} system was skipped because it existed several times. {systems_multiple_list}')
        else:
            messages.warning(request, f'{systems_multiple_counter} systems were skipped because they existed several times. {systems_multiple_list}')

    # return to 'csv_main.system_handler'
    return

def final_messages_cron(systems_created_counter, systems_updated_counter, systems_skipped_counter, systems_multiple_counter, systems_multiple_list, starttime, endtime):
    """ final messages if function was called from 'system_cron' (w/o request) """

    # get all users
    all_users = User.objects.all()

    # call message for all users
    message_users(
        all_users,
        f'System CSV importer:'
        f' created: {systems_created_counter}'
        f' | updated: {systems_updated_counter}'
        f' | skipped: {systems_skipped_counter}'
        f' | multiple: {systems_multiple_counter}'
        f' [{starttime} - {endtime}]',
        constants.SUCCESS
    )

    # show systems_multiple_list
    if systems_multiple_list:
        if systems_multiple_counter  == 1:
            # call message for all users
            message_users(
                all_users,
                f'{systems_multiple_counter} system was skipped because it existed several times. {systems_multiple_list}',
                constants.WARNING
            )
        else:
            # call message for all users
            message_users(
                all_users,
                f'{systems_multiple_counter} systems were skipped because they existed several times. {systems_multiple_list}',
                constants.WARNING
            )

    # return to 'csv_main.system_handler'
    return

def error_message_cron(message_text):
    """ error message for all users if function was called from 'system_cron' (w/o request) """

    # get all users
    all_users = User.objects.all()

    # call message for all users
    message_users(
        all_users,
        f'[Scheduled task CSV system importer] {message_text}',
        constants.ERROR
    )

    # return to calling function in 'csv_checks'
    return
