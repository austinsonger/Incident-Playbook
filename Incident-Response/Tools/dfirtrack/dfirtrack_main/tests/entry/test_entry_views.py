from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Entry, System, Systemstatus
import urllib.parse

class EntryViewTestCase(TestCase):
    """ entry view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        system_1 = System.objects.create(
            system_name='system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        Entry.objects.create(
            system = system_1,
            entry_time = timezone.now(),
            entry_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
            entry_created_by_user_id = test_user,
            entry_modified_by_user_id = test_user,
        )

    def test_entry_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/entry/', safe='')
        # get response
        response = self.client.get('/entry/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_list.html')

    def test_entry_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_entry')

    def test_entry_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create url
        destination = urllib.parse.quote('/entry/', safe='/')
        # get response
        response = self.client.get('/entry', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_entry_detail_not_logged_in(self):
        """ test detail view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/entry/' + str(entry_1.entry_id) + '/', safe='')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_detail_logged_in(self):
        """ test detail view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_detail_template(self):
        """ test detail view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_detail.html')

    def test_entry_detail_get_user_context(self):
        """ test detail view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_entry')

    def test_entry_detail_redirect(self):
        """ test detail view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create url
        destination = urllib.parse.quote('/entry/' + str(entry_1.entry_id) + '/', safe='/')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_entry_add_not_logged_in(self):
        """ test add view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/entry/add/', safe='')
        # get response
        response = self.client.get('/entry/add/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_add_logged_in(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/add/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_add_system_selected(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get object
        system_id = System.objects.get(system_name = 'system_1').system_id
        # get response
        response = self.client.get('/entry/add/?system=' + str(system_id))
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_add_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/add/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_add.html')

    def test_entry_add_get_user_context(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/add/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_entry')

    def test_entry_add_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create url
        destination = urllib.parse.quote('/entry/add/', safe='/')
        # get response
        response = self.client.get('/entry/add', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_entry_add_post_redirect(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get user
        test_user_id = User.objects.get(username = 'testuser_entry').id
        # get object
        system_id = System.objects.get(system_name = 'system_1').system_id
        # create post data
        data_dict = {
            'system': system_id,
            'entry_time': '2013-12-11 23:45:01',
            'entry_sha1': '988881adc9fc3655077dc2d4d757d480b5ea0e11',
            'entry_created_by_user_id': test_user_id,
            'entry_modified_by_user_id': test_user_id,
        }
        # get response
        response = self.client.post('/entry/add/', data_dict)
        # create url
        destination = urllib.parse.quote('/system/' + str(system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_add_post_invalid_reload(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/entry/add/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_add_post_invalid_template(self):
        """ test add view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/entry/add/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_add.html')


    def test_entry_edit_not_logged_in(self):
        """ test edit view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/entry/' + str(entry_1.entry_id) + '/edit/', safe='')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/edit/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_edit_logged_in(self):
        """ test edit view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/edit/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_edit_template(self):
        """ test edit view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/edit/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_edit.html')

    def test_entry_edit_get_user_context(self):
        """ test edit view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/edit/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_entry')

    def test_entry_edit_redirect(self):
        """ test edit view """

        # get object
        entry_1 = Entry.objects.get(entry_sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709')
        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # create url
        destination = urllib.parse.quote('/entry/' + str(entry_1.entry_id) + '/edit/', safe='/')
        # get response
        response = self.client.get('/entry/' + str(entry_1.entry_id) + '/edit', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_entry_edit_post_redirect(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get user
        test_user = User.objects.get(username = 'testuser_entry')
        # get object
        system_1 = System.objects.get(system_name = 'system_1')
        # create object
        entry_1 = Entry.objects.create(
            system = system_1,
            entry_time = timezone.now(),
            entry_sha1 = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            entry_created_by_user_id = test_user,
            entry_modified_by_user_id = test_user,
        )
        # create post data
        data_dict = {
            'system': system_1.system_id,
            'entry_time': '2013-12-11 23:45:01',
            'entry_sha1': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
            'entry_modified_by_user_id': test_user.id,
        }
        # get response
        response = self.client.post('/entry/' + str(entry_1.entry_id) + '/edit/', data_dict)
        # create url
        destination = urllib.parse.quote('/system/' + str(system_1.system_id) + '/', safe='/')
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_entry_edit_post_invalid_reload(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get object
        entry_id = Entry.objects.get(entry_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709').entry_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/entry/' + str(entry_id) + '/edit/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_entry_edit_post_invalid_template(self):
        """ test edit view """

        # login testuser
        self.client.login(username='testuser_entry', password='GBabI7lbSGB13jXjCRoL')
        # get object
        entry_id = Entry.objects.get(entry_sha1 = 'da39a3ee5e6b4b0d3255bfef95601890afd80709').entry_id
        # create post data
        data_dict = {}
        # get response
        response = self.client.post('/entry/' + str(entry_id) + '/edit/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/entry/entry_edit.html')
