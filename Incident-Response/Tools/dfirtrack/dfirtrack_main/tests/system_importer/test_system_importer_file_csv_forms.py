from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from dfirtrack_main.importer.file.csv_importer_forms import SystemImporterFileCsvForm


class SystemImporterFileCsvFormTestCase(TestCase):
    """ system importer file CSV form tests """

    def test_system_importer_file_csv_systemcsv_form_label(self):
        """ test form label """

        # get object
        form = SystemImporterFileCsvForm()
        # compare
        self.assertEqual(form.fields['systemcsv'].label, 'CSV with systems (*)')

    def test_system_importer_file_csv_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemImporterFileCsvForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_system_importer_file_csv_systemcsv_form_filled(self):
        """ test minimum form requirements / VALID """

        # get file
        upload_csv = open('dfirtrack_main/tests/system_importer/system_importer_file_csv_files/system_importer_file_csv_testfile_01_minimal_double_quotation.csv', 'rb')
        # create dictionaries
        data_dict = {}
        file_dict = {
            'systemcsv': SimpleUploadedFile(upload_csv.name, upload_csv.read()),
        }
        # get object
        form = SystemImporterFileCsvForm(
            data = data_dict,
            files = file_dict,
        )
        # close file
        upload_csv.close()
        # compare
        self.assertTrue(form.is_valid())
