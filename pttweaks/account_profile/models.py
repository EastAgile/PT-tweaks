from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserConfiguration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    pt_token = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return 'Configuration of %s' % self.user
