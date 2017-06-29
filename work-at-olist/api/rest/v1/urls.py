from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^channels/$', views.ChannelList.as_view()),
    url(r'^channels/(?P<id>[0-9]+)/$', views.ChannelCategories.as_view()),
    url(r'^categories/(?P<id>[0-9]+)/$', views.CategoriesRelated.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)