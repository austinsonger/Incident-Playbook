from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Taskstatus

class TaskstatusList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Taskstatus
    template_name = 'dfirtrack_main/taskstatus/taskstatus_list.html'
    context_object_name = 'taskstatus_list'
    def get_queryset(self):
        debug_logger(str(self.request.user), " TASKSTATUS_ENTERED")
        return Taskstatus.objects.order_by('taskstatus_name')

class TaskstatusDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Taskstatus
    template_name = 'dfirtrack_main/taskstatus/taskstatus_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taskstatus = self.object
        taskstatus.logger(str(self.request.user), " TASKSTATUSDETAIL_ENTERED")
        return context
