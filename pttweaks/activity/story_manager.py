from django.conf import settings

from .pt_client import PTClient
from .models import Activity


class StoryManager(object):
    def __init__(self, *args, **kwargs):
        self.client = PTClient(settings.PIVOTALTRACKER_TOKEN_API)

    def get_story_activities(self, project_id, story_id):
        activities = self.client.get_story_activities(project_id, story_id)
        return [Activity(item) for item in activities]

    def update_story(self, project_id, story_id, **kwargs):
        return self.client.update_story(project_id, story_id, **kwargs)


story_manager = StoryManager()
