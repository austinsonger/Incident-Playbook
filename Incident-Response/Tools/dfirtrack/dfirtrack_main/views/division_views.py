from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import DivisionForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Division

class DivisionList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Division
    template_name = 'dfirtrack_main/division/division_list.html'
    context_object_name = 'division_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " DIVISION_LIST_ENTERED")
        return Division.objects.order_by('division_name')

class DivisionDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Division
    template_name = 'dfirtrack_main/division/division_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        division = self.object
        division.logger(str(self.request.user), " DIVISION_DETAIL_ENTERED")
        return context

class DivisionCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Division
    form_class = DivisionForm
    template_name = 'dfirtrack_main/division/division_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DIVISION_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            division = form.save(commit=False)
            division.save()
            division.logger(str(request.user), " DIVISION_ADD_EXECUTED")
            messages.success(request, 'Division added')
            return redirect(reverse('division_detail', args=(division.division_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class DivisionUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Division
    form_class = DivisionForm
    template_name = 'dfirtrack_main/division/division_edit.html'

    def get(self, request, *args, **kwargs):
        division = self.get_object()
        form = self.form_class(instance=division)
        division.logger(str(request.user), " DIVISION_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        division = self.get_object()
        form = self.form_class(request.POST, instance=division)
        if form.is_valid():
            division = form.save(commit=False)
            division.save()
            division.logger(str(request.user), " DIVISION_EDIT_EXECUTED")
            messages.success(request, 'Division edited')
            return redirect(reverse('division_detail', args=(division.division_id,)))
        else:
            return render(request, self.template_name, {'form': form})
