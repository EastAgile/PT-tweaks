from django.test import SimpleTestCase

from robber import expect

from account_profile.factories import CustomUserFactory, UserConfigurationFactory


class CustomUserTestCase(SimpleTestCase):
    def test_model_str(self):
        user = CustomUserFactory.build(username='anthony')
        expect(str(user)).to.eq('anthony')


class UserConfigurationTestCase(SimpleTestCase):
    def test_model_str(self):
        user = CustomUserFactory.build(username='anthony')
        user_conf = UserConfigurationFactory.build(user=user)
        expect(str(user_conf)).to.eq('Configuration of anthony')
