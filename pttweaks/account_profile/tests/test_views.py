from django.urls import reverse
from django.test import TestCase

from robber import expect

from account_profile.factories import CustomUserFactory, UserConfigurationFactory
from account_profile.models import CustomUser, UserConfiguration


class UserConfigurationViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='admin', password='password')
        self.client.login(username='admin', password='password')

    def test_not_exist_configuration(self):
        response = self.client.get(reverse('settings'))
        expect(response.status_code).to.eq(200)
        user_conf = UserConfiguration.objects.get(user=self.user)
        expect(user_conf.pt_token).to.eq('')
        expect(response.context['form'].instance).to.eq(user_conf)

    def test_exist_configuration(self):
        user_conf = UserConfigurationFactory(user=self.user, pt_token='user_token')
        response = self.client.get(reverse('settings'))
        expect(response.status_code).to.eq(200)
        expect(response.context['form'].instance).to.eq(user_conf)

    def test_update_configuration(self):
        user_conf = UserConfigurationFactory(user=self.user, pt_token='user_token')
        response = self.client.post(
            reverse('settings'),
            {'pt_token': 'changed_token'},
            follow=True
        )

        expect(response.status_code).to.eq(200)
        expect(str(response.content)).to.contain('Setting has been saved!')
        user_conf.refresh_from_db()
        expect(user_conf.pt_token).to.eq('changed_token')
