from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_artifacts.models import Artifactstatus
from dfirtrack_main.logger.default_logger import debug_logger

class ArtifactstatusListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Artifactstatus
    template_name = 'dfirtrack_artifacts/artifactstatus/artifactstatus_list.html'
    context_object_name = 'artifactstatus_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), ' ARTIFACTSTATUS_LIST_ENTERED')
        return Artifactstatus.objects.order_by('artifactstatus_name')

class ArtifactstatusDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Artifactstatus
    template_name = 'dfirtrack_artifacts/artifactstatus/artifactstatus_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artifactstatus = self.object
        artifactstatus.logger(str(self.request.user), " ARTIFACTSTATUSDETAIL_ENTERED")
        return context
