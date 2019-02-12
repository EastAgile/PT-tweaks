from datetime import datetime
from unittest.mock import patch

from django.test import SimpleTestCase

from robber import expect

from activity.story_manager import story_manager
from activity.models import Story


class StoryManagerTestCase(SimpleTestCase):
    @patch('activity.story_manager.PTClient.get_story_activities')
    def test_get_story_activities(self, get_story_activities_mock):
        story_activity_dict_result = [
            {
                'project': {'id': 11},
                'changes': [
                    {
                        'id': 22,
                        'new_values': {
                            'current_state': 'started'
                        }
                    }
                ]
            }
        ]

        get_story_activities_mock.return_value = story_activity_dict_result

        activities = story_manager.get_story_activities(11, 22)

        expect(get_story_activities_mock).to.called_with(11, 22)
        expect(activities).to.have.length(1)
        expect(activities[0].project.id).to.eq(11)
        expect(activities[0].changes).to.have.length(1)
        expect(activities[0].changes[0].id).to.eq(22)
        expect(activities[0].changes[0].new_values).to.eq({'current_state': 'started'})

    @patch('activity.story_manager.PTClient.update_story')
    def test_update_story(self, update_story_mock):
        story_manager.update_story(11, 22, name='Do it')
        expect(update_story_mock).to.called_with(11, 22, name='Do it')

    @patch('activity.story_manager.PTClient.get_project')
    def test_get_project(self, get_project_mock):
        get_project_mock.return_value = {
            'id': 123,
            'iteration_length': 1,
            'start_time': '2017-11-21T11:00:00Z'
        }

        project = story_manager.get_project(123)
        expect(get_project_mock).to.be.called_with(123)
        expect(project.id).to.eq(123)
        expect(project.iteration_length).to.eq(1)
        expect(project.start_time).to.eq(datetime(2017, 11, 21, 11, 0, 0))

    @patch('activity.story_manager.PTClient.create_story')
    def test_create_story(self, create_story_mock):
        story_manager.create_story(11, Story({'name': 'Do it'}))
        expect(create_story_mock).to.called_with(11, {'name': 'Do it'})
