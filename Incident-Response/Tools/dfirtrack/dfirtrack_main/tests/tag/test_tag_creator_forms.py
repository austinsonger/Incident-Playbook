from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import TagCreatorForm
from dfirtrack_main.models import System, Systemstatus, Tag, Tagcolor

class TagCreatorFormTestCase(TestCase):
    """ tag creator form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_tag_creator', password='rJaOH5aKfrbPpFmzdG3b')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_2',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')

        # create object
        Tag.objects.create(
            tag_name = 'tag_1',
            tagcolor = tagcolor_1,
        )
        Tag.objects.create(
            tag_name = 'tag_2',
            tagcolor = tagcolor_1,
        )

    def test_tag_creator_tag_form_label(self):
        """ test form label """

        # get object
        form = TagCreatorForm()
        # compare
        self.assertEqual(form.fields['tag'].label, 'Tags (*)')

    def test_tag_creator_system_form_label(self):
        """ test form label """

        # get object
        form = TagCreatorForm()
        # compare
        self.assertEqual(form.fields['system'].label, 'Systems (*)')

    def test_tag_creator_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = TagCreatorForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_tag_creator_system_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        system_1_id = System.objects.get(system_name='system_1').system_id
        system_2_id = System.objects.get(system_name='system_2').system_id
        # get object
        form = TagCreatorForm(data = {
            'system': [system_1_id, system_2_id],
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_tag_creator_tag_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        tag_1_id = Tag.objects.get(tag_name='tag_1').tag_id
        tag_2_id = Tag.objects.get(tag_name='tag_2').tag_id
        # get object
        system_1_id = System.objects.get(system_name='system_1').system_id
        system_2_id = System.objects.get(system_name='system_2').system_id
        # get object
        form = TagCreatorForm(data = {
            'system': [system_1_id, system_2_id],
            'tag': [tag_1_id, tag_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())
