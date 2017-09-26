from channels import Group

from .utils import channel_group_name


def ws_add(message):
    message.reply_channel.send({'accept': True})
    Group(channel_group_name).add(message.reply_channel)


def ws_disconnect(message):
    Group(channel_group_name).discard(message.reply_channel)
