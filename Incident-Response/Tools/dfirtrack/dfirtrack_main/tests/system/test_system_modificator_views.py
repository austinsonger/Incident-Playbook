from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, Company, System, Systemstatus, Tag, Tagcolor
import urllib.parse

class SystemModificatorViewTestCase(TestCase):
    """ system modificator view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')

        # create objects
        analysisstatus_1 = Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_1')
        Analysisstatus.objects.create(analysisstatus_name = 'analysisstatus_2')
        Company.objects.create(
            company_name = 'company_1',
        )
        Company.objects.create(
            company_name = 'company_2',
        )
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')
        Systemstatus.objects.create(systemstatus_name = 'systemstatus_2')
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name = 'tagcolor_1')
        Tag.objects.create(
            tag_name = 'tag_1',
            tagcolor = tagcolor_1,
        )
        Tag.objects.create(
            tag_name = 'tag_2',
            tagcolor = tagcolor_1,
        )
        System.objects.create(
            system_name = 'system_modificator_system_1',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_system_2',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_system_3',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_redirect',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_char_field_1',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_char_field_2',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_messages_1',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_messages_2',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_double',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        System.objects.create(
            system_name = 'system_modificator_double',
            analysisstatus = analysisstatus_1,
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_modificator_not_logged_in(self):
        """ test modificator view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/modificator/', safe='')
        # get response
        response = self.client.get('/system/modificator/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_modificator_logged_in(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get response
        response = self.client.get('/system/modificator/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_modificator_template(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get response
        response = self.client.get('/system/modificator/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/system/system_modificator.html')

    def test_system_modificator_get_user_context(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get response
        response = self.client.get('/system/modificator/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_modificator')

    def test_system_modificator_redirect(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # create url
        destination = urllib.parse.quote('/system/modificator/', safe='/')
        # get response
        response = self.client.get('/system/modificator', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_modificator_post_redirect(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get objects
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_2')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_modificator_redirect',
            'analysisstatus': analysisstatus_2.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # create url
        destination = '/system/'
        # get response
        response = self.client.post('/system/modificator/', data_dict)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_modificator_post_systems(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get objects
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_2')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        company_1 = Company.objects.get(company_name = 'company_1')
        company_2 = Company.objects.get(company_name = 'company_2')
        tag_1 = Tag.objects.get(tag_name = 'tag_1')
        tag_2 = Tag.objects.get(tag_name = 'tag_2')
        # create post data
        data_dict = {
            'systemlist': 'system_modificator_system_1\nsystem_modificator_system_2',
            'analysisstatus': analysisstatus_2.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
            'company': [str(company_1.company_id), str(company_2.company_id)],
            'tag': [str(tag_1.tag_id), str(tag_2.tag_id)],
        }
        # get response
        self.client.post('/system/modificator/', data_dict)
        # compare
        self.assertEqual(System.objects.get(system_name='system_modificator_system_1').analysisstatus.analysisstatus_name, 'analysisstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_system_2').analysisstatus.analysisstatus_name, 'analysisstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_system_3').analysisstatus.analysisstatus_name, 'analysisstatus_1')
        self.assertEqual(System.objects.get(system_name='system_modificator_system_1').systemstatus.systemstatus_name, 'systemstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_system_2').systemstatus.systemstatus_name, 'systemstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_system_3').systemstatus.systemstatus_name, 'systemstatus_1')
        self.assertTrue(System.objects.get(system_name='system_modificator_system_1').company.filter(company_name='company_1').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_1').company.filter(company_name='company_2').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_2').company.filter(company_name='company_1').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_2').company.filter(company_name='company_2').exists())
        self.assertFalse(System.objects.get(system_name='system_modificator_system_3').company.filter(company_name='company_1').exists())
        self.assertFalse(System.objects.get(system_name='system_modificator_system_3').company.filter(company_name='company_2').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_1').tag.filter(tag_name='tag_1').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_1').tag.filter(tag_name='tag_2').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_2').tag.filter(tag_name='tag_1').exists())
        self.assertTrue(System.objects.get(system_name='system_modificator_system_2').tag.filter(tag_name='tag_2').exists())
        self.assertFalse(System.objects.get(system_name='system_modificator_system_3').tag.filter(tag_name='tag_1').exists())
        self.assertFalse(System.objects.get(system_name='system_modificator_system_3').tag.filter(tag_name='tag_2').exists())

    def test_system_modificator_post_char_field(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get objects
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_2')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        system_modificator_char_field_1 = System.objects.get(system_name = 'system_modificator_char_field_1')
        system_modificator_char_field_2 = System.objects.get(system_name = 'system_modificator_char_field_2')
        # create system list and append system IDs
        systemlist = []
        systemlist.append(str(system_modificator_char_field_1.system_id))
        systemlist.append(str(system_modificator_char_field_2.system_id))
        # create post data
        data_dict = {
            'systemlist': systemlist,
            'analysisstatus': analysisstatus_2.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        self.client.post('/system/modificator/', data_dict)
        # compare
        self.assertEqual(System.objects.get(system_name='system_modificator_char_field_1').analysisstatus.analysisstatus_name, 'analysisstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_char_field_2').analysisstatus.analysisstatus_name, 'analysisstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_char_field_1').systemstatus.systemstatus_name, 'systemstatus_2')
        self.assertEqual(System.objects.get(system_name='system_modificator_char_field_2').systemstatus.systemstatus_name, 'systemstatus_2')

    def test_system_modificator_post_messages(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get objects
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_2')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_modificator_messages_1\n\nsystem_modificator_double',
            'analysisstatus': analysisstatus_2.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        response = self.client.post('/system/modificator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'System modificator started')
        self.assertEqual(str(messages[1]), '1 system was created / modified.')
        self.assertEqual(str(messages[2]), "1 system was skipped. ['system_modificator_double']")
        self.assertEqual(str(messages[3]), '1 line out of 3 lines was faulty (see log file for details).')

    def test_system_modificator_post_other_messages(self):
        """ test modificator view """

        # login testuser
        self.client.login(username='testuser_system_modificator', password='QDX5Xp9yhnejSIuYaE1G')
        # get objects
        analysisstatus_2 = Analysisstatus.objects.get(analysisstatus_name = 'analysisstatus_2')
        systemstatus_2 = Systemstatus.objects.get(systemstatus_name = 'systemstatus_2')
        # create post data
        data_dict = {
            'systemlist': 'system_modificator_messages_1\n\nsystem_modificator_not_existent\nsystem_modificator_double\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nsystem_modificator_messages_2',
            'analysisstatus': analysisstatus_2.analysisstatus_id,
            'systemstatus': systemstatus_2.systemstatus_id,
        }
        # get response
        response = self.client.post('/system/modificator/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[1]), '2 systems were created / modified.')
        self.assertEqual(str(messages[2]), "2 systems were skipped. ['system_modificator_not_existent', 'system_modificator_double']")
        self.assertEqual(str(messages[3]), '2 lines out of 6 lines were faulty (see log file for details).')
