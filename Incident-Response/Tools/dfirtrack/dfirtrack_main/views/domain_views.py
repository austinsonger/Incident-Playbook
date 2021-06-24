from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import DomainForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Domain

class DomainList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Domain
    template_name = 'dfirtrack_main/domain/domain_list.html'
    context_object_name = 'domain_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " DOMAIN_LIST_ENTERED")
        return Domain.objects.order_by('domain_name')

class DomainDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Domain
    template_name = 'dfirtrack_main/domain/domain_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain = self.object
        domain.logger(str(self.request.user), " DOMAIN_DETAIL_ENTERED")
        return context

class DomainCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Domain
    form_class = DomainForm
    template_name = 'dfirtrack_main/domain/domain_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DOMAIN_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.save()
            domain.logger(str(request.user), " DOMAIN_ADD_EXECUTED")
            messages.success(request, 'Domain added')
            return redirect(reverse('domain_detail', args=(domain.domain_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class DomainCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Domain
    form_class = DomainForm
    template_name = 'dfirtrack_main/domain/domain_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DOMAIN_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.save()
            domain.logger(str(request.user), " DOMAIN_ADD_POPUP_EXECUTED")
            messages.success(request, 'Domain added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class DomainUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Domain
    form_class = DomainForm
    template_name = 'dfirtrack_main/domain/domain_edit.html'

    def get(self, request, *args, **kwargs):
        domain = self.get_object()
        form = self.form_class(instance=domain)
        domain.logger(str(request.user), " DOMAIN_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        domain = self.get_object()
        form = self.form_class(request.POST, instance=domain)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.save()
            domain.logger(str(request.user), " DOMAIN_EDIT_EXECUTED")
            messages.success(request, 'Domain edited')
            return redirect(reverse('domain_detail', args=(domain.domain_id,)))
        else:
            return render(request, self.template_name, {'form': form})
