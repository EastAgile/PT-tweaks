from django.urls import path

from .views import UserConfigurationView


urlpatterns = [
    path('settings', UserConfigurationView.as_view(), name='settings')
]
