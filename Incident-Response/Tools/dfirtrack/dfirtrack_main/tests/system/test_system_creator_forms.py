from django.contrib.auth.models import User
from django.test import TestCase
from dfirtrack_main.forms import SystemCreatorForm
from dfirtrack_main.models import Analysisstatus, Case, Company, Contact, Dnsname, Domain, Location, Os, Osarch, Reason, Serviceprovider, Systemstatus, Systemtype, Tag, Tagcolor

class SystemCreatorFormTestCase(TestCase):
    """ system creator form tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_creator', password='HN9KSZUyIx5sWgrX9rIx')

        # create object
        Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create object
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')

        # create object
        Reason.objects.create(reason_name='reason_1')

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


    def test_system_creator_systemlist_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['systemlist'].label, 'System list')

    def test_system_creator_systemstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['systemstatus'].label, 'Systemstatus')

    def test_system_creator_analysisstatus_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['analysisstatus'].label, 'Analysisstatus')

    def test_system_creator_reason_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['reason'].label, 'Reason')

    def test_system_creator_systemtype_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['systemtype'].label, 'Systemtype')

    def test_system_creator_domain_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['domain'].label, 'Domain')

    def test_system_creator_dnsname_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['dnsname'].label, 'Dnsname')

    def test_system_creator_os_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['os'].label, 'Os')

    def test_system_creator_osarch_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['osarch'].label, 'Osarch')

    def test_system_creator_company_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['company'].label, 'Company')

    def test_system_creator_location_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['location'].label, 'Location')

    def test_system_creator_serviceprovider_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['serviceprovider'].label, 'Serviceprovider')

    def test_system_creator_contact_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['contact'].label, 'Contact')

    def test_system_creator_tag_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['tag'].label, 'Tag')

    def test_system_creator_case_form_label(self):
        """ test form label """

        # get object
        form = SystemCreatorForm()
        # compare
        self.assertEqual(form.fields['case'].label, 'Case')

    def test_system_creator_form_empty(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemCreatorForm(data = {})
        # compare
        self.assertFalse(form.is_valid())

    def test_system_creator_systemlist_form_filled(self):
        """ test minimum form requirements / INVALID """

        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
        })
        # compare
        self.assertFalse(form.is_valid())

    def test_system_creator_systemstatus_form_filled(self):
        """ test minimum form requirements / VALID """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_analysisstatus_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'analysisstatus': analysisstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_reason_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        reason_id = Reason.objects.get(reason_name='reason_1').reason_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'reason': reason_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_systemtype_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        systemtype_id = Systemtype.objects.get(systemtype_name='systemtype_1').systemtype_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'systemtype': systemtype_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_domain_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'domain': domain_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_dnsname_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        dnsname_id = Dnsname.objects.get(dnsname_name='dnsname_1').dnsname_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'dnsname': dnsname_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_os_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'os': os_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_osarch_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        osarch_id = Osarch.objects.get(osarch_name='osarch_1').osarch_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'osarch': osarch_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_company_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        company_1_id = Company.objects.get(company_name='company_1').company_id
        company_2_id = Company.objects.get(company_name='company_2').company_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'company': [company_1_id, company_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_location_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        location_id = Location.objects.get(location_name='location_1').location_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'location': location_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_serviceprovider_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'serviceprovider': serviceprovider_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_contact_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'contact': contact_id,
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_tag_form_filled(self):
        """ test additional form content """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        tag_1_id = Tag.objects.get(tag_name='tag_1').tag_id
        tag_2_id = Tag.objects.get(tag_name='tag_2').tag_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
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
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1',
            'systemstatus': systemstatus_id,
            'case': [case_1_id, case_2_id],
        })
        # compare
        self.assertTrue(form.is_valid())

    def test_system_creator_systemlist_multi_line(self):
        """ test for multiple line input """

        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        form = SystemCreatorForm(data = {
            'systemlist': 'system_1\nsystem_2\nsystem_3',
            'systemstatus': systemstatus_id,
        })
        # compare
        self.assertTrue(form.is_valid())
