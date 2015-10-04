from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django_netjsongraph.rest_framework import urls as rest_urls

admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(rest_urls)),
]

urlpatterns += staticfiles_urlpatterns()
