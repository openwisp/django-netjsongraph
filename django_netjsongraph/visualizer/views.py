from django.shortcuts import render_to_response, get_object_or_404

from ..models import Topology


def topology_list(request):
    topologies = Topology.objects.filter(published=True)
    return render_to_response('netjsongraph/list.html',
                              {'topologies': topologies})


def topology_detail(request, pk):
    topology = get_object_or_404(Topology, pk=pk, published=True)
    return render_to_response('netjsongraph/detail.html',
                              {'topology': topology})
