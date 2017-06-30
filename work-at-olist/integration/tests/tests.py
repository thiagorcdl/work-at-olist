from django.core.management import call_command
from django.test import TestCase

from integration.models import Channel, Category


class ImportCategoriesTestCase(TestCase):
    csv_dir = 'integration/tests/'

    def test_created_objects(self):
        """
        Asserts the correct amount of created objects.

        Multiple kinds of tests are used:
            running normally, repeating the same command, using a file with
            repeating rows and using a file with categories in a random order
        """

        for channel, file in [('channel1', 'importcategories.csv'),
                              ('channel1', 'importcategories.csv'),
                              ('channel2', 'importcategories-repeated.csv'),
                              ('channel3', 'importcategories-unordered.csv')]:
            args = [channel, self.csv_dir + file]
            call_command('importcategories', *args)

            self.assertEquals(Channel.objects.filter(name=channel).count(), 1)
            self.assertEquals(
                Category.objects.filter(channel__name=channel).count(), 23)
            c = Category.objects.filter(name__contains='360').first()
            anc = c.get_ancestors(c.reference)
            self.assertEquals(anc.count(), 1)

    def test_relatives(self):
        """
        Asserts the correct retrieval of both ancestors and descendants
        :return:
        """
        args = ['channel1', self.csv_dir + 'importcategories.csv']
        call_command('importcategories', *args)
        c = Category.objects.filter(name__contains='360').first()

        # Ancestors
        self.assertEquals(c.get_ancestors(c.reference).count(), 1)
        anc = c.get_ancestors(c.reference, get_current=True)
        self.assertEquals(anc.count(), 2)
        self.assertTrue(c in anc)

        # Descendants
        self.assertEquals(c.get_descendants(c.reference).count(), 3)
        desc = c.get_descendants(c.reference, get_current=True)
        self.assertEquals(desc.count(), 4)
        self.assertTrue(c in desc)
