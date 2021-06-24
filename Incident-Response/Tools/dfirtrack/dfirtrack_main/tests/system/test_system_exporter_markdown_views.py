from dateutil.parser import parse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.utils import timezone
from dfirtrack.settings import BASE_DIR
from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.models import Dnsname, Domain, Entry, Headline, Ip, Os, Reason, Recommendation, Reportitem, System, Systemstatus, Systemtype, Systemuser
import filecmp
import os
import shutil
import stat
import urllib.parse

def clean_markdown_path(markdown_path):
    """ helper function """

    # clean or create markdown directory
    if os.path.exists(markdown_path):
        # remove markdown directory (recursivly)
        shutil.rmtree(markdown_path)
        # recreate markdown directory
        os.makedirs(markdown_path)
    else:
        # create markdown directory
        os.makedirs(markdown_path)

def remove_markdown_path(markdown_path):
    """ helper function """

    # remove markdown directory
    if os.path.exists(markdown_path):
        # remove markdown directory (recursivly)
        shutil.rmtree(markdown_path)

def change_permission_markdown_path(markdown_path):
    """ helper function """

    # clean or create markdown directory
    if os.path.exists(markdown_path):
        # remove markdown directory (recursivly)
        shutil.rmtree(markdown_path)
        # recreate markdown directory
        os.makedirs(markdown_path)
        os.chmod(markdown_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    else:
        # create markdown directory
        os.makedirs(markdown_path)
        os.chmod(markdown_path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

class SystemExporterMarkdownViewTestCase(TestCase):
    """ system exporter markdown view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')

        # create object
        dnsname_1 = Dnsname.objects.create(dnsname_name = 'dnsname_1')

        # create objects
        domain_1 = Domain.objects.create(domain_name = 'domain_1')
        domain_2 = Domain.objects.create(domain_name = 'domain_2')

        # create object
        ip_1 = Ip.objects.create(ip_ip = '127.0.0.1')

        # create object
        os_1 = Os.objects.create(os_name = 'os_1')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name = 'systemstatus_1')

        # get objects
        systemstatus_compromised = Systemstatus.objects.get(systemstatus_name = '30_compromised')
        systemstatus_unknown = Systemstatus.objects.get(systemstatus_name = '10_unknown')
        systemstatus_analysis_ongoing = Systemstatus.objects.get(systemstatus_name = '20_analysis_ongoing')
        systemstatus_not_analyzed = Systemstatus.objects.get(systemstatus_name = '90_not_analyzed')
        systemstatus_clean = Systemstatus.objects.get(systemstatus_name = '40_clean')

        # update object (used with 'admonition' extension of mkdocs)
        systemstatus_clean.systemstatus_note = 'This system is clean.'
        systemstatus_clean.save()

        # create object
        reason_1 = Reason.objects.create(reason_name = 'reason_1', reason_note = 'reason_1_note')

        # create object
        recommendation_1 = Recommendation.objects.create(recommendation_name = 'recommendation_1', recommendation_note = 'recommendation_1_note')

        # create object
        systemtype_1 = Systemtype.objects.create(systemtype_name = 'systemtype_1')

        # set system_install_time
        system_install_time = parse('2020-01-02 12:34:56-00')

        # create system objects

        # standard system covering all used attributes
        system_1 = System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_compromised,
            dnsname = dnsname_1,
            domain = domain_1,
            os = os_1,
            reason = reason_1,
            recommendation = recommendation_1,
            systemtype = systemtype_1,
            system_install_time = system_install_time,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        system_1.ip.add(ip_1)
        # system with different domain
        System.objects.create(
            system_name = 'system_2',
            systemstatus = systemstatus_unknown,
            domain = domain_2,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # system without domain
        System.objects.create(
            system_name = 'system_3',
            systemstatus = systemstatus_analysis_ongoing,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # system that will not be exported
        System.objects.create(
            system_name = 'system_4',
            systemstatus = systemstatus_1,
            system_export_markdown = False,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # system with same domain (needed during creation of `mkdocs.yml`)
        System.objects.create(
            system_name = 'system_5',
            systemstatus = systemstatus_clean,
            domain = domain_2,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # system covering last special status that is used with 'admonition' extension of mkdocs
        System.objects.create(
            system_name = 'system_6',
            systemstatus = systemstatus_not_analyzed,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

        # create object
        headline_1 = Headline.objects.create(headline_name='headline_1')

        # create object
        Reportitem.objects.create(
            reportitem_note = 'lorem ipsum',
            system = system_1,
            headline = headline_1,
            reportitem_subheadline = 'subheadline_1',
            reportitem_created_by_user_id = test_user,
            reportitem_modified_by_user_id = test_user,
        )

        # create object
        Systemuser.objects.create(systemuser_name='systemuser_1', system = system_1)

        # create objects
        Entry.objects.create(
            system = system_1,
            entry_time = timezone.now(),
            entry_created_by_user_id = test_user,
            entry_modified_by_user_id = test_user,
        )
        Entry.objects.create(
            system = system_1,
            entry_date = '2020-02-03',
            entry_utc = '01:23:45',
            entry_system = 'system_1',
            entry_type = 'type_1',
            entry_content = 'lorem ipsum',
            entry_time = timezone.now(),
            entry_created_by_user_id = test_user,
            entry_modified_by_user_id = test_user,
        )

    def test_system_exporter_markdown_not_logged_in(self):
        """ test exporter view """

        # create url
        destination = '/login/?next=' + urllib.parse.quote('/system/exporter/markdown/system/', safe='')
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_markdown_logged_in(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=302, target_status_code=200)

    def test_system_exporter_markdown_redirect(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # create url
        destination = urllib.parse.quote('/system/', safe='/')
        # get response
        response = self.client.get('/system/exporter/markdown/system', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_exporter_markdown_empty_markdown_path_message(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # remove directory
        remove_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = ''
        system_exporter_markdown_config_model.save()
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), '`MARKDOWN_PATH` contains an emtpy string. Check config!')

    def test_system_exporter_markdown_non_existing_markdown_path_message(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # remove directory
        remove_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'dom'      # different sorting to cover returns in both functions
        system_exporter_markdown_config_model.save()
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), '`MARKDOWN_PATH` does not exist in file system. Check config or filesystem!')

    def test_system_exporter_markdown_non_writeable_markdown_path_message(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # change permission for directory
        change_permission_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'sys'      # different sorting to cover returns in both functions
        system_exporter_markdown_config_model.save()
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        if os.geteuid() != 0:
            self.assertEqual(str(messages[0]), '`MARKDOWN_PATH` is not writeable. Check config or filesystem!')
        else:
            pass #TODO: if we are running in docker container, we are root and the path is therefore writable. think of an alternative to check here

    def test_system_exporter_markdown_systemsorted(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # clean directory
        clean_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'sys'
        system_exporter_markdown_config_model.save()
        # get response
        self.client.get('/system/exporter/markdown/system/', follow=True)
        # compare
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test//mkdocs.yml'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_1_domain_1_20200102_123456.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_2_domain_2.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_3.md'))
        self.assertFalse(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_4.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_5_domain_2.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/system_6.md'))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/system_1_domain_1_20200102_123456.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_1.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/system_2_domain_2.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_2.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/system_3.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_3.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/system_5_domain_2.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_5.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/system_6.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_6.md'), shallow = False))

    def test_system_exporter_markdown_domainsorted(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # clean directory
        clean_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'dom'
        system_exporter_markdown_config_model.save()
        # get response
        self.client.get('/system/exporter/markdown/system/', follow=True)
        # compare
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/'))
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/domain_1/'))
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/domain_2/'))
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/other_domains/'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test//mkdocs.yml'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/domain_1/system_1_domain_1_20200102_123456.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/domain_2/system_2_domain_2.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/other_domains/system_3.md'))
        self.assertFalse(os.path.isfile('/tmp/dfirtrack_test/docs/systems/other_domains/system_4.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/domain_2/system_5_domain_2.md'))
        self.assertTrue(os.path.isfile('/tmp/dfirtrack_test/docs/systems/other_domains/system_6.md'))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/domain_1/system_1_domain_1_20200102_123456.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_1.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/domain_2/system_2_domain_2.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_2.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/other_domains/system_3.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_3.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/domain_2/system_5_domain_2.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_5.md'), shallow = False))
        self.assertTrue(filecmp.cmp('/tmp/dfirtrack_test/docs/systems/other_domains/system_6.md', os.path.join(BASE_DIR, 'dfirtrack_main/tests/system/files/system_exporter_markdown_testfile_system_6.md'), shallow = False))

    def test_system_exporter_markdown_clean_directory(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # clean directory (this time it is simulated that an instance previously existed)
        clean_markdown_path('/tmp/dfirtrack_test/docs/systems')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.save()
        # get response
        self.client.get('/system/exporter/markdown/system/', follow=True)
        # compare
        self.assertTrue(os.path.exists('/tmp/dfirtrack_test/docs/systems/'))

    def test_system_exporter_markdown_systemsorted_messages(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # clean directory
        clean_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'sys'
        system_exporter_markdown_config_model.save()
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'System exporter markdown (sorted by system) started')
        self.assertEqual(str(messages[1]), 'System exporter markdown (sorted by system) finished')

    def test_system_exporter_markdown_domainsorted_messages(self):
        """ test exporter view """

        # login testuser
        self.client.login(username='testuser_system_exporter_markdown', password='2anJuuSjzjLmb2pOYuLf')
        # clean directory
        clean_markdown_path('/tmp/dfirtrack_test')
        # change config
        system_exporter_markdown_config_model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        system_exporter_markdown_config_model.markdown_path = '/tmp/dfirtrack_test'
        system_exporter_markdown_config_model.markdown_sorting = 'dom'
        system_exporter_markdown_config_model.save()
        # get response
        response = self.client.get('/system/exporter/markdown/system/', follow=True)
        # get messages
        messages = list(get_messages(response.wsgi_request))
        # compare
        self.assertEqual(str(messages[0]), 'System exporter markdown (sorted by domain) started')
        self.assertEqual(str(messages[1]), 'System exporter markdown (sorted by domain) finished')
