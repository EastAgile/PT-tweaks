import logging

from .story_manager import story_manager
from .utils import utc_from_str, utc_to_str, strip_none, utc_from_timestamp


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
        accepted_changes = [
            (change.id, utc_from_timestamp(change.new_values.get('accepted_at', None)))
            for change in activity.changes if change.is_accept_activity()
        ]
        project = story_manager.get_project(activity.project.id)

        for story_id, accepted_at in accepted_changes:
            story_activities = story_manager.get_story_activities(project.id, story_id)

            delivered_date = self._get_latest_updated_date(story_activities)

            iteration_length = project.iteration_length * 7  # week to days

            if delivered_date:
                delivered_iteration = (delivered_date.date() - project.start_time.date()).days // iteration_length
                accepted_iteration = (accepted_at.date() - project.start_time.date()).days // iteration_length

                if accepted_iteration != delivered_iteration:
                    # TODO: log the changes
                    logging.info('Update accepted date of story {story_id} from {from_date} to {to_date}'.format(
                        story_id=story_id,
                        from_date=accepted_at,
                        to_date=delivered_date
                    ))
                    story_manager.update_story(project.id, story_id, accepted_at=utc_to_str(delivered_date))
