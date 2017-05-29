from django.shortcuts import render_to_response

from ..models import Topology
from ..settings import VISUALIZER_CSS
from ..utils import get_object_or_404


def topology_list(request):
    topologies = Topology.objects.filter(published=True)
    return render_to_response('netjsongraph/list.html',
                              {'topologies': topologies,
                               'VISUALIZER_CSS': VISUALIZER_CSS})


def topology_detail(request, pk):
    topology = get_object_or_404(Topology, pk)
    return render_to_response('netjsongraph/detail.html',
                              {'topology': topology,
                               'VISUALIZER_CSS': VISUALIZER_CSS})
