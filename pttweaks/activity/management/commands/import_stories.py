import sys
import json
import argparse

from django.core.management.base import BaseCommand

from activity.story_manager import story_manager
from activity.models import Story


class Command(BaseCommand):
    help = 'Import stories to PT project'

    def add_arguments(self, parser):
        parser.add_argument('project_id', nargs=1, type=int)
        parser.add_argument('input', nargs=1, type=argparse.FileType('r'), default=sys.stdin)

    def handle(self, *args, **options):
        project_id = options['project_id'][0]
        file = options['input'][0]
        stories = json.load(file)
        print(project_id)
        print(stories)

        for story in stories:
            print('Importing story {name}'.format(name=story['name']))
            story = story_manager.create_story(project_id, Story(story))
            print('Done {id}'.format(id=story.id))
        # self.stdout.write(self.style.SUCCESS('Stories activities of project "%s"' % project_id))
