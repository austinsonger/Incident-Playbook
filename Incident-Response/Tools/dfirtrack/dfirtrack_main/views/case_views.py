from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_artifacts.models import Artifact
from dfirtrack_main.forms import CaseForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Case
from dfirtrack.settings import INSTALLED_APPS as installed_apps

class CaseList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Case
    template_name = 'dfirtrack_main/case/case_list.html'
    context_object_name = 'case_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " CASE_LIST_ENTERED")
        return Case.objects.order_by('case_name')

class CaseDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Case
    template_name = 'dfirtrack_main/case/case_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        case = self.object

        # set dfirtrack_artifacts for template
        if 'dfirtrack_artifacts' in installed_apps:
            context['dfirtrack_artifacts'] = True
            context['artifacts'] = Artifact.objects.filter(case=case)
        else:
            context['dfirtrack_artifacts'] = False

        # call logger
        case.logger(str(self.request.user), " CASE_DETAIL_ENTERED")
        return context

class CaseCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Case
    form_class = CaseForm
    template_name = 'dfirtrack_main/case/case_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " CASE_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.case_created_by_user_id = request.user
            case.save()
            case.logger(str(request.user), " CASE_ADD_EXECUTED")
            messages.success(request, 'Case added')
            return redirect(reverse('case_detail', args=(case.case_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class CaseUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Case
    form_class = CaseForm
    template_name = 'dfirtrack_main/case/case_edit.html'

    def get(self, request, *args, **kwargs):
        case = self.get_object()
        form = self.form_class(instance=case)
        case.logger(str(request.user), " CASE_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        case = self.get_object()
        form = self.form_class(request.POST, instance=case)
        if form.is_valid():
            case = form.save(commit=False)
            case.case_created_by_user_id = request.user
            case.save()
            case.logger(str(request.user), " CASE_EDIT_EXECUTED")
            messages.success(request, 'Case edited')
            return redirect(reverse('case_detail', args=(case.case_id,)))
        else:
            return render(request, self.template_name, {'form': form})
