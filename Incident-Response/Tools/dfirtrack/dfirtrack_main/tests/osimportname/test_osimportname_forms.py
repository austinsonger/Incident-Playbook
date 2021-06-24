from django.test import TestCase
from dfirtrack_main.forms import OsimportnameForm
from dfirtrack_main.models import Os

class OsimportnameFormTestCase(TestCase):
    """ osimportname form tests """

    @classmethod
    def setUpTestData(cls):

        # create object
        Os.objects.create(os_name='os_1')

    def test_osimportname_name_form_label(self):
        """ test form label """

        # get object
        form = OsimportnameForm()
        # compare
        self.assertEqual(form.fields['osimportname_name'].label, 'Importname (*)')

    def test_osimportname_os_form_label(self):
        """ test form label """

        # get object
        form = OsimportnameForm()
        # compare
        self.assertEqual(form.fields['os'].label, 'Operating system (*)')

    def test_osimportname_importer_form_label(self):
        """ test form label """

        # get object
        form = OsimportnameForm()
        # compare
        self.assertEqual(form.fields['osimportname_importer'].label, 'Importer (*)')

    def test_osimportname_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = OsimportnameForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_osimportname_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = OsimportnameForm(data = {'osimportname_name': 'osimportname_1'})
        # compare
        self.assertFalse(form.is_valid())

    def test_osimportname_importer_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'osimportname_1',
            'osimportname_importer': 'osimportname_importer_1',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_osimportname_os_form_filled(self):
        """ test minimum form requirements / VALID """

        # get foreign key object id
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'osimportname_1',
            'osimportname_importer': 'osimportname_importer_1',
            'os': os_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_osimportname_name_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'oooooooooooooooooooooooooooooo',
            'osimportname_importer': 'osimportname_importer_1',
            'os': os_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_osimportname_name_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'ooooooooooooooooooooooooooooooo',
            'osimportname_importer': 'osimportname_importer_1',
            'os': os_id
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_osimportname_importer_proper_chars(self):
        """ test for max length """

        # get foreign key object id
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'osimportname_1',
            'osimportname_importer': 'oooooooooooooooooooooooooooooo',
            'os': os_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_osimportname_importer_too_many_chars(self):
        """ test for max length """

        # get foreign key object id
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = OsimportnameForm(data = {
            'osimportname_name': 'osimportname_1',
            'osimportname_importer': 'ooooooooooooooooooooooooooooooo',
            'os': os_id,
        })
        # compare
        self.assertFalse(form.is_valid())
