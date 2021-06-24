from datetime import datetime, timedelta, time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from dfirtrack_artifacts.models import Artifact, Artifactpriority, Artifactstatus
from dfirtrack_config.models import MainConfigModel, Statushistory
from dfirtrack_main.models import Analysisstatus, System, Systemstatus, Task, Taskstatus, Taskpriority
from dfirtrack_main.logger.default_logger import debug_logger

def get_status_objects(context):

        # get config model
        main_config_model = MainConfigModel.objects.get(main_config_name = 'MainConfig')
        # get number of entrys to show
        statushistory_entry_numbers = main_config_model .statushistory_entry_numbers

        # get last statushistory objects for dropdown menu according to config
        context['statushistory_all'] = Statushistory.objects.all().order_by('-statushistory_id')[:statushistory_entry_numbers]
        # reverse order for better dropdown display
        context['statushistory_all'] = reversed(context['statushistory_all'])

        # prepare dates
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        yesterday = today - timedelta(1)
        two_days_ago = today - timedelta(2)
        three_days_ago = today - timedelta(3)
        today_start = datetime.combine(today, time(), tzinfo=timezone.utc)
        today_end = datetime.combine(tomorrow, time(), tzinfo=timezone.utc)
        yesterday_start = datetime.combine(yesterday, time(), tzinfo=timezone.utc)
        two_days_ago_start = datetime.combine(two_days_ago, time(), tzinfo=timezone.utc)
        three_days_ago_start = datetime.combine(three_days_ago, time(), tzinfo=timezone.utc)

        # get numbers
        context['artifacts_number'] = Artifact.objects.all().count()
        context['systems_number'] = System.objects.all().count()
        context['tasks_number'] = Task.objects.all().count()

        # get numbers according to date
        context['artifacts_today_number'] = Artifact.objects.filter(artifact_create_time__lt=today_end, artifact_create_time__gte=today_start).count()
        context['artifacts_yesterday_number'] = Artifact.objects.filter(artifact_create_time__lt=today_start, artifact_create_time__gte=yesterday_start).count()
        context['artifacts_two_days_ago_number'] = Artifact.objects.filter(artifact_create_time__lt=yesterday_start, artifact_create_time__gte=two_days_ago_start).count()
        context['artifacts_three_days_ago_number'] = Artifact.objects.filter(artifact_create_time__lt=two_days_ago_start, artifact_create_time__gte=three_days_ago_start).count()
        context['systems_today_number'] = System.objects.filter(system_create_time__lt=today_end, system_create_time__gte=today_start).count()
        context['systems_yesterday_number'] = System.objects.filter(system_create_time__lt=today_start, system_create_time__gte=yesterday_start).count()
        context['systems_two_days_ago_number'] = System.objects.filter(system_create_time__lt=yesterday_start, system_create_time__gte=two_days_ago_start).count()
        context['systems_three_days_ago_number'] = System.objects.filter(system_create_time__lt=two_days_ago_start, system_create_time__gte=three_days_ago_start).count()
        context['tasks_today_number'] = Task.objects.filter(task_create_time__lt=today_end, task_create_time__gte=today_start).count()
        context['tasks_yesterday_number'] = Task.objects.filter(task_create_time__lt=today_start, task_create_time__gte=yesterday_start).count()
        context['tasks_two_days_ago_number'] = Task.objects.filter(task_create_time__lt=yesterday_start, task_create_time__gte=two_days_ago_start).count()
        context['tasks_three_days_ago_number'] = Task.objects.filter(task_create_time__lt=two_days_ago_start, task_create_time__gte=three_days_ago_start).count()

        # get objects
        context['analysisstatus_all'] = Analysisstatus.objects.all().order_by('analysisstatus_name')
        context['artifactpriority_all'] = Artifactpriority.objects.all().order_by('artifactpriority_name')
        context['artifactstatus_all'] = Artifactstatus.objects.all().order_by('artifactstatus_name')
        context['systemstatus_all'] = Systemstatus.objects.all().order_by('systemstatus_name')
        context['taskstatus_all'] = Taskstatus.objects.all().order_by('taskstatus_name')
        context['taskpriority_all'] = Taskpriority.objects.all().order_by('taskpriority_name')

        return context

class StatusDetailView(LoginRequiredMixin, DetailView):
    """ status view to show current and one saved status """

    login_url = '/login'
    model = Statushistory
    template_name = 'dfirtrack_config/status/status_detail.html'

    def get_context_data(self, *args, **kwargs):

        # get context
        context = super(StatusDetailView, self).get_context_data(*args, **kwargs)

        # get object for detail view
        statushistory = self.object

        # add status objects to context dictionary
        context = get_status_objects(context)

        # call logger
        debug_logger(str(self.request.user), ' STATUS_DETAIL_ENTERED statushistory_id:' + str(statushistory.statushistory_id) + '|statushistory_time:' + str(statushistory))

        # return context dictionary
        return context

class StatusView(LoginRequiredMixin, TemplateView):
    """ status view to show current status """

    login_url = '/login'
    template_name = 'dfirtrack_config/status/status.html'

    def get_context_data(self, *args, **kwargs):

        # get context
        context = super(StatusView, self).get_context_data(*args, **kwargs)

        # add status objects to context dictionary
        context = get_status_objects(context)

        # call logger
        debug_logger(str(self.request.user), ' STATUS_ENTERED')

        # return context dictionary
        return context
