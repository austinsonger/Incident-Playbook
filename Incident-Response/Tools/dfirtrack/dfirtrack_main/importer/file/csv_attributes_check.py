from django.contrib import messages
from dfirtrack_main.logger.default_logger import warning_logger
from dfirtrack_main.models import Ip
import ipaddress


def check_and_create_ip(ip_ip, model, row_counter, request=None):
    """ check IPs for valid values """

    """ set username for logger """

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        logger_username = model.csv_import_username.username

    """ perform checks """

    # value is an IP
    try:

        # check ip column for IP(s)
        ipaddress.ip_address(ip_ip)

        # create ip
        ip, created = Ip.objects.get_or_create(ip_ip=ip_ip)
        # IP was created
        if created:
            # call logger
            ip.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_IP_CREATED')

        # return IP to 'csv_attributes_add.add_many2many_attributes'
        return ip

    # value is not an IP
    except ValueError:

        # if function was called from 'system_instant' and 'system_upload'
        if request:
            # call message
            messages.warning(request, f'Value for IP address in row {row_counter} was not a valid IP address.')

        # call logger
        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_IP_COLUMN row_{row_counter}:invalid_ip')

        # return nothing to 'csv_attributes_add.add_many2many_attributes'
        return None

def check_system_name(model, row, row_counter, request=None):
    """ check system name for valid value """

    # reset continue condition
    stop_system_importer_file_csv = False

    """ set username for logger """

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        logger_username = model.csv_import_username.username

    """ perform checks (for system_name, return immediately) """

    # check for index error
    try:
        system_name = row[model.csv_column_system - 1]
    except IndexError:
        # if function was called from 'system_instant' and 'system_upload'
        if request:
            # call message
            messages.warning(request, f'Index for system in row {row_counter} was out of range. System not created.')
        # call logger
        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SYSTEM_COLUMN row_{row_counter}:out_of_range')
        # set stop condition
        stop_system_importer_file_csv = True
        # return stop condition to 'csv_main.system_handler'
        return stop_system_importer_file_csv

    """ perform checks (remaining checks, need system_name) """

    # check system column for empty string
    if not system_name:
        # if function was called from 'system_instant' and 'system_upload'
        if request:
            # call message
            messages.warning(request, f'Value for system in row {row_counter} was an empty string. System not created.')
        # call logger
        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SYSTEM_COLUMN row_{row_counter}:empty_column')
        # set stop condition
        stop_system_importer_file_csv = True

    # check system column for length of string
    if len(system_name) > 50:
        # if function was called from 'system_instant' and 'system_upload'
        if request:
            # call message
            messages.warning(request, f'Value for system in row {row_counter} was too long. System not created.')
        # call logger
        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SYSTEM_COLUMN row_{row_counter}:long_string')
        # set stop condition
        stop_system_importer_file_csv = True

    # return stop condition to 'csv_main.system_handler'
    return stop_system_importer_file_csv
