from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView
from django.contrib.auth import get_user_model

from .forms import CustomUserChangeForm


class SettingsPageView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    model = get_user_model()
    success_url = reverse_lazy('questions:question_list')
    template_name = 'account/settings.html'
    context_object_name = 'settings'

    def get_object(self, queryset=None):
        return self.request.user
