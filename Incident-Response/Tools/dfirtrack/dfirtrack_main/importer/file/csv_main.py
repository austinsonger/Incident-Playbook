import csv
from django.utils import timezone
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv_attributes_add import add_fk_attributes, add_many2many_attributes, create_lock_tags
from dfirtrack_main.importer.file.csv_attributes_check import check_system_name
from dfirtrack_main.importer.file.csv_checks import check_content_file_type
from dfirtrack_main.importer.file.csv_messages import final_messages, final_messages_cron
from dfirtrack_main.logger.default_logger import debug_logger, info_logger, warning_logger
from dfirtrack_main.models import System
from io import TextIOWrapper


def system_handler(request=None, uploadfile=False):

    # get config model
    model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

    """ set username for logger and object """

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        # get user for object
        csv_import_user = request.user
        # get user for logger
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        # get user for object
        csv_import_user = model.csv_import_username
        # get user for logger
        logger_username = model.csv_import_username.username

    """ start system importer """

    # get starttime
    starttime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    # call logger
    debug_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_START')

    # create lock tags
    create_lock_tags(model)

    """ file handling  """

    # file was uploaded via form (called via 'system_upload')
    if uploadfile:
        # text object can not be passed as argument from 'system_upload'
        systemcsv = TextIOWrapper(request.FILES['systemcsv'].file, encoding=request.encoding)
    # file was fetched from file system (called via 'system_instant' or 'system_cron')
    else:
        # build csv file path
        csv_import_file = model.csv_import_path + '/' + model.csv_import_filename
        # open file
        systemcsv = open(csv_import_file, 'r')

    # get field delimiter from config
    if model.csv_field_delimiter == 'field_comma':
        delimiter = ','
    elif model.csv_field_delimiter == 'field_semicolon':
        delimiter = ';'

    # get text quotechar from config
    if model.csv_text_quote == 'text_double_quotation_marks':
        quotechar = '"'
    elif model.csv_text_quote == 'text_single_quotation_marks':
        quotechar = "'"

    # read rows out of csv
    rows = csv.reader(systemcsv, delimiter=delimiter, quotechar=quotechar)

    """ check file """

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        # check file for csv respectively some kind of text file
        file_check = check_content_file_type(rows, logger_username, request)
    # if function was called from 'system_cron'
    else:
        # check file for csv respectively some kind of text file
        file_check = check_content_file_type(rows, logger_username)

    # leave system_importer_file_csv if file check throws errors
    if not file_check:
        # close file
        systemcsv.close()
        # return to calling function 'csv.system_cron' or 'csv.system_instant' or 'csv.system_upload'
        return

    # jump to begin of file again after iterating in file check
    systemcsv.seek(0)

    """ prepare loop """

    # set row_counter (needed for logger)
    row_counter = 1

    # set systems_created_counter (needed for logger)
    systems_created_counter = 0

    # set systems_updated_counter (needed for logger)
    systems_updated_counter = 0

    # set systems_multiple_counter (needed for logger)
    systems_multiple_counter = 0

    # create empty list (needed for logger)
    systems_multiple_list = []

    # set systems_skipped_counter (needed for logger)
    systems_skipped_counter = 0

    """ start loop """

    # iterate over rows
    for row in rows:

        """ skip headline if necessary """

        # check for first row and headline condition
        if row_counter == 1 and model.csv_headline:
            # autoincrement row counter
            row_counter += 1
            # leave loop for headline row
            continue

        """ filter for systems """

        # if function was called from 'system_instant' and 'system_upload'
        if request:
            # check system_name for valid value
            stop_system_importer_file_csv = check_system_name(model, row, row_counter, request)
        # if function was called from 'system_cron'
        else:
            # check system_name for valid value
            stop_system_importer_file_csv = check_system_name(model, row, row_counter)

        # leave loop if system_name caused errors
        if stop_system_importer_file_csv:
            # autoincrement counter
            systems_skipped_counter += 1
            # autoincrement row counter
            row_counter += 1
            # leave loop
            continue

        # get system name (for domain name comparison)
        system_name = row[model.csv_column_system - 1]

        # TODO: [logic] add option which attributes are used for filtering?
        # TODO: [logic] (like domain, dnsname, company)
        # TODO: [logic] e.g. 'csv_identification_dnsname'

        # get all systems
        systemquery = System.objects.filter(
            system_name = system_name,
        )

        """ check how many systems were returned """

        # if there is only one system -> modify system
        if len(systemquery) == 1:

            # skip if system already exists (depending on csv_skip_existing_system)
            if model.csv_skip_existing_system:

                # autoincrement counter
                systems_skipped_counter += 1
                # autoincrement row counter
                row_counter += 1
                # leave loop
                continue

            # TODO: [logic] add option which attributes are used for filtering?
            # TODO: [logic] (like domain, dnsname, company)
            # TODO: [logic] e.g. 'csv_identification_dnsname'

            # get existing system object
            system = System.objects.get(
                system_name=system_name,
            )

            # change mandatory meta attributes
            system.system_modify_time = timezone.now()
            system.system_modified_by_user_id = csv_import_user

            # set value for already existing system (modify system)
            system_created = False

            # if function was called from 'system_instant' and 'system_upload'
            if request:
                # add foreign key relationships to system
                system = add_fk_attributes(system, system_created, model, row, row_counter, request)
            # if function was called from 'system_cron'
            else:
                # add foreign key relationships to system
                system = add_fk_attributes(system, system_created, model, row, row_counter)

            # save object
            system.save()

            # if function was called from 'system_instant' and 'system_upload'
            if request:
                # add many2many relationships to system
                system = add_many2many_attributes(system, system_created, model, row, row_counter, request)
            # if function was called from 'system_cron'
            else:
                # add many2many relationships to system
                system = add_many2many_attributes(system, system_created, model, row, row_counter)

            # autoincrement systems_updated_counter
            systems_updated_counter += 1

            # call logger
            system.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_SYSTEM_MODIFIED')

        # if there is more than one system
        elif len(systemquery) > 1:

            # add system name to list
            systems_multiple_list.append(system_name)

            # autoincrement systems_multiple_counter
            systems_multiple_counter += 1

            # call logger
            warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_MULTIPLE_SYSTEMS System:{system_name}')

        # if there is no system -> create system
        else:

            # create new system object
            system = System()

            # add system_name from csv
            system.system_name = system_name

            # add mandatory meta attributes
            system.system_modify_time = timezone.now()
            system.system_created_by_user_id = csv_import_user
            system.system_modified_by_user_id = csv_import_user

            # set value for new system (create system)
            system_created = True

            # if function was called from 'system_instant' and 'system_upload'
            if request:
                # add foreign key relationships to system
                system = add_fk_attributes(system, system_created, model, row, row_counter, request)
            # if function was called from 'system_cron'
            else:
                # add foreign key relationships to system
                system = add_fk_attributes(system, system_created, model, row, row_counter)

            # save object
            system.save()

            # if function was called from 'system_instant' and 'system_upload'
            if request:
                # add many2many relationships to system
                system = add_many2many_attributes(system, system_created, model, row, row_counter, request)
            # if function was called from 'system_cron'
            else:
                # add many2many relationships to system
                system = add_many2many_attributes(system, system_created, model, row, row_counter)

            # autoincrement systems_created_counter
            systems_created_counter += 1

            # call logger
            system.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_SYSTEM_CREATED')

        # autoincrement row counter
        row_counter += 1

    # close file
    systemcsv.close()

    """ finish system importer """

    # get endtime
    endtime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        # call final messages
        final_messages(
            systems_created_counter,
            systems_updated_counter,
            systems_skipped_counter,
            systems_multiple_counter,
            systems_multiple_list,
            request,
        )
    # if function was called from 'system_cron'
    else:
        # call final messages
        final_messages_cron(
            systems_created_counter,
            systems_updated_counter,
            systems_skipped_counter,
            systems_multiple_counter,
            systems_multiple_list,
            starttime,
            endtime,
        )

    # call logger
    info_logger(
        logger_username,
        f' SYSTEM_IMPORTER_FILE_CSV_STATUS'
        f' created:{systems_created_counter}'
        f'|updated:{systems_updated_counter}'
        f'|skipped:{systems_skipped_counter}'
        f'|multiple:{systems_multiple_counter}'
    )
    # call logger
    debug_logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_END')

    # return to calling function 'csv.system_cron' or 'csv.system_instant' or 'csv.system_upload'
    return
