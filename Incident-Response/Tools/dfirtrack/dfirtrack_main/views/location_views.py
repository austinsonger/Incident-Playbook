from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import LocationForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Location

class LocationList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Location
    template_name = 'dfirtrack_main/location/location_list.html'
    context_object_name = 'location_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " LOCATION_LIST_ENTERED")
        return Location.objects.order_by('location_name')

class LocationDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Location
    template_name = 'dfirtrack_main/location/location_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        location = self.object
        location.logger(str(self.request.user), " LOCATION_DETAIL_ENTERED")
        return context

class LocationCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Location
    form_class = LocationForm
    template_name = 'dfirtrack_main/location/location_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " LOCATION_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            location.logger(str(request.user), " LOCATION_ADD_EXECUTED")
            messages.success(request, 'Location added')
            return redirect(reverse('location_detail', args=(location.location_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class LocationCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Location
    form_class = LocationForm
    template_name = 'dfirtrack_main/location/location_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " LOCATION_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            location.logger(str(request.user), " LOCATION_ADD_POPUP_EXECUTED")
            messages.success(request, 'Location added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class LocationUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Location
    form_class = LocationForm
    template_name = 'dfirtrack_main/location/location_edit.html'

    def get(self, request, *args, **kwargs):
        location = self.get_object()
        form = self.form_class(instance=location)
        location.logger(str(request.user), " LOCATION_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        location = self.get_object()
        form = self.form_class(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            location.logger(str(request.user), " LOCATION_EDIT_EXECUTED")
            messages.success(request, 'Location edited')
            return redirect(reverse('location_detail', args=(location.location_id,)))
        else:
            return render(request, self.template_name, {'form': form})
