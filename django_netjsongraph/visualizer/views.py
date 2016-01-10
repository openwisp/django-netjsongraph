from django.shortcuts import render_to_response

from ..models import Topology
from ..utils import get_topology_or_404


def topology_list(request):
    topologies = Topology.objects.filter(published=True)
    return render_to_response('netjsongraph/list.html',
                              {'topologies': topologies})


def topology_detail(request, pk):
    topology = get_topology_or_404(pk)
    return render_to_response('netjsongraph/detail.html',
                              {'topology': topology})
