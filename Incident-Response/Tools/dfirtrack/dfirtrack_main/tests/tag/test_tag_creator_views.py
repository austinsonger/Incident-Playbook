from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import System, Systemstatus, Tag, Tagcolor
import urllib.parse

class TagCreatorViewTestCase(TestCase):
    """ tag creator view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')

        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        # create objects
        Tag.objects.create(tag_name='tag_creator_tag_1', tagcolor = tagcolor_1)
        Tag.objects.create(tag_name='tag_creator_tag_2', tagcolor = tagcolor_1)
        Tag.objects.create(tag_name='tag_creator_tag_3', tagcolor = tagcolor_1)

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='tag_creator_systemstatus_1')
        # create objects
        System.objects.create(
            system_name = 'tag_creator_system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'tag_creator_system_2',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'tag_creator_system_3',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_tag_creator_not_logged_in(self):
        """ test creator view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/tag/creator/', safe='')
        # get response
        response = self.client.get('/tag/creator/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_tag_creator_logged_in(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get response
        response = self.client.get('/tag/creator/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_tag_creator_template(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get response
        response = self.client.get('/tag/creator/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/tag/tag_creator.html')

    def test_tag_creator_get_user_context(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get response
        response = self.client.get('/tag/creator/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_tag_creator')

    def test_tag_creator_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # create url
        destination = urllib.parse.quote('/tag/creator/', safe='/')
        # get response
        response = self.client.get('/tag/creator', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_tag_creator_post_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get objects
        tag_1 = Tag.objects.get(tag_name='tag_creator_tag_1')
        system_1 = System.objects.get(system_name='tag_creator_system_1')
        # create post data
        data_dict = {
            'system': [system_1.system_id,],
            'tag': [tag_1.tag_id,],
        }
        # create url
        destination = '/tag/'
        # get response
        response = self.client.post('/tag/creator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_tag_creator_post_system_and_tags(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get objects
        tag_1 = Tag.objects.get(tag_name='tag_creator_tag_1')
        tag_2 = Tag.objects.get(tag_name='tag_creator_tag_2')
        tag_3 = Tag.objects.get(tag_name='tag_creator_tag_3')
        system_1 = System.objects.get(system_name='tag_creator_system_1')
        system_2 = System.objects.get(system_name='tag_creator_system_2')
        system_3 = System.objects.get(system_name='tag_creator_system_3')
        # create post data
        data_dict = {
            'system': [system_1.system_id, system_2.system_id],
            'tag': [tag_1.tag_id, tag_2.tag_id],
        }
        # get response
        self.client.post('/tag/creator/', data_dict)
        # compare
        self.assertTrue(system_1.tag.filter(tag_name=tag_1.tag_name).exists())
        self.assertTrue(system_1.tag.filter(tag_name=tag_2.tag_name).exists())
        self.assertFalse(system_1.tag.filter(tag_name=tag_3.tag_name).exists())
        self.assertTrue(system_2.tag.filter(tag_name=tag_1.tag_name).exists())
        self.assertTrue(system_2.tag.filter(tag_name=tag_2.tag_name).exists())
        self.assertFalse(system_2.tag.filter(tag_name=tag_3.tag_name).exists())
        self.assertFalse(system_3.tag.filter(tag_name=tag_1.tag_name).exists())
        self.assertFalse(system_3.tag.filter(tag_name=tag_2.tag_name).exists())
        self.assertFalse(system_3.tag.filter(tag_name=tag_3.tag_name).exists())

    def test_tag_creator_post_empty_redirect(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # create post data
        data_dict = {}
        # create url
        destination = '/tag/'
        # get response
        response = self.client.post('/tag/creator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_tag_creator_post_messages(self):
        """ test creator view """

        # login testuser
        self.client.login(username='testuser_tag_creator', password='X4zm4Em28xrKgVMBpsWF')
        # get objects
        tag_1 = Tag.objects.get(tag_name='tag_creator_tag_1')
        tag_2 = Tag.objects.get(tag_name='tag_creator_tag_2')
        tag_3 = Tag.objects.get(tag_name='tag_creator_tag_3')
        system_1 = System.objects.get(system_name='tag_creator_system_1')
        system_2 = System.objects.get(system_name='tag_creator_system_2')
        system_3 = System.objects.get(system_name='tag_creator_system_3')
        # create post data
        data_dict = {
            'system': [system_1.system_id, system_2.system_id, system_3.system_id],
            'tag': [tag_1.tag_id, tag_2.tag_id, tag_3.tag_id],
        }
        # get response
        response = self.client.post('/tag/creator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'Tag creator started')
        self.assertEqual(str(messages[1]), '9 tags created for 3 systems.')
