from django.contrib import admin

from .models import Topology, Node, Link
from .base import TimeStampedEditableAdmin


class TopologyAdmin(TimeStampedEditableAdmin):
    list_display = ('label', 'parser', 'url', 'created', 'modified')
    readonly_fields = ['protocol', 'version', 'revision', 'metric']


class NodeAdmin(TimeStampedEditableAdmin):
    list_display = ('name', 'addresses')


class LinkAdmin(TimeStampedEditableAdmin):
    raw_id_fields  = ('source', 'target')
    list_display = ('__str__', 'topology', 'cost', 'cost_text')


admin.site.register(Topology, TopologyAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Link, LinkAdmin)
