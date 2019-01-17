from .story_manager import story_manager
from .utils import utc_from_str, utc_to_str, strip_none


class Job(object):
    def run(self, activity):
        raise NotImplementedError()


class AdjustStoryAcceptedDateJob(Job):
    def _get_latest_updated_date(self, story_activities):
        updated_dates = []

        for activity in story_activities:
            updated_dates += [
                utc_from_str(change.new_values.get('updated_at', None))
                for change in activity.changes
                if change.new_values.get('current_state', None) in ['delivered', 'finished']
            ]

        return max(strip_none(updated_dates), default=None)

    def run(self, activity):
        story_ids = [
            change.id for change in activity.changes if change.is_accept_activity()
        ]
        project_id = activity.project.id

        for story_id in story_ids:
            story_activities = story_manager.get_story_activities(project_id, story_id)

            updated_date = self._get_latest_updated_date(story_activities)
            if updated_date:
                story_manager.update_story(project_id, story_id, accepted_at=utc_to_str(updated_date))
