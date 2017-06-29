from django.core.management import call_command
from django.test import TestCase

from integration.models import Channel, Category


class ImportCategoriesTestCase(TestCase):
    def test_mycommand(self):
        """
        Asserts the correct amount of created objects.

        Multiple kinds of tests ar used:
            running normally, repeating the same command, using a file with repeating rows and
            using a file with categories in a random order
        """

        for channel, file in [('channel1', 'importcategories.csv'), ('channel1', 'importcategories.csv'),
                              ('channel2', 'importcategories-repeated.csv'),
                              ('channel3', 'importcategories-unordered.csv')]:
            args = [channel, 'integration/tests/%s' % file]
            call_command('importcategories', *args)

            self.assertEquals(Channel.objects.filter(name=channel).count(), 1)
            self.assertEquals(Category.objects.filter(channel__name=channel).count(), 23)
