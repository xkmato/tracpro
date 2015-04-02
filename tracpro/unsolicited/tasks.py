from celery.task import task
from dash.orgs.models import Org
from tracpro.unsolicited.models import Unsolicited, Reply

__author__ = 'awesome'


@task
def fetch_all_unsolicited():
    for org in Org.objects.all():
        Unsolicited.fetch_and_update(org)

@task
def push_all_queued_messages():
    for org in Org.objects.all():
        Reply.send_queued(org)