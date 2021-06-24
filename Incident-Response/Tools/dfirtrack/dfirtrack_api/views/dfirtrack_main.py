from dfirtrack_api.serializers.dfirtrack_main import AnalysisstatusSerializer, CaseSerializer, CompanySerializer, ContactSerializer, DivisionSerializer, DnsnameSerializer, DomainSerializer, DomainuserSerializer, IpSerializer, LocationSerializer, OsSerializer, OsarchSerializer, ReasonSerializer, RecommendationSerializer, ServiceproviderSerializer, SystemSerializer, SystemstatusSerializer, SystemtypeSerializer, SystemuserSerializer, TagSerializer, TagcolorSerializer, TaskSerializer, TasknameSerializer, TaskprioritySerializer, TaskstatusSerializer
from dfirtrack_main.models import Analysisstatus, Case, Company, Contact, Division, Dnsname, Domain, Domainuser, Ip, Location, Os, Osarch, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Systemuser, Tag, Tagcolor, Task, Taskname, Taskpriority, Taskstatus
from rest_framework import generics

class AnalysisstatusListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Analysisstatus.objects.all()
    serializer_class = AnalysisstatusSerializer

class AnalysisstatusDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Analysisstatus.objects.all()
    serializer_class = AnalysisstatusSerializer

class CaseListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class CaseDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Case.objects.all()
    serializer_class = CaseSerializer

class CompanyListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ContactListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ContactDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class DivisionListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class DivisionDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Division.objects.all()
    serializer_class = DivisionSerializer

class DnsnameListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Dnsname.objects.all()
    serializer_class = DnsnameSerializer

class DnsnameDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Dnsname.objects.all()
    serializer_class = DnsnameSerializer

class DomainListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

class DomainDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

class DomainuserListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Domainuser.objects.all()
    serializer_class = DomainuserSerializer

class DomainuserDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Domainuser.objects.all()
    serializer_class = DomainuserSerializer

class IpListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Ip.objects.all()
    serializer_class = IpSerializer

class IpDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Ip.objects.all()
    serializer_class = IpSerializer

class LocationListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class LocationDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class OsListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Os.objects.all()
    serializer_class = OsSerializer

class OsDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Os.objects.all()
    serializer_class = OsSerializer

class OsarchListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Osarch.objects.all()
    serializer_class = OsarchSerializer

class OsarchDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Osarch.objects.all()
    serializer_class = OsarchSerializer

class ReasonListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

class ReasonDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer

class RecommendationListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

class RecommendationDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer

class ServiceproviderListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Serviceprovider.objects.all()
    serializer_class = ServiceproviderSerializer

class ServiceproviderDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Serviceprovider.objects.all()
    serializer_class = ServiceproviderSerializer

class SystemListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = System.objects.all()
    serializer_class = SystemSerializer

class SystemDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = System.objects.all()
    serializer_class = SystemSerializer

class SystemstatusListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Systemstatus.objects.all()
    serializer_class = SystemstatusSerializer

class SystemstatusDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Systemstatus.objects.all()
    serializer_class = SystemstatusSerializer

class SystemtypeListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Systemtype.objects.all()
    serializer_class = SystemtypeSerializer

class SystemtypeDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Systemtype.objects.all()
    serializer_class = SystemtypeSerializer

class SystemuserListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Systemuser.objects.all()
    serializer_class = SystemuserSerializer

class SystemuserDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Systemuser.objects.all()
    serializer_class = SystemuserSerializer

class TagListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagcolorListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Tagcolor.objects.all()
    serializer_class = TagcolorSerializer

class TagcolorDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Tagcolor.objects.all()
    serializer_class = TagcolorSerializer

class TaskListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TasknameListApi(generics.ListCreateAPIView):
    """ all objects, allowed: GET + POST """

    queryset = Taskname.objects.all()
    serializer_class = TasknameSerializer

class TasknameDetailApi(generics.RetrieveUpdateAPIView):
    """ single object, allowed: GET + PUT """

    queryset = Taskname.objects.all()
    serializer_class = TasknameSerializer

class TaskpriorityListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Taskpriority.objects.all()
    serializer_class = TaskprioritySerializer

class TaskpriorityDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Taskpriority.objects.all()
    serializer_class = TaskprioritySerializer

class TaskstatusListApi(generics.ListAPIView):
    """ all objects, allowed: GET """

    queryset = Taskstatus.objects.all()
    serializer_class = TaskstatusSerializer

class TaskstatusDetailApi(generics.RetrieveAPIView):
    """ single object, allowed: GET """

    queryset = Taskstatus.objects.all()
    serializer_class = TaskstatusSerializer
