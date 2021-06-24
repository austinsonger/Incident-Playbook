from django.test import TestCase
from dfirtrack_main.forms import TagForm
from dfirtrack_main.models import Tagcolor

class TagFormTestCase(TestCase):
    """ tag form tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Tagcolor.objects.create(tagcolor_name='tagcolor_1')

    def test_tag_name_form_label(self):
        """ test form label """

        # get object
        form = TagForm()
        # compare
        self.assertEqual(form.fields['tag_name'].label, 'Tag name (*)')

    def test_tag_tagcolor_form_label(self):
        """ test form label """

        # get object
        form = TagForm()
        # compare
        self.assertEqual(form.fields['tagcolor'].label, 'Tag color (*)')

    def test_tag_note_form_label(self):
        """ test form label """

        # get object
        form = TagForm()
        # compare
        self.assertEqual(form.fields['tag_note'].label, 'Tag note')

    def test_tag_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = TagForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_tag_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = TagForm(data = {
            'tag_name': 'tag_1',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_tag_tagcolor_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        tagcolor_id = Tagcolor.objects.get(tagcolor_name='tagcolor_1').tagcolor_id
        # get object
        form = TagForm(data = {
            'tag_name': 'tag_1',
            'tagcolor': tagcolor_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_tag_note_form_filled(self):
        """ test additional form content """

        # get foreign key object id
        tagcolor_id = Tagcolor.objects.get(tagcolor_name='tagcolor_1').tagcolor_id
        # get object
        form = TagForm(data = {
            'tag_name': 'tag_1',
            'tagcolor': tagcolor_id,
            'tag_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_tag_name_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        tagcolor_id = Tagcolor.objects.get(tagcolor_name='tagcolor_1').tagcolor_id
        # get object
        form = TagForm(data = {'tag_name': 'tttttttttttttttttttttttttttttttttttttttttttttttttt', 'tagcolor': tagcolor_id})
        # compare
        self.assertTrue(form.is_valid())

    def test_tag_name_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        tagcolor_id = Tagcolor.objects.get(tagcolor_name='tagcolor_1').tagcolor_id
        # get object
        form = TagForm(data = {'tag_name': 'ttttttttttttttttttttttttttttttttttttttttttttttttttt', 'tagcolor': tagcolor_id})
        # compare
        self.assertFalse(form.is_valid())
