from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Systemstatus

class SystemstatusList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Systemstatus
    template_name = 'dfirtrack_main/systemstatus/systemstatus_list.html'
    context_object_name = 'systemstatus_list'
    def get_queryset(self):
        debug_logger(str(self.request.user), " SYSTEMSTATUS_ENTERED")
        return Systemstatus.objects.order_by('systemstatus_name')

class SystemstatusDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Systemstatus
    template_name = 'dfirtrack_main/systemstatus/systemstatus_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        systemstatus = self.object
        systemstatus.logger(str(self.request.user), " SYSTEMSTATUSDETAIL_ENTERED")
        return context
