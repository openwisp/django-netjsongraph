from django.shortcuts import render
from django.urls import reverse
from django.views import View

from ..settings import VISUALIZER_CSS
from ..utils import get_object_or_404


class BaseTopologyListView(View):
    def get(self, request):
        topologies = self.topology_model.objects.filter(published=True)
        return render(request, 'netjsongraph/list.html',
                      {'topologies': topologies,
                       'VISUALIZER_CSS': VISUALIZER_CSS})


class BaseTopologyDetailView(View):
    def get(self, request, pk):
        topology = get_object_or_404(self.topology_model, pk)
        return render(request, 'netjsongraph/detail.html', {
            'topology': topology,
            'graph_url': reverse('network_graph', args=[topology.pk]),
            'history_url': reverse('network_graph_history', args=[topology.pk]),
            'VISUALIZER_CSS': VISUALIZER_CSS
        })
