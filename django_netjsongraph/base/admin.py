from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.templatetags.admin_static import static
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from ..contextmanagers import log_failure

try:
    from django.urls import reverse
except:
    # django < 1.10
    from django.core.urlresolvers import reverse


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    def __init__(self, *args, **kwargs):
        self.readonly_fields += ('created', 'modified',)
        super(TimeStampedEditableAdmin, self).__init__(*args, **kwargs)


class BaseAdmin(TimeStampedEditableAdmin):
    class Media:
        css = {'all': [static('netjsongraph/admin.css')]}
        js = [static('netjsongraph/receive-url.js'),
              static('netjsongraph/strategy-switcher.js')]


class AbstractTopologyAdmin(BaseAdmin):
    list_display = ('label', 'parser', 'strategy', 'published', 'created', 'modified')
    readonly_fields = ['protocol', 'version', 'revision', 'metric', 'receive_url']
    list_filter = ('parser', 'strategy')
    actions = ['update_selected', 'unpublish_selected', 'publish_selected']
    fields = ['label', 'parser', 'strategy', 'url', 'key',
              'expiration_time', 'receive_url', 'published', 'protocol',
              'version', 'revision', 'metric', 'created']

    def receive_url(self, obj):
        url = reverse('receive_topology', kwargs={'pk': obj.pk})
        return '{0}?key={1}'.format(url, obj.key)

    receive_url.short_description = _('receive url')

    def get_actions(self, request):
        """
        move delete action to last position
        """
        actions = super(AbstractTopologyAdmin, self).get_actions(request)
        delete = actions['delete_selected']
        del actions['delete_selected']
        actions['delete_selected'] = delete
        return actions

    def _message(self, request, rows, suffix, level=messages.SUCCESS):
        if rows == 1:
            prefix = _('1 {0} was'.format(self.model._meta.verbose_name))
        else:  # pragma: nocover
            prefix = _('{0} {1} were'.format(rows, self.model._meta.verbose_name_plural))
        self.message_user(request, '{0} {1}'.format(prefix, suffix), level=level)

    def update_selected(self, request, queryset):
        items = list(queryset)
        failed = []
        for item in items:
            try:
                item.update()
            except Exception as e:
                failed.append('{0}: {1}'.format(item.label, str(e)))
                with log_failure('update topology admin action', item):
                    raise e
        failures = len(failed)
        successes = len(items) - failures
        if successes > 0:
            self._message(request, successes, _('successfully updated'))
        if failures > 0:
            message = _('not updated. %s') % '; '.join(failed)
            self._message(request, failures, message, level=messages.ERROR)
    update_selected.short_description = _('Update selected topologies')

    def publish_selected(self, request, queryset):
        rows_updated = queryset.update(published=True)
        self._message(request, rows_updated, _('successfully published'))
    publish_selected.short_description = _('Publish selected topologies')

    def unpublish_selected(self, request, queryset):
        rows_updated = queryset.update(published=False)
        self._message(request, rows_updated, _('successfully unpublished'))
    unpublish_selected.short_description = _('Unpublish selected items')


class AbstractNodeAdmin(BaseAdmin):
    list_display = ('name', 'topology', 'addresses')
    list_filter = ('topology',)
    search_fields = ('addresses', 'label', 'properties')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        link_model = self.model.source_link_set.field.model
        extra_context.update({
            'node_links': link_model.objects.select_related('source', 'target')
                                            .only('source__label',
                                                  'target__label',
                                                  'cost',
                                                  'status')
                                            .filter(Q(source_id=object_id) |
                                                    Q(target_id=object_id))
        })
        return super(AbstractNodeAdmin, self).change_view(request, object_id, form_url, extra_context)


class AbstractLinkAdmin(BaseAdmin):
    raw_id_fields = ('source', 'target')
    list_display = ('__str__', 'topology', 'status', 'cost', 'cost_text')
    list_filter = ('status', 'topology')
    search_fields = (
        'source__label',
        'target__label',
        'source__addresses',
        'target__addresses',
        'properties',
    )
