from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from dfirtrack_artifacts.models import Artifactpriority
from dfirtrack_main.logger.default_logger import debug_logger

class ArtifactpriorityListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Artifactpriority
    template_name = 'dfirtrack_artifacts/artifactpriority/artifactpriority_list.html'
    context_object_name = 'artifactpriority_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), ' ARTIFACTPRIORITY_LIST_ENTERED')
        return Artifactpriority.objects.order_by('artifactpriority_name')

class ArtifactpriorityDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Artifactpriority
    template_name = 'dfirtrack_artifacts/artifactpriority/artifactpriority_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artifactpriority = self.object
        artifactpriority.logger(str(self.request.user), " ARTIFACTPRIORITYDETAIL_ENTERED")
        return context
