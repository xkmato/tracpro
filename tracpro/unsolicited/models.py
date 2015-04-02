from celery.utils.log import get_task_logger
from dash.orgs.models import Org
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
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

    class Meta:
        verbose_name = "Query & Feedback"
        verbose_name_plural = "Queries & Feedback"

    def __unicode__(self):
        return "%s, by %s" % (self.text[:10], self.contact.urn)

    @classmethod
    def fetch_and_update(cls, org):
        client = org.get_temba_client()
        if Unsolicited.objects.exists():
            latest = Unsolicited.objects.latest('created_on').created_on
            messages = client.get_messages(directions=['I'], _types=['I'], after=latest)
        else:
            messages = client.get_messages(directions=['I'], _types=['I'])
        _messages = []
        for i in range(len(messages)):
            message = messages.pop(i)
            try:
                if Unsolicited.objects.filter(contact=Contact.get_or_fetch(org, message.contact), org=org,
                                              status=message.status, text=message.text, created_on=message.created_on,
                                              delivered_on=message.delivered_on).exists():
                    logger.info("Message sent on %s Already exists" % str(message.created_on))
                    continue
                _messages.append(
                    Unsolicited(contact=Contact.get_or_fetch(org, message.contact), org=org, status=message.status,
                                text=message.text, created_on=message.created_on,
                                delivered_on=message.delivered_on))
            except Exception as e:
                logger.error("Message skipped - Reason:", e)
        Unsolicited.objects.bulk_create(_messages)


class Reply(models.Model):
    QUEUED = 'Q'
    SENT = 'S'
    FAILED = 'F'

    STATUS_CHOICES = ((QUEUED, _('Queued')), (SENT, _('Sent')), (FAILED, _('Failed')))

    reply_to = models.ForeignKey(Unsolicited, related_name='replies')
    reply_by = models.ForeignKey(User, related_name='unsolicited_replies')
    text = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=QUEUED)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s, by %s" % (self.text[:10], self.reply_by.username)

    def to_json(self):
        return dict(id=self.pk, text=self.text, reply_to=self.reply_to_id, reply_by=self.reply_by_id,
                    created_on=str(self.created_on))

    @classmethod
    def send_queued(cls, org):
        client = org.get_temba_client()
        for message in cls.objects.filter(status=cls.QUEUED):
            try:
                client.create_broadcast(message.text, contacts=[message.reply_to.contact.uuid])
                message.status = cls.SENT
                logger.info("Sent message %d from user #%d" % (message.pk, message.reply_by.pk))
            except Exception as e:
                # TODO use that e
                message.status = cls.FAILED
                logger.error("Sending message %d failed" % message.pk, exc_info=1)
            message.save(update_fields=('status',))

