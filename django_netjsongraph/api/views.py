from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import ugettext_lazy as _
from netdiff.exceptions import NetdiffException

from ..models import Topology
from ..utils import get_topology_or_404
from .serializers import NetworkGraphSerializer
from .parsers import TextParser


class NetworkCollectionView(generics.ListAPIView):
    """
    Data of all the topologies returned
    in NetJSON NetworkCollection format
    """
    queryset = Topology.objects.filter(published=True)
    serializer_class = NetworkGraphSerializer

network_collection = NetworkCollectionView.as_view()


class NetworkGraphView(generics.RetrieveAPIView):
    """
    Data of a specific topology returned
    in NetJSON NetworkGraph format
    """
    queryset = Topology.objects.filter(published=True)
    serializer_class = NetworkGraphSerializer

network_graph = NetworkGraphView.as_view()


class ReceiveTopologyView(APIView):
    """
    This views allow nodes to send topology data using the RECEIVE strategy.

    Required query string parameters:
        * key

    Allowed content-types:
        * text/plain
    """
    parser_classes = (TextParser,)

    def post(self, request, pk, format=None):
        topology = get_topology_or_404(pk, strategy='receive')
        key = request.query_params.get('key')
        # wrong content type: 415
        if request.content_type != 'text/plain':
            return Response({'detail': _('expected content type "text/plain"')},
                            status=415)
        # missing key: 400
        if not key:
            return Response({'detail': _('missing required "key" parameter')},
                            status=400)
        # wrong key 403
        if topology.key != key:
            return Response({'detail': _('wrong key')},
                            status=403)
        try:
            topology.receive(request.data)
        except NetdiffException as e:
            error = _('Supplied data not recognized as %s, '
                      'got exception of type "%s" '
                      'with message "%s"') % (topology.get_parser_display(),
                                              e.__class__.__name__, e)
            return Response({'detail': error}, status=400)
        return Response({'detail': _('data received successfully')})

receive_topology = ReceiveTopologyView.as_view()
