"""
API views for Channel and Category models
"""
from rest_framework import generics
from integration.models import Channel, Category
from .serializers import ChannelSerializer, CategorySerializer


class ChannelList(generics.ListCreateAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
