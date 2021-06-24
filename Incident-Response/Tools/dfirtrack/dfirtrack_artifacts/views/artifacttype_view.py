from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from dfirtrack_artifacts.models import Artifacttype
from dfirtrack_artifacts.forms import ArtifacttypeForm
from dfirtrack_main.logger.default_logger import debug_logger

class ArtifacttypeListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Artifacttype
    template_name = 'dfirtrack_artifacts/artifacttype/artifacttype_list.html'
    context_object_name = 'artifacttype_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " ARTIFACTTYPE_LIST_ENTERED")
        return Artifacttype.objects.order_by('artifacttype_name')

class ArtifacttypeDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Artifacttype
    template_name = 'dfirtrack_artifacts/artifacttype/artifacttype_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artifacttype = self.object
        artifacttype.logger(str(self.request.user), ' ARTIFACTTYPE_DETAIL_ENTERED')
        return context

class ArtifacttypeCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Artifacttype
    form_class = ArtifacttypeForm
    template_name = 'dfirtrack_artifacts/artifacttype/artifacttype_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), ' ARTIFACTTYPE_ADD_ENTERED')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        self.object = form.save()
        self.object.logger(str(self.request.user), ' ARTIFACTTYPE_ADD_EXECUTED')
        messages.success(self.request, 'Artifacttype added')
        return super().form_valid(form)

class ArtifacttypeUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Artifacttype
    form_class = ArtifacttypeForm
    template_name = 'dfirtrack_artifacts/artifacttype/artifacttype_edit.html'

    def get(self, request, *args, **kwargs):
        artifacttype = self.get_object()
        form = self.form_class(instance = artifacttype)
        artifacttype.logger(str(request.user), ' ARTIFACTTYPE_EDIT_ENTERED')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        self.object = form.save()
        self.object.logger(str(self.request.user), ' ARTIFACTTYPE_EDIT_EXECUTED')
        messages.success(self.request, 'Artifacttype edited')
        return super().form_valid(form)
