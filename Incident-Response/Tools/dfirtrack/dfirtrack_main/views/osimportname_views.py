from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import OsimportnameForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Osimportname

class OsimportnameList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Osimportname
    template_name = 'dfirtrack_main/osimportname/osimportname_list.html'
    context_object_name = 'osimportname_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " OSIMPORTNAME_LIST_ENTERED")
        return Osimportname.objects.order_by('osimportname_name')

class OsimportnameCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Osimportname
    form_class = OsimportnameForm
    template_name = 'dfirtrack_main/osimportname/osimportname_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " OSIMPORTNAME_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            osimportname = form.save(commit=False)
            osimportname.save()
            osimportname.logger(str(request.user), " OSIMPORTNAME_ADD_EXECUTED")
            messages.success(request, 'OS-Importname added')
            return redirect(reverse('osimportname_list'))
        else:
            return render(request, self.template_name, {'form': form})

class OsimportnameUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Osimportname
    form_class = OsimportnameForm
    template_name = 'dfirtrack_main/osimportname/osimportname_edit.html'

    def get(self, request, *args, **kwargs):
        osimportname = self.get_object()
        form = self.form_class(instance=osimportname)
        osimportname.logger(str(request.user), " OSIMPORTNAME_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        osimportname = self.get_object()
        form = self.form_class(request.POST, instance=osimportname)
        if form.is_valid():
            osimportname = form.save(commit=False)
            osimportname.save()
            osimportname.logger(str(request.user), " OSIMPORTNAME_EDIT_EXECUTED")
            messages.success(request, 'OS-Importname edited')
            return redirect(reverse('osimportname_list'))
        else:
            return render(request, self.template_name, {'form': form})
