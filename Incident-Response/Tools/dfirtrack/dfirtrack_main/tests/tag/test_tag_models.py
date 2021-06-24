from django.test import TestCase
from dfirtrack_main.models import Tag, Tagcolor

class TagModelTestCase(TestCase):
    """ tag model tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')

        # create object
        Tag.objects.create(tag_name='tag_1', tagcolor = tagcolor_1)

    def test_tag_string(self):
        """ test string representation """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # compare
        self.assertEqual(str(tag_1), 'tag_1')

    def test_tag_id_attribute_label(self):
        """ test attribute label """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # get label
        field_label = tag_1._meta.get_field('tag_id').verbose_name
        # compare
        self.assertEqual(field_label, 'tag id')

    def test_tag_tagcolor_attribute_label(self):
        """ test attribute label """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # get label
        field_label = tag_1._meta.get_field('tagcolor').verbose_name
        # compare
        self.assertEqual(field_label, 'tagcolor')

    def test_tag_name_attribute_label(self):
        """ test attribute label """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # get label
        field_label = tag_1._meta.get_field('tag_name').verbose_name
        # compare
        self.assertEqual(field_label, 'tag name')

    def test_tag_note_attribute_label(self):
        """ test attribute label """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # get label
        field_label = tag_1._meta.get_field('tag_note').verbose_name
        # compare
        self.assertEqual(field_label, 'tag note')

    def test_tag_name_length(self):
        """ test for max length """

        # get object
        tag_1 = Tag.objects.get(tag_name='tag_1')
        # get max length
        max_length = tag_1._meta.get_field('tag_name').max_length
        # compare
        self.assertEqual(max_length, 50)
