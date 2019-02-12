from datetime import datetime
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from robber import expect

from activity.pt_models import Project, Story


class ImportStoriesCommandTestCase(TestCase):
    @patch('activity.story_manager.story_manager')
    @patch('activity.jobs.AdjustStoryAcceptedDateJob.process_story')
    def test_command(self, process_story_mock, story_manager_mock):
        project = Project({'id': '11', 'name': 'Project test'})
        story_manager_mock.get_project.return_value = project
        story_manager_mock.get_project_stories.return_value = [
            Story({
                'id': '1',
                'accepted_at': '2017-08-09T11:11:22Z'
            }),
            Story({
                'id': '2',
                'accepted_at': '2017-11-09T11:00:00Z'
            })
        ]

        call_command('adjust_old_stories', project_id=[11])

        expect(process_story_mock.call_count).to.eq(2)
        expect(process_story_mock).to.be.ever_called_with(
            project,
            '1',
            accepted_at=datetime(2017, 8, 9, 11, 11, 22)
        )
        expect(process_story_mock).to.be.ever_called_with(
            project,
            '2',
            accepted_at=datetime(2017, 11, 9, 11, 0, 0)
        )
        expect(story_manager_mock.get_project_stories).to.be.called_once_with(
            project_id='11',
            limit=50,
            offset=0,
            with_state='accepted'
        )
