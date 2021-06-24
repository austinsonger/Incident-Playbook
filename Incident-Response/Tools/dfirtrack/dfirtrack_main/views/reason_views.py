from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import ReasonForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Reason

class ReasonList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Reason
    template_name = 'dfirtrack_main/reason/reason_list.html'
    context_object_name = 'reason_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " REASON_LIST_ENTERED")
        return Reason.objects.order_by('reason_name')

class ReasonDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Reason
    template_name = 'dfirtrack_main/reason/reason_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reason = self.object
        reason.logger(str(self.request.user), " REASON_DETAIL_ENTERED")
        return context

class ReasonCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Reason
    form_class = ReasonForm
    template_name = 'dfirtrack_main/reason/reason_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " REASON_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reason = form.save(commit=False)
            reason.save()
            reason.logger(str(request.user), " REASON_ADD_EXECUTED")
            messages.success(request, 'Reason added')
            return redirect(reverse('reason_detail', args=(reason.reason_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class ReasonCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Reason
    form_class = ReasonForm
    template_name = 'dfirtrack_main/reason/reason_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " REASON_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            reason = form.save(commit=False)
            reason.save()
            reason.logger(str(request.user), " REASON_ADD_POPUP_EXECUTED")
            messages.success(request, 'Reason added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class ReasonUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Reason
    form_class = ReasonForm
    template_name = 'dfirtrack_main/reason/reason_edit.html'

    def get(self, request, *args, **kwargs):
        reason = self.get_object()
        form = self.form_class(instance=reason)
        reason.logger(str(request.user), " REASON_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        reason = self.get_object()
        form = self.form_class(request.POST, instance=reason)
        if form.is_valid():
            reason = form.save(commit=False)
            reason.save()
            reason.logger(str(request.user), " REASON_EDIT_EXECUTED")
            messages.success(request, 'Reason edited')
            return redirect(reverse('reason_detail', args=(reason.reason_id,)))
        else:
            return render(request, self.template_name, {'form': form})
