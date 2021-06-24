from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from dfirtrack_main.forms import RecommendationForm
from dfirtrack_main.logger.default_logger import debug_logger
from dfirtrack_main.models import Recommendation

class RecommendationList(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Recommendation
    template_name = 'dfirtrack_main/recommendation/recommendation_list.html'
    context_object_name = 'recommendation_list'

    def get_queryset(self):
        debug_logger(str(self.request.user), " RECOMMENDATION_LIST_ENTERED")
        return Recommendation.objects.order_by('recommendation_name')

class RecommendationDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    model = Recommendation
    template_name = 'dfirtrack_main/recommendation/recommendation_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recommendation = self.object
        recommendation.logger(str(self.request.user), " RECOMMENDATION_DETAIL_ENTERED")
        return context

class RecommendationCreate(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Recommendation
    form_class = RecommendationForm
    template_name = 'dfirtrack_main/recommendation/recommendation_add.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " RECOMMENDATION_ADD_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.save()
            recommendation.logger(str(request.user), " RECOMMENDATION_ADD_EXECUTED")
            messages.success(request, 'Recommendation added')
            return redirect(reverse('recommendation_detail', args=(recommendation.recommendation_id,)))
        else:
            return render(request, self.template_name, {'form': form})

class RecommendationCreatePopup(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Recommendation
    form_class = RecommendationForm
    template_name = 'dfirtrack_main/recommendation/recommendation_add_popup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        debug_logger(str(request.user), " RECOMMENDATION_ADD_POPUP_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.save()
            recommendation.logger(str(request.user), " RECOMMENDATION_ADD_POPUP_EXECUTED")
            messages.success(request, 'Recommendation added')
            return HttpResponse('<script type="text/javascript">window.close();</script>')
        else:
            return render(request, self.template_name, {'form': form})

class RecommendationUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Recommendation
    form_class = RecommendationForm
    template_name = 'dfirtrack_main/recommendation/recommendation_edit.html'

    def get(self, request, *args, **kwargs):
        recommendation = self.get_object()
        form = self.form_class(instance=recommendation)
        recommendation.logger(str(request.user), " RECOMMENDATION_EDIT_ENTERED")
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        recommendation = self.get_object()
        form = self.form_class(request.POST, instance=recommendation)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.save()
            recommendation.logger(str(request.user), " RECOMMENDATION_EDIT_EXECUTED")
            messages.success(request, 'Recommendation edited')
            return redirect(reverse('recommendation_detail', args=(recommendation.recommendation_id,)))
        else:
            return render(request, self.template_name, {'form': form})
