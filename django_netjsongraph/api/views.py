from rest_framework import generics

from ..models import Topology
from .serializers import NetworkGraphSerializer


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
