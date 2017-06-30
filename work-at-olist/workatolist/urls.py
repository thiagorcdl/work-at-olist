from django.conf.urls import url, include
from django.contrib import admin
from api.rest.v1 import urls as apiurls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(apiurls, namespace='api'))
]
