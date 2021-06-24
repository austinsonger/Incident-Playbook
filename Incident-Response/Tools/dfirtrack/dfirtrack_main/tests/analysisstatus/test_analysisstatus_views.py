from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Analysisstatus
import urllib.parse

class AnalysisstatusViewTestCase(TestCase):
    """ analysisstatus view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        # create user
        User.objects.create_user(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')

    def test_analysisstatus_list_not_logged_in(self):
        """ test list view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analysisstatus/', safe='')
        # get response
        response = self.client.get('/analysisstatus/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analysisstatus_list_logged_in(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analysisstatus_list_template(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analysisstatus/analysisstatus_list.html')

    def test_analysisstatus_list_get_user_context(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analysisstatus')

    def test_analysisstatus_list_redirect(self):
        """ test list view """

        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # create url
        destination = urllib.parse.quote('/analysisstatus/', safe='/')
        # get response
        response = self.client.get('/analysisstatus', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_analysisstatus_detail_not_logged_in(self):
        """ test detail view """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # create url
        destination = '/login/?next=' + urllib.parse.quote('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/', safe='')
        # get response
        response = self.client.get('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_analysisstatus_detail_logged_in(self):
        """ test detail view """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_analysisstatus_detail_template(self):
        """ test detail view """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_main/analysisstatus/analysisstatus_detail.html')

    def test_analysisstatus_detail_get_user_context(self):
        """ test detail view """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # get response
        response = self.client.get('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_analysisstatus')

    def test_analysisstatus_detail_redirect(self):
        """ test detail view """

        # get object
        analysisstatus_1 = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1')
        # login testuser
        self.client.login(username='testuser_analysisstatus', password='9u2Ew4XdFHLcCG5xyTvR')
        # create url
        destination = urllib.parse.quote('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id) + '/', safe='/')
        # get response
        response = self.client.get('/analysisstatus/' + str(analysisstatus_1.analysisstatus_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
