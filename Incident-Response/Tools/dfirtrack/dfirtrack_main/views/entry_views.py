from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import EntryForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Entry

class EntryList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Entry
    template_name = 'dfirtrack_main/entry/entry_list.html'
    context_object_name = 'entry_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " ENTRY_LIST_ENTERED")
        return Entry.objects.order_by('entry_id')

class EntryDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Entry
    template_name = 'dfirtrack_main/entry/entry_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object
        entry.logger(str(self.request.user), " ENTRY_DETAIL_ENTERED")
        return context

class EntryCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Entry
    form_class = EntryForm
    template_name = 'dfirtrack_main/entry/entry_add.html'

    def get(self, request, *args, **kwargs):
        if 'system' in request.GET:
            system = request.GET['system']
            form = self.form_class(
                initial={'system': system,}
            )
        else:
            form = self.form_class()
        debug_logger(str(request.user), " ENTRY_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.entry_created_by_user_id = request.user
            entry.entry_modified_by_user_id = request.user
            entry.save()
            entry.logger(str(request.user), " ENTRY_ADD_EXECUTED")
            messages.success(request, 'Entry added')
            return redirect(reverse('system_detail', args=(entry.system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class EntryUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Entry
    form_class = EntryForm
    template_name = 'dfirtrack_main/entry/entry_edit.html'

    def get(self, request, *args, **kwargs):
        entry = self.get_object()
        form = self.form_class(instance=entry)
        entry.logger(str(request.user), " ENTRY_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        entry = self.get_object()
        form = self.form_class(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.entry_modified_by_user_id = request.user
            entry.save()
            entry.logger(str(request.user), " ENTRY_EDIT_EXECUTED")
            messages.success(request, 'Entry edited')
            return redirect(reverse('system_detail', args=(entry.system.system_id,)))
        else:
            return render(request, self.template_name, {'form': form})
