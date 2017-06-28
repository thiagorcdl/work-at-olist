from django.db import models


class Channel(models.Model):
    """The media where products are published"""
    name = models.CharField(max_length=64)


class Category(models.Model):
    """A self-referencing model that represents a product's category or subcategory"""
    channel = models.ForeignKey(Channel)
    parent = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=64)


class Seller(models.Model):
    """The users who are publishing products"""
    name = models.CharField(max_length=64)


class Product(models.Model):
    """The object on sale"""
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=64)
