"""
Serializers for Channel and Category models
"""
from rest_framework import serializers

from integration.models import Category, Channel


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for a simple Channel model"""
    class Meta:
        model = Channel
        fields = ('name', 'reference')


class SingleCategorySerializer(serializers.ModelSerializer):
    """Serializer for a simple Category model"""
    class Meta:
        model = Category
        fields = ('name', 'reference')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for complete information on a Category"""
    parent = SingleCategorySerializer()
    children = SingleCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'reference', 'parent', 'children')
