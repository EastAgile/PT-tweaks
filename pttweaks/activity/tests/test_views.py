import json
from unittest.mock import patch, Mock

from django.urls import reverse
from django.test import TestCase, override_settings

from robber import expect


@override_settings(WEBHOOK_VERIFY_TOKEN='verified_token')
class ActivityWebhookTestCase(TestCase):
    def test_post(self):
        request_dict = {
            'projects': 'abc',
            'changes': 'changes set'
        }
        job_mock = Mock()
        with patch('activity.views.jobs', [job_mock]):
            response = self.client.post(
                reverse('activity:webhook', kwargs={'token': 'verified_token'}),
                json.dumps(request_dict),
                content_type='application/json',
            )

            expect(job_mock.run).to.be.called_once()
            expect(response.status_code).to.eq(200)

    def test_post_wrong_token(self):
        response = self.client.post(
            reverse('activity:webhook', kwargs={'token': 'wrong_token'}),
            json.dumps({}),
            content_type='application/json',
        )

        expect(response.status_code).to.eq(403)
