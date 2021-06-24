from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import CompanyForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Company

class CompanyList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Company
    template_name = 'dfirtrack_main/company/company_list.html'
    context_object_name = 'company_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " COMPANY_LIST_ENTERED")
        return Company.objects.order_by('company_name')

class CompanyDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Company
    template_name = 'dfirtrack_main/company/company_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.object
        company.logger(str(self.request.user), " COMPANY_DETAIL_ENTERED")
        return context

class CompanyCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Company
    form_class = CompanyForm
    template_name = 'dfirtrack_main/company/company_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " COMPANY_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            company.logger(str(request.user), " COMPANY_ADD_EXECUTED")
            messages.success(request, 'Company added')
            return redirect(reverse('company_detail', args=(company.company_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class CompanyCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Company
    form_class = CompanyForm
    template_name = 'dfirtrack_main/company/company_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " COMPANY_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            company.logger(str(request.user), " COMPANY_ADD_POPUP_EXECUTED")
            messages.success(request, 'Company added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class CompanyUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Company
    form_class = CompanyForm
    template_name = 'dfirtrack_main/company/company_edit.html'

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        form = self.form_class(instance=company)
        company.logger(str(request.user), " COMPANY_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        company = self.get_object()
        form = self.form_class(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.save()
            company.logger(str(request.user), " COMPANY_EDIT_EXECUTED")
            messages.success(request, 'Company edited')
            return redirect(reverse('company_detail', args=(company.company_id,)))
        else:
            return render(request, self.template_name, {'form': form})
