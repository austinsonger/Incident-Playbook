from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.models import Recommendation
import urllib.parse

class RecommendationAPIViewTestCase(TestCase):
    """ recommendation API view tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Recommendation.objects.create(recommendation_name='recommendation_api_1')
        # create user
        User.objects.create_user(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')

    def test_recommendation_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/recommendation/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_recommendation_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/recommendation/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_recommendation_list_api_method_post(self):
        """ POST is allowed """

        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create POST string
        poststring = {"recommendation_name": "recommendation_api_2"}
        # get response
        response = self.client.post('/api/recommendation/', data=poststring)
        # compare
        self.assertEqual(response.status_code, 201)

    def test_recommendation_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/recommendation/', safe='/')
        # get response
        response = self.client.get('/api/recommendation', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_recommendation_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        recommendation_api_1 = Recommendation.objects.get(recommendation_name='recommendation_api_1')
        # get response
        response = self.client.get('/api/recommendation/' + str(recommendation_api_1.recommendation_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_recommendation_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        recommendation_api_1 = Recommendation.objects.get(recommendation_name='recommendation_api_1')
        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.get('/api/recommendation/' + str(recommendation_api_1.recommendation_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_recommendation_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        recommendation_api_1 = Recommendation.objects.get(recommendation_name='recommendation_api_1')
        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # get response
        response = self.client.delete('/api/recommendation/' + str(recommendation_api_1.recommendation_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_recommendation_detail_api_method_put(self):
        """ PUT is allowed """

        # get object
        recommendation_api_1 = Recommendation.objects.get(recommendation_name='recommendation_api_1')
        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/recommendation/' + str(recommendation_api_1.recommendation_id) + '/', safe='/')
        # create PUT string
        putstring = {"recommendation_name": "new_recommendation_api_1"}
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_recommendation_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        recommendation_api_1 = Recommendation.objects.get(recommendation_name='recommendation_api_1')
        # login testuser
        self.client.login(username='testuser_recommendation_api', password='tvjnIPBlhP9P3ixDHVE7')
        # create url
        destination = urllib.parse.quote('/api/recommendation/' + str(recommendation_api_1.recommendation_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/recommendation/' + str(recommendation_api_1.recommendation_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
