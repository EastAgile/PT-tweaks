from unittest.mock import Mock, patch

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from robber import expect

from activity.admin import ActivityChangeLogAdmin
from activity.models import ActivityChangeLog
from activity.factories import ActivityChangeLogFactory


class ActivityChangeLogAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = ActivityChangeLogAdmin(ActivityChangeLog, self.site)

    def test_model_permissions(self):
        request = Mock()
        request.user.has_perm.return_value = True

        expect(self.admin.get_model_perms(request)).to.eq({
            'add': False,
            'delete': False,
            'change':  False,
            'view': True
        })

    def test_changes_display(self):
        log = ActivityChangeLogFactory.build(
            changes={
                'accepted_at': {
                    'old': '2015-09-01T11:00:11Z',
                    'new': '2016-11-12T12:00:12Z'
                },
                'estimate': {
                    'old': 1,
                    'new': 2
                }
            }
        )

        expect(self.admin.changes_display(log)).to.eq(
            'Change on "accepted_at": From "2015-09-01T11:00:11Z" to "2016-11-12T12:00:12Z"\n' + \
            'Change on "estimate": From "1" to "2"'
        )

    def test_story_link_display(self):
        log = ActivityChangeLogFactory.build(story_id="123123")
        story_link = self.admin.story_link_display(log)
        expect(story_link).to.eq(
            '<a href="https://www.pivotaltracker.com/story/show/123123" target="_blank">123123</a>'
        )

    def test_project_link_display(self):
        log = ActivityChangeLogFactory.build(project_id="111")
        project_link = self.admin.project_link_display(log)
        expect(project_link).to.eq(
            '<a href="https://www.pivotaltracker.com/n/projects/111" target="_blank">111</a>'
        )

    @patch('activity.admin.story_manager')
    def test_revert_accepted_date_change_not_reverted(self, story_manager_mock):
        ActivityChangeLogFactory(
            project_id=11,
            story_id=22,
            changes={
                'accepted_at': {
                    'old': '2015-09-01T11:00:11Z',
                    'new': '2016-11-12T12:00:12Z'
                }
            }
        )

        self.admin.revert_accepted_date_change(Mock(), ActivityChangeLog.objects.all())

        log = ActivityChangeLog.objects.first()
        expect(log.is_reverted).to.be.true()
        expect(story_manager_mock.update_story).to.be.called_with('11', '22', accepted_at='2015-09-01T11:00:11Z')

    @patch('activity.admin.story_manager')
    def test_revert_accepted_date_change_was_reverted(self, story_manager_mock):
        ActivityChangeLogFactory(
            project_id=11,
            story_id=22,
            is_reverted=True,
            changes={
                'accepted_at': {
                    'old': '2015-09-01T11:00:11Z',
                    'new': '2016-11-12T12:00:12Z'
                }
            }
        )

        request = Mock()
        self.admin.revert_accepted_date_change(request, ActivityChangeLog.objects.all())

        log = ActivityChangeLog.objects.first()
        expect(log.is_reverted).to.be.false()
        expect(story_manager_mock.update_story).to.be.called_with('11', '22', accepted_at='2016-11-12T12:00:12Z')
