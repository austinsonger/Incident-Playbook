from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Case
import urllib.parse

class CaseAPIViewTestCase(TestCase):
    """ case API view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')

        # create object
        Case.objects.create(
            case_name='case_api_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )

    def test_case_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/case/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_case_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # get response
        response = self.client.get('/api/case/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_case_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # get user
        test_user_id = str(User.objects.get(username='testuser_case_api').id)
        # create POST string
        poststring = {
            "case_name": "case_api_2",
            "case_is_incident": True,
            "case_created_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/case/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_case_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # create url
        destination = urllib.parse.quote('/api/case/', safe='/')
        # get response
        response = self.client.get('/api/case', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_case_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        case_api_1 = Case.objects.get(case_name='case_api_1')
        # get response
        response = self.client.get('/api/case/' + str(case_api_1.case_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_case_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        case_api_1 = Case.objects.get(case_name='case_api_1')
        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # get response
        response = self.client.get('/api/case/' + str(case_api_1.case_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_case_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        case_api_1 = Case.objects.get(case_name='case_api_1')
        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # get response
        response = self.client.delete('/api/case/' + str(case_api_1.case_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_case_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        case_api_1 = Case.objects.get(case_name='case_api_1')
        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # get user
        test_user_id = str(User.objects.get(username='testuser_case_api').id)
        # create url
        destination = urllib.parse.quote('/api/case/' + str(case_api_1.case_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "case_name": "case_api_3",
            "case_is_incident": False,
            "case_created_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_case_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        case_api_1 = Case.objects.get(case_name='case_api_1')
        # login testuser
        self.client.login(username='testuser_case_api', password='nkeZDU2qGKXWR49sAVf5')
        # create url
        destination = urllib.parse.quote('/api/case/' + str(case_api_1.case_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/case/' + str(case_api_1.case_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
