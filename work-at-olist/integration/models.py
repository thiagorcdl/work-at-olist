from django.db import models


class Channel(models.Model):
    """The media where products are published"""
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()


class Category(models.Model):
    """A self-referencing model that represents a product's category or subcategory"""
    channel = models.ForeignKey(Channel)
    parent = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'(%s) %s' % (self.channel, self.name)

    def __str__(self):
        return self.__unicode__()
