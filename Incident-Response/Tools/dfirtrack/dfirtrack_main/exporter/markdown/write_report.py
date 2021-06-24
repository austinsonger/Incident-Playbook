from time import strftime


def emptyline(django_report):
    """ easy to read function for an empty line """
    django_report.write("\n")


def write_headline(django_report, system):
    """ write headline """

    django_report.write("# " + system.system_name + "\n")
    emptyline(django_report)


def write_systemstatus(django_report, system):
    """ write systemstatus in admonation style """

    if system.systemstatus.systemstatus_name == "30_compromised":
        django_report.write('!!! danger "Systemstatus"\n')
        django_report.write("    " + system.systemstatus.systemstatus_name)
    elif system.systemstatus.systemstatus_name == "10_unknown":
        django_report.write('!!! warning "Systemstatus"\n')
        django_report.write("    " + system.systemstatus.systemstatus_name)
    elif system.systemstatus.systemstatus_name == "20_analysis_ongoing":
        django_report.write('!!! warning "Systemstatus"\n')
        django_report.write("    " + system.systemstatus.systemstatus_name)
    elif system.systemstatus.systemstatus_name == "90_not_analyzed":
        django_report.write('!!! warning "Systemstatus"\n')
        django_report.write("    " + system.systemstatus.systemstatus_name)
    else:
        django_report.write('!!! success "Systemstatus"\n')
        django_report.write("    " + system.systemstatus.systemstatus_name)
    # write note if it exists directly after systemstatus_name separated by '-'
    if system.systemstatus.systemstatus_note != None:
        django_report.write(" - " + system.systemstatus.systemstatus_note + "\n")
    else:
        # just add newline character after systemstatus_name
        emptyline(django_report)


def write_systemoverview_to_table(django_report, system):
    """ write system overview headline and markdown table head """

    django_report.write("# System overview\n")
    emptyline(django_report)
    # start table
    django_report.write("| Setting  | Information |\n")
    django_report.write("|:---------|:------------|\n")


def write_systemidentification_to_table(django_report, system):
    """ dnsname (for fqdn) and domain (add to table) """

    # systemname and dnsname
    if system.dnsname != None:
        django_report.write("| Hostname / FQDN (Domain) | " + system.system_name + "." + system.dnsname.dnsname_name + " ")
    else:
        django_report.write("| Hostname / FQDN (Domain) | " + system.system_name + " ")
    # domain
    if system.domain != None:
        django_report.write("(" + system.domain.domain_name + ") |\n")
    else:
        django_report.write("(---) |\n")


def write_ip_to_table(django_report, system):
    """ ip(s) to a markdown table """

    ips = system.ip.all()
    if ips.exists():
        for ip in ips:
            django_report.write("| IP | " + ip.ip_ip + " |\n")
    else:
        # place holder
        django_report.write("| IP | \--- |\n")


def write_os_to_table(django_report, system):
    """ os (add to table) """

    if system.os != None:
        django_report.write("| OS | " + system.os.os_name + " |\n")
    else:
        # place holder
        django_report.write("| OS | \--- |\n")


def write_systemtype_to_table(django_report, system):
    """ systemtype (add to table) """

    if system.systemtype != None:
        django_report.write("| Type | " + system.systemtype.systemtype_name + " |\n")
    else:
        # place holder
        django_report.write("| Type | \--- |\n")


def write_system_install_time_to_table(django_report, system):
    """ system_install_time (add to table) """

    if system.system_install_time != None:
        django_report.write("| Install | " + system.system_install_time.strftime('%Y-%m-%d %H:%M:%S') + " |\n")
    else:
        # place holder
        django_report.write("| Install | \--- |\n")
    emptyline(django_report)


def write_reason(django_report, system):
    """ reason """

    django_report.write("## Identification / Reason for investigation\n")
    emptyline(django_report)
    if system.reason != None:
        django_report.write(system.reason.reason_name + "\n")
        if system.reason.reason_note != '':
            emptyline(django_report)
            django_report.write(system.reason.reason_note + "\n")
    else:
        # place holder
        django_report.write("\---\n")
    emptyline(django_report)


def write_recommendation(django_report, system):
    """ recommendation """

    django_report.write("## Recommendation\n")
    emptyline(django_report)
    if system.recommendation != None:
        django_report.write(system.recommendation.recommendation_name + "\n")
        if system.recommendation.recommendation_note != '':
            emptyline(django_report)
            django_report.write(system.recommendation.recommendation_note + "\n")
    else:
        django_report.write("\---\n")
    emptyline(django_report)


def write_reportitem(django_report, system):
    """ reportitem """

    reportitems = system.reportitem_set.all().order_by('headline')
    if reportitems.exists():
        for reportitem in reportitems:
            # headline
            django_report.write("## " + reportitem.headline.headline_name + "\n")
            emptyline(django_report)
            # check for subheadline
            if reportitem.reportitem_subheadline != None:
                # subheadline
                django_report.write("### " + reportitem.reportitem_subheadline + "\n")
                emptyline(django_report)
            django_report.write(reportitem.reportitem_note + "\n")
            emptyline(django_report)


def write_systemusers(django_report, system):
    """ write systemuser """

    django_report.write("## Potentially compromised accounts\n")
    emptyline(django_report)
    users = system.systemuser_set.all().order_by('systemuser_name')
    if users.exists():
        for user in users:
            django_report.write("* " + user.systemuser_name + "\n")
    else:
        # place holder
        django_report.write("\---\n")
    emptyline(django_report)


def write_timeline_table(django_report, system):
    """ write timeline table headline and head of table """

    # timeline (table)
    django_report.write("# Timeline\n")
    emptyline(django_report)
    # start table
    django_report.write("| Date     | Time (UTC)  | System      | Type        | Content     |\n")
    django_report.write("|:---------|:------------|:------------|:------------|:------------|\n")


def write_entries_to_table(django_report, system):
    """ write all entries to table """

    # TODO: change behavior, currently check for entry attributes is necessary because of 'null=True'
    entrys = system.entry_set.all().order_by('entry_date', 'entry_utc')
    if entrys.exists():
        # iterate over entries
        for entry in entrys:
            # print entries line by line
            if entry.entry_date:
                django_report.write("| " + entry.entry_date + " ")
            else:
                django_report.write("| ")
            if entry.entry_utc:
                django_report.write("| " + entry.entry_utc + " ")
            else:
                django_report.write("| ")
            if entry.entry_system:
                django_report.write("| " + entry.entry_system + " ")
            else:
                django_report.write("| ")
            if entry.entry_type:
                django_report.write("| " + entry.entry_type + " ")
            else:
                django_report.write("| ")
            if entry.entry_content:
                django_report.write("| " + entry.entry_content + "|\n")
            else:
                django_report.write("| |\n")
    else:
        # place holder
        django_report.write("| \---      | \---         | \---         | \---         | \---         |\n")
    emptyline(django_report)


def write_report(django_report, system):
    """
    write systemreport
    to change order of items change it here
    """

    # headline
    write_headline(django_report, system)

    # systemstatus
    write_systemstatus(django_report, system)

    # systemoverview and table head
    write_systemoverview_to_table(django_report, system)

    # systemname, dnsname (for fqdn) and domain (add to table)
    write_systemidentification_to_table(django_report, system)

    # ip(s) (add to table)
    write_ip_to_table(django_report, system)

    # os (add to table)
    write_os_to_table(django_report, system)

    # systemtype (add to table)
    write_systemtype_to_table(django_report, system)

    # system_install_time (add to table)
    write_system_install_time_to_table(django_report, system)

    # reason
    write_reason(django_report, system)

    # recommendation
    write_recommendation(django_report, system)

    # reportitem
    write_reportitem(django_report, system)

    # systemuser
    write_systemusers(django_report, system)

    # timeline (table)
    write_timeline_table(django_report, system)

    # entries
    write_entries_to_table(django_report, system)
