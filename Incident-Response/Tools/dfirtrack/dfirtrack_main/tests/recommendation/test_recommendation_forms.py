from django.test import TestCase
from dfirtrack_main.forms import RecommendationForm

class RecommendationFormTestCase(TestCase):
    """ recommendation form tests """

    def test_recommendation_name_form_label(self):
        """ test form label """

        # get object
        form = RecommendationForm()
        # compare
        self.assertEqual(form.fields['recommendation_name'].label, 'Recommendation name (*)')

    def test_recommendation_note_form_label(self):
        """ test form label """

        # get object
        form = RecommendationForm()
        # compare
        self.assertEqual(form.fields['recommendation_note'].label, 'Recommendation note')

    def test_recommendation_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = RecommendationForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_recommendation_name_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        form = RecommendationForm(data = {'recommendation_name': 'recommendation_1'})
        # compare
        self.assertTrue(form.is_valid())

    def test_recommendation_note_form_filled(self):
        """ test additional form content """

        # get object
        form = RecommendationForm(data = {
            'recommendation_name': 'recommendation_1',
            'recommendation_note': 'lorem ipsum',
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_recommendation_name_proper_chars(self):
        """ test for max length """

        # get object
        form = RecommendationForm(data = {'recommendation_name': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'})
        # compare
        self.assertTrue(form.is_valid())

    def test_recommendation_name_too_many_chars(self):
        """ test for max length """

        # get object
        form = RecommendationForm(data = {'recommendation_name': 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'})
        # compare
        self.assertFalse(form.is_valid())
