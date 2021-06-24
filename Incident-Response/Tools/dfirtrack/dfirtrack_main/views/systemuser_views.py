from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import SystemuserForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Systemuser

class SystemuserList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Systemuser
    template_name = 'dfirtrack_main/systemuser/systemuser_list.html'
    context_object_name = 'systemuser_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " SYSTEMUSER_LIST_ENTERED")
        return Systemuser.objects.order_by('systemuser_name')

class SystemuserDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Systemuser
    template_name = 'dfirtrack_main/systemuser/systemuser_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        systemuser = self.object
        systemuser.logger(str(self.request.user), " SYSTEMUSER_DETAIL_ENTERED")
        return context

class SystemuserCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Systemuser
    form_class = SystemuserForm
    template_name = 'dfirtrack_main/systemuser/systemuser_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " SYSTEMUSER_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            systemuser = form.save(commit=False)
            systemuser.save()
            systemuser.logger(str(request.user), " SYSTEMUSER_ADD_EXECUTED")
            messages.success(request, 'Systemuser added')
            return redirect(reverse('systemuser_detail', args=(systemuser.systemuser_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class SystemuserUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Systemuser
    form_class = SystemuserForm
    template_name = 'dfirtrack_main/systemuser/systemuser_edit.html'

    def get(self, request, *args, **kwargs):
        systemuser = self.get_object()
        form = self.form_class(instance=systemuser)
        systemuser.logger(str(request.user), " SYSTEMUSER_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        systemuser = self.get_object()
        form = self.form_class(request.POST, instance=systemuser)
        if form.is_valid():
            systemuser = form.save(commit=False)
            systemuser.save()
            systemuser.logger(str(request.user), " SYSTEMUSER_EDIT_EXECUTED")
            messages.success(request, 'Systemuser edited')
            return redirect(reverse('systemuser_detail', args=(systemuser.systemuser_id,)))
        else:
            return render(request, self.template_name, {'form': form})
