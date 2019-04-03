from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import UserConfiguration


class UserConfigurationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'user_configuration.html'
    model = UserConfiguration
    fields = ['pt_token']
    success_url = reverse_lazy('home')
    success_message = "Setting has been saved!"

    def get_object(self, queryset=None):
        configuration, _ = UserConfiguration.objects.get_or_create(user=self.request.user)
        return configuration
