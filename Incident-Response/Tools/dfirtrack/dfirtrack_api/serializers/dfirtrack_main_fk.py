from dfirtrack_main.models import Analysisstatus, Case, Company, Contact, Division, Dnsname, Domain, Ip, Location, Os, Osarch, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor, Task, Taskname, Taskpriority, Taskstatus
from rest_framework import serializers

# serializers for foreignkey relationsships

class AnalysisstatusFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Analysisstatus
        # attributes made available for api
        fields = (
            'analysisstatus_name',
        )

class CaseFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsship """

    class Meta:
        model = Case
        # attributes made available for api
        fields = (
            'case_name',
        )

class CompanyFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Company
        # attributes made available for api
        fields = (
            'company_name',
        )

class ContactFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Contact
        # attributes made available for api
        fields = (
            'contact_email',
        )

class DivisionFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Division
        # attributes made available for api
        fields = (
            'division_name',
        )

class DnsnameFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Dnsname
        # attributes made available for api
        fields = (
            'dnsname_name',
        )

class DomainFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Domain
        # attributes made available for api
        fields = (
            'domain_name',
        )

class HostSystemFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsship """

    class Meta:
        model = System
        # attributes made available for api
        fields = (
            'system_id',
            'system_name',
        )

class IpFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Ip
        # attributes made available for api
        fields = (
            'ip_ip',
        )

class LocationFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Location
        # attributes made available for api
        fields = (
            'location_name',
        )

class OsFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Os
        # attributes made available for api
        fields = (
            'os_name',
        )

class OsarchFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Osarch
        # attributes made available for api
        fields = (
            'osarch_name',
        )

class ParentTaskFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsship """

    class Meta:
        model = Task
        # attributes made available for api
        fields = (
            'task_id',
        )

class ReasonFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Reason
        # attributes made available for api
        fields = (
            'reason_name',
        )

class RecommendationFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Recommendation
        # attributes made available for api
        fields = (
            'recommendation_name',
        )

class ServiceproviderFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Serviceprovider
        # attributes made available for api
        fields = (
            'serviceprovider_name',
        )

class SystemFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = System
        # attributes made available for api
        fields = (
            'system_name',
        )

class SystemstatusFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Systemstatus
        # attributes made available for api
        fields = (
            'systemstatus_name',
        )

class SystemtypeFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Systemtype
        # attributes made available for api
        fields = (
            'systemtype_name',
        )

class TagFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Tag
        # attributes made available for api
        fields = (
            'tag_name',
        )

class TagcolorFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Tagcolor
        # attributes made available for api
        fields = (
            'tagcolor_name',
        )

class TasknameFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Taskname
        # attributes made available for api
        fields = (
            'taskname_name',
        )

class TaskpriorityFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Taskpriority
        # attributes made available for api
        fields = (
            'taskpriority_name',
        )

class TaskstatusFkSerializer(serializers.ModelSerializer):
    """ create serializer for foreignkey relationsships """

    class Meta:
        model = Taskstatus
        # attributes made available for api
        fields = (
            'taskstatus_name',
        )
