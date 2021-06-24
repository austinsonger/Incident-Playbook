from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from dfirtrack_config.models import MainConfigModel, SystemExporterSpreadsheetXlsConfigModel
from dfirtrack_main.logger.default_logger import debug_logger, info_logger
from dfirtrack_main.models import Analysisstatus, Reason, Recommendation, System, Systemstatus, Tag
from time import strftime
import xlwt


def write_row(worksheet, content, row_num, style):
    """ write single row to worksheet """

    # write row depending on column number
    for col_num in range(len(content)):
        worksheet.write(row_num, col_num, content[col_num], style)

    # return worksheet object
    return worksheet

def style_headline():
    """ change style to headline """

    # define styling for headline
    style = xlwt.XFStyle()
    style = xlwt.easyxf(
        'font: bold on; alignment: horizontal center'
    )

    # return style object
    return style

def style_default():
    """ change style to default """

    # clear styling to default
    style = xlwt.XFStyle()
    style = xlwt.easyxf(
        'alignment: vertical top, horizontal left'
    )

    # return style object
    return style

def write_xls(username):

    # create workbook object with UTF-8 encoding
    workbook = xlwt.Workbook(encoding='utf-8')

    # define name of worksheet within file
    worksheet_system = workbook.add_sheet('systems')

    # define styling for headline
    style = style_headline()

    # get config model
    model = SystemExporterSpreadsheetXlsConfigModel.objects.get(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')

    """ start with headline """

    # set counter
    row_num = 0

    # create empty list
    headline = []

    # check for attribute id
    if model.spread_xls_system_id:
        headline.append('ID')

    # append mandatory attribute
    headline.append('System')

    # check for remaining attributes
    if model.spread_xls_dnsname:
        headline.append('DNS name')
    if model.spread_xls_domain:
        headline.append('Domain')
    if model.spread_xls_systemstatus:
        headline.append('Systemstatus')
    if model.spread_xls_analysisstatus:
        headline.append('Analysisstatus')
    if model.spread_xls_reason:
        headline.append('Reason')
    if model.spread_xls_recommendation:
        headline.append('Recommendation')
    if model.spread_xls_systemtype:
        headline.append('Systemtype')
    if model.spread_xls_ip:
        headline.append('IP')
    if model.spread_xls_os:
        headline.append('OS')
    if model.spread_xls_company:
        headline.append('Company')
    if model.spread_xls_location:
        headline.append('Location')
    if model.spread_xls_serviceprovider:
        headline.append('Serviceprovider')
    if model.spread_xls_tag:
        headline.append('Tag')
    if model.spread_xls_case:
        headline.append('Case')
    if model.spread_xls_system_create_time:
        headline.append('Created')
    if model.spread_xls_system_modify_time:
        headline.append('Modified')

    # write headline
    worksheet_system = write_row(worksheet_system, headline, row_num, style)

    # clear styling to default
    style = style_default()

    """ append systems """

    # get all System objects ordered by system_name
    systems = System.objects.all().order_by("system_name")

    # iterate over systems
    for system in systems:

        # skip system depending on export variable
        if system.system_export_spreadsheet == False:
            continue

        # autoincrement row counter
        row_num += 1

        # set column counter
        col_num = 1

        # create empty list for line
        entryline = []

        """ check for attribute """

        # system id
        if model.spread_xls_system_id:
            entryline.append(system.system_id)

        """ append mandatory attribute """

        # system name
        entryline.append(system.system_name)

        """ check for remaining attributes """

        # dnsname
        if model.spread_xls_dnsname:
            if system.dnsname == None:
                dnsname = ''
            else:
                dnsname = system.dnsname.dnsname_name
            entryline.append(dnsname)
        # domain
        if model.spread_xls_domain:
            if system.domain == None:
                domain = ''
            else:
                domain = system.domain.domain_name
            entryline.append(domain)
        # systemstatus
        if model.spread_xls_systemstatus:
            entryline.append(system.systemstatus.systemstatus_name)
        # analysisstatus
        if model.spread_xls_analysisstatus:
            if system.analysisstatus == None:
                analysisstatus = ''
            else:
                analysisstatus = system.analysisstatus.analysisstatus_name
            entryline.append(analysisstatus)
        # reason
        if model.spread_xls_reason:
            if system.reason == None:
                reason = ''
            else:
                reason = system.reason.reason_name
            entryline.append(reason)
        # recommendation
        if model.spread_xls_recommendation:
            if system.recommendation== None:
                recommendation = ''
            else:
                recommendation = system.recommendation.recommendation_name
            entryline.append(recommendation)
        # systemtype
        if model.spread_xls_systemtype:
            if system.systemtype == None:
                systemtype = ''
            else:
                systemtype = system.systemtype.systemtype_name
            entryline.append(systemtype)
        # ip
        if model.spread_xls_ip:
            # get all ips of system
            ips_all = system.ip.all().order_by('ip_ip')
            # count ips
            n = system.ip.count()
            # create empty ip string
            ip = ''
            # set counter
            i = 1
            # iterate over ip objects in ip list
            for ip_obj in ips_all:
                # add actual ip to ip string
                ip = ip + ip_obj.ip_ip
                # add newline except for last ip
                if i < n:
                    ip = ip + '\n'
                    i = i + 1
            entryline.append(ip)
        # os
        if model.spread_xls_os:
            if system.os == None:
                os = ''
            else:
                os = system.os.os_name
            entryline.append(os)
        # company
        if model.spread_xls_company:
            companys_all = system.company.all().order_by('company_name')
            # count companies
            n = system.company.count()
            # create empty company string
            company = ''
            # set counter
            i = 1
            # iterate over company objects in company list
            for company_obj in companys_all:
                # add actual company to company string
                company = company + company_obj.company_name
                # add newline except for last company
                if i < n:
                    company = company + '\n'
                    i = i + 1
            entryline.append(company)
        # location
        if model.spread_xls_location:
            if system.location == None:
                location = ''
            else:
                location = system.location.location_name
            entryline.append(location)
        # serviceprovider
        if model.spread_xls_serviceprovider:
            if system.serviceprovider == None:
                serviceprovider = ''
            else:
                serviceprovider = system.serviceprovider.serviceprovider_name
            entryline.append(serviceprovider)
        # tag
        if model.spread_xls_tag:
            tags_all = system.tag.all().order_by('tag_name')
            # count tags
            n = system.tag.count()
            # create empty tag string
            tag = ''
            # set counter
            i = 1
            # iterate over tag objects in tag list
            for tag_obj in tags_all:
                # add actual tag to tag string
                tag = tag + tag_obj.tag_name
                # add newline except for last tag
                if i < n:
                    tag = tag + '\n'
                    i = i + 1
            entryline.append(tag)
        # case
        if model.spread_xls_case:
            cases_all = system.case.all().order_by('case_name')
            # count cases
            n = system.case.count()
            # create empty case string
            case = ''
            # set counter
            i = 1
            # iterate over case objects in case list
            for case_obj in cases_all:
                # add actual case to case string
                case = case + case_obj.case_name
                # add newline except for last case
                if i < n:
                    case = case + '\n'
                    i = i + 1
            entryline.append(case)
        # system create time
        if model.spread_xls_system_create_time:
            system_create_time = system.system_create_time.strftime('%Y-%m-%d %H:%M')
            entryline.append(system_create_time)
        # system modify time
        if model.spread_xls_system_modify_time:
            system_modify_time = system.system_modify_time.strftime('%Y-%m-%d %H:%M')
            entryline.append(system_modify_time)

        # write line for system
        worksheet_system = write_row(worksheet_system, entryline, row_num, style)

        # call logger
        debug_logger(username, ' SYSTEM_XLS_SYSTEM_EXPORTED ' + 'system_id:' + str(system.system_id) + '|system_name:' + system.system_name)

    # write an empty row
    row_num += 2

    # write meta information for file creation
    actualtime = timezone.now().strftime('%Y-%m-%d %H:%M')
    worksheet_system.write(row_num, 0, 'Created:', style)
    worksheet_system.write(row_num, 1, actualtime, style)
    row_num += 1
    creator = username
    worksheet_system.write(row_num, 0, 'Created by:', style)
    worksheet_system.write(row_num, 1, creator, style)

    """ add worksheet for systemstatus """

    # check all conditions
    if model.spread_xls_worksheet_systemstatus and model.spread_xls_systemstatus and Systemstatus.objects.count() != 0:

        # define name of worksheet within file
        worksheet_systemstatus = workbook.add_sheet('systemstatus')

        # create empty list
        headline_systemstatus = []

        # append attributes
        headline_systemstatus.append('ID')
        headline_systemstatus.append('Systemstatus')
        headline_systemstatus.append('Note')

        # define styling for headline
        style = style_headline()

        # set counter
        row_num = 0

        # write headline
        worksheet_systemstatus = write_row(worksheet_systemstatus, headline_systemstatus, row_num, style)

        # clear styling to default
        style = style_default()

        """ append systemstatus """

        # get all Systemstatus objects ordered by systemstatus_id
        systemstatuss = Systemstatus.objects.all().order_by("systemstatus_name")

        # iterate over systemstatus
        for systemstatus in systemstatuss:

            # autoincrement row counter
            row_num += 1

            # set column counter
            col_num = 1

            # create empty list for line
            entryline_systemstatus = []

            entryline_systemstatus.append(systemstatus.systemstatus_id)
            entryline_systemstatus.append(systemstatus.systemstatus_name)
            entryline_systemstatus.append(systemstatus.systemstatus_note)

            # write line for systemstatus
            worksheet_systemstatus = write_row(worksheet_systemstatus, entryline_systemstatus, row_num, style)

    """ add worksheet for analysisstatus """

    # check all conditions
    if model.spread_xls_worksheet_analysisstatus and model.spread_xls_analysisstatus and Analysisstatus.objects.count() != 0:

        # define name of worksheet within file
        worksheet_analysisstatus = workbook.add_sheet('analysisstatus')

        # create empty list
        headline_analysisstatus = []

        # append attributes
        headline_analysisstatus.append('ID')
        headline_analysisstatus.append('Analysisstatus')
        headline_analysisstatus.append('Note')

        # define styling for headline
        style = style_headline()

        # set counter
        row_num = 0

        # write headline
        worksheet_analysisstatus = write_row(worksheet_analysisstatus, headline_analysisstatus, row_num, style)

        # clear styling to default
        style = style_default()

        """ append analysisstatus """

        # get all Analysisstatus objects ordered by analysisstatus_id
        analysisstatuss = Analysisstatus.objects.all().order_by("analysisstatus_name")

        # iterate over analysisstatus
        for analysisstatus in analysisstatuss:

            # autoincrement row counter
            row_num += 1

            # set column counter
            col_num = 1

            # create empty list for line
            entryline_analysisstatus = []

            entryline_analysisstatus.append(analysisstatus.analysisstatus_id)
            entryline_analysisstatus.append(analysisstatus.analysisstatus_name)
            entryline_analysisstatus.append(analysisstatus.analysisstatus_note)

            # write line for analysisstatus
            worksheet_analysisstatus = write_row(worksheet_analysisstatus, entryline_analysisstatus, row_num, style)

    """ add worksheet for reason """

    # check all conditions
    if model.spread_xls_worksheet_reason and model.spread_xls_reason and Reason.objects.count() != 0:

        # define name of worksheet within file
        worksheet_reason = workbook.add_sheet('reasons')

        # create empty list
        headline_reason = []

        # append attributes
        headline_reason.append('ID')
        headline_reason.append('Reason')
        headline_reason.append('Note')

        # define styling for headline
        style = style_headline()

        # set counter
        row_num = 0

        # write headline
        worksheet_reason = write_row(worksheet_reason, headline_reason, row_num, style)

        # clear styling to default
        style = style_default()

        """ append reasons """

        # get all Reason objects ordered by reason_name
        reasons = Reason.objects.all().order_by("reason_name")

        # iterate over reasons
        for reason in reasons:

            # autoincrement row counter
            row_num += 1

            # set column counter
            col_num = 1

            # create empty list for line
            entryline_reason = []

            entryline_reason.append(reason.reason_id)
            entryline_reason.append(reason.reason_name)
            entryline_reason.append(reason.reason_note)

            # write line for reason
            worksheet_reason = write_row(worksheet_reason, entryline_reason, row_num, style)

    """ add worksheet for recommendation """

    # check all conditions
    if model.spread_xls_worksheet_recommendation and model.spread_xls_recommendation and Recommendation.objects.count() != 0:

        # define name of worksheet within file
        worksheet_recommendation = workbook.add_sheet('recommendations')

        # create empty list
        headline_recommendation = []

        # append attributes
        headline_recommendation.append('ID')
        headline_recommendation.append('Recommendation')
        headline_recommendation.append('Note')

        # define styling for headline
        style = style_headline()

        # set counter
        row_num = 0

        # write headline
        worksheet_recommendation = write_row(worksheet_recommendation, headline_recommendation, row_num, style)

        # clear styling to default
        style = style_default()

        """ append recommendations """

        # get all Recommendation objects ordered by recommendation_name
        recommendations = Recommendation.objects.all().order_by("recommendation_name")

        # iterate over recommendations
        for recommendation in recommendations:

            # autoincrement row counter
            row_num += 1

            # set column counter
            col_num = 1

            # create empty list for line
            entryline_recommendation = []

            entryline_recommendation.append(recommendation.recommendation_id)
            entryline_recommendation.append(recommendation.recommendation_name)
            entryline_recommendation.append(recommendation.recommendation_note)

            # write line for recommendation
            worksheet_recommendation = write_row(worksheet_recommendation, entryline_recommendation, row_num, style)

    """ add worksheet for tag """

    # check all conditions
    if model.spread_xls_worksheet_tag and model.spread_xls_tag and Tag.objects.count() != 0:

        # define name of worksheet within file
        worksheet_tag = workbook.add_sheet('tags')

        # create empty list
        headline_tag = []

        # append attributes
        headline_tag.append('ID')
        headline_tag.append('Tag')
        headline_tag.append('Note')

        # define styling for headline
        style = style_headline()

        # set counter
        row_num = 0

        # write headline
        worksheet_tag = write_row(worksheet_tag, headline_tag, row_num, style)

        # clear styling to default
        style = style_default()

        """ append tags """

        # get all Tag objects ordered by tag_name
        tags = Tag.objects.all().order_by("tag_name")

        # iterate over tags
        for tag in tags:

            # autoincrement row counter
            row_num += 1

            # set column counter
            col_num = 1

            # create empty list for line
            entryline_tag = []

            entryline_tag.append(tag.tag_id)
            entryline_tag.append(tag.tag_name)
            entryline_tag.append(tag.tag_note)

            # write line for tag
            worksheet_tag = write_row(worksheet_tag, entryline_tag, row_num, style)

    # call logger
    info_logger(username, " SYSTEM_XLS_CREATED")

    # return xls object
    return workbook

@login_required(login_url="/login")
def system(request):

    # create xls MIME type object
    xls_browser = HttpResponse(content_type='application/ms-excel')

    # prepare interactive file including filename
    xls_browser['Content-Disposition'] = 'attachment; filename="systems.xls"'

    # get username from request object
    username = str(request.user)

    # call main function
    xls_workbook = write_xls(username)

    # save workbook to interactive file
    xls_workbook.save(xls_browser)

    # return spreadsheet object to browser
    return xls_browser

def system_cron():

    # prepare time for output file
    filetime = timezone.now().strftime('%Y%m%d_%H%M')

    # get config
    main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')

    # prepare output file path
    output_file_path = main_config_model.cron_export_path + '/' + filetime + '_systems.xls'

    # get username from config
    username = main_config_model.cron_username

    # call main function
    xls_disk = write_xls(username)

    # save spreadsheet to disk
    xls_disk.save(output_file_path)

    # call logger
    info_logger(username, ' SYSTEM_XLS_FILE_WRITTEN ' + output_file_path)
