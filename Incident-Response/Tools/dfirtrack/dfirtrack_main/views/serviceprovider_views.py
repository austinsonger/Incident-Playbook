from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import ServiceproviderForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Serviceprovider

class ServiceproviderList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Serviceprovider
    template_name = 'dfirtrack_main/serviceprovider/serviceprovider_list.html'
    context_object_name = 'serviceprovider_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " SERVICEPROVIDER_LIST_ENTERED")
        return Serviceprovider.objects.order_by('serviceprovider_name')

class ServiceproviderDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Serviceprovider
    template_name = 'dfirtrack_main/serviceprovider/serviceprovider_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serviceprovider = self.object
        serviceprovider.logger(str(self.request.user), " SERVICEPROVIDER_DETAIL_ENTERED")
        return context

class ServiceproviderCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Serviceprovider
    form_class = ServiceproviderForm
    template_name = 'dfirtrack_main/serviceprovider/serviceprovider_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " SERVICEPROVIDER_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            serviceprovider = form.save(commit=False)
            serviceprovider.save()
            serviceprovider.logger(str(request.user), " SERVICEPROVIDER_ADD_EXECUTED")
            messages.success(request, 'Serviceprovider added')
            return redirect(reverse('serviceprovider_detail', args=(serviceprovider.serviceprovider_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class ServiceproviderCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Serviceprovider
    form_class = ServiceproviderForm
    template_name = 'dfirtrack_main/serviceprovider/serviceprovider_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " SERVICEPROVIDER_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            serviceprovider = form.save(commit=False)
            serviceprovider.save()
            serviceprovider.logger(str(request.user), " SERVICEPROVIDER_ADD_POPUP_EXECUTED")
            messages.success(request, 'Serviceprovider added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class ServiceproviderUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Serviceprovider
    form_class = ServiceproviderForm
    template_name = 'dfirtrack_main/serviceprovider/serviceprovider_edit.html'

    def get(self, request, *args, **kwargs):
        serviceprovider = self.get_object()
        form = self.form_class(instance=serviceprovider)
        serviceprovider.logger(str(request.user), " SERVICEPROVIDER_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        serviceprovider = self.get_object()
        form = self.form_class(request.POST, instance=serviceprovider)
        if form.is_valid():
            serviceprovider = form.save(commit=False)
            serviceprovider.save()
            serviceprovider.logger(str(request.user), " SERVICEPROVIDER_EDIT_EXECUTED")
            messages.success(request, 'Serviceprovider edited')
            return redirect(reverse('serviceprovider_detail', args=(serviceprovider.serviceprovider_id,)))
        else:
            return render(request, self.template_name, {'form': form})
