from unittest.mock import patch

from django.test import TestCase

from robber import expect

from activity.story_manager import story_manager


class StoryManagerTestCase(TestCase):
    def test_get_story_activities(self):
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
        with patch(
            'activity.story_manager.PTClient.get_story_activities', return_value=story_activity_dict_result
        ) as get_story_activities_mock:
            activities = story_manager.get_story_activities(11, 22)

            expect(get_story_activities_mock).to.called_with(11, 22)
            expect(activities).to.have.length(1)
            expect(activities[0].project.id).to.eq(11)
            expect(activities[0].changes).to.have.length(1)
            expect(activities[0].changes[0].id).to.eq(22)
            expect(activities[0].changes[0].new_values).to.eq({'current_state': 'started'})

    def test_update_story(self):
        with patch('activity.story_manager.PTClient.update_story') as update_story_mock:
            story_manager.update_story(11, 22, name='Do it')
            expect(update_story_mock).to.called_with(11, 22, name='Do it')
