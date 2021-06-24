from django.contrib import messages
from dfirtrack_config.models import MainConfigModel
from dfirtrack_main.importer.file.csv_messages import error_message_cron
from dfirtrack_main.logger.default_logger import error_logger
import os


def check_config_cron_user(model, request=None):
    """ check config user  """

    # reset stop condition
    stop_system_importer_file_csv = False

    # check for csv_import_username (after initial migration w/o user defined) - stop immediately
    if not model.csv_import_username:
        # if function was called from 'system_create_cron' (creating scheduled task)
        if request:
            # call message
            messages.error(request, 'No user for import defined. Check config!')
            # get username (needed for logger)
            logger_username = str(request.user)
        # if function was called from 'system_cron' (scheduled task)
        else:
            # call message for all users
            error_message_cron('No user for import defined. Check config!')
            # get main config model
            mainconfigmodel = MainConfigModel.objects.get(main_config_name = 'MainConfig')
            # get cron username from main config (needed for logger if no user was defined in the proper config)
            logger_username = mainconfigmodel.cron_username
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_NO_USER_DEFINED')
        # set stop condition
        stop_system_importer_file_csv = True

    # return stop condition to 'csv.system_create_cron' or 'csv.system_cron'
    return stop_system_importer_file_csv

def check_content_file_system(model, request=None):
    """ check file system """

    # reset stop condition
    stop_system_importer_file_csv = False

    """ set username for logger """

    # if function was called from 'system_instant'
    if request:
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        logger_username = model.csv_import_username.username   # check for existence of user in config was done before

    # build csv file path
    csv_import_file = model.csv_import_path + '/' + model.csv_import_filename

    # CSV import path does not exist - stop immediately
    if not os.path.isdir(model.csv_import_path):
        # if function was called from 'system_instant'
        if request:
            # call messsage
            messages.error(request, 'CSV import path does not exist. Check config or file system!')
        # if function was called from 'system_cron'
        else:
            # call message for all users
            error_message_cron('CSV import path does not exist. Check config or file system!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_PATH_NOT_EXISTING')
        # set stop condition
        stop_system_importer_file_csv = True
    else:
        # no read permission for CSV import path - stop immediately
        if not os.access(model.csv_import_path, os.R_OK):
            # if function was called from 'system_instant'
            if request:
                # call messsage
                messages.error(request, 'No read permission for CSV import path. Check config or file system!')
            # if function was called from 'system_cron'
            else:
                # call message for all users
                error_message_cron('No read permission for CSV import path. Check config or file system!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_PATH_NO_READ_PERMISSION')
            # set stop condition
            stop_system_importer_file_csv = True
        else:
            # CSV import file does not exist - stop immediately
            if not os.path.isfile(csv_import_file):
                # if function was called from 'system_instant'
                if request:
                    # call messsage
                    messages.error(request, 'CSV import file does not exist. Check config or provide file!')
                # if function was called from 'system_cron'
                else:
                    # call message for all users
                    error_message_cron('CSV import file does not exist. Check config or provide file!')
                # call logger
                error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_FILE_NOT_EXISTING')
                # set stop condition
                stop_system_importer_file_csv = True
            else:
                # no read permission for CSV import file - stop immediately
                if not os.access(csv_import_file, os.R_OK):
                    # if function was called from 'system_instant'
                    if request:
                        # call messsage
                        messages.error(request, 'No read permission for CSV import file. Check config or file system!')
                    # if function was called from 'system_cron'
                    else:
                        # call message for all users
                        error_message_cron('No read permission for CSV import file. Check config or file system!')
                    # call logger
                    error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_FILE_NO_READ_PERMISSION')
                    # set stop condition
                    stop_system_importer_file_csv = True
                else:
                    # CSV import file is empty - stop immediately
                    if os.path.getsize(csv_import_file) == 0:
                        # if function was called from 'system_instant'
                        if request:
                            # call messsage
                            messages.error(request, 'CSV import file is empty. Check config or file system!')
                        # if function was called from 'system_cron'
                        else:
                            # call message for all users
                            error_message_cron('CSV import file is empty. Check config or file system!')
                        # call logger
                        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_FILE_EMPTY')
                        # set stop condition
                        stop_system_importer_file_csv = True

    # return stop condition to 'csv.system_create_cron' or 'csv.system_cron' or 'csv.system_instant'
    return stop_system_importer_file_csv

def check_config_attributes(model, request=None):
    """ check config for logic errors about attributes """

    # reset stop condition
    stop_system_importer_file_csv = False

    """ set username for logger """

    # if function was called from 'system_instant' or 'system_upload' or 'system_create_cron'
    if request:
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        logger_username = model.csv_import_username.username   # check for existence of user in config was done before

    """ check numeric values for column fields """

    # CSV_COLUMN_SYSTEM
    if not 1 <= model.csv_column_system <= 99:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, '`CSV_COLUMN_SYSTEM` is outside the allowed range. Check config!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_SYSTEM out of range')
        # set stop condition
        stop_system_importer_file_csv = True

    # CSV_COLUMN_IP
    if model.csv_column_ip:
        # check CSV_COLUMN_IP for value
        if not 1 <= model.csv_column_ip <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_IP` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_IP out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_DNSNAME
    if model.csv_column_dnsname:
        # check CSV_COLUMN_DNSNAME for value
        if not 1 <= model.csv_column_dnsname <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_DNSNAME` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_DNSNAME out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_DOMAIN
    if model.csv_column_domain:
        # check CSV_COLUMN_DOMAIN for value
        if not 1 <= model.csv_column_domain <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_DOMAIN` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_DOMAIN out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_LOCATION
    if model.csv_column_location:
        # check CSV_COLUMN_LOCATION for value
        if not 1 <= model.csv_column_location <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_LOCATION` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_LOCATION out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_OS
    if model.csv_column_os:
        # check CSV_COLUMN_OS for value
        if not 1 <= model.csv_column_os <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_OS` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_OS out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_REASON
    if model.csv_column_reason:
        # check CSV_COLUMN_REASON for value
        if not 1 <= model.csv_column_reason <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_REASON` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_REASON out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_RECOMMENDATION
    if model.csv_column_recommendation:
        # check CSV_COLUMN_RECOMMENDATION for value
        if not 1 <= model.csv_column_recommendation <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_RECOMMENDATION` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_RECOMMENDATION out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_SERVICEPROVIDER
    if model.csv_column_serviceprovider:
        # check CSV_COLUMN_SERVICEPROVIDER for value
        if not 1 <= model.csv_column_serviceprovider <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_SERVICEPROVIDER` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_SERVICEPROVIDER out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_SYSTEMTYPE
    if model.csv_column_systemtype:
        # check CSV_COLUMN_SYSTEMTYPE for value
        if not 1 <= model.csv_column_systemtype <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_SYSTEMTYPE` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_SYSTEMTYPE out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_CASE
    if model.csv_column_case:
        # check CSV_COLUMN_CASE for value
        if not 1 <= model.csv_column_case <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_CASE` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_CASE out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_COMPANY
    if model.csv_column_company:
        # check CSV_COLUMN_COMPANY for value
        if not 1 <= model.csv_column_company <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_COMPANY` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_COMPANY out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    # CSV_COLUMN_TAG
    if model.csv_column_tag:
        # check CSV_COLUMN_TAG for value
        if not 1 <= model.csv_column_tag <= 99:
            # if function was called from 'system_instant' or 'system_upload'
            if request:
                # call message
                messages.error(request, '`CSV_COLUMN_TAG` is outside the allowed range. Check config!')
            # call logger
            error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV variable CSV_COLUMN_TAG out of range')
            # set stop condition
            stop_system_importer_file_csv = True

    """ check for EITHER 'choice' and 'column' OR 'default' """

    # reset error condition
    attribute_error = False

    # set error counter
    attribute_error_counter = 0

    # create empty list for error IDs
    attribute_error_id = []

    # ip - CSV chosen and no CSV column filled out
    if model.csv_choice_ip and not model.csv_column_ip:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('ip_01')
    # ip - CSV not chosen and CSV column filled out
    if not model.csv_choice_ip and model.csv_column_ip:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('ip_02')

    # dnsname - CSV chosen and no CSV column filled out
    if model.csv_choice_dnsname and not model.csv_column_dnsname:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('dnsname_01')
    # dnsname - CSV not chosen and CSV column filled out
    if not model.csv_choice_dnsname and model.csv_column_dnsname:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('dnsname_02')
    # dnsname - CSV chosen and DB chosen
    if model.csv_choice_dnsname and model.csv_default_dnsname:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('dnsname_03')
    # dnsname - CSV column filled out and DB chosen
    if model.csv_column_dnsname and model.csv_default_dnsname:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('dnsname_04')

    # domain - CSV chosen and no CSV column filled out
    if model.csv_choice_domain and not model.csv_column_domain:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('domain_01')
    # domain - CSV not chosen and CSV column filled out
    if not model.csv_choice_domain and model.csv_column_domain:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('domain_02')
    # domain - CSV chosen and DB chosen
    if model.csv_choice_domain and model.csv_default_domain:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('domain_03')
    # domain - CSV column filled out and DB chosen
    if model.csv_column_domain and model.csv_default_domain:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('domain_04')

    # location - CSV chosen and no CSV column filled out
    if model.csv_choice_location and not model.csv_column_location:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('location_01')
    # location - CSV not chosen and CSV column filled out
    if not model.csv_choice_location and model.csv_column_location:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('location_02')
    # location - CSV chosen and DB chosen
    if model.csv_choice_location and model.csv_default_location:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('location_03')
    # location - CSV column filled out and DB chosen
    if model.csv_column_location and model.csv_default_location:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('location_04')

    # os - CSV chosen and no CSV column filled out
    if model.csv_choice_os and not model.csv_column_os:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('os_01')
    # os - CSV not chosen and CSV column filled out
    if not model.csv_choice_os and model.csv_column_os:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('os_02')
    # os - CSV chosen and DB chosen
    if model.csv_choice_os and model.csv_default_os:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('os_03')
    # os - CSV column filled out and DB chosen
    if model.csv_column_os and model.csv_default_os:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('os_04')

    # reason - CSV chosen and no CSV column filled out
    if model.csv_choice_reason and not model.csv_column_reason:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('reason_01')
    # reason - CSV not chosen and CSV column filled out
    if not model.csv_choice_reason and model.csv_column_reason:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('reason_02')
    # reason - CSV chosen and DB chosen
    if model.csv_choice_reason and model.csv_default_reason:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('reason_03')
    # reason - CSV column filled out and DB chosen
    if model.csv_column_reason and model.csv_default_reason:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('reason_04')

    # recommendation - CSV chosen and no CSV column filled out
    if model.csv_choice_recommendation and not model.csv_column_recommendation:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('recommendation_01')
    # recommendation - CSV not chosen and CSV column filled out
    if not model.csv_choice_recommendation and model.csv_column_recommendation:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('recommendation_02')
    # recommendation - CSV chosen and DB chosen
    if model.csv_choice_recommendation and model.csv_default_recommendation:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('recommendation_03')
    # recommendation - CSV column filled out and DB chosen
    if model.csv_column_recommendation and model.csv_default_recommendation:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('recommendation_04')

    # serviceprovider - CSV chosen and no CSV column filled out
    if model.csv_choice_serviceprovider and not model.csv_column_serviceprovider:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('serviceprovider_01')
    # serviceprovider - CSV not chosen and CSV column filled out
    if not model.csv_choice_serviceprovider and model.csv_column_serviceprovider:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('serviceprovider_02')
    # serviceprovider - CSV chosen and DB chosen
    if model.csv_choice_serviceprovider and model.csv_default_serviceprovider:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('serviceprovider_03')
    # serviceprovider - CSV column filled out and DB chosen
    if model.csv_column_serviceprovider and model.csv_default_serviceprovider:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('serviceprovider_04')

    # systemtype - CSV chosen and no CSV column filled out
    if model.csv_choice_systemtype and not model.csv_column_systemtype:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('systemtype_01')
    # systemtype - CSV not chosen and CSV column filled out
    if not model.csv_choice_systemtype and model.csv_column_systemtype:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('systemtype_02')
    # systemtype - CSV chosen and DB chosen
    if model.csv_choice_systemtype and model.csv_default_systemtype:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('systemtype_03')
    # systemtype - CSV column filled out and DB chosen
    if model.csv_column_systemtype and model.csv_default_systemtype:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('systemtype_04')

    # case - CSV chosen and no CSV column filled out
    if model.csv_choice_case and not model.csv_column_case:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('case_01')
    # case - CSV not chosen and CSV column filled out
    if not model.csv_choice_case and model.csv_column_case:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('case_02')
    # case - CSV chosen and DB chosen
    if model.csv_choice_case and model.csv_default_case.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('case_03')
    # case - CSV column filled out and DB chosen
    if model.csv_column_case and model.csv_default_case.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('case_04')

    # company - CSV chosen and no CSV column filled out
    if model.csv_choice_company and not model.csv_column_company:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('company_01')
    # company - CSV not chosen and CSV column filled out
    if not model.csv_choice_company and model.csv_column_company:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('company_02')
    # company - CSV chosen and DB chosen
    if model.csv_choice_company and model.csv_default_company.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('company_03')
    # company - CSV column filled out and DB chosen
    if model.csv_column_company and model.csv_default_company.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('company_04')

    # tag - CSV chosen and no CSV column filled out
    if model.csv_choice_tag and not model.csv_column_tag:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('tag_01')
    # tag - CSV not chosen and CSV column filled out
    if not model.csv_choice_tag and model.csv_column_tag:
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('tag_02')
    # tag - CSV chosen and DB chosen
    if model.csv_choice_tag and model.csv_default_tag.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('tag_03')
    # tag - CSV column filled out and DB chosen
    if model.csv_column_tag and model.csv_default_tag.all():
        # set attribute error
        attribute_error = True
        # autoincrement counter
        attribute_error_counter += 1
        # add error code
        attribute_error_id.append('tag_04')

    # check previous checks for error - one message / log for all
    if attribute_error:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            if attribute_error_counter == 1:
                # call message
                messages.error(request, f'There was {attribute_error_counter} error regarding attributes. Check config!')
            elif attribute_error_counter > 1:
                # call message
                messages.error(request, f'There were {attribute_error_counter} errors regarding attributes. Check config!')
        # call logger
        error_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV attributes misconfigured {attribute_error_id}')
        # set stop condition
        stop_system_importer_file_csv = True

    """ check tag pefix and delimiter in combination with CSV and DB """

    # tag - CSV chosen and prefix and / or prefix delimiter not set
    if model.csv_choice_tag and (not model.csv_tag_prefix or not model.csv_tag_prefix_delimiter):
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV tag prefix and / or tag delimiter not set')
        # set stop condition
        stop_system_importer_file_csv = True
    # tag - DB chosen and prefix and / or prefix delimiter chosen
    if model.csv_default_tag.all() and (model.csv_tag_prefix or model.csv_tag_prefix_delimiter):
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Prefix and delimiter are not available when setting tags from database.')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV tag prefix and / or tag delimiter not compatible with csv_default_tag')
        # set stop condition
        stop_system_importer_file_csv = True
    # tag - DB chosen but special option 'tag_remove_prefix' set
    if model.csv_remove_tag == 'tag_remove_prefix' and model.csv_default_tag.all():
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Removing tags with prefix is only available when setting tags from CSV.')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV remove tags with prefix not compatible with csv_default_tag')
        # set stop condition
        stop_system_importer_file_csv = True

    """ check tagfree choices (systemstatus / analysisstatus) in combination with tag from CSV """

    # tag - alternative choice systemstatus (tagfree) chosen without tag choice from CSV
    if model.csv_choice_tagfree_systemstatus and not model.csv_choice_tag:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Alternative systemstatus only available with tags from CSV.')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV tagfree systemstatus only compatible with csv_choice_tag')
        # set stop condition
        stop_system_importer_file_csv = True
    # tag - alternative choice analysisstatus (tagfree) chosen without tag choice from CSV
    if model.csv_choice_tagfree_analysisstatus and not model.csv_choice_tag:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Alternative analysisstatus only available with tags from CSV.')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV tagfree analysisstatus only compatible with csv_choice_tag')
        # set stop condition
        stop_system_importer_file_csv = True

    """ check if the column fields are different """

    # reset error condition
    column_error = False

    # create empty dict for column values
    all_columns_dict = {}

    # add column values to dict
    all_columns_dict['csv_column_system'] = model.csv_column_system
    if model.csv_column_ip:
        all_columns_dict['csv_column_ip'] = model.csv_column_ip
    if model.csv_column_dnsname:
        all_columns_dict['csv_column_dnsname'] = model.csv_column_dnsname
    if model.csv_column_domain:
        all_columns_dict['csv_column_domain'] = model.csv_column_domain
    if model.csv_column_location:
        all_columns_dict['csv_column_location'] = model.csv_column_location
    if model.csv_column_os:
        all_columns_dict['csv_column_os'] = model.csv_column_os
    if model.csv_column_reason:
        all_columns_dict['csv_column_reason'] = model.csv_column_reason
    if model.csv_column_recommendation:
        all_columns_dict['csv_column_recommendation'] = model.csv_column_recommendation
    if model.csv_column_serviceprovider:
        all_columns_dict['csv_column_serviceprovider'] = model.csv_column_serviceprovider
    if model.csv_column_systemtype:
        all_columns_dict['csv_column_systemtype'] = model.csv_column_systemtype
    if model.csv_column_case:
        all_columns_dict['csv_column_case'] = model.csv_column_case
    if model.csv_column_company:
        all_columns_dict['csv_column_company'] = model.csv_column_company
    if model.csv_column_tag:
        all_columns_dict['csv_column_tag'] = model.csv_column_tag

    # check all column values against each other
    for column in all_columns_dict:

        # explicitly copy dict
        pruned_columns_dict = dict(all_columns_dict)
        # remove column from copied dict
        del pruned_columns_dict[column]
        # check for the same value in pruned dict
        if all_columns_dict[column] in pruned_columns_dict.values():
            # set error condition
            column_error = True

    # check previous checks for error - one message / log for all
    if column_error:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'The columns have to be unique. Check config!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV columns not unique')
        # set stop condition
        stop_system_importer_file_csv = True

    """ check remove conditions in combination with skip condition """

    # reset error condition
    remove_error = False

    # remove systemstatus
    if model.csv_skip_existing_system and model.csv_remove_systemstatus:
        # set remove error
        remove_error = True
    # remove analysisstatus
    if model.csv_skip_existing_system and model.csv_remove_analysisstatus:
        # set remove error
        remove_error = True
    # remove ip
    if model.csv_skip_existing_system and model.csv_remove_ip:
        # set remove error
        remove_error = True
    # remove dnsname
    if model.csv_skip_existing_system and model.csv_remove_dnsname:
        # set remove error
        remove_error = True
    # remove domain
    if model.csv_skip_existing_system and model.csv_remove_domain:
        # set remove error
        remove_error = True
    # remove location
    if model.csv_skip_existing_system and model.csv_remove_location:
        # set remove error
        remove_error = True
    # remove os
    if model.csv_skip_existing_system and model.csv_remove_os:
        # set remove error
        remove_error = True
    # remove reason
    if model.csv_skip_existing_system and model.csv_remove_reason:
        # set remove error
        remove_error = True
    # remove recommendation
    if model.csv_skip_existing_system and model.csv_remove_recommendation:
        # set remove error
        remove_error = True
    # remove serviceprovider
    if model.csv_skip_existing_system and model.csv_remove_serviceprovider:
        # set remove error
        remove_error = True
    # remove systemtype
    if model.csv_skip_existing_system and model.csv_remove_systemtype:
        # set remove error
        remove_error = True
    # remove case
    if model.csv_skip_existing_system and model.csv_remove_case:
        # set remove error
        remove_error = True
    # remove company
    if model.csv_skip_existing_system and model.csv_remove_company:
        # set remove error
        remove_error = True

    # check previous checks for error - one message / log for all
    if remove_error:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'There is an error regarding removing existing attributes. Check config!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV remove attributes misconfigured ')
        # set stop condition
        stop_system_importer_file_csv = True

    """ check remove conditions without CSV or DB """

    # TODO: [code] add checks like in 'dfirtrack_config.forms'

    """ call single message (to avoid noise) for all users and return """

    # error occurred and function was called from 'system_cron'
    if stop_system_importer_file_csv and not request:
        # call message for all users
        error_message_cron('There was an error within the configuration. Check config!')

    # return stop condition to 'csv.system_create_cron' or 'csv.system_cron' or 'csv.system_instant' or 'csv.system_upload'
    return stop_system_importer_file_csv

def check_content_file_type(rows, logger_username, request=None):
    """ check file for csv respectively some kind of text file """

    try:
        # try to iterate over rows
        for row in rows:
            # do nothing
            pass

        # return True if successful to 'csv_main.system_handler'
        return True

    # wrong file type
    except UnicodeDecodeError:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'Wrong file type for CSV import. Check config or file system!')
        # if function was called from 'system_cron'
        else:
            # call message for all users
            error_message_cron('Wrong file type for CSV import. Check config or file system!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_WRONG_FILE_TYPE')
        # return False if not successful to 'csv_main.system_handler'
        return False

    # other file errors (e. g. file containing null bytes)
    except:
        # if function was called from 'system_instant' or 'system_upload'
        if request:
            # call message
            messages.error(request, 'File is corrupted. Check config or file system!')
        # if function was called from 'system_cron'
        else:
            # call message for all users
            error_message_cron('File is corrupted. Check config or file system!')
        # call logger
        error_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_CORRUPTED_FILE')
        # return False if not successful to 'csv_main.system_handler'
        return False
