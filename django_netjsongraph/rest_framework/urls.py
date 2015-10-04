from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^topology/$', views.network_collection, name='topology_list'),
    url(r'^topology/(?P<pk>[^/]+)/$', views.network_graph, name='topology_detail'),
]
