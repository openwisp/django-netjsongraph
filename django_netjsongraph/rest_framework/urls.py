from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^topology/$', views.network_collection, name='network_collection'),
    url(r'^topology/(?P<pk>[^/]+)/$', views.network_graph, name='network_graph'),
]
