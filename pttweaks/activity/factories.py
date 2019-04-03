from factory.django import DjangoModelFactory

from .models import ActivityChangeLog


class ActivityChangeLogFactory(DjangoModelFactory):
    class Meta:
        model = ActivityChangeLog
