from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, Systemstatus
import urllib.parse

class SystemImporterFileCsvConfigViewTestCase(TestCase):
    """ system importer file CSV config view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        User.objects.create_user(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')

        # create objects
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        Systemstatus.objects.create(systemstatus_name='systemstatus_1')

    def test_system_importer_file_csv_config_not_logged_in(self):
        """ test importer view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/config/system/importer/file/csv/', safe='')
        # get response
        response = self.client.get('/config/system/importer/file/csv/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_importer_file_csv_config_logged_in(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get response
        response = self.client.get('/config/system/importer/file/csv/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_importer_file_csv_config_template(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get response
        response = self.client.get('/config/system/importer/file/csv/')
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/system/system_importer_file_csv_config_popup.html')

    def test_system_importer_file_csv_config_get_user_context(self):
        """ test importer view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get response
        response = self.client.get('/config/system/importer/file/csv/')
        # compare
        self.assertEqual(str(response.context['user']), 'testuser_system_importer_file_csv_config')

    def test_system_importer_file_csv_config_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # create url
        destination = urllib.parse.quote('/config/system/importer/file/csv/', safe='/')
        # get response
        response = self.client.get('/config/system/importer/file/csv', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_importer_file_csv_config_post_message_valid(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_system_importer_file_csv_exists.csv'
        csv_path = f'{csv_import_path}/{csv_import_filename}'
        # create file
        csv_file = open(csv_path, 'w')
        # write content to file
        csv_file.write('This is no valid CSV file but that does not matter at the moment.')
        # close file
        csv_file.close()
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, 'System importer file CSV config changed')
        self.assertEqual(messages[0].level_tag, 'success')

    def test_system_importer_file_csv_config_post_message_file_not_exists(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_system_importer_file_csv_not_exists.csv'
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, 'System importer file CSV config changed')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, 'CSV import file does not exist at the moment. Make sure the file is available during import.')
        self.assertEqual(messages[1].level_tag, 'warning')

    def test_system_importer_file_csv_config_post_message_file_empty(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_system_importer_file_csv_empty.csv'
        csv_path = f'{csv_import_path}/{csv_import_filename}'
        # create file
        csv_file = open(csv_path, 'w')
        # close file
        csv_file.close()
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, 'System importer file CSV config changed')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, 'CSV import file is empty. Make sure the file contains systems during import.')
        self.assertEqual(messages[1].level_tag, 'warning')

    def test_system_importer_file_csv_config_post_message_update_existing_systems(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get timestamp string
        t1 = timezone.now().strftime('%Y%m%d_%H%M%S')
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = f'{t1}_system_importer_file_csv_update_existing_systems.csv'
        csv_path = f'{csv_import_path}/{csv_import_filename}'
        # create file
        csv_file = open(csv_path, 'w')
        # write content to file
        csv_file.write('This is no valid CSV file but that does not matter at the moment.')
        # close file
        csv_file.close()
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': False,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(messages[0].message, 'System importer file CSV config changed')
        self.assertEqual(messages[0].level_tag, 'success')
        self.assertEqual(messages[1].message, 'WARNING: Existing systems will be updated!')
        self.assertEqual(messages[1].level_tag, 'warning')

    def test_system_importer_file_csv_config_post_redirect(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = 'systems.csv'
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_importer_file_csv_config_post_invalid_reload(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = 'systems.csv'
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_column_ip': 1,
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_importer_file_csv_config_post_invalid_template(self):
        """ test view """

        # login testuser
        self.client.login(username='testuser_system_importer_file_csv_config', password='EZE14dpUK4CZey02x6U6')
        # get user
        testuser_id = User.objects.get(username='testuser_system_importer_file_csv_config').id
        # get objects
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # build csv file path
        csv_import_path = '/tmp'
        csv_import_filename = 'systems.csv'
        # create post data
        data_dict = {
            'csv_column_system': 1,
            'csv_skip_existing_system': True,
            'csv_import_path': csv_import_path,
            'csv_import_filename': csv_import_filename,
            'csv_import_username': testuser_id,
            'csv_default_systemstatus': systemstatus_id,
            'csv_default_analysisstatus': analysisstatus_id,
            'csv_default_tagfree_systemstatus': systemstatus_id,
            'csv_default_tagfree_analysisstatus': analysisstatus_id,
            'csv_tag_lock_systemstatus': 'LOCK_SYSTEMSTATUS',
            'csv_tag_lock_analysisstatus': 'LOCK_ANALYSISSTATUS',
            'csv_remove_tag': 'tag_remove_prefix',
            'csv_field_delimiter': 'field_comma',
            'csv_text_quote': 'text_double_quotation_marks',
            'csv_ip_delimiter': 'ip_semicolon',
            'csv_tag_delimiter': 'tag_space',
            'csv_column_ip': 1,
        }
        # get response
        response = self.client.post('/config/system/importer/file/csv/', data_dict)
        # compare
        self.assertTemplateUsed(response, 'dfirtrack_config/system/system_importer_file_csv_config_popup.html')
