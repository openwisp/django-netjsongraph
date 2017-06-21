from django.shortcuts import render_to_response
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
        return render_to_response('netjsongraph/detail.html',
                                  {'topology': topology,
                                   'VISUALIZER_CSS': VISUALIZER_CSS})
