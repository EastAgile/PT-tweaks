from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from robber import expect

from account_profile.admin import CustomUserAdmin, UserConfigurationAdmin
from account_profile.models import CustomUser, UserConfiguration
from account_profile.factories import CustomUserFactory, UserConfigurationFactory


class CustomUserAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = CustomUserAdmin(CustomUser, self.site)

    def test_full_name(self):
        user = CustomUserFactory.build(first_name='Peter', last_name='Parker')
        expect(self.admin.full_name(user)).to.eq('Peter Parker')
