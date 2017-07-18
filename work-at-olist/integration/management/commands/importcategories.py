import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from integration.models import Category, Channel


class Command(BaseCommand):
    help = 'Imports channel\'s categories from CSV file.'

    def log_msg(self, msg):
        if settings.DEBUG:
            print(msg)

    def add_categories(self, channel, parent, children, ancestors):
        """
        Recursive function responsible for creating new categories and setting
        their parent category.

        :param channel: <integration.models.Channel> object
        :param parent: <integration.models.Category> object
        :param children: <dict> of category names (<dicts>)
        :param ancestors: <str> of parent category names
        :return:
        """
        delimiter = Category.delimiter
        for category_name in children:
            references = delimiter.join([ancestors, category_name])
            category = Category.objects.create(channel=channel, parent=parent,
                                               reference=slugify(references),
                                               name=category_name)
            self.log_msg(u'# Creating category %s' % category_name)

            # Call recursion using current category as parent
            self.add_categories(channel, parent=category,
                                children=children[category_name],
                                ancestors=references)

    def add_arguments(self, parser):
        """Specifies the command parameters"""
        parser.add_argument('channel', type=str)
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        """Main method of the command"""
        category_tree = {}

        # Get or create given channel
        channel_name = kwargs.get('channel')
        slug = slugify(channel_name)
        channel, created = Channel.objects.get_or_create(name=channel_name,
                                                         reference=slug)
        if created:
            self.log_msg(u'# Creating new channel "%s"' % channel_name)
        else:
            self.log_msg(u'# Performing full update on all of '
                         u'%s\'s categories' % channel_name)
            Category.objects.filter(channel=channel).delete()

        # Open CSV file as dictionary
        file_path = kwargs.get('file_path')
        try:
            dictlines = csv.DictReader(open(file_path))
        except TypeError:
            raise TypeError(
                u'Failed to open CSV file. Please inform a valid path.')
        for line in dictlines:
            # Acquire category path for each entry
            try:
                path = line['Category']
            except KeyError:
                raise KeyError(u'Missing column "Category"')
            categories = path.split('/')
            parent = category_tree
            for category in categories:
                parent = parent.setdefault(category.strip(), {})

        # Start recursion at the root of the dictionary
        self.add_categories(channel, parent=None, children=category_tree,
                            ancestors=channel_name)
