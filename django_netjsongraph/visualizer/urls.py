from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.topology_list, name='topology_list'),
    url(r'^topology/(?P<pk>[^/]+)/$', views.topology_detail, name='topology_detail'),
]
