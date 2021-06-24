from django.contrib.messages import constants
from dfirtrack_main.async_messages import message_user


def final_messages(systems_touched_counter, systems_skipped_counter, lines_faulty_counter, skipped_systems, number_of_lines, request_user):
    """ final messages for 'system_creator' and 'system_modificator' """

    # number messages

    if systems_touched_counter > 0:
        if systems_touched_counter  == 1:
            message_user(
                request_user,
                f'{systems_touched_counter} system was created / modified.',
                constants.SUCCESS
            )
        else:
            message_user(
                request_user,
                f'{systems_touched_counter} systems were created / modified.',
                constants.SUCCESS
            )

    if systems_skipped_counter > 0:
        if systems_skipped_counter  == 1:
            message_user(
                request_user,
                f'{systems_skipped_counter} system was skipped. {skipped_systems}',
                constants.WARNING
            )
        else:
            message_user(
                request_user,
                f'{systems_skipped_counter} systems were skipped. {skipped_systems}',
                constants.WARNING
            )

    if lines_faulty_counter > 0:
        if lines_faulty_counter  == 1:
            message_user(
                request_user,
                f'{lines_faulty_counter} line out of {number_of_lines} lines was faulty (see log file for details).',
                constants.WARNING
            )
        else:
            message_user(
                request_user,
                f'{lines_faulty_counter} lines out of {number_of_lines} lines were faulty (see log file for details).',
                constants.WARNING
            )

    # return to 'system_creator' and 'system_modificator'
    return
