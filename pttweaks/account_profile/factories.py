from factory.django import DjangoModelFactory

from .models import CustomUser, UserConfiguration


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser


class UserConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = UserConfiguration
