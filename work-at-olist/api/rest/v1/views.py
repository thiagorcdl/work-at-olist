"""
API views for Channel and Category models
"""
from rest_framework import generics
from integration.models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer, \
    SingleCategorySerializer


class ChannelListView(generics.ListCreateAPIView):
    """A simple ListView that returns all existing channels"""
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelCategoryListView(generics.ListCreateAPIView):
    """ListView which returns every Category for a given Channel"""
    queryset = Category.objects.all()
    serializer_class = SingleCategorySerializer

    def get_queryset(self):
        channel_reference = self.kwargs.get('reference')
        return self.queryset.filter(channel__reference=channel_reference)


class CategoryView(generics.RetrieveAPIView):
    """DetailView which returns a single"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'reference'


class RelatedCategoriesListView(generics.ListCreateAPIView):
    """
    ListView which returns the given category and
    all of its ancestors and descendants
    """
    queryset = Category.objects.all()
    serializer_class = SingleCategorySerializer

    def get_queryset(self):
        channel_reference = self.kwargs.get('reference')
        ascendants = Category.get_ancestors(channel_reference)
        descendants = Category.get_descendants(channel_reference,
                                               get_current=True)
        return ascendants | descendants
