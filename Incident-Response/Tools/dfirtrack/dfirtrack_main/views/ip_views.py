from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Ip

class IpList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Ip
    template_name = 'dfirtrack_main/ip/ip_list.html'
    context_object_name = 'ip_list'
    def get_queryset(self):
        debug_logger(str(self.request.user), " IP_ENTERED")
        return Ip.objects.order_by('ip_ip')

class IpDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Ip
    template_name = 'dfirtrack_main/ip/ip_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip = self.object
        ip.logger(str(self.request.user), " IPDETAIL_ENTERED")
        return context
