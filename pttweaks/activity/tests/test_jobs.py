from datetime import datetime, timezone
from unittest.mock import patch

from django.test import SimpleTestCase, TestCase

from robber import expect

from activity.jobs import AdjustStoryAcceptedDateJob, Job
from activity.pt_models import Activity, Project
from activity.models import ActivityChangeLog


class JobTestCase(SimpleTestCase):
    def test_run(self):
        job = Job()
        expect(lambda: job.run(None)).to.throw(NotImplementedError)


class AdjustStoryAcceptedDateJobTestCase(TestCase):
    def setUp(self):
        self.job = AdjustStoryAcceptedDateJob()

    @patch('activity.jobs.story_manager')
    def test_run(self, story_manager_mock):
        accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'change_type': 'update',
                'new_values': {
                    'current_state': 'accepted',
                    'accepted_at': datetime(2017, 11, 30, 8, 0, 0, tzinfo=timezone.utc).timestamp() * 1e3
                }
            }]
        })
        story_manager_mock.get_story_activities.return_value = [
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

        story_manager_mock.get_project.return_value = Project({
            'id': 11,
            'iteration_length': 1,
            'start_time': '2017-11-21T11:00:00Z'
        })

        self.job.run(accepting_activity)
        expect(story_manager_mock.get_project).to.be.called_with(11)
        expect(story_manager_mock.get_story_activities).to.be.called_with(11, 22)
        expect(story_manager_mock.update_story).to.be.called_with(11, 22, accepted_at='2017-11-23T11:00:00Z')
        activity_logs = ActivityChangeLog.objects.all()
        expect(activity_logs).to.have.length(1)
        expect(activity_logs[0].project_id).to.eq('11')
        expect(activity_logs[0].story_id).to.eq('22')
        expect(activity_logs[0].origin).to.eq('ADJUST_STORY_ACCEPTED_DATE')
        expect(activity_logs[0].changes).to.eq({
            'accepted_at': {
                'new': '2017-11-23T11:00:00Z',
                'old': '2017-11-30T08:00:00Z'
            }
        })

    @patch('activity.jobs.story_manager')
    def test_run_do_nothing_if_not_accepting_activity(self, story_manager_mock):
        not_accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [
                {
                    'id': 22,
                    'change_type': 'update',
                    'new_values': {
                        'current_state': 'finished'
                    }
                },
                {
                    'id': 23,
                    'change_type': 'delete'
                }
            ]
        })
        self.job.run(not_accepting_activity)

        expect(story_manager_mock.update_story).not_to.be.called()

    @patch('activity.jobs.story_manager')
    def test_run_empty_activity_history(self, story_manager_mock):
        accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'change_type': 'update',
                'new_values': {
                    'current_state': 'accepted'
                }
            }]
        })
        story_manager_mock.get_story_activities.return_value = []
        self.job.run(accepting_activity)
        expect(story_manager_mock.update_story).not_to.be.called()

    @patch('activity.jobs.story_manager')
    def test_do_not_update_story_if_accepted_within_iteration(self, story_manager_mock):
        story_manager_mock.get_project.return_value = Project({
            'id': 11,
            'iteration_length': 1,
            'start_time': '2017-11-21T11:00:00Z'
        })

        story_manager_mock.get_story_activities.return_value = [
            Activity({
                'project': {'id': 11},
                'changes': [{
                    'id': 22,
                    'new_values': {
                        'current_state': 'delivered',
                        'updated_at': '2017-11-23T11:00:00Z'
                    }
                }]
            })
        ]

        accepting_activity = Activity({
            'project': {'id': 11},
            'changes': [{
                'id': 22,
                'change_type': 'update',
                'new_values': {
                    'current_state': 'accepted',
                    'accepted_at': datetime(2017, 11, 25, 8, 0, 0, tzinfo=timezone.utc).timestamp() * 1e3
                }
            }]
        })

        self.job.run(accepting_activity)
        expect(story_manager_mock.update_story).not_to.be.called()
