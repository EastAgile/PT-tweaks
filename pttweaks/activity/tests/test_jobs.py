from unittest.mock import patch

from django.test import TestCase

from robber import expect

from activity.jobs import AdjustStoryAcceptedDateJob, Job
from activity.models import Activity


class JobTestCase(TestCase):
    def test_run(self):
        job = Job()
        expect(lambda: job.run(None)).to.throw(NotImplementedError)


class AdjustStoryAcceptedDateJobTestCase(TestCase):
    def setUp(self):
        self.job = AdjustStoryAcceptedDateJob()

    @patch('activity.jobs.story_manager.update_story')
    @patch('activity.jobs.story_manager.get_story_activities')
    def test_run(self, get_story_activities_mock, update_story_mock):
        accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'new_values': {
                    'current_state': 'accepted'
                }
            }]
        })
        get_story_activities_mock.return_value = [
            Activity({
                'project': {'id': 11},
                'changes': [{
                    'id': 22,
                    'new_values': {
                        'current_state': 'finished',
                        'updated_at': '2017-11-22T11:00:00Z'
                    }
                }]
            }),
            Activity({
                'project': {'id': 11},
                'changes': [{
                    'id': 22,
                    'new_values': {
                        'current_state': 'delivered',
                        'updated_at': '2017-11-23T11:00:00Z'
                    }
                }]
            }),
            Activity({
                'project': {'id': 11},
                'changes': [{
                    'id': 22,
                    'new_values': {
                        'current_state': 'rejected',
                        'updated_at': '2017-11-24T11:00:00Z'
                    }
                }]
            })
        ]
        self.job.run(accepting_activity)
        expect(get_story_activities_mock).to.be.called_with(11, 22)
        expect(update_story_mock).to.be.called_with(11, 22, accepted_at='2017-11-23T11:00:00Z')

    @patch('activity.jobs.story_manager.update_story')
    def test_run_do_nothing_if_not_accepting_activity(self, update_story_mock):
        not_accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'new_values': {
                    'current_state': 'finished'
                }
            }]
        })
        self.job.run(not_accepting_activity)

        expect(update_story_mock).not_to.be.called()

    @patch('activity.jobs.story_manager.update_story')
    @patch('activity.jobs.story_manager.get_story_activities')
    def test_run_empty_activity_history(self, get_story_activities_mock, update_story_mock):
        accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'new_values': {
                    'current_state': 'accepted'
                }
            }]
        })
        get_story_activities_mock.return_value = []
        self.job.run(accepting_activity)
        expect(update_story_mock).not_to.be.called()
