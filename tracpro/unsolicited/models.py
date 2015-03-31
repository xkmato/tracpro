import datetime
from celery.utils.log import get_task_logger
from dash.orgs.models import Org
from django.db import models
from tracpro.contacts.models import Contact

__author__ = 'awesome'
logger = get_task_logger(__name__)


class Unsolicited(models.Model):
    contact = models.ForeignKey(Contact, related_name="unsolicited_messages", to_field="uuid")
    org = models.ForeignKey(Org)
    status = models.CharField(max_length=100)
    text = models.TextField()
    created_on = models.DateTimeField()
    delivered_on = models.DateTimeField(null=True)

    def __unicode__(self):
        return "%s, by %s" % (self.text[:10], self.contact.urn)

    @classmethod
    def fetch_and_update(cls, org):
        client = org.get_temba_client()
        if Unsolicited.objects.exists():
            latest = Unsolicited.objects.latest('created_on').created_on + datetime.timedelta(0, 0.5)#Adding 1/2 sec(rapidpro will with the time after)
            messages = client.get_messages(directions=['I'], _types=['I'], after=latest)
        else:
            messages = client.get_messages(directions=['I'], _types=['I'])
        _messages = []
        for message in messages:
            try:
                _messages.append(
                    Unsolicited(contact=Contact.get_or_fetch(org, message.contact), org=org, status=message.status,
                                text=message.text, created_on=message.created_on, delivered_on=message.delivered_on))
            except Exception as e:
                logger.error("Message skipped - Reason:", e)
        Unsolicited.objects.bulk_create(_messages)