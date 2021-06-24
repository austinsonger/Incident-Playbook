from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import DnsnameForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Dnsname

class DnsnameList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Dnsname
    template_name = 'dfirtrack_main/dnsname/dnsname_list.html'
    context_object_name = 'dnsname_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " DNSNAME_LIST_ENTERED")
        return Dnsname.objects.order_by('dnsname_name')

class DnsnameDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Dnsname
    template_name = 'dfirtrack_main/dnsname/dnsname_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dnsname = self.object
        dnsname.logger(str(self.request.user), " DNSNAME_DETAIL_ENTERED")
        return context

class DnsnameCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Dnsname
    form_class = DnsnameForm
    template_name = 'dfirtrack_main/dnsname/dnsname_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DNSNAME_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            dnsname = form.save(commit=False)
            dnsname.save()
            dnsname.logger(str(request.user), " DNSNAME_ADD_EXECUTED")
            messages.success(request, 'DNS name added')
            return redirect(reverse('dnsname_detail', args=(dnsname.dnsname_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class DnsnameCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Dnsname
    form_class = DnsnameForm
    template_name = 'dfirtrack_main/dnsname/dnsname_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DNSNAME_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            dnsname = form.save(commit=False)
            dnsname.save()
            dnsname.logger(str(request.user), " DNSNAME_ADD_POPUP_EXECUTED")
            messages.success(request, 'DNS name added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class DnsnameUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Dnsname
    form_class = DnsnameForm
    template_name = 'dfirtrack_main/dnsname/dnsname_edit.html'

    def get(self, request, *args, **kwargs):
        dnsname = self.get_object()
        form = self.form_class(instance=dnsname)
        dnsname.logger(str(request.user), " DNSNAME_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        dnsname = self.get_object()
        form = self.form_class(request.POST, instance=dnsname)
        if form.is_valid():
            dnsname = form.save(commit=False)
            dnsname.save()
            dnsname.logger(str(request.user), " DNSNAME_EDIT_EXECUTED")
            messages.success(request, 'DNS name edited')
            return redirect(reverse('dnsname_detail', args=(dnsname.dnsname_id,)))
        else:
            return render(request, self.template_name, {'form': form})
