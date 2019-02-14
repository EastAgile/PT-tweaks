import os
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase

from robber import expect

from activity.pt_models import Story


class ImportStoriesCommandTestCase(SimpleTestCase):
    @patch('activity.story_manager.story_manager.create_story')
    def test_command(self, create_story_mock):
        create_story_mock.return_value = Story({'id': '123123'})
        out = StringIO()
        call_command(
            'import_stories',
            '11',
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stories_dump.json'),
            stdout=out
        )
        expect(create_story_mock).to.be.called_once()
        expect(out.getvalue()).to.contain('delivered story')
        expect(out.getvalue()).to.contain('123123')
