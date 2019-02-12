import re

from django.test import SimpleTestCase

import httpretty
from robber import expect

from activity.pt_client import PTClient


class PTClientTestCase(SimpleTestCase):
    def setUp(self):
        self.client = PTClient('token')

    @httpretty.activate
    def test_get_story_activities(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(r'.*pivotaltracker.com/.*'),
            body='{}',
            status=200,
            content_type='application/json'
        )

        self.client.get_story_activities(11, 22)

        last_req = httpretty.last_request()
        expect(last_req.path).to.contain('/projects/11/stories/22/activity')

    @httpretty.activate
    def test_update_story(self):
        httpretty.register_uri(
            httpretty.PUT,
            re.compile(r'.*pivotaltracker.com/.*'),
            body='{}',
            status=200,
            content_type='application/json'
        )

        self.client.update_story(11, 22, name='Test story')

        last_req = httpretty.last_request()
        req_body = last_req.parsed_body

        expect(last_req.path).to.contain('/projects/11/stories/22')
        expect(req_body['name']).to.eq('Test story')

    @httpretty.activate
    def test_get_project(self):
        httpretty.register_uri(
            httpretty.GET,
            re.compile(r'.*pivotaltracker.com/.*'),
            body='{}',
            status=200,
            content_type='application/json'
        )

        self.client.get_project(11)

        last_req = httpretty.last_request()
        expect(last_req.path).to.contain('/projects/11')

    @httpretty.activate
    def test_create_story(self):
        httpretty.register_uri(
            httpretty.POST,
            re.compile(r'.*pivotaltracker.com/.*'),
            body='{}',
            status=200,
            content_type='application/json'
        )

        self.client.create_story(11, {'name': 'story 1'})

        last_req = httpretty.last_request()
        req_body = last_req.parsed_body
        expect(last_req.path).to.contain('/projects/11/stories')
        expect(req_body['name']).to.eq('story 1')
