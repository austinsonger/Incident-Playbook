from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import HeadlineForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Headline

class HeadlineList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Headline
    template_name = 'dfirtrack_main/headline/headline_list.html'
    context_object_name = 'headline_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " HEADLINE_LIST_ENTERED")
        return Headline.objects.order_by('headline_name')

class HeadlineDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Headline
    template_name = 'dfirtrack_main/headline/headline_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        headline = self.object
        headline.logger(str(self.request.user), " HEADLINE_DETAIL_ENTERED")
        return context

class HeadlineCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Headline
    form_class = HeadlineForm
    template_name = 'dfirtrack_main/headline/headline_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " HEADLINE_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            headline = form.save(commit=False)
            headline.save()
            headline.logger(str(request.user), " HEADLINE_ADD_EXECUTED")
            messages.success(request, 'Headline added')
            return redirect(reverse('headline_detail', args=(headline.headline_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class HeadlineUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Headline
    form_class = HeadlineForm
    template_name = 'dfirtrack_main/headline/headline_edit.html'

    def get(self, request, *args, **kwargs):
        headline = self.get_object()
        form = self.form_class(instance=headline)
        headline.logger(str(request.user), " HEADLINE_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        headline = self.get_object()
        form = self.form_class(request.POST, instance=headline)
        if form.is_valid():
            headline = form.save(commit=False)
            headline.save()
            headline.logger(str(request.user), " HEADLINE_EDIT_EXECUTED")
            messages.success(request, 'Headline edited')
            return redirect(reverse('headline_detail', args=(headline.headline_id,)))
        else:
            return render(request, self.template_name, {'form': form})
