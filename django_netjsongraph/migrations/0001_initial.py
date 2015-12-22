# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import jsonfield.fields
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('cost', models.FloatField()),
                ('cost_text', models.CharField(max_length=24, blank=True)),
                ('status', model_utils.fields.StatusField(default=b'up', max_length=100, no_check_for_status=True, choices=[(b'up', b'up'), (b'down', b'down')])),
                ('properties', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=64, blank=True)),
                ('addresses', models.CharField(max_length=255, db_index=True)),
                ('properties', jsonfield.fields.JSONField(default=dict, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topology',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=64, verbose_name='label')),
                ('parser', models.CharField(help_text='Select topology format', max_length=128, verbose_name='format', choices=[(b'netdiff.OlsrParser', b'OLSRd (txtinfo/jsoninfo)'), (b'netdiff.BatmanParser', b'batman-advanced (jsondoc/txtinfo)'), (b'netdiff.BmxParser', b'BMX6 (q6m)'), (b'netdiff.NetJsonParser', b'NetJSON NetworkGraph'), (b'netdiff.CnmlParser', b'CNML 1.0')])),
                ('url', models.URLField(help_text='Topology data will be fetched from this URL', verbose_name='url')),
                ('protocol', models.CharField(max_length=64, verbose_name='protocol', blank=True)),
                ('version', models.CharField(max_length=24, verbose_name='version', blank=True)),
                ('revision', models.CharField(max_length=64, verbose_name='revision', blank=True)),
                ('metric', models.CharField(max_length=24, verbose_name='metric', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'topologies',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='source',
            field=models.ForeignKey(related_name='source_node_set', to='django_netjsongraph.Node'),
        ),
        migrations.AddField(
            model_name='link',
            name='target',
            field=models.ForeignKey(related_name='target_node_set', to='django_netjsongraph.Node'),
        ),
        migrations.AddField(
            model_name='link',
            name='topology',
            field=models.ForeignKey(to='django_netjsongraph.Topology'),
        ),
    ]
