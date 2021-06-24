from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import AnalystmemoForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Analystmemo

class AnalystmemoList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Analystmemo
    template_name = 'dfirtrack_main/analystmemo/analystmemo_list.html'
    context_object_name = 'analystmemo_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " ANALYSTMEMO_LIST_ENTERED")
        return Analystmemo.objects.order_by('analystmemo_id')

class AnalystmemoDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Analystmemo
    template_name = 'dfirtrack_main/analystmemo/analystmemo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analystmemo = self.object
        analystmemo.logger(str(self.request.user), " ANALYSTMEMO_DETAIL_ENTERED")
        return context

class AnalystmemoCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Analystmemo
    form_class = AnalystmemoForm
    template_name = 'dfirtrack_main/analystmemo/analystmemo_add.html'

    def get(self, request, *args, **kwargs):
        if 'system' in request.GET:
            system = request.GET['system']
            form = self.form_class(
                initial= {'system': system,}
            )
        else:
            form = self.form_class()
        debug_logger(str(request.user), " ANALYSTMEMO_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            analystmemo = form.save(commit=False)
            analystmemo.analystmemo_created_by_user_id = request.user
            analystmemo.analystmemo_modified_by_user_id = request.user
            analystmemo.save()
            analystmemo.logger(str(request.user), " ANALYSTMEMO_ADD_EXECUTED")
            messages.success(request, 'Analystmemo added')
            return redirect(reverse('system_detail', args=(analystmemo.system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class AnalystmemoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Analystmemo
    form_class = AnalystmemoForm
    template_name = 'dfirtrack_main/analystmemo/analystmemo_edit.html'

    def get(self, request, *args, **kwargs):
        analystmemo = self.get_object()
        form = self.form_class(instance=analystmemo)
        analystmemo.logger(str(request.user), " ANALYSTMEMO_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        analystmemo = self.get_object()
        form = self.form_class(request.POST, instance=analystmemo)
        if form.is_valid():
            analystmemo = form.save(commit=False)
            analystmemo.analystmemo_modified_by_user_id = request.user
            analystmemo.save()
            analystmemo.logger(str(request.user), " ANALYSTMEMO_EDIT_EXECUTED")
            messages.success(request, 'Analystmemo edited')
            return redirect(reverse('system_detail', args=(analystmemo.system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})
