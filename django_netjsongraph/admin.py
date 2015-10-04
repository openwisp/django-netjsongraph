from django.contrib import admin

from .models import Topology, Node, Link
from .base import TimeStampedEditableAdmin


class TopologyAdmin(TimeStampedEditableAdmin):
    list_display = ('label', 'parser', 'link_url', 'created', 'modified')
    readonly_fields = ['protocol', 'version', 'revision', 'metric']
    list_filter = ('parser',)

    def link_url(self, obj):  # pragma nocover
        return '<a href="{0}" target="_blank">{0}</a>'.format(obj.url)
    link_url.allow_tags = True


class NodeAdmin(TimeStampedEditableAdmin):
    list_display = ('name', 'addresses')
    search_fields = ('addresses', 'label', 'properties')


class LinkAdmin(TimeStampedEditableAdmin):
    raw_id_fields = ('source', 'target')
    list_display = ('__str__', 'topology', 'status', 'cost', 'cost_text')
    list_filter = ('status', 'topology')
    search_fields = ('source__addresses', 'target__addresses', 'properties',)


admin.site.register(Topology, TopologyAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Link, LinkAdmin)
