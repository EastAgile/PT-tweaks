from django.conf import settings

from .pt_client import PTClient
from .pt_models import Activity, Project, Story


class StoryManager(object):
    def __init__(self, *args, **kwargs):
        self.client = PTClient(settings.PIVOTALTRACKER_TOKEN_API)

    def get_story_activities(self, project_id, story_id):
        activities = self.client.get_story_activities(project_id, story_id)
        return [Activity(item) for item in activities]

    def update_story(self, project_id, story_id, **kwargs):
        return self.client.update_story(project_id, story_id, **kwargs)

    def get_project(self, project_id):
        project = self.client.get_project(project_id)
        return Project(project)

    def create_story(self, project_id, story):
        story = self.client.create_story(project_id, story.get_json())
        return Story(story)

    def get_project_stories(self, project_id, params={}):
        stories = self.client.get_project_stories(project_id, **params)
        return [Story(story) for story in stories]


story_manager = StoryManager()
