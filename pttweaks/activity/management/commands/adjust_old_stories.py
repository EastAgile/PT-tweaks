from tqdm import tqdm

from django.core.management.base import BaseCommand

from activity.story_manager import story_manager
from activity.jobs import AdjustStoryAcceptedDateJob
from activity.utils import utc_from_str


class Command(BaseCommand):
    help = 'Adjust the accepted date for old stories'

    def add_arguments(self, parser):
        parser.add_argument('--project_id', nargs='+', type=int)

    def handle(self, *args, **options):
        job = AdjustStoryAcceptedDateJob()

        for project_id in options['project_id']:
            project = story_manager.get_project(project_id)

            self.stdout.write('Processing project {}:'.format(project.name))

            limit = 50
            offset = 0

            while True:
                accepted_stories = story_manager.get_project_stories(
                    project_id=project.id,
                    limit=limit,
                    offset=offset,
                    with_state='accepted'
                )

                self.stdout.write('Processing batch {batch_no}:'.format(batch_no=offset // limit + 1))
                for story in tqdm(accepted_stories):
                    job.process_story(project, story.id, accepted_at=utc_from_str(story.accepted_at))

                offset += limit
                if len(accepted_stories) < limit:
                    break
