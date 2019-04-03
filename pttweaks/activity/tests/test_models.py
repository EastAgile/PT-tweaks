from django.test import SimpleTestCase

from robber import expect

from activity.factories import ActivityChangeLogFactory


class ActivityChangeLogTestCase(SimpleTestCase):
    def test_model_str(self):
        activity = ActivityChangeLogFactory.build(story_id='123123')
        expect(str(activity)).to.eq('123123')
