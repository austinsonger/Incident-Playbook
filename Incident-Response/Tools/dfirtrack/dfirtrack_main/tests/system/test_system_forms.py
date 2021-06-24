from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.forms import SystemForm, SystemNameForm
from dfirtrack_main.models import Analysisstatus, Case, Company, Contact, Dnsname, Domain, Location, Os, Osarch, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor

class SystemFormTestCase(TestCase):
    """ system form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system', password='zU7LnCr4vW9C8HwQ9gGl')

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')

        # create object
        Reason.objects.create(reason_name='reason_1')

        # create object
        Recommendation.objects.create(recommendation_name='recommendation_1')

        # create object
        Systemtype.objects.create(systemtype_name='systemtype_1')

        # create object
        Domain.objects.create(domain_name='domain_1')

        # create object
        Dnsname.objects.create(dnsname_name='dnsname_1')

        # create object
        Os.objects.create(os_name='os_1')

        # create object
        Osarch.objects.create(osarch_name='osarch_1')

        # create object
        Company.objects.create(company_name='company_1')
        Company.objects.create(company_name='company_2')

        # create object
        Location.objects.create(location_name='location_1')

        # create object
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')

        # create object
        Contact.objects.create(
            contact_name='contact_1',
            contact_email='contact_1@example.com',
        )

        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')

        # create object
        Tag.objects.create(
            tag_name = 'tag_1',
            tagcolor = tagcolor_1,
        )
        Tag.objects.create(
            tag_name = 'tag_2',
            tagcolor = tagcolor_1,
        )

        # create object
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )
        Case.objects.create(
            case_name = 'case_2',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )

        # create object
        System.objects.create(
            system_name = 'system_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )


    def test_system_name_form_label(self):
        """ test form label """

        # get object
        form = SystemNameForm()
        # compare
        self.assertEqual(form.fields['system_name'].label, 'System name')

    def test_system_systemstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['systemstatus'].label, 'Systemstatus')

    def test_system_analysisstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['analysisstatus'].label, 'Analysisstatus')

    def test_system_reason_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['reason'].label, 'Reason')

    def test_system_recommendation_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['recommendation'].label, 'Recommendation')

    def test_system_systemtype_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['systemtype'].label, 'Systemtype')

    def test_system_domain_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['domain'].label, 'Domain')

    def test_system_dnsname_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['dnsname'].label, 'Dnsname')

    def test_system_os_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['os'].label, 'Os')

    def test_system_osarch_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['osarch'].label, 'Osarch')

    def test_system_install_time_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['system_install_time'].label, 'System install time')

    def test_system_lastbooted_time_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['system_lastbooted_time'].label, 'System lastbooted time')

    def test_system_deprecated_time_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['system_deprecated_time'].label, 'System deprecated time')

    def test_system_is_vm_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['system_is_vm'].label, 'System is vm')

    def test_system_host_system_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['host_system'].label, 'Host system')

    def test_system_company_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['company'].label, 'Company')

    def test_system_location_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['location'].label, 'Location')

    def test_system_serviceprovider_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['serviceprovider'].label, 'Serviceprovider')

    def test_system_contact_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['contact'].label, 'Contact')

    def test_system_tag_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['tag'].label, 'Tag')

    def test_system_case_form_label(self):
        """ test form label """

        # get object
        form = SystemForm()
        # compare
        self.assertEqual(form.fields['case'].label, 'Case')

    def test_system_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_system_name_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_systemstatus_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_analysisstatus_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'analysisstatus': analysisstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_reason_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        reason_id = Reason.objects.get(reason_name='reason_1').reason_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'reason': reason_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_recommendation_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        recommendation_id = Recommendation.objects.get(recommendation_name='recommendation_1').recommendation_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'recommendation': recommendation_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_systemtype_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        systemtype_id = Systemtype.objects.get(systemtype_name='systemtype_1').systemtype_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'systemtype': systemtype_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_domain_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'domain': domain_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_dnsname_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        dnsname_id = Dnsname.objects.get(dnsname_name='dnsname_1').dnsname_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'dnsname': dnsname_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_os_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'os': os_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_osarch_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        osarch_id = Osarch.objects.get(osarch_name='osarch_1').osarch_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'osarch': osarch_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_install_time_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_install_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_lastbooted_time_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_lastbooted_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_deprecated_time_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_deprecated_time': timezone.now(),
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_is_vm_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_is_vm': True,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_host_system_form_filled(self):
        """ test additional form content """

        # get object
        system_id = System.objects.get(system_name='system_1').system_id
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_2',
            'systemstatus': systemstatus_id,
            'host_system': system_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_company_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        company_1_id = Company.objects.get(company_name='company_1').company_id
        company_2_id = Company.objects.get(company_name='company_2').company_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'company': [company_1_id, company_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_location_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        location_id = Location.objects.get(location_name='location_1').location_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'location': location_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_serviceprovider_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'serviceprovider': serviceprovider_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_contact_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'contact': contact_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_tag_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        tag_1_id = Tag.objects.get(tag_name='tag_1').tag_id
        tag_2_id = Tag.objects.get(tag_name='tag_2').tag_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'tag': [tag_1_id, tag_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_case_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        case_1_id = Case.objects.get(case_name='case_1').case_id
        case_2_id = Case.objects.get(case_name='case_2').case_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'case': [case_1_id, case_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_name_proper_chars(self):
        """ test for max length """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'systemstatus': systemstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_name_too_many_chars(self):
        """ test for max length """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemNameForm(data = {
            'system_name': 'nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'systemstatus': systemstatus_id,
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_install_time_formatcheck(self):
        """ test input format """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_install_time': 'wrong format',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_lastbooted_time_formatcheck(self):
        """ test input format """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_lastbooted_time': 'wrong format',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_deprecated_time_formatcheck(self):
        """ test input format """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemForm(data = {
            'system_name': 'system_1',
            'systemstatus': systemstatus_id,
            'system_deprecated_time': 'wrong format',
        })
        # compare
        self.assertFalse(form.is_valid())
