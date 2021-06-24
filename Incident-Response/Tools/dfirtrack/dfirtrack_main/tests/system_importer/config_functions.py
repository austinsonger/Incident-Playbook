from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.models import Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemtype, Tag

def set_config_column_system(csv_column_system):
    """ set config """

    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_column_system = csv_column_system
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_single_quotation():
    """ set config """

    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_text_quote = 'text_single_quotation_marks'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_headline():
    """ set config """

    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_headline = True
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_field_delimiter_comma():
    """ set config """

    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_field_delimiter = 'field_comma'
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = 2
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_field_delimiter_semicolon():
    """ set config """

    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_field_delimiter = 'field_semicolon'
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = 2
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_check_attributes_csv():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_column_system = 1
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = 2
    system_importer_file_csv_config_model.csv_choice_dnsname = True
    system_importer_file_csv_config_model.csv_column_dnsname = 3
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = 4
    system_importer_file_csv_config_model.csv_choice_location = True
    system_importer_file_csv_config_model.csv_column_location = 5
    system_importer_file_csv_config_model.csv_choice_os = True
    system_importer_file_csv_config_model.csv_column_os = 6
    system_importer_file_csv_config_model.csv_choice_reason = True
    system_importer_file_csv_config_model.csv_column_reason = 7
    system_importer_file_csv_config_model.csv_choice_recommendation = True
    system_importer_file_csv_config_model.csv_column_recommendation = 8
    system_importer_file_csv_config_model.csv_choice_serviceprovider = True
    system_importer_file_csv_config_model.csv_column_serviceprovider = 9
    system_importer_file_csv_config_model.csv_choice_systemtype = True
    system_importer_file_csv_config_model.csv_column_systemtype = 10
    system_importer_file_csv_config_model.csv_choice_case = True
    system_importer_file_csv_config_model.csv_column_case = 11
    system_importer_file_csv_config_model.csv_choice_company = True
    system_importer_file_csv_config_model.csv_column_company = 12
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 13
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_check_attributes_domain_name():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_column_system = 1
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = 2
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_check_config_attributes_choices_true(system_importer_file_csv_config_model):
    """ set choices to true for all columns """

    # set config values
    system_importer_file_csv_config_model.csv_choice_system = True
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_choice_dnsname = True
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_choice_location = True
    system_importer_file_csv_config_model.csv_choice_os = True
    system_importer_file_csv_config_model.csv_choice_reason = True
    system_importer_file_csv_config_model.csv_choice_recommendation = True
    system_importer_file_csv_config_model.csv_choice_serviceprovider = True
    system_importer_file_csv_config_model.csv_choice_systemtype = True
    system_importer_file_csv_config_model.csv_choice_case = True
    system_importer_file_csv_config_model.csv_choice_company = True
    system_importer_file_csv_config_model.csv_choice_tag = True

    # return config to config function
    return system_importer_file_csv_config_model

def set_config_check_config_attributes_column_fields_numeric_values():
    """ set numeric values for columns out of range """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set choices to true for all columns
    system_importer_file_csv_config_model = set_config_check_config_attributes_choices_true(system_importer_file_csv_config_model)

    # set config values
    system_importer_file_csv_config_model.csv_column_system = 100
    system_importer_file_csv_config_model.csv_column_ip = 101
    system_importer_file_csv_config_model.csv_column_dnsname = 102
    system_importer_file_csv_config_model.csv_column_domain = 103
    system_importer_file_csv_config_model.csv_column_location = 104
    system_importer_file_csv_config_model.csv_column_os = 105
    system_importer_file_csv_config_model.csv_column_reason = 106
    system_importer_file_csv_config_model.csv_column_recommendation = 107
    system_importer_file_csv_config_model.csv_column_serviceprovider = 108
    system_importer_file_csv_config_model.csv_column_systemtype = 109
    system_importer_file_csv_config_model.csv_column_case = 110
    system_importer_file_csv_config_model.csv_column_company = 111
    system_importer_file_csv_config_model.csv_column_tag = 112

    # save config
    system_importer_file_csv_config_model.save()

    # return to column fields numeric values test function
    return

def set_config_check_config_attributes_column_choice_vs_default_single_error():
    """ set column, choice and default single error """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_column_system = 1
    system_importer_file_csv_config_model.csv_choice_ip = False
    system_importer_file_csv_config_model.csv_column_ip = 2

    # save config
    system_importer_file_csv_config_model.save()

    # return to column choice vs default test function
    return

def set_config_check_config_attributes_column_choice_vs_default_multiple_errors_1():
    """ set column, choice and default randomly faulty """

    # get objects
    case_1 = Case.objects.get(case_name='case_1')
    company_1 = Company.objects.get(company_name='company_1')
    dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
    domain_1 = Domain.objects.get(domain_name='domain_1')
    location_1 = Location.objects.get(location_name='location_1')
    reason_1 = Reason.objects.get(reason_name='reason_1')
    recommendation_1 = Recommendation.objects.get(recommendation_name='recommendation_1')
    serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
    systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
    os_1 = Os.objects.get(os_name='os_1')
    tag_1 = Tag.objects.get(tag_name='tag_1')

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_column_system = 1
    # CSV not chosen and CSV column filled out / +1
    system_importer_file_csv_config_model.csv_choice_ip = False
    system_importer_file_csv_config_model.csv_column_ip = 2
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_dnsname = False
    system_importer_file_csv_config_model.csv_column_dnsname = 3
    system_importer_file_csv_config_model.csv_default_dnsname = dnsname_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_domain = False
    system_importer_file_csv_config_model.csv_column_domain = 4
    system_importer_file_csv_config_model.csv_default_domain = domain_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_location = False
    system_importer_file_csv_config_model.csv_column_location = 5
    system_importer_file_csv_config_model.csv_default_location = location_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_os = False
    system_importer_file_csv_config_model.csv_column_os = 6
    system_importer_file_csv_config_model.csv_default_os = os_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_reason = False
    system_importer_file_csv_config_model.csv_column_reason = 7
    system_importer_file_csv_config_model.csv_default_reason = reason_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_recommendation = False
    system_importer_file_csv_config_model.csv_column_recommendation = 8
    system_importer_file_csv_config_model.csv_default_recommendation = recommendation_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_serviceprovider = False
    system_importer_file_csv_config_model.csv_column_serviceprovider = 9
    system_importer_file_csv_config_model.csv_default_serviceprovider = serviceprovider_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_systemtype = False
    system_importer_file_csv_config_model.csv_column_systemtype = 10
    system_importer_file_csv_config_model.csv_default_systemtype = systemtype_1
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_case = False
    system_importer_file_csv_config_model.csv_column_case = 11
    system_importer_file_csv_config_model.csv_default_case.add(case_1)
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_company = False
    system_importer_file_csv_config_model.csv_column_company = 12
    system_importer_file_csv_config_model.csv_default_company.add(company_1)
    # CSV not chosen and CSV column filled out / CSV column filled out and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_tag = False
    system_importer_file_csv_config_model.csv_column_tag = 13
    system_importer_file_csv_config_model.csv_default_tag.add(tag_1)

    # save config
    system_importer_file_csv_config_model.save()

    # return to column choice vs default test function
    return

def set_config_check_config_attributes_column_choice_vs_default_multiple_errors_2():
    """ set column, choice and default randomly faulty """

    # get objects
    case_1 = Case.objects.get(case_name='case_1')
    company_1 = Company.objects.get(company_name='company_1')
    dnsname_1 = Dnsname.objects.get(dnsname_name='dnsname_1')
    domain_1 = Domain.objects.get(domain_name='domain_1')
    location_1 = Location.objects.get(location_name='location_1')
    reason_1 = Reason.objects.get(reason_name='reason_1')
    recommendation_1 = Recommendation.objects.get(recommendation_name='recommendation_1')
    serviceprovider_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1')
    systemtype_1 = Systemtype.objects.get(systemtype_name='systemtype_1')
    os_1 = Os.objects.get(os_name='os_1')
    tag_1 = Tag.objects.get(tag_name='tag_1')

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_column_system = 1
    # CSV chosen and no CSV column filled out / +1
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = None
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_dnsname = True
    system_importer_file_csv_config_model.csv_column_dnsname = None
    system_importer_file_csv_config_model.csv_default_dnsname = dnsname_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = None
    system_importer_file_csv_config_model.csv_default_domain = domain_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_location = True
    system_importer_file_csv_config_model.csv_column_location = None
    system_importer_file_csv_config_model.csv_default_location = location_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_os = True
    system_importer_file_csv_config_model.csv_column_os = None
    system_importer_file_csv_config_model.csv_default_os = os_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_reason = True
    system_importer_file_csv_config_model.csv_column_reason = None
    system_importer_file_csv_config_model.csv_default_reason = reason_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_recommendation = True
    system_importer_file_csv_config_model.csv_column_recommendation = None
    system_importer_file_csv_config_model.csv_default_recommendation = recommendation_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_serviceprovider = True
    system_importer_file_csv_config_model.csv_column_serviceprovider = None
    system_importer_file_csv_config_model.csv_default_serviceprovider = serviceprovider_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_systemtype = True
    system_importer_file_csv_config_model.csv_column_systemtype = None
    system_importer_file_csv_config_model.csv_default_systemtype = systemtype_1
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_case = True
    system_importer_file_csv_config_model.csv_column_case = None
    system_importer_file_csv_config_model.csv_default_case.add(case_1)
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_company = True
    system_importer_file_csv_config_model.csv_column_company = None
    system_importer_file_csv_config_model.csv_default_company.add(company_1)
    # CSV chosen and no CSV column filled out / CSV chosen and DB chosen / +2
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = None
    system_importer_file_csv_config_model.csv_default_tag.add(tag_1)

    # save config
    system_importer_file_csv_config_model.save()

    # return to column choice vs default test function
    return

def set_config_check_config_attributes_tagfree_choices():
    """ set tagfree statuses without tag choice """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_choice_tag = False
    system_importer_file_csv_config_model.csv_choice_tagfree_systemstatus = True
    system_importer_file_csv_config_model.csv_choice_tagfree_analysisstatus = True

    # save config
    system_importer_file_csv_config_model.save()

    # return to tagfree choices test function
    return

def set_config_check_config_attributes_column_fields_equal_values():
    """ set numeric values for column fields equal """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set choices to true for all columns
    system_importer_file_csv_config_model = set_config_check_config_attributes_choices_true(system_importer_file_csv_config_model)

    # set config values
    system_importer_file_csv_config_model.csv_column_system = 1
    system_importer_file_csv_config_model.csv_column_ip = 1
    system_importer_file_csv_config_model.csv_column_dnsname = 1
    system_importer_file_csv_config_model.csv_column_domain = 1
    system_importer_file_csv_config_model.csv_column_location = 1
    system_importer_file_csv_config_model.csv_column_os = 1
    system_importer_file_csv_config_model.csv_column_reason = 1
    system_importer_file_csv_config_model.csv_column_recommendation = 1
    system_importer_file_csv_config_model.csv_column_serviceprovider = 1
    system_importer_file_csv_config_model.csv_column_systemtype = 1
    system_importer_file_csv_config_model.csv_column_case = 1
    system_importer_file_csv_config_model.csv_column_company = 1
    system_importer_file_csv_config_model.csv_column_tag = 1

    # save config
    system_importer_file_csv_config_model.save()

    # return to column fields different values test function
    return

def set_config_check_config_attributes_remove_choices():
    """ set remove choices in combination with skipping systems """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_skip_existing_system = True
    system_importer_file_csv_config_model.csv_remove_systemstatus = True
    system_importer_file_csv_config_model.csv_remove_analysisstatus = True
    system_importer_file_csv_config_model.csv_remove_ip = True
    system_importer_file_csv_config_model.csv_remove_dnsname = True
    system_importer_file_csv_config_model.csv_remove_domain = True
    system_importer_file_csv_config_model.csv_remove_location = True
    system_importer_file_csv_config_model.csv_remove_os = True
    system_importer_file_csv_config_model.csv_remove_reason = True
    system_importer_file_csv_config_model.csv_remove_recommendation = True
    system_importer_file_csv_config_model.csv_remove_serviceprovider = True
    system_importer_file_csv_config_model.csv_remove_systemtype = True
    system_importer_file_csv_config_model.csv_remove_case = True
    system_importer_file_csv_config_model.csv_remove_company = True

    # save config
    system_importer_file_csv_config_model.save()

    # return to remove choices test function
    return

def set_config_tagfree_status():
    """ set config to set status depending on tag in CSV """

    # get config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')

    # set config values
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_choice_tagfree_systemstatus = True
    system_importer_file_csv_config_model.csv_choice_tagfree_analysisstatus = True

    # save config
    system_importer_file_csv_config_model.save()

    # return to tagfree status test function
    return

def set_config_complete_attributes_csv():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tagfree_systemstatus = True
    system_importer_file_csv_config_model.csv_choice_tagfree_analysisstatus = True
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = 2
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 3
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
    system_importer_file_csv_config_model.csv_choice_dnsname = True
    system_importer_file_csv_config_model.csv_column_dnsname = 4
    system_importer_file_csv_config_model.csv_choice_domain = True
    system_importer_file_csv_config_model.csv_column_domain = 5
    system_importer_file_csv_config_model.csv_choice_location = True
    system_importer_file_csv_config_model.csv_column_location = 6
    system_importer_file_csv_config_model.csv_choice_os = True
    system_importer_file_csv_config_model.csv_column_os = 7
    system_importer_file_csv_config_model.csv_choice_reason = True
    system_importer_file_csv_config_model.csv_column_reason = 8
    system_importer_file_csv_config_model.csv_choice_recommendation = True
    system_importer_file_csv_config_model.csv_column_recommendation = 9
    system_importer_file_csv_config_model.csv_choice_serviceprovider = True
    system_importer_file_csv_config_model.csv_column_serviceprovider = 10
    system_importer_file_csv_config_model.csv_choice_systemtype = True
    system_importer_file_csv_config_model.csv_column_systemtype = 11
    system_importer_file_csv_config_model.csv_choice_case = True
    system_importer_file_csv_config_model.csv_column_case = 12
    system_importer_file_csv_config_model.csv_choice_company = True
    system_importer_file_csv_config_model.csv_column_company = 13
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_complete_attributes_database():
    """ set config """

    # get objects
    case_db_1 = Case.objects.get(case_name='case_db_1')
    company_db_1 = Company.objects.get(company_name='company_db_1')
    dnsname_db_1 = Dnsname.objects.get(dnsname_name='dnsname_db_1')
    domain_db_1 = Domain.objects.get(domain_name='domain_db_1')
    location_db_1 = Location.objects.get(location_name='location_db_1')
    os_db_1 = Os.objects.get(os_name='os_db_1')
    reason_db_1 = Reason.objects.get(reason_name='reason_db_1')
    recommendation_db_1 = Recommendation.objects.get(recommendation_name='recommendation_db_1')
    serviceprovider_db_1 = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_db_1')
    systemtype_db_1 = Systemtype.objects.get(systemtype_name='systemtype_db_1')
    tag_db_1 = Tag.objects.get(tag_name='tag_db_1')

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_column_system = 1
    system_importer_file_csv_config_model.csv_default_dnsname = dnsname_db_1
    system_importer_file_csv_config_model.csv_default_domain = domain_db_1
    system_importer_file_csv_config_model.csv_default_location = location_db_1
    system_importer_file_csv_config_model.csv_default_os = os_db_1
    system_importer_file_csv_config_model.csv_default_reason = reason_db_1
    system_importer_file_csv_config_model.csv_default_recommendation = recommendation_db_1
    system_importer_file_csv_config_model.csv_default_serviceprovider = serviceprovider_db_1
    system_importer_file_csv_config_model.csv_default_systemtype = systemtype_db_1
    system_importer_file_csv_config_model.csv_tag_prefix = None
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = None
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
    system_importer_file_csv_config_model.save()

    system_importer_file_csv_config_model.csv_default_case.add(case_db_1)
    system_importer_file_csv_config_model.csv_default_company.add(company_db_1)
    system_importer_file_csv_config_model.csv_default_tag.add(tag_db_1)

    # return to test function
    return

def set_config_complete_overwrite_csv():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_remove_systemstatus = True
    system_importer_file_csv_config_model.csv_remove_analysisstatus = True
    system_importer_file_csv_config_model.csv_remove_ip = True
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
    system_importer_file_csv_config_model.csv_remove_dnsname = True
    system_importer_file_csv_config_model.csv_remove_domain = True
    system_importer_file_csv_config_model.csv_remove_location = True
    system_importer_file_csv_config_model.csv_remove_os = True
    system_importer_file_csv_config_model.csv_remove_reason = True
    system_importer_file_csv_config_model.csv_remove_recommendation = True
    system_importer_file_csv_config_model.csv_remove_serviceprovider = True
    system_importer_file_csv_config_model.csv_remove_systemtype = True
    system_importer_file_csv_config_model.csv_remove_case = True
    system_importer_file_csv_config_model.csv_remove_company = True
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_complete_preserve_csv():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_remove_systemstatus = False
    system_importer_file_csv_config_model.csv_remove_analysisstatus = False
    system_importer_file_csv_config_model.csv_remove_ip = False
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
    system_importer_file_csv_config_model.csv_remove_dnsname = False
    system_importer_file_csv_config_model.csv_remove_domain = False
    system_importer_file_csv_config_model.csv_remove_location = False
    system_importer_file_csv_config_model.csv_remove_os = False
    system_importer_file_csv_config_model.csv_remove_reason = False
    system_importer_file_csv_config_model.csv_remove_recommendation = False
    system_importer_file_csv_config_model.csv_remove_serviceprovider = False
    system_importer_file_csv_config_model.csv_remove_systemtype = False
    system_importer_file_csv_config_model.csv_remove_case = False
    system_importer_file_csv_config_model.csv_remove_company = False
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_ip_delimiter_comma():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = 2
    system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_comma'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_ip_delimiter_semicolon():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = 2
    system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_semicolon'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_ip_delimiter_space():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_ip = True
    system_importer_file_csv_config_model.csv_column_ip = 2
    system_importer_file_csv_config_model.csv_ip_delimiter = 'ip_space'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_delimiter_comma():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_comma'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_delimiter_semicolon():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_semicolon'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_delimiter_space():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_prefix_delimiter_underscore():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_underscore'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_prefix_delimiter_hyphen():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_hyphen'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_prefix_delimiter_period():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_choice_tag = True
    system_importer_file_csv_config_model.csv_column_tag = 2
    system_importer_file_csv_config_model.csv_tag_delimiter = 'tag_space'
    system_importer_file_csv_config_model.csv_tag_prefix = 'AUTO'
    system_importer_file_csv_config_model.csv_tag_prefix_delimiter = 'tag_prefix_period'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_remove_all():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_all'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_remove_prefix():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_prefix'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_config_tag_remove_none():
    """ set config """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_remove_tag = 'tag_remove_none'
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_csv_import_username(test_user):
    """ set csv_import_username """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_import_username = test_user
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_csv_import_filename(csv_import_filename):
    """ set csv_import_filename """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_import_filename = csv_import_filename
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_csv_import_path(csv_import_path):
    """ set csv_import_path """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_import_path = csv_import_path
    system_importer_file_csv_config_model.save()

    # return to test function
    return

def set_csv_skip_existing_system(csv_skip_existing_system):
    """ set csv_skip_existing_system """

    # change config
    system_importer_file_csv_config_model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name='SystemImporterFileCsvConfig')
    system_importer_file_csv_config_model.csv_skip_existing_system = csv_skip_existing_system
    system_importer_file_csv_config_model.save()

    # return to test function
    return
