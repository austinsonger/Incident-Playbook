from django.test import TestCase
from dfirtrack_main.models import Tagcolor

class TagcolorModelTestCase(TestCase):
    """ tagcolor model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Tagcolor.objects.create(tagcolor_name='tagcolor_1')

    def test_tagcolor_string(self):
        """ test string representation """

        # get object
        tagcolor_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_1')
        # compare
        self.assertEqual(str(tagcolor_1), 'tagcolor_1')

    def test_tagcolor_id_attribute_label(self):
        """ test attribute label """

        # get object
        tagcolor_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_1')
        # get label
        field_label = tagcolor_1._meta.get_field('tagcolor_id').verbose_name
        # compare
        self.assertEqual(field_label, 'tagcolor id')

    def test_tagcolor_name_attribute_label(self):
        """ test attribute label """

        # get object
        tagcolor_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_1')
        # get label
        field_label = tagcolor_1._meta.get_field('tagcolor_name').verbose_name
        # compare
        self.assertEqual(field_label, 'tagcolor name')

    def test_tagcolor_name_length(self):
        """ test for max length """

        # get object
        tagcolor_1 = Tagcolor.objects.get(tagcolor_name='tagcolor_1')
        # get max length
        max_length = tagcolor_1._meta.get_field('tagcolor_name').max_length
        # compare
        self.assertEqual(max_length, 20)
