from django.shortcuts import render_to_response
from django.urls import reverse
from django.views import View

from ..settings import VISUALIZER_CSS
from ..utils import get_object_or_404


class BaseTopologyListView(View):
    def get(self, request):
        topologies = self.topology_model.objects.filter(published=True)
        return render_to_response('netjsongraph/list.html',
                                  {'topologies': topologies,
                                   'VISUALIZER_CSS': VISUALIZER_CSS})


class BaseTopologyDetailView(View):
    def get(self, request, pk):
        topology = get_object_or_404(self.topology_model, pk)
        api_url = reverse('network_graph', args=[topology.pk])
        graph_url = reverse('topology_history', args=[topology.pk])
        return render_to_response('netjsongraph/detail.html',
                                  {'api_url': api_url,
                                   'graph_url': graph_url,
                                   'VISUALIZER_CSS': VISUALIZER_CSS})


class BaseTopologyHistoryView(View):
    def get(self, request, pk):
        topology = get_object_or_404(self.topology_model, pk)
        date = request.GET.get('date', '')
        api_url = '{0}?date={1}'.format(reverse('network_graph_history', args=[topology.pk]), date)
        graph_url = reverse('topology_history', args=[topology.pk])
        return render_to_response('netjsongraph/detail.html',
                                  {'api_url': api_url,
                                   'graph_url': graph_url,
                                   'VISUALIZER_CSS': VISUALIZER_CSS})
