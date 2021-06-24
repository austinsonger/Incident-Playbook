from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Analysisstatus

class AnalysisstatusList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Analysisstatus
    template_name = 'dfirtrack_main/analysisstatus/analysisstatus_list.html'
    context_object_name = 'analysisstatus_list'
    def get_queryset(self):
        debug_logger(str(self.request.user), " ANALYSISSTATUS_ENTERED")
        return Analysisstatus.objects.order_by('analysisstatus_name')

class AnalysisstatusDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Analysisstatus
    template_name = 'dfirtrack_main/analysisstatus/analysisstatus_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysisstatus = self.object
        analysisstatus.logger(str(self.request.user), " ANALYSISSTATUSDETAIL_ENTERED")
        return context
