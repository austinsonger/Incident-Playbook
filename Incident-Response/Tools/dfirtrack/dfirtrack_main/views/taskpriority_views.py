from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Taskpriority

class TaskpriorityList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Taskpriority
    template_name = 'dfirtrack_main/taskpriority/taskpriority_list.html'
    context_object_name = 'taskpriority_list'
    def get_queryset(self):
        debug_logger(str(self.request.user), " TASKPRIORITY_ENTERED")
        return Taskpriority.objects.order_by('taskpriority_name')

class TaskpriorityDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Taskpriority
    template_name = 'dfirtrack_main/taskpriority/taskpriority_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taskpriority = self.object
        taskpriority.logger(str(self.request.user), " TASKPRIORITYDETAIL_ENTERED")
        return context
