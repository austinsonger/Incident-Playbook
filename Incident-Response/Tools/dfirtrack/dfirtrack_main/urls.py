from django import views as django_views
from django.conf.urls import url
from django.urls import path
from dfirtrack_main.views import analysisstatus_views, analystmemo_views, case_views, company_views, contact_views, division_views, dnsname_views, domain_views, domainuser_views, entry_views, headline_views, ip_views, location_views, os_views, osimportname_views, reason_views, recommendation_views, reportitem_views, serviceprovider_views, system_views, systemstatus_views, systemtype_views, systemuser_views, tag_views, task_views, taskname_views, taskpriority_views, taskstatus_views
from dfirtrack_main.creator import system_creator, tag_creator, task_creator
from dfirtrack_main.exporter.spreadsheet import csv as spreadsheet_csv
from dfirtrack_main.exporter.spreadsheet import xls
from dfirtrack_main.exporter.markdown import markdown
from dfirtrack_main.importer.file import csv as csv_importer
from dfirtrack_main.modificator import system_modificator

urlpatterns = [

    path(r'analysisstatus/', analysisstatus_views.AnalysisstatusList.as_view(), name='analysisstatus_list'),
    path(r'analysisstatus/<int:pk>/', analysisstatus_views.AnalysisstatusDetail.as_view(), name='analysisstatus_detail'),

    path(r'analystmemo/', analystmemo_views.AnalystmemoList.as_view(), name='analystmemo_list'),
    path(r'analystmemo/<int:pk>/', analystmemo_views.AnalystmemoDetail.as_view(), name='analystmemo_detail'),
    path(r'analystmemo/add/', analystmemo_views.AnalystmemoCreate.as_view(), name='analystmemo_create'),
    path(r'analystmemo/<int:pk>/edit/', analystmemo_views.AnalystmemoUpdate.as_view(), name='analystmemo_update'),

    path(r'case/', case_views.CaseList.as_view(), name='case_list'),
    path(r'case/<int:pk>/', case_views.CaseDetail.as_view(), name='case_detail'),
    path(r'case/add/', case_views.CaseCreate.as_view(), name='case_create'),
    path(r'case/<int:pk>/edit/', case_views.CaseUpdate.as_view(), name='case_update'),

    path(r'company/', company_views.CompanyList.as_view(), name='company_list'),
    path(r'company/<int:pk>/', company_views.CompanyDetail.as_view(), name='company_detail'),
    path(r'company/add/', company_views.CompanyCreate.as_view(), name='company_create'),
    path(r'company/add_popup/', company_views.CompanyCreatePopup.as_view(), name='company_add_popup'),
    path(r'company/<int:pk>/edit/', company_views.CompanyUpdate.as_view(), name='company_update'),

    path(r'contact/', contact_views.ContactList.as_view(), name='contact_list'),
    path(r'contact/<int:pk>/', contact_views.ContactDetail.as_view(), name='contact_detail'),
    path(r'contact/add/', contact_views.ContactCreate.as_view(), name='contact_create'),
    path(r'contact/add_popup/', contact_views.ContactCreatePopup.as_view(), name='contact_add_popup'),
    path(r'contact/<int:pk>/edit/', contact_views.ContactUpdate.as_view(), name='contact_update'),

    path(r'division/', division_views.DivisionList.as_view(), name='division_list'),
    path(r'division/<int:pk>/', division_views.DivisionDetail.as_view(), name='division_detail'),
    path(r'division/add/', division_views.DivisionCreate.as_view(), name='division_create'),
    path(r'division/<int:pk>/edit/', division_views.DivisionUpdate.as_view(), name='division_update'),

    path(r'dnsname/', dnsname_views.DnsnameList.as_view(), name='dnsname_list'),
    path(r'dnsname/<int:pk>/', dnsname_views.DnsnameDetail.as_view(), name='dnsname_detail'),
    path(r'dnsname/add/', dnsname_views.DnsnameCreate.as_view(), name='dnsname_create'),
    path(r'dnsname/add_popup/', dnsname_views.DnsnameCreatePopup.as_view(), name='dnsname_add_popup'),
    path(r'dnsname/<int:pk>/edit/', dnsname_views.DnsnameUpdate.as_view(), name='dnsname_update'),

    path(r'domain/', domain_views.DomainList.as_view(), name='domain_list'),
    path(r'domain/<int:pk>/', domain_views.DomainDetail.as_view(), name='domain_detail'),
    path(r'domain/add/', domain_views.DomainCreate.as_view(), name='domain_create'),
    path(r'domain/add_popup/', domain_views.DomainCreatePopup.as_view(), name='domain_add_popup'),
    path(r'domain/<int:pk>/edit/', domain_views.DomainUpdate.as_view(), name='domain_update'),

    path(r'domainuser/', domainuser_views.DomainuserList.as_view(), name='domainuser_list'),
    path(r'domainuser/<int:pk>/', domainuser_views.DomainuserDetail.as_view(), name='domainuser_detail'),
    path(r'domainuser/add/', domainuser_views.DomainuserCreate.as_view(), name='domainuser_create'),
    path(r'domainuser/<int:pk>/edit/', domainuser_views.DomainuserUpdate.as_view(), name='domainuser_update'),

    path(r'entry/', entry_views.EntryList.as_view(), name='entry_list'),
    path(r'entry/<int:pk>/', entry_views.EntryDetail.as_view(), name='entry_detail'),
    path(r'entry/add/', entry_views.EntryCreate.as_view(), name='entry_create'),
    path(r'entry/<int:pk>/edit/', entry_views.EntryUpdate.as_view(), name='entry_update'),

    path(r'headline/', headline_views.HeadlineList.as_view(), name='headline_list'),
    path(r'headline/<int:pk>/', headline_views.HeadlineDetail.as_view(), name='headline_detail'),
    path(r'headline/add/', headline_views.HeadlineCreate.as_view(), name='headline_create'),
    path(r'headline/<int:pk>/edit/', headline_views.HeadlineUpdate.as_view(), name='headline_update'),

    path(r'ip/', ip_views.IpList.as_view(), name='ip_list'),
    path(r'ip/<int:pk>/', ip_views.IpDetail.as_view(), name='ip_detail'),

    path(r'location/', location_views.LocationList.as_view(), name='location_list'),
    path(r'location/<int:pk>/', location_views.LocationDetail.as_view(), name='location_detail'),
    path(r'location/add/', location_views.LocationCreate.as_view(), name='location_create'),
    path(r'location/add_popup/', location_views.LocationCreatePopup.as_view(), name='location_add_popup'),
    path(r'location/<int:pk>/edit/', location_views.LocationUpdate.as_view(), name='location_update'),

    path(r'os/', os_views.OsList.as_view(), name='os_list'),
    path(r'os/<int:pk>/', os_views.OsDetail.as_view(), name='os_detail'),
    path(r'os/add/', os_views.OsCreate.as_view(), name='os_create'),
    path(r'os/add_popup/', os_views.OsCreatePopup.as_view(), name='os_add_popup'),
    path(r'os/<int:pk>/edit/', os_views.OsUpdate.as_view(), name='os_update'),

    path(r'osimportname/', osimportname_views.OsimportnameList.as_view(), name='osimportname_list'),
    path(r'osimportname/add/', osimportname_views.OsimportnameCreate.as_view(), name='osimportname_create'),
    path(r'osimportname/<int:pk>/edit/', osimportname_views.OsimportnameUpdate.as_view(), name='osimportname_update'),

    path(r'reason/', reason_views.ReasonList.as_view(), name='reason_list'),
    path(r'reason/<int:pk>/', reason_views.ReasonDetail.as_view(), name='reason_detail'),
    path(r'reason/add/', reason_views.ReasonCreate.as_view(), name='reason_create'),
    path(r'reason/add_popup/', reason_views.ReasonCreatePopup.as_view(), name='reason_add_popup'),
    path(r'reason/<int:pk>/edit/', reason_views.ReasonUpdate.as_view(), name='reason_update'),

    path(r'recommendation/', recommendation_views.RecommendationList.as_view(), name='recommendation_list'),
    path(r'recommendation/<int:pk>/', recommendation_views.RecommendationDetail.as_view(), name='recommendation_detail'),
    path(r'recommendation/add/', recommendation_views.RecommendationCreate.as_view(), name='recommendation_create'),
    path(r'recommendation/add_popup/', recommendation_views.RecommendationCreatePopup.as_view(), name='recommendation_create_popup'),
    path(r'recommendation/<int:pk>/edit/', recommendation_views.RecommendationUpdate.as_view(), name='recommendation_update'),

    path(r'reportitem/', reportitem_views.ReportitemList.as_view(), name='reportitem_list'),
    path(r'reportitem/<int:pk>/', reportitem_views.ReportitemDetail.as_view(), name='reportitem_detail'),
    path(r'reportitem/add/', reportitem_views.ReportitemCreate.as_view(), name='reportitem_create'),
    path(r'reportitem/<int:pk>/edit/', reportitem_views.ReportitemUpdate.as_view(), name='reportitem_update'),

    path(r'serviceprovider/', serviceprovider_views.ServiceproviderList.as_view(), name='serviceprovider_list'),
    path(r'serviceprovider/<int:pk>/', serviceprovider_views.ServiceproviderDetail.as_view(), name='serviceprovider_detail'),
    path(r'serviceprovider/add/', serviceprovider_views.ServiceproviderCreate.as_view(), name='serviceprovider_create'),
    path(r'serviceprovider/add_popup/', serviceprovider_views.ServiceproviderCreatePopup.as_view(), name='serviceprovider_add_popup'),
    path(r'serviceprovider/<int:pk>/edit/', serviceprovider_views.ServiceproviderUpdate.as_view(), name='serviceprovider_update'),

    path(r'system/', system_views.SystemList.as_view(), name='system_list'),
    path(r'system/<int:pk>/', system_views.SystemDetail.as_view(), name='system_detail'),
    path(r'system/add/', system_views.SystemCreate.as_view(), name='system_create'),
    path(r'system/<int:pk>/edit/', system_views.SystemUpdate.as_view(), name='system_update'),
    path(r'system/json/', system_views.get_systems_json, name='system_json'),

    path(r'system/creator/', system_creator.system_creator, name='system_creator'),
    path(r'system/exporter/markdown/system/', markdown.system, name='system_exporter_markdown'),
    path(r'system/exporter/spreadsheet/csv/system/', spreadsheet_csv.system, name='system_exporter_spreadsheet_csv'),
    path(r'system/exporter/spreadsheet/xls/system/', xls.system, name='system_exporter_spreadsheet_xls'),
    path(r'system/importer/file/csv/cron/', csv_importer.system_create_cron, name='system_importer_file_csv_cron'),
    path(r'system/importer/file/csv/instant/', csv_importer.system_instant, name='system_importer_file_csv_instant'),
    path(r'system/importer/file/csv/upload/', csv_importer.system_upload, name='system_importer_file_csv_upload'),
    path(r'system/modificator/', system_modificator.system_modificator, name='system_modificator'),

    path(r'systemstatus/', systemstatus_views.SystemstatusList.as_view(), name='systemstatus_list'),
    path(r'systemstatus/<int:pk>/', systemstatus_views.SystemstatusDetail.as_view(), name='systemstatus_detail'),

    path(r'systemtype/', systemtype_views.SystemtypeList.as_view(), name='systemtype_list'),
    path(r'systemtype/<int:pk>/', systemtype_views.SystemtypeDetail.as_view(), name='systemtype_detail'),
    path(r'systemtype/add/', systemtype_views.SystemtypeCreate.as_view(), name='systemtype_create'),
    path(r'systemtype/add_popup/', systemtype_views.SystemtypeCreatePopup.as_view(), name='systemtype_add_popup'),
    path(r'systemtype/<int:pk>/edit/', systemtype_views.SystemtypeUpdate.as_view(), name='systemtype_update'),

    path(r'systemuser/', systemuser_views.SystemuserList.as_view(), name='systemuser_list'),
    path(r'systemuser/<int:pk>/', systemuser_views.SystemuserDetail.as_view(), name='systemuser_detail'),
    path(r'systemuser/add/', systemuser_views.SystemuserCreate.as_view(), name='systemuser_create'),
    path(r'systemuser/<int:pk>/edit/', systemuser_views.SystemuserUpdate.as_view(), name='systemuser_update'),

    path(r'tag/', tag_views.TagList.as_view(), name='tag_list'),
    path(r'tag/<int:pk>/', tag_views.TagDetail.as_view(), name='tag_detail'),
    path(r'tag/add/', tag_views.TagCreate.as_view(), name='tag_create'),
    path(r'tag/<int:pk>/edit/', tag_views.TagUpdate.as_view(), name='tag_update'),
    path(r'tag/<int:pk>/delete/', tag_views.TagDelete.as_view(), name='tag_delete'),

    path(r'tag/creator/', tag_creator.tag_creator, name='tag_creator'),

    path(r'task/', task_views.TaskList.as_view(), name='task_list'),
    path(r'task/closed/', task_views.TaskClosed.as_view(), name='task_closed'),
    path(r'task/all/', task_views.TaskAll.as_view(), name='task_all'),
    path(r'task/<int:pk>/', task_views.TaskDetail.as_view(), name='task_detail'),
    path(r'task/add/', task_views.TaskCreate.as_view(), name='task_create'),
    path(r'task/<int:pk>/edit/', task_views.TaskUpdate.as_view(), name='task_update'),

    path(r'task/<int:pk>/start/', task_views.TaskStart.as_view(), name='task_start'),
    path(r'task/<int:pk>/finish/', task_views.TaskFinish.as_view(), name='task_finish'),
    path(r'task/<int:pk>/renew/', task_views.TaskRenew.as_view(), name='task_renew'),
    path(r'task/<int:pk>/set_user/', task_views.TaskSetUser.as_view(), name='task_set_user'),
    path(r'task/<int:pk>/unset_user/', task_views.TaskUnsetUser.as_view(), name='task_unset_user'),

    path(r'task/creator/', task_creator.task_creator, name='task_creator'),

    path(r'taskname/', taskname_views.TasknameList.as_view(), name='taskname_list'),
    path(r'taskname/<int:pk>/', taskname_views.TasknameDetail.as_view(), name='taskname_detail'),
    path(r'taskname/add/', taskname_views.TasknameCreate.as_view(), name='taskname_create'),
    path(r'taskname/<int:pk>/edit/', taskname_views.TasknameUpdate.as_view(), name='taskname_update'),
    path(r'taskname/<int:pk>/close/', taskname_views.TasknameClose.as_view(), name='taskname_close'),

    path(r'taskpriority/', taskpriority_views.TaskpriorityList.as_view(), name='taskpriority_list'),
    path(r'taskpriority/<int:pk>/', taskpriority_views.TaskpriorityDetail.as_view(), name='taskpriority_detail'),

    path(r'taskstatus/', taskstatus_views.TaskstatusList.as_view(), name='taskstatus_list'),
    path(r'taskstatus/<int:pk>/', taskstatus_views.TaskstatusDetail.as_view(), name='taskstatus_detail'),

    url(r'^jsi18n/$', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),

]
