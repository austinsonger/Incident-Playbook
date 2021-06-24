from django.contrib import messages
from django.db import DataError
from dfirtrack_main.importer.file.csv_attributes_check import check_and_create_ip
from dfirtrack_main.logger.default_logger import warning_logger
from dfirtrack_main.models import Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemtype, Tag, Tagcolor


def create_lock_tags(model):

    # get tagcolor
    tagcolor_white = Tagcolor.objects.get(tagcolor_name = 'white')

    """ lock systemstatus """

    # get existing lock systemstatus tag
    try:
        tag_lock_systemstatus = Tag.objects.get(
            tag_name = model.csv_tag_lock_systemstatus,
        )

    # get or create lock systemstatus tag
    except Tag.DoesNotExist:
        tag_lock_systemstatus, created = Tag.objects.get_or_create(
            tag_name = model.csv_tag_lock_systemstatus,
            tagcolor = tagcolor_white,
        )
        # call logger
        if created:
            tag_lock_systemstatus.logger(model.csv_import_username.username, ' SYSTEM_IMPORTER_FILE_CSV_TAG_CREATED')

    """ lock analysisstatus """

    # get existing lock analysisstatus tag
    try:
        tag_lock_analysisstatus = Tag.objects.get(
            tag_name = model.csv_tag_lock_analysisstatus,
        )

    # get or create lock analysisstatus tag
    except Tag.DoesNotExist:
        tag_lock_analysisstatus, created = Tag.objects.get_or_create(
            tag_name = model.csv_tag_lock_analysisstatus,
            tagcolor = tagcolor_white,
        )
        # call logger
        if created:
            tag_lock_analysisstatus.logger(model.csv_import_username.username, ' SYSTEM_IMPORTER_FILE_CSV_TAG_CREATED')

def add_fk_attributes(system, system_created, model, row, row_counter, request=None):
    """ add foreign key relationships to system """

    """ set username for logger """

    # if function was called from 'system_instant' and 'system_upload'
    if request:
        logger_username = str(request.user)
    # if function was called from 'system_cron'
    else:
        logger_username = model.csv_import_username.username

    """ systemstatus (tagfree is set with tags in 'csv_attributes_add.add_many2many_attributes()') """

    # set systemstatus for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_systemstatus):

        # set default systemstatus for new system
        if system_created:
            # set systemstatus for new system
            system.systemstatus = model.csv_default_systemstatus
        # change systemstatus for existing system if not locked
        else:
            # get lockstatus
            tag_lock_systemstatus = Tag.objects.get(tag_name = model.csv_tag_lock_systemstatus)
            # check for lockstatus in all tags of system
            if tag_lock_systemstatus not in system.tag.all():
                # change to default systemstatus for existing system
                system.systemstatus = model.csv_default_systemstatus

    """ analysisstatus (tagfree is set with tags in 'csv_attributes_add.add_many2many_attributes()') """

    # set analysisstatus for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_analysisstatus):

        # set default analysisstatus for new system
        if system_created:
            # set analysisstatus for new system
            system.analysisstatus = model.csv_default_analysisstatus
        # change analysisstatus for existing system if not locked
        else:
            # get lockstatus
            tag_lock_analysisstatus = Tag.objects.get(tag_name = model.csv_tag_lock_analysisstatus)
            # check for lockstatus in all tags of system
            if tag_lock_analysisstatus not in system.tag.all():
                # change to default analysisstatus for existing system
                system.analysisstatus = model.csv_default_analysisstatus

    """ dnsname """

    # set dnsname for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_dnsname):
        # get dnsname from CSV
        if model.csv_choice_dnsname:
            # check for index error
            try:
                # get dnsname from CSV column
                dnsname_name = row[model.csv_column_dnsname - 1]
                # check for empty string
                if dnsname_name:
                    # value is valid
                    try:
                        # get or create dnsname
                        dnsname, created = Dnsname.objects.get_or_create(dnsname_name = dnsname_name)
                        # call logger if created
                        if created:
                            dnsname.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_DNSNAME_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for DNS name in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_DNSNAME_COLUMN row_{row_counter}:invalid_dnsname')
                        # set empty value
                        dnsname = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    dnsname = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for DNS name in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_DNSNAME_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                dnsname = None
        # get dnsname from DB
        elif model.csv_default_dnsname:
            dnsname = model.csv_default_dnsname
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            dnsname = None
        # set dnsname for system
        system.dnsname = dnsname

    """ domain """

    # set domain for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_domain):
        # get domain from CSV
        if model.csv_choice_domain:
            # check for index error
            try:
                # get domain from CSV column
                domain_name = row[model.csv_column_domain - 1]
                # check for empty string and compare to system name (when queried with local account, hostname is returned under some circumstances depending on tool)
                if domain_name and domain_name != system.system_name:
                    # value is valid
                    try:
                        # get or create domain
                        domain, created = Domain.objects.get_or_create(domain_name = domain_name)
                        # call logger if created
                        if created:
                            domain.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_DOMAIN_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for domain in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_DOMAIN_COLUMN row_{row_counter}:invalid_domain')
                        # set empty value
                        domain = None
                # string was empty or same as system_name
                else:
                    # set empty value (field is empty)
                    domain = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for domain in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_DOMAIN_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                domain = None
        # get domain from DB
        elif model.csv_default_domain:
            domain = model.csv_default_domain
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            domain = None
        # set domain for system
        system.domain = domain

    """ location """

    # set location for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_location):
        # get location from CSV
        if model.csv_choice_location:
            # check for index error
            try:
                # get location from CSV column
                location_name = row[model.csv_column_location - 1]
                # check for empty string
                if location_name:
                    # value is valid
                    try:
                        # get or create location
                        location, created = Location.objects.get_or_create(location_name = location_name)
                        # call logger if created
                        if created:
                            location.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_LOCATION_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for location in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_LOCATION_COLUMN row_{row_counter}:invalid_location')
                        # set empty value
                        location = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    location = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for location in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_LOCATION_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                location = None
        # get location from DB
        elif model.csv_default_location:
            location = model.csv_default_location
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            location = None
        # set location for system
        system.location = location

    """ os """

    # set os for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_os):
        # get os from CSV
        if model.csv_choice_os:
            # check for index error
            try:
                # get os from CSV column
                os_name = row[model.csv_column_os - 1]
                # check for empty string
                if os_name:
                    # value is valid
                    try:
                        # get or create os
                        os, created = Os.objects.get_or_create(os_name = os_name)
                        # call logger if created
                        if created:
                            os.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_OS_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for OS in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_OS_COLUMN row_{row_counter}:invalid_os')
                        # set empty value
                        os = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    os = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for OS in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_OS_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                os = None
        # get os from DB
        elif model.csv_default_os:
            os = model.csv_default_os
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            os = None
        # set os for system
        system.os = os

    """ reason """

    # set reason for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_reason):
        # get reason from CSV
        if model.csv_choice_reason:
            # check for index error
            try:
                # get reason from CSV column
                reason_name = row[model.csv_column_reason - 1]
                # check for empty string
                if reason_name:
                    # value is valid
                    try:
                        # get or create reason
                        reason, created = Reason.objects.get_or_create(reason_name = reason_name)
                        # call logger if created
                        if created:
                            reason.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_REASON_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for reason in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_REASON_COLUMN row_{row_counter}:invalid_reason')
                        # set empty value
                        reason = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    reason = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for reason in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_REASON_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                reason = None
        # get reason from DB
        elif model.csv_default_reason:
            reason = model.csv_default_reason
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            reason = None
        # set reason for system
        system.reason = reason

    """ recommendation """

    # set recommendation for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_recommendation):
        # get recommendation from CSV
        if model.csv_choice_recommendation:
            # check for index error
            try:
                # get recommendation from CSV column
                recommendation_name = row[model.csv_column_recommendation - 1]
                # check for empty string
                if recommendation_name:
                    # value is valid
                    try:
                        # get or create recommendation
                        recommendation, created = Recommendation.objects.get_or_create(recommendation_name = recommendation_name)
                        # call logger if created
                        if created:
                            recommendation.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_RECOMMENDATION_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for recommendation in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_RECOMMENDATION_COLUMN row_{row_counter}:invalid_recommendation')
                        # set empty value
                        recommendation = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    recommendation = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for recommendation in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_RECOMMENDATION_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                recommendation = None
        # get recommendation from DB
        elif model.csv_default_recommendation:
            recommendation = model.csv_default_recommendation
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            recommendation = None
        # set recommendation for system
        system.recommendation = recommendation

    """ serviceprovider """

    # set serviceprovider for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_serviceprovider):
        # get serviceprovider from CSV
        if model.csv_choice_serviceprovider:
            # check for index error
            try:
                # get serviceprovider from CSV column
                serviceprovider_name = row[model.csv_column_serviceprovider - 1]
                # check for empty string
                if serviceprovider_name:
                    # value is valid
                    try:
                        # get or create serviceprovider
                        serviceprovider, created = Serviceprovider.objects.get_or_create(serviceprovider_name = serviceprovider_name)
                        # call logger if created
                        if created:
                            serviceprovider.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_SERVICEPROVIDER_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for serviceprovider in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SERVICEPROVIDER_COLUMN row_{row_counter}:invalid_serviceprovider')
                        # set empty value
                        serviceprovider = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    serviceprovider = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for serviceprovider in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SERVICEPROVIDER_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                serviceprovider = None
        # get serviceprovider from DB
        elif model.csv_default_serviceprovider:
            serviceprovider = model.csv_default_serviceprovider
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            serviceprovider = None
        # set serviceprovider for system
        system.serviceprovider = serviceprovider

    """ systemtype """

    # set systemtype for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_systemtype):
        # get systemtype from CSV
        if model.csv_choice_systemtype:
            # check for index error
            try:
                # get systemtype from CSV column
                systemtype_name = row[model.csv_column_systemtype - 1]
                # check for empty string
                if systemtype_name:
                    # value is valid
                    try:
                        # get or create systemtype
                        systemtype, created = Systemtype.objects.get_or_create(systemtype_name = systemtype_name)
                        # call logger if created
                        if created:
                            systemtype.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_SYSTEMTYPE_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for systemtype in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SYSTEMTYPE_COLUMN row_{row_counter}:invalid_systemtype')
                        # set empty value
                        systemtype = None
                # string was empty
                else:
                    # set empty value (field is empty)
                    systemtype = None
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for systemtype in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_SYSTEMTYPE_COLUMN row_{row_counter}:out_of_range')
                # set empty value
                systemtype = None
        # get systemtype from DB
        elif model.csv_default_systemtype:
            systemtype = model.csv_default_systemtype
        # set empty value (removes for existing system if neither CSV nor DB is chosen, does nothing for new system)
        else:
            systemtype = None
        # set systemtype for system
        system.systemtype = systemtype

    # return system with foreign key relations to 'csv_main.system_handler'
    return system

def add_many2many_attributes(system, system_created, model, row, row_counter, request=None):
    """ add many2many relationships to system """

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

    """ IP addresses """

    # add IPs for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_ip):

        # remove IPs if not new system
        if not system_created:
            # remove all IPs
            system.ip.clear()

        # get IPs from CSV
        if model.csv_choice_ip:
            # check for index error
            try:
                # get IP string
                ip_string = row[model.csv_column_ip - 1]
                # check for empty string
                if ip_string:
                    # get IP delimiter from config
                    if model.csv_ip_delimiter == 'ip_comma':
                        ip_delimiter = ','
                    elif model.csv_ip_delimiter == 'ip_semicolon':
                        ip_delimiter = ';'
                    elif model.csv_ip_delimiter == 'ip_space':
                        ip_delimiter = ' '
                    # split IP string to list depending on delimiter
                    ip_list = ip_string.split(ip_delimiter)
                    # iterate over list elements
                    for ip_ip in ip_list:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # check, get or create IP
                            ip = check_and_create_ip(ip_ip, model, row_counter, request)
                        # if function was called from 'system_cron'
                        else:
                            # check, get or create IP
                            ip = check_and_create_ip(ip_ip, model, row_counter)
                        # IP was returned from 'check_and_create_ip'
                        if ip:
                            # add ip to system
                            system.ip.add(ip)
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for IP in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_IP_COLUMN row_{row_counter}:out_of_range')

    """ case """

    # set case for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_case):

        # remove cases if not new system
        if not system_created:
            # remove all cases
            system.case.clear()

        # get case from CSV
        if model.csv_choice_case:
            # check for index error
            try:
                # get case from CSV column
                case_name = row[model.csv_column_case - 1]
                # check for empty string
                if case_name:
                    # get existing case
                    try:
                        case = Case.objects.get(
                            case_name = case_name,
                        )
                    # create new case
                    except Case.DoesNotExist:
                        # value is valid
                        try:
                            case, created = Case.objects.get_or_create(
                                case_name = case_name,
                                case_is_incident = False,
                                case_created_by_user_id = csv_import_user,
                            )
                            # call logger if created
                            if created:
                                case.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_CASE_CREATED')
                        # value is not valid
                        except DataError:
                            # if function was called from 'system_instant' and 'system_upload'
                            if request:
                                # call message
                                messages.warning(request, f'Value for case in row {row_counter} was not a valid value.')
                            # call logger
                            warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_CASE_COLUMN row_{row_counter}:invalid_case')
                            # set empty value
                            case = None
                    # only add case to system if one of the previous checks was successful
                    if case:
                        # set case for system
                        system.case.add(case)
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for case in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_CASE_COLUMN row_{row_counter}:out_of_range')

        # get case from DB
        elif model.csv_default_case:
            cases = model.csv_default_case
            for case in cases.all():
                # add case to system
                system.case.add(case)

    """ company """

    # set company for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_company):

        # remove companies if not new system
        if not system_created:
            # remove all companies
            system.company.clear()

        # get company from CSV
        if model.csv_choice_company:
            # check for index error
            try:
                # get company from CSV column
                company_name = row[model.csv_column_company - 1]
                # check for empty string
                if company_name:
                    # value is valid
                    try:
                        # get or create company
                        company, created = Company.objects.get_or_create(company_name = company_name)
                        # call logger if created
                        if created:
                            company.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_COMPANY_CREATED')
                    # value is not valid
                    except DataError:
                        # if function was called from 'system_instant' and 'system_upload'
                        if request:
                            # call message
                            messages.warning(request, f'Value for company in row {row_counter} was not a valid value.')
                        # call logger
                        warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_COMPANY_COLUMN row_{row_counter}:invalid_company')
                        # set empty value
                        company = None
                    # only add company to system if one of the previous checks was successful
                    if company:
                        # set company for system
                        system.company.add(company)
            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for company in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_COMPANY_COLUMN row_{row_counter}:out_of_range')

        # get company from DB
        elif model.csv_default_company:
            companys = model.csv_default_company
            for company in companys.all():
                # add company to system
                system.company.add(company)

    """ tag """

    # set tag for new system or change if remove old is set
    if system_created or (not system_created and model.csv_remove_tag != 'tag_remove_none'):

        """ prepare tag prefix """

        # get tag delimiter from config
        if model.csv_tag_prefix_delimiter == 'tag_prefix_underscore':
            tag_prefix_delimiter = '_'
        elif model.csv_tag_prefix_delimiter == 'tag_prefix_hyphen':
            tag_prefix_delimiter = '-'
        elif model.csv_tag_prefix_delimiter == 'tag_prefix_period':
            tag_prefix_delimiter = '.'
        else:
            tag_prefix_delimiter = None

        # build tagprefix string from prefix and delimiter
        if model.csv_tag_prefix and tag_prefix_delimiter:
            tagprefix = model.csv_tag_prefix + tag_prefix_delimiter

        """ remove tags for existing systems (either all or just with prefix) """

        # remove all tags
        if not system_created and model.csv_remove_tag == 'tag_remove_all':
            # remove all tags
            system.tag.clear()

        # remove tags with prefix (and keep other / manually set tags)
        elif not system_created and model.csv_remove_tag == 'tag_remove_prefix':
            # get all relevant tags for this system
            prefixtags = system.tag.filter(tag_name__startswith=tagprefix)
            # iterate over tags
            for prefixtag in prefixtags:
                # remove this tag relation from system
                prefixtag.system_set.remove(system)

        """ add tags from CSV or DB """

        # get tags from CSV
        if model.csv_choice_tag:

            # check for index error
            try:

                # get tagstring from CSV column
                tag_string = row[model.csv_column_tag - 1]

                # check for empty string
                if tag_string:

                    # get tag delimiter from config
                    if model.csv_tag_delimiter == 'tag_comma':
                        tag_delimiter = ','
                    elif model.csv_tag_delimiter == 'tag_semicolon':
                        tag_delimiter = ';'
                    elif model.csv_tag_delimiter == 'tag_space':
                        tag_delimiter = ' '
                    # split tag string to list depending on delimiter
                    tag_list = tag_string.split(tag_delimiter)

                    # get tagcolor
                    tagcolor_primary = Tagcolor.objects.get(tagcolor_name='primary')
                    # iterate over tags
                    for tag in tag_list:
                        # build tagname from prefix, prefix delimiter and name
                        tagname = tagprefix + tag
                        # get existing tag
                        try:
                            tag = Tag.objects.get(
                                tag_name = tagname,
                            )
                        # create new tag
                        except Tag.DoesNotExist:
                            # value is valid
                            try:
                                tag, created = Tag.objects.get_or_create(
                                    tag_name = tagname,
                                    tagcolor = tagcolor_primary,
                                )
                                # call logger if created
                                if created:
                                    tag.logger(logger_username, ' SYSTEM_IMPORTER_FILE_CSV_TAG_CREATED')
                            # value is not valid
                            except DataError:
                                # if function was called from 'system_instant' and 'system_upload'
                                if request:
                                    # call message
                                    messages.warning(request, f'Value for tag in row {row_counter} was not a valid value.')
                                # call logger
                                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_TAG_COLUMN row_{row_counter}:invalid_tag')
                                # set empty value
                                tag = None
                        # only add tag to system if one of the previous checks was successful
                        if tag:
                            # add tag to system
                            system.tag.add(tag)

            # index out of range
            except IndexError:
                # if function was called from 'system_instant' and 'system_upload'
                if request:
                    # call message
                    messages.warning(request, f'Index for tag in row {row_counter} was out of range.')
                # call logger
                warning_logger(logger_username, f' SYSTEM_IMPORTER_FILE_CSV_TAG_COLUMN row_{row_counter}:out_of_range')

        # get tags from DB
        elif model.csv_default_tag:
            tags = model.csv_default_tag
            for tag in tags.all():
                # add tag to system
                system.tag.add(tag)

        """ change systemstatus / analysisstatus for systems w/o tags"""

        # if tag from CSV are enabled
        if model.csv_choice_tag:

            # check for index error
            try:

                # get tagstring from CSV column
                tag_string = row[model.csv_column_tag - 1]

                # no tags for this system
                if not tag_string:

                    """ systemstatus """

                    # tagfree systemstatus is set
                    if model.csv_choice_tagfree_systemstatus:

                        # set tagfree systemstatus for new system or change tagfree systemsstatus if remove old is set
                        if system_created or (not system_created and model.csv_remove_systemstatus):

                            # set tagfree systemstatus for new system
                            if system_created:
                                # set systemstatus for new system
                                system.systemstatus = model.csv_default_tagfree_systemstatus
                            # change systemstatus for existing system if not locked
                            else:
                                # get lockstatus
                                tag_lock_systemstatus = Tag.objects.get(tag_name = model.csv_tag_lock_systemstatus)
                                # check for lockstatus in all tags of system
                                if tag_lock_systemstatus not in system.tag.all():
                                    # change to tagfree systemstatus for existing system
                                    system.systemstatus = model.csv_default_tagfree_systemstatus

                            # save object
                            system.save()

                    """ analysisstatus """

                    # tagfree analysisstatus is set
                    if model.csv_choice_tagfree_analysisstatus:

                        # set tagfree status for new system or change to tagfree status if remove old is set
                        if system_created or (not system_created and model.csv_remove_analysisstatus):

                            # set tagfree analysisstatus for new system
                            if system_created:
                                # set analysisstatus for new system
                                system.analysisstatus = model.csv_default_tagfree_analysisstatus
                            # change analysisstatus for existing system if not locked
                            else:
                                # get lockstatus
                                tag_lock_analysisstatus = Tag.objects.get(tag_name = model.csv_tag_lock_analysisstatus)
                                # check for lockstatus in all tags of system
                                if tag_lock_analysisstatus not in system.tag.all():
                                    # change to tagfree analysisstatus for existing system
                                    system.analysisstatus = model.csv_default_tagfree_analysisstatus

                            # save object
                            system.save()

            # index out of range
            except IndexError:
                # do not change systemstatus and / or analysisstatus
                pass

    # return system with many2many relations to 'csv_main.system_handler'
    return system
