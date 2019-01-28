from django.db import models
from django.contrib.postgres.fields import JSONField

from model_utils.models import TimeStampedModel


ADJUST_STORY_ACCEPTED_DATE = 'ADJUST_STORY_ACCEPTED_DATE'

JOB_CHOICES = (
    (ADJUST_STORY_ACCEPTED_DATE, 'adjust_accepted_date'),
)


class ActivityChangeLog(TimeStampedModel):
    story_id = models.CharField(max_length=255)
    project_id = models.CharField(max_length=255)
    is_reverted = models.BooleanField(default=False)
    origin = models.CharField(max_length=100, choices=JOB_CHOICES)
    changes = JSONField()

    def __str__(self):
        return self.story_id
