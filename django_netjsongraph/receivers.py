import json

from channels import Group
from django.dispatch import receiver
from django_netjsongraph.models import Link
from django_netjsongraph.utils import link_status_changed

from .utils import channel_group_name


@receiver(link_status_changed, sender=Link, dispatch_uid='ws_update_status')
def update_link_status(sender, **kwargs):
    link = kwargs['link']
    text = json.dumps({'id': link.id.hex, 'status': link.status})
    Group(channel_group_name).send({'text': text}, immediately=True)
