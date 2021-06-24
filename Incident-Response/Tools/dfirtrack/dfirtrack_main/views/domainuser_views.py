from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import DomainuserForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Domainuser

class DomainuserList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Domainuser
    template_name = 'dfirtrack_main/domainuser/domainuser_list.html'
    context_object_name = 'domainuser_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " DOMAINUSER_LIST_ENTERED")
        return Domainuser.objects.order_by('domainuser_name')

class DomainuserDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Domainuser
    template_name = 'dfirtrack_main/domainuser/domainuser_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domainuser = self.object
        domainuser.logger(str(self.request.user), " DOMAINUSER_DETAIL_ENTERED")
        return context

class DomainuserCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Domainuser
    form_class = DomainuserForm
    template_name = 'dfirtrack_main/domainuser/domainuser_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " DOMAINUSER_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            domainuser = form.save(commit=False)
            domainuser.save()
            form.save_m2m()
            domainuser.logger(str(request.user), " DOMAINUSER_ADD_EXECUTED")
            messages.success(request, 'Domainuser added')
            return redirect(reverse('domainuser_detail', args=(domainuser.domainuser_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class DomainuserUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Domainuser
    form_class = DomainuserForm
    template_name = 'dfirtrack_main/domainuser/domainuser_edit.html'

    def get(self, request, *args, **kwargs):
        domainuser = self.get_object()
        form = self.form_class(instance=domainuser)
        domainuser.logger(str(request.user), " DOMAINUSER_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        domainuser = self.get_object()
        form = self.form_class(request.POST, instance=domainuser)
        if form.is_valid():
            domainuser = form.save(commit=False)
            domainuser.save()
            form.save_m2m()
            domainuser.logger(str(request.user), " DOMAINUSER_EDIT_EXECUTED")
            messages.success(request, 'Domainuser edited')
            return redirect(reverse('domainuser_detail', args=(domainuser.domainuser_id,)))
        else:
            return render(request, self.template_name, {'form': form})
