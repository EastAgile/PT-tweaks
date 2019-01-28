import json
import logging

from django.http import HttpResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .jobs import AdjustStoryAcceptedDateJob
from .pt_models import Activity


jobs = [AdjustStoryAcceptedDateJob()]


def verify_webhook_source(token):
    if token != settings.WEBHOOK_VERIFY_TOKEN:
        raise PermissionDenied


@csrf_exempt
@require_http_methods(['POST'])
def activity_webhook(request, token):
    verify_webhook_source(token)
    logging.info(json.loads(request.body))

    activity = Activity(json.loads(request.body))
    for job in jobs:
        job.run(activity=activity)
    return HttpResponse(status=200)
