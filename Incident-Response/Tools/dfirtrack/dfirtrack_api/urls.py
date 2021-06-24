from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken.views import obtain_auth_token
from dfirtrack_api.views import dfirtrack_artifacts, dfirtrack_main
from dfirtrack_api.openapi.dfirtrack_openapi import DFIRTrackSchemaGenerator

urlpatterns = [

    # dfirtrack_artifacts
    re_path(r'^artifact/$', dfirtrack_artifacts.ArtifactListApi.as_view()),
    re_path(r'^artifact/(?P<pk>\d+)/$', dfirtrack_artifacts.ArtifactDetailApi.as_view()),
    re_path(r'^artifactstatus/$', dfirtrack_artifacts.ArtifactstatusListApi.as_view()),
    re_path(r'^artifactstatus/(?P<pk>\d+)/$', dfirtrack_artifacts.ArtifactstatusDetailApi.as_view()),
    re_path(r'^artifacttype/$', dfirtrack_artifacts.ArtifacttypeListApi.as_view()),
    re_path(r'^artifacttype/(?P<pk>\d+)/$', dfirtrack_artifacts.ArtifacttypeDetailApi.as_view()),

    # dfirtrack_main
    re_path(r'^analysisstatus/$', dfirtrack_main.AnalysisstatusListApi.as_view()),
    re_path(r'^analysisstatus/(?P<pk>\d+)/$', dfirtrack_main.AnalysisstatusDetailApi.as_view()),
    re_path(r'^case/$', dfirtrack_main.CaseListApi.as_view()),
    re_path(r'^case/(?P<pk>\d+)/$', dfirtrack_main.CaseDetailApi.as_view()),
    re_path(r'^company/$', dfirtrack_main.CompanyListApi.as_view()),
    re_path(r'^company/(?P<pk>\d+)/$', dfirtrack_main.CompanyDetailApi.as_view()),
    re_path(r'^contact/$', dfirtrack_main.ContactListApi.as_view()),
    re_path(r'^contact/(?P<pk>\d+)/$', dfirtrack_main.ContactDetailApi.as_view()),
    re_path(r'^division/$', dfirtrack_main.DivisionListApi.as_view()),
    re_path(r'^division/(?P<pk>\d+)/$', dfirtrack_main.DivisionDetailApi.as_view()),
    re_path(r'^dnsname/$', dfirtrack_main.DnsnameListApi.as_view()),
    re_path(r'^dnsname/(?P<pk>\d+)/$', dfirtrack_main.DnsnameDetailApi.as_view()),
    re_path(r'^domain/$', dfirtrack_main.DomainListApi.as_view()),
    re_path(r'^domain/(?P<pk>\d+)/$', dfirtrack_main.DomainDetailApi.as_view()),
    re_path(r'^domainuser/$', dfirtrack_main.DomainuserListApi.as_view()),
    re_path(r'^domainuser/(?P<pk>\d+)/$', dfirtrack_main.DomainuserDetailApi.as_view()),
    re_path(r'^ip/$', dfirtrack_main.IpListApi.as_view()),
    re_path(r'^ip/(?P<pk>\d+)/$', dfirtrack_main.IpDetailApi.as_view()),
    re_path(r'^location/$', dfirtrack_main.LocationListApi.as_view()),
    re_path(r'^location/(?P<pk>\d+)/$', dfirtrack_main.LocationDetailApi.as_view()),
    re_path(r'^os/$', dfirtrack_main.OsListApi.as_view()),
    re_path(r'^os/(?P<pk>\d+)/$', dfirtrack_main.OsDetailApi.as_view()),
    re_path(r'^osarch/$', dfirtrack_main.OsarchListApi.as_view()),
    re_path(r'^osarch/(?P<pk>\d+)/$', dfirtrack_main.OsarchDetailApi.as_view()),
    re_path(r'^reason/$', dfirtrack_main.ReasonListApi.as_view()),
    re_path(r'^reason/(?P<pk>\d+)/$', dfirtrack_main.ReasonDetailApi.as_view()),
    re_path(r'^recommendation/$', dfirtrack_main.RecommendationListApi.as_view()),
    re_path(r'^recommendation/(?P<pk>\d+)/$', dfirtrack_main.RecommendationDetailApi.as_view()),
    re_path(r'^serviceprovider/$', dfirtrack_main.ServiceproviderListApi.as_view()),
    re_path(r'^serviceprovider/(?P<pk>\d+)/$', dfirtrack_main.ServiceproviderDetailApi.as_view()),
    re_path(r'^system/$', dfirtrack_main.SystemListApi.as_view()),
    re_path(r'^system/(?P<pk>\d+)/$', dfirtrack_main.SystemDetailApi.as_view()),
    re_path(r'^systemstatus/$', dfirtrack_main.SystemstatusListApi.as_view()),
    re_path(r'^systemstatus/(?P<pk>\d+)/$', dfirtrack_main.SystemstatusDetailApi.as_view()),
    re_path(r'^systemtype/$', dfirtrack_main.SystemtypeListApi.as_view()),
    re_path(r'^systemtype/(?P<pk>\d+)/$', dfirtrack_main.SystemtypeDetailApi.as_view()),
    re_path(r'^systemuser/$', dfirtrack_main.SystemuserListApi.as_view()),
    re_path(r'^systemuser/(?P<pk>\d+)/$', dfirtrack_main.SystemuserDetailApi.as_view()),
    re_path(r'^tag/$', dfirtrack_main.TagListApi.as_view()),
    re_path(r'^tag/(?P<pk>\d+)/$', dfirtrack_main.TagDetailApi.as_view()),
    re_path(r'^tagcolor/$', dfirtrack_main.TagcolorListApi.as_view()),
    re_path(r'^tagcolor/(?P<pk>\d+)/$', dfirtrack_main.TagcolorDetailApi.as_view()),
    re_path(r'^task/$', dfirtrack_main.TaskListApi.as_view()),
    re_path(r'^task/(?P<pk>\d+)/$', dfirtrack_main.TaskDetailApi.as_view()),
    re_path(r'^taskname/$', dfirtrack_main.TasknameListApi.as_view()),
    re_path(r'^taskname/(?P<pk>\d+)/$', dfirtrack_main.TasknameDetailApi.as_view()),
    re_path(r'^taskpriority/$', dfirtrack_main.TaskpriorityListApi.as_view()),
    re_path(r'^taskpriority/(?P<pk>\d+)/$', dfirtrack_main.TaskpriorityDetailApi.as_view()),
    re_path(r'^taskstatus/$', dfirtrack_main.TaskstatusListApi.as_view()),
    re_path(r'^taskstatus/(?P<pk>\d+)/$', dfirtrack_main.TaskstatusDetailApi.as_view()),
    # Token Authentication
    re_path(r'^token-auth/$', obtain_auth_token),
    # openapi
    re_path(r'^openapi/$', get_schema_view(generator_class=DFIRTrackSchemaGenerator,
            public=True,
        ), name='openapi-schema'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
