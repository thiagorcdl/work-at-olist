from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ChannelListView, ChannelCategoryListView, RelatedCategoriesListView, CategoryView

urlpatterns = [
    url(r'^channels/$', ChannelListView.as_view()),
    url(r'^channels/categories/(?P<reference>[-\w]+)/$', ChannelCategoryListView.as_view()),
    url(r'^categories/(?P<reference>[-\w]+)/$', CategoryView.as_view()),
    url(r'^categories/related/(?P<reference>[-\w]+)/$', RelatedCategoriesListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
