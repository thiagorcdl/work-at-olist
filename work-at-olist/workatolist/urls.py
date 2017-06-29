from django.conf.urls import url, include
from django.contrib import admin
import api

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api.rest.v1.urls, namespace='api'))
]
