"""
Test cases for each endpoint
"""

import json

from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APITestCase


class IntegrationAPITestCase(APITestCase):
    csv_dir = 'integration/tests/'

    def setUp(self):
        """Initial setup for tests. Populates database."""
        self.maxDiff = None
        args = ['channel1', self.csv_dir + 'importcategories.csv']
        call_command('importcategories', *args)
        args = ['channel2', self.csv_dir + 'importcategories-repeated.csv']
        call_command('importcategories', *args)

    def test_channel_listview(self):
        """Asserts ChannelListView"""
        url = reverse('api:channels')
        request = self.client.get(url)
        self.assertEqual(len(request.data), 2)

    def test_channelcategory_listview(self):
        """Asserts ChannelCategoryListView"""
        url = reverse('api:channel_category', kwargs={'reference': 'channel1'})
        request = self.client.get(url)
        self.assertEqual(len(request.data), 23)

    def test_category_view(self):
        """Asserts CategoryView"""
        reference = 'channel2_books_national-literature'
        kwargs = {'reference': reference}
        url = reverse('api:categories', kwargs=kwargs)
        request = self.client.get(url)
        self.assertEqual(json.loads(request.content), {
            "name": "National Literature",
            "reference": "channel2_books_national-literature",
            "parent": {
                "name": "Books",
                "reference": "channel2_books"
            },
            "children": [
                {
                    "name": "Fiction Fantastic",
                    "reference": "channel2_books_national-"
                                 "literature_fiction-fantastic"
                },
                {
                    "name": "Science Fiction",
                    "reference": "channel2_books_national-"
                                 "literature_science-fiction"
                }
            ]
        })

    def test_relatedcategories_listview(self):
        """Asserts RelatedCategoriesListView"""
        reference = 'channel1_books_national-literature_fiction-fantastic'
        kwargs = {'reference': reference}
        url = reverse('api:related_categories', kwargs=kwargs)
        request = self.client.get(url)
        self.assertEqual(len(request.data), 3)
        self.assertEqual(json.loads(request.content), [
            {
                "name": "Books",
                "reference": "channel1_books"
            },
            {
                "name": "National Literature",
                "reference": "channel1_books_national-literature"
            },
            {
                "name": "Fiction Fantastic",
                "reference": "channel1_books_national-"
                             "literature_fiction-fantastic"
            }
        ])
