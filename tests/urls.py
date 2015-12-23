from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_netjsongraph.api import urls as netjsongraph_api
from django_netjsongraph.visualizer import urls as netjsongraph_visualizer

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(netjsongraph_api)),
    url(r'', include(netjsongraph_visualizer)),
]

urlpatterns += staticfiles_urlpatterns()
