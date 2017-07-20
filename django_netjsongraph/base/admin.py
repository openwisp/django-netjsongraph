from django.conf.urls import url
from django.contrib import messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.templatetags.admin_static import static
from django.db.models import Q
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from ..contextmanagers import log_failure
from ..utils import get_object_or_404


class TimeStampedEditableAdmin(ModelAdmin):
    """
    ModelAdmin for TimeStampedEditableModel
    """
    def __init__(self, *args, **kwargs):
        self.readonly_fields += ('created', 'modified',)
        super(TimeStampedEditableAdmin, self).__init__(*args, **kwargs)


class BaseAdmin(TimeStampedEditableAdmin):
    save_on_top = True

    class Media:
        css = {'all': [static('netjsongraph/css/src/netjsongraph.css'),
                       static('netjsongraph/css/style.css'),
                       static('netjsongraph/css/admin.css')]}
        js = [static('netjsongraph/js/lib/d3.min.js'),
              static('netjsongraph/js/src/netjsongraph.js'),
              static('netjsongraph/js/receive-url.js'),
              static('netjsongraph/js/strategy-switcher.js'),
              static('netjsongraph/js/visualize.js')]


class AbstractTopologyAdmin(BaseAdmin):
    list_display = ['label', 'parser', 'strategy', 'published', 'created', 'modified']
    readonly_fields = ['protocol', 'version', 'revision', 'metric', 'receive_url']
    list_filter = ['parser', 'strategy']
    search_fields = ['label', 'id']
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

    def change_view(self, request, pk, form_url='', extra_context=None):
        extra_context = extra_context or {}
        prefix = 'admin:{0}_{1}'.format(self.opts.app_label, self.model.__name__.lower())
        text = _('View topology graph')
        extra_context.update({
            'additional_buttons': [
                {
                    'type': 'button',
                    'url': reverse('{0}_visualize'.format(prefix), args=[pk]),
                    'class': 'visualizelink',
                    'value': text,
                    'title': '{0} (ALT+P)'.format(text)
                }
            ]
        })
        return super(AbstractTopologyAdmin, self).change_view(request, pk, form_url, extra_context)

    def get_urls(self):
        options = getattr(self.model, '_meta')
        url_prefix = '{0}_{1}'.format(options.app_label, options.model_name)
        return [
            url(r'^visualize/(?P<pk>[^/]+)/$',
                self.admin_site.admin_view(self.visualize_view),
                name='{0}_visualize'.format(url_prefix))
        ] + super(AbstractTopologyAdmin, self).get_urls()

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

    def visualize_view(self, request, pk):
        topology = get_object_or_404(self.model, pk)
        context = self.admin_site.each_context(request)
        opts = self.model._meta
        context.update({
            'is_popup': True,
            'opts': opts,
            'change': False,
            'media': self.media,
            'topology': topology
        })
        return TemplateResponse(request, 'admin/%s/visualize.html' % opts.app_label, context)


class AbstractNodeAdmin(BaseAdmin):
    list_display = ['name', 'topology', 'addresses']
    list_filter = ['topology']
    search_fields = ['addresses', 'label', 'properties']

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
    raw_id_fields = ['source', 'target']
    list_display = ['__str__', 'topology', 'status', 'cost', 'cost_text']
    list_filter = ['status', 'topology']
    search_fields = [
        'source__label',
        'target__label',
        'source__addresses',
        'target__addresses',
        'properties',
    ]
