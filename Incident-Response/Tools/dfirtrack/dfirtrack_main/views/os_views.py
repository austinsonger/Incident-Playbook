from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import OsForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Os

class OsList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Os
    template_name = 'dfirtrack_main/os/os_list.html'
    context_object_name = 'os_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " OS_LIST_ENTERED")
        return Os.objects.order_by('os_name')

class OsDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Os
    template_name = 'dfirtrack_main/os/os_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        os = self.object
        os.logger(str(self.request.user), " OS_DETAIL_ENTERED")
        return context

class OsCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Os
    form_class = OsForm
    template_name = 'dfirtrack_main/os/os_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " OS_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.save()
            os.logger(str(request.user), " OS_ADD_EXECUTED")
            messages.success(request, 'OS added')
            return redirect(reverse('os_detail', args=(os.os_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class OsCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Os
    form_class = OsForm
    template_name = 'dfirtrack_main/os/os_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " OS_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.save()
            os.logger(str(request.user), " OS_ADD_POPUP_EXECUTED")
            messages.success(request, 'OS added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class OsUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Os
    form_class = OsForm
    template_name = 'dfirtrack_main/os/os_edit.html'

    def get(self, request, *args, **kwargs):
        os = self.get_object()
        form = self.form_class(instance=os)
        os.logger(str(request.user), " OS_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        os = self.get_object()
        form = self.form_class(request.POST, instance=os)
        if form.is_valid():
            os = form.save(commit=False)
            os.save()
            os.logger(str(request.user), " OS_EDIT_EXECUTED")
            messages.success(request, 'OS edited')
            return redirect(reverse('os_detail', args=(os.os_id,)))
        else:
            return render(request, self.template_name, {'form': form})
