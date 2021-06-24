from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import ContactForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Contact

class ContactList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Contact
    template_name = 'dfirtrack_main/contact/contact_list.html'
    context_object_name = 'contact_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " CONTACT_LIST_ENTERED")
        return Contact.objects.order_by('contact_name')

class ContactDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Contact
    template_name = 'dfirtrack_main/contact/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact = self.object
        contact.logger(str(self.request.user), " CONTACT_DETAIL_ENTERED")
        return context

class ContactCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Contact
    form_class = ContactForm
    template_name = 'dfirtrack_main/contact/contact_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " CONTACT_ADD_ENTERED")
        return render(request, 'dfirtrack_main/contact/contact_add.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            contact.logger(str(request.user), " CONTACT_ADD_EXECUTED")
            messages.success(request, 'Contact added')
            return redirect(reverse('contact_detail', args=(contact.contact_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class ContactCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Contact
    form_class = ContactForm
    template_name = 'dfirtrack_main/contact/contact_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " CONTACT_ADD_POPUP_ENTERED")
        return render(request, 'dfirtrack_main/contact/contact_add_popup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            contact.logger(str(request.user), " CONTACT_ADD_POPUP_EXECUTED")
            messages.success(request, 'Contact added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class ContactUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Contact
    form_class = ContactForm
    template_name = 'dfirtrack_main/contact/contact_edit.html'

    def get(self, request, *args, **kwargs):
        contact = self.get_object()
        form = self.form_class(instance=contact)
        contact.logger(str(request.user), " CONTACT_EDIT_ENTERED")
        return render(request, 'dfirtrack_main/contact/contact_edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        contact = self.get_object()
        form = self.form_class(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            contact.logger(str(request.user), " CONTACT_EDIT_EXECUTED")
            messages.success(request, 'Contact edited')
            return redirect(reverse('contact_detail', args=(contact.contact_id,)))
        else:
            return render(request, 'dfirtrack_main/contact/contact_edit.html', {'form': form})
