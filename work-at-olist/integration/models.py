from django.db import models
from django.db.models import Q


class Channel(models.Model):
    """The media where products are published"""
    reference = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Category(models.Model):
    """A self-referencing model that represents a product's category or subcategory"""
    channel = models.ForeignKey(Channel)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    reference = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    delimiter = '_'

    def __unicode__(self):
        return u'(%s) %s' % (self.channel, self.name)

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_ancestors(reference, get_current=False):
        """
        Returns all ancestors of the given category.
        Considering the way references are built (using double hifen to separate levels), all parent's are guaranteed
        to have a prefix of the current reference as their own.
        :param reference: <str> reference of a Category object
        :param get_current: <bool> defines whether to retrieve the current Category as well or not
        :return: <Category> QuerySet
        """
        references = reference.split(Category.delimiter)[:None if get_current else -1]

        query = Q()
        while len(references) > 1:
            query |= Q(reference=Category.delimiter.join(references))
            references.pop()

        return Category.objects.filter(query) if query else Category.objects.none()

    @staticmethod
    def get_descendants(reference, get_current=False):
        """
        Returns all children of the given category and their respective children, recursively.
        Considering the reference is the category path, all subcategories are guaranteed to have
        this category's reference as a prefix to their own.
        :param reference: <str> reference of a Category object
        :param get_current: <bool> defines whether to retrieve the current Category as well or not
        :return: <Category> QuerySet
        """
        queryset = Category.objects.filter(reference__startswith=reference)
        return queryset if get_current else queryset.exclude(reference=reference)
