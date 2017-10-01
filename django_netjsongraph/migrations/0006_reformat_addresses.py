from __future__ import unicode_literals

from django.db import migrations
from django_netjsongraph.models import Node


def reformat_address_forward(apps, schema_editor):
    for node in Node.objects.all():
        if not node.addresses.startswith(';'):
            node.addresses = ';{0}'.format(node.addresses)
            node.save()


def reformat_address_backward(apps, schema_editor):
    fake_node_model = apps.get_model('django_netjsongraph', 'Node')
    for node in fake_node_model.objects.all():
        if node.addresses.startswith(';'):
            node.addresses = node.addresses[1:]
            node.save()


class Migration(migrations.Migration):
    dependencies = [
        ('django_netjsongraph', '0005_snapshot'),
    ]

    operations = [
        migrations.RunPython(reformat_address_forward,
                             reformat_address_backward),
    ]
