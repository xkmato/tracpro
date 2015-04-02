# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orgs', '0009_auto_20150331_0728'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contacts', '0003_auto_20150224_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name=b' ')),
                ('status', models.CharField(default=b'Q', max_length=1, choices=[(b'Q', 'Queued'), (b'S', 'Sent'), (b'F', 'Failed')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('reply_by', models.ForeignKey(related_name='unsolicited_replies', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unsolicited',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('created_on', models.DateTimeField()),
                ('delivered_on', models.DateTimeField(null=True)),
                ('contact', models.ForeignKey(related_name='unsolicited_messages', to='contacts.Contact', to_field=b'uuid')),
                ('org', models.ForeignKey(to='orgs.Org')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reply',
            name='reply_to',
            field=models.ForeignKey(related_name='replies', to='unsolicited.Unsolicited'),
            preserve_default=True,
        ),
    ]
