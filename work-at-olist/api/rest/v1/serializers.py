"""
Serializers for Channel and Category models
"""
from rest_framework import serializers
from integration.models import Channel, Category


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
