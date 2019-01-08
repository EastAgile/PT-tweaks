from django.urls import path

from .views import activity_webhook


urlpatterns = [
    path('webhook/<token>/', activity_webhook, name='webhook'),
]
