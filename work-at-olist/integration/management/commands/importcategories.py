from django.core.management.base import BaseCommand
from integration.models import Channel, Category
import csv


class Command(BaseCommand):
    help = 'Imports channel\'s categories from CSV file.'

    def add_categories(self, channel, parent, children):
        """
        Recursive function responsible for creating new categories and setting their parent category.

        :param channel: <integration.models.Channel> object
        :param parent: <integration.models.Category> object
        :param children: <dict> of category names (<dicts>)
        :return:
        """
        for category_name in children:
            category = Category.objects.create(channel=channel, parent=parent, name=category_name)
            print(u'# Creating category %s' % category_name)

            # Call recursion using current category as parent
            self.add_categories(channel, parent=category, children=children[category_name])

    def add_arguments(self, parser):
        """Specifies the command parameters"""
        parser.add_argument('channel', type=str)
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        """Main method of the command"""
        category_tree = {}

        # Get or create given channel
        channel_name = kwargs.get('channel')
        channel, created = Channel.objects.get_or_create(name=channel_name)
        if created:
            print(u'# Creating new channel "%s"' % channel_name)
        else:
            print(u'# Performing full update on all of %s\'s categories' % channel_name)
            Category.objects.filter(channel=channel).delete()

        # Open CSV file as dictionary
        file_path = kwargs.get('file_path')
        try:
            dictlines = csv.DictReader(open(file_path))
        except TypeError:
            raise TypeError(u'Failed to open CSV file. Please inform a valid path.')
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
        self.add_categories(channel, None, category_tree)
