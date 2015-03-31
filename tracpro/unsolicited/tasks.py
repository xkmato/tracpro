from celery.task import task
from dash.orgs.models import Org
from tracpro.unsolicited.models import Unsolicited

__author__ = 'awesome'


@task
def fetch_all_unsolicited():
    for org in Org.objects.all():
        Unsolicited.fetch_and_update(org)