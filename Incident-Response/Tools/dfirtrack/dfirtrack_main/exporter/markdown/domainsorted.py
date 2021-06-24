from django.contrib import messages
from django.contrib.messages import constants
from django.core.files import File
from django_q.tasks import async_task
from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.async_messages import message_user
from dfirtrack_main.exporter.markdown.markdown_check_data import check_config
from dfirtrack_main.exporter.markdown import clean_directory, read_or_create_mkdocs_yml, write_report
from dfirtrack_main.logger.default_logger import debug_logger, info_logger
from dfirtrack_main.models import Domain, System
import fileinput
import os
import re
from time import strftime
import yaml


def write_report_domainsorted(system, request_user):
    """ function that prepares return values and pathes """

    """
    the return values (prefix 'r') are used for the `mkdocs.yml` file
    they build the key-value-pair for every system
    """

    # return system_id for mkdocs.yml
    rid = str(system.system_id)

    # return fqdn for mkdocs.yml
    if system.dnsname != None:
        rfqdn = system.system_name + "." + system.dnsname.dnsname_name
    else:
        rfqdn = system.system_name

    """
    build the path for every file
    it is distinguished between the short version for the `mkdocs.yml` file ('value' of key-value-pair)
    and the long version that is used to write to the file system
    """

    # build path
    path = system.system_name

    # check for domain and add to path
    if system.domain != None:
        path = path + "_" + system.domain.domain_name
        # get domain_name
        domain_name = system.domain.domain_name
        # return domain for mkdocs.yml
        rdomain = domain_name
    else:
        # return string instead of domain for mkdocs.yml
        rdomain = 'other_domains'

    # check for system_install_time and add to path
    if system.system_install_time != None:
        install_time = system.system_install_time.strftime('%Y%m%d_%H%M%S')
        path = path + "_" + install_time

    # return shortened path for mkdocs.yml ('value')
    if system.domain != None:
        rpath = "systems/" + domain_name + "/" + path + ".md"
    else:
        rpath = "systems/" + "other_domains/" + path + ".md"

    # get config model
    model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')

    # finish path for markdown file
    if system.domain != None:
        path = model.markdown_path + "/docs/systems/" + domain_name + "/" + path + ".md"
    else:
        path = model.markdown_path + "/docs/systems/" + "other_domains/" + path + ".md"

    # open file for system
    report = open(path, "w")
    django_report = File(report)

    # write systemreport
    write_report.write_report(django_report, system)

    # close and save file
    django_report.closed
    report.close()

    # call logger
    info_logger(request_user, " SYSTEM_MARKDOWN_CREATED system_id:" + str(system.system_id) + "|system_name:" + str(system.system_name))

    # return strings for mkdocs.yml (only used in domainsorted_async)
    return(rid, rfqdn, rpath, rdomain)

def domainsorted(request):
    """ exports markdown report for all systems sorted by domain (helper function to call the real function) """

    request_user = request.user

    # call logger
    debug_logger(str(request_user), " SYSTEM_EXPORTER_MARKDOWN_DOMAINSORTED_START")

    # check variables
    stop_exporter_markdown = check_config(request)

    # leave if variables caused errors
    if stop_exporter_markdown:
        return

    # show immediate message for user (but only if no errors have occured before)
    messages.success(request, 'System exporter markdown (sorted by domain) started')

    # call async function
    async_task(
        "dfirtrack_main.exporter.markdown.domainsorted.domainsorted_async",
        request_user,
    )

    return

def domainsorted_async(request_user):
    """ exports markdown report for all systems sorted by domain """

    # call directory cleaning function
    clean_directory.clean_directory(str(request_user))

    # get all domains
    domains = Domain.objects.all()

    # get config model
    model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')

    # (re)create markdown directory for existing domains
    if len(domains) > 0:
        for domain in domains:
            os.mkdir(model.markdown_path + "/docs/systems/" + domain.domain_name)

    # create directory for systems without domains
    os.mkdir(model.markdown_path + "/docs/systems/other_domains/")

    # get all systems
    systems = System.objects.all().order_by('domain','system_name')

    # create empty list and dict (needed for mkdocs.yml)
    systemlist = []
    systemdict = {}
    domaindict = {}
    domainlist = []

    # iterate over systems
    for system in systems:

        # skip system depending on export variable
        if system.system_export_markdown == False:
            continue

        # call writing function (and get return values)
        rid, rfqdn, rpath, rdomain = write_report_domainsorted(system, str(request_user))

        """ build a dict that is used for the system section in mkdocs.yml """

        # build string as key for systemdict (needed for mkdocs.yml)
        index = rfqdn + " (" + rid + ")"
        # add value to key in 1-value dict (needed for mkdocs.yml)
        systemdict[index] = rpath
        # check whether domain was already used as second level entry (headline)
        if rdomain in domainlist:
            # add placeholder instead of (r)domain (because it was used before)
            domaindict["already_used_domain"] = systemdict
        else:
            # add dict to another 1-value dict (needed for mkdocs.yml)
            if rdomain == "other_domains":
                # add "Other domains"
                domaindict["Other domains"] = systemdict
            else:
                # add real domains
                domaindict[rdomain] = systemdict
            # add (r)domain to domainlist so it will not be written to systemlist the next iteration
            domainlist.append(rdomain)
        # add dict to list (needed for mkdocs.yml)
        systemlist.append(domaindict)
        # set dicts to empty dicts (for next iteration)
        systemdict = {}
        domaindict = {}

    # get path for mkdocs.yml
    mkdconfpath = model.markdown_path + "/mkdocs.yml"

    # read content (dictionary) of mkdocs.yml if existent, else create dummy content
    mkdconfdict = read_or_create_mkdocs_yml.read_or_create_mkdocs_yml(str(request_user), mkdconfpath)

    # get pages list
    mkdconflist = mkdconfdict['pages']

    # set counter
    i = 0
    j = 0

    # iterate over 'pages' list
    for item in mkdconflist:

        # find subsection 'Systems' in list
        try:
            dummy = item['Systems']
            # set index
            j = i
        except:     # coverage: ignore branch
            # do nothing
            pass

        # autoincrement counter for next loop
        i += 1

    # set at dict 'Systems' in list mkdconflist at index j (replace section 'Systems')
    mkdconflist[j]['Systems'] = systemlist

    # set pages with old entries and new 'Systems' section
    mkdconfdict['pages'] = mkdconflist

    # open mkdocs.yml for writing (new file)
    mkdconffile = open(mkdconfpath, "w")
    # write mkdocs.yml
    yaml.dump(mkdconfdict, mkdconffile, default_flow_style=False, default_style='"')
    # close mkdocs.yml
    mkdconffile.close()

    """ adds hyphens for third level entries (are generated without but mkdocs needs them) """

    # open mkdocs.yml again for inplace replacement
    mkdconffile= fileinput.FileInput(mkdconfpath, inplace=True)
    # iterate over lines in mkdocs.yml
    for line in mkdconffile:
        # add hyphen for entries in third level (needed by mkdocs)
        line = re.sub(r"^      ",
                      "    - ",
                      line.rstrip()
        )
        print(line)

    """ remove placeholder 'already_used_domain' that was created before for second level entries """

    # open mkdocs.yml again for inplace replacement
    mkdconffile= fileinput.FileInput(mkdconfpath, inplace=True)
    # iterate over lines in mkdocs.yml
    for line in mkdconffile:
        # change placeholder to empty line
        line = re.sub(r'^  - "already_used_domain":',
                      '',
                      line.rstrip()
        )
        print(line)

    """ remove empty lines created before instead of placeholder """

    # open mkdocs.yml
    with open(mkdconfpath) as filehandle:
        # read all lines
        lines = filehandle.readlines()
        # filter out every line with nothing in it ('strip'ed to nothing)
        lines = filter(lambda x: x.strip(), lines)
    # open mkdocs.yml for writing
    with open(mkdconfpath, 'w') as filehandle:
        # write filtered lines back to file
        filehandle.writelines(lines)

    # finish message
    message_user(request_user, 'System exporter markdown (sorted by domain) finished', constants.SUCCESS)

    # call logger
    debug_logger(str(request_user), " SYSTEM_EXPORTER_MARKDOWN_DOMAINSORTED_END")
