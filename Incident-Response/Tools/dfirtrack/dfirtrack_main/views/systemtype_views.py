from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import SystemtypeForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Systemtype

class SystemtypeList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Systemtype
    template_name = 'dfirtrack_main/systemtype/systemtype_list.html'
    context_object_name = 'systemtype_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " SYSTEMTYPE_LIST_ENTERED")
        return Systemtype.objects.order_by('systemtype_name')

class SystemtypeDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Systemtype
    template_name = 'dfirtrack_main/systemtype/systemtype_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        systemtype = self.object
        systemtype.logger(str(self.request.user), " SYSTEMTYPE_DETAIL_ENTERED")
        return context

class SystemtypeCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Systemtype
    form_class = SystemtypeForm
    template_name = 'dfirtrack_main/systemtype/systemtype_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " SYSTEMTYPE_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            systemtype = form.save(commit=False)
            systemtype.save()
            systemtype.logger(str(request.user), " SYSTEMTYPE_ADD_EXECUTED")
            messages.success(request, 'Systemtype added')
            return redirect(reverse('systemtype_detail', args=(systemtype.systemtype_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class SystemtypeCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Systemtype
    form_class = SystemtypeForm
    template_name = 'dfirtrack_main/systemtype/systemtype_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " SYSTEMTYPE_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            systemtype = form.save(commit=False)
            systemtype.save()
            systemtype.logger(str(request.user), " SYSTEMTYPE_ADD_POPUP_EXECUTED")
            messages.success(request, 'Systemtype added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class SystemtypeUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Systemtype
    form_class = SystemtypeForm
    template_name = 'dfirtrack_main/systemtype/systemtype_edit.html'

    def get(self, request, *args, **kwargs):
        systemtype = self.get_object()
        form = self.form_class(instance=systemtype)
        systemtype.logger(str(request.user), " SYSTEMTYPE_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        systemtype = self.get_object()
        form = self.form_class(request.POST, instance=systemtype)
        if form.is_valid():
            systemtype = form.save(commit=False)
            systemtype.save()
            systemtype.logger(str(request.user), " SYSTEMTYPE_EDIT_EXECUTED")
            messages.success(request, 'Systemtype edited')
            return redirect(reverse('systemtype_detail', args=(systemtype.systemtype_id,)))
        else:
            return render(request, self.template_name, {'form': form})
