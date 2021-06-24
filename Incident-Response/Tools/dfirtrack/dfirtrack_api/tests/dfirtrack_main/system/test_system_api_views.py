from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from dfirtrack_main.models import Analysisstatus, Case, Company, Contact, Dnsname, Domain, Ip, Location, Os, Osarch, Reason, Recommendation, Serviceprovider, System, Systemstatus, Systemtype, Tag, Tagcolor
import urllib.parse

class SystemAPIViewTestCase(TestCase):
    """ system API view tests """

    @classmethod
    def setUpTestData(cls):

        # create user
        test_user = User.objects.create_user(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')

        # create mandatory foreign key objects

        # create object
        systemstatus_1 = Systemstatus.objects.create(systemstatus_name='systemstatus_1')

        # create optional foreign key objects

        # create object
        Analysisstatus.objects.create(analysisstatus_name='analysisstatus_1')
        # create object
        Case.objects.create(
            case_name = 'case_1',
            case_is_incident = True,
            case_created_by_user_id = test_user,
        )
        # create object
        Company.objects.create(company_name='company_1')
        # create object
        Contact.objects.create(
            contact_name = 'contact_1',
            contact_email = 'contact_email_1',
        )
        # create object
        Dnsname.objects.create(dnsname_name='dnsname_1')
        # create object
        Domain.objects.create(domain_name='domain_1')
        # create foreign key system
        System.objects.create(
            system_name = 'hostsystem_api_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )
        # create object
        Ip.objects.create(ip_ip='127.0.0.1')
        # create object
        Location.objects.create(location_name='location_1')
        # create object
        Os.objects.create(os_name='os_1')
        # create object
        Osarch.objects.create(osarch_name='osarch_1')
        # create object
        Reason.objects.create(reason_name='reason_1')
        # create object
        Recommendation.objects.create(recommendation_name='recommendation_1')
        # create object
        Serviceprovider.objects.create(serviceprovider_name='serviceprovider_1')
        # create object
        Systemtype.objects.create(systemtype_name='systemtype_1')
        # create object
        tagcolor_1 = Tagcolor.objects.create(tagcolor_name='tagcolor_1')
        # create object
        Tag.objects.create(
            tagcolor = tagcolor_1,
            tag_name = 'tag_1',
        )

        # create object
        System.objects.create(
            system_name = 'system_api_1',
            systemstatus = systemstatus_1,
            system_modify_time = timezone.now(),
            system_created_by_user_id = test_user,
            system_modified_by_user_id = test_user,
        )

    def test_system_list_api_unauthorized(self):
        """ unauthorized access is forbidden"""

        # get response
        response = self.client.get('/api/system/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_system_list_api_method_get(self):
        """ GET is allowed """

        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # get response
        response = self.client.get('/api/system/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_list_api_method_post(self):
        """ POST is allowed """

        # get user
        test_user_id = User.objects.get(username='testuser_system_api').id
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create POST string
        poststring = {
            "system_name": "system_api_2",
            "systemstatus": systemstatus_id,
            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_created_by_user_id": test_user_id,
            "system_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.post('/api/system/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

    def test_system_list_api_method_post_all_id(self):
        """ POST is allowed """

        # get user
        test_user_id = User.objects.get(username='testuser_system_api').id
        # get object
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        # get object
        case_id = Case.objects.get(case_name='case_1').case_id
        # get object
        company_id = Company.objects.get(company_name='company_1').company_id
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # get object
        dnsname_id = Dnsname.objects.get(dnsname_name='dnsname_1').dnsname_id
        # get object
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        hostsystem_id = System.objects.get(system_name='hostsystem_api_1').system_id
        # get object
        ip_id = Ip.objects.get(ip_ip='127.0.0.1').ip_id
        # get object
        location_id = Location.objects.get(location_name='location_1').location_id
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        osarch_id = Osarch.objects.get(osarch_name='osarch_1').osarch_id
        # get object
        reason_id = Reason.objects.get(reason_name='reason_1').reason_id
        # get object
        recommendation_id = Recommendation.objects.get(recommendation_name='recommendation_1').recommendation_id
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        systemtype_id = Systemtype.objects.get(systemtype_name='systemtype_1').systemtype_id
        # get object
        tag_id = Tag.objects.get(tag_name='tag_1').tag_id
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create POST string
        poststring = {
            "system_name": "system_api_2",
            "analysisstatus": analysisstatus_id,
            "case": [
                case_id,
            ],
            "company": [
                company_id,
            ],
            "contact": contact_id,
            "dnsname": dnsname_id,
            "domain": domain_id,
            "hostsystem": hostsystem_id,
            "ip": [
                ip_id,
            ],
            "location": location_id,
            "os": os_id,
            "osarch": osarch_id,
            "reason": reason_id,
            "recommendation": recommendation_id,
            "serviceprovider": serviceprovider_id,
            "systemstatus": systemstatus_id,
            "systemtype": systemtype_id,
            "tag": [
                tag_id,
            ],
            "system_lastbooted_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_deprecated_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_is_vm": True,
            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_created_by_user_id": test_user_id,
            "system_modified_by_user_id": test_user_id,
            "system_export_markdown": False,
            "system_export_spreadsheet": False,
        }
        # get response
        response = self.client.post('/api/system/', data=poststring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 201)

# TODO: is it possible to declare (and therefore test) nested serializers this way (like with analysisstatus in this example)?
#    def test_system_list_api_method_post_all_fk(self):
#        """ POST is allowed """
#
#        # get user
#        test_user_id = User.objects.get(username='testuser_system_api').id
#        # get object
#        analysisstatus_name = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_name
#        # get object
#        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
#        # login testuser
#        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
#        # create POST string
#        poststring = {
#            "system_name": "system_api_2",
#            "analysisstatus": {
#                "analysisstatus_name": analysisstatus_name,
#            },
#            "systemstatus": systemstatus_id,
#            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
#            "system_created_by_user_id": test_user_id,
#            "system_modified_by_user_id": test_user_id,
#        }
#        # get response
#        response = self.client.post('/api/system/', data=poststring, content_type='application/json')
#        # compare
#        self.assertEqual(response.status_code, 201)

    def test_system_list_api_redirect(self):
        """ test redirect with appending slash """

        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create url
        destination = urllib.parse.quote('/api/system/', safe='/')
        # get response
        response = self.client.get('/api/system', follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)

    def test_system_detail_api_unauthorized (self):
        """ unauthorized access is forbidden"""

        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # get response
        response = self.client.get('/api/system/' + str(system_api_1.system_id) + '/')
        # compare
        self.assertEqual(response.status_code, 401)

    def test_system_detail_api_method_get(self):
        """ GET is allowed """

        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # get response
        response = self.client.get('/api/system/' + str(system_api_1.system_id) + '/')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_detail_api_method_delete(self):
        """ DELETE is forbidden """

        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # get response
        response = self.client.delete('/api/system/' + str(system_api_1.system_id) + '/')
        # compare
        self.assertEqual(response.status_code, 405)

    def test_system_detail_api_method_put(self):
        """ PUT is allowed """

        # get user
        test_user_id = User.objects.get(username='testuser_system_api').id
        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create url
        destination = urllib.parse.quote('/api/system/' + str(system_api_1.system_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "system_name": "new_system_api_1",
            "systemstatus": systemstatus_id,
            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_created_by_user_id": test_user_id,
            "system_modified_by_user_id": test_user_id,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

    def test_system_detail_api_method_put_all_id(self):
        """ PUT is allowed """

        # get user
        test_user_id = User.objects.get(username='testuser_system_api').id
        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # get object
        analysisstatus_id = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_id
        # get object
        case_id = Case.objects.get(case_name='case_1').case_id
        # get object
        company_id = Company.objects.get(company_name='company_1').company_id
        # get object
        contact_id = Contact.objects.get(contact_name='contact_1').contact_id
        # get object
        dnsname_id = Dnsname.objects.get(dnsname_name='dnsname_1').dnsname_id
        # get object
        domain_id = Domain.objects.get(domain_name='domain_1').domain_id
        # get object
        hostsystem_id = System.objects.get(system_name='hostsystem_api_1').system_id
        # get object
        ip_id = Ip.objects.get(ip_ip='127.0.0.1').ip_id
        # get object
        location_id = Location.objects.get(location_name='location_1').location_id
        # get object
        os_id = Os.objects.get(os_name='os_1').os_id
        # get object
        osarch_id = Osarch.objects.get(osarch_name='osarch_1').osarch_id
        # get object
        reason_id = Reason.objects.get(reason_name='reason_1').reason_id
        # get object
        recommendation_id = Recommendation.objects.get(recommendation_name='recommendation_1').recommendation_id
        # get object
        serviceprovider_id = Serviceprovider.objects.get(serviceprovider_name='serviceprovider_1').serviceprovider_id
        # get object
        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
        # get object
        systemtype_id = Systemtype.objects.get(systemtype_name='systemtype_1').systemtype_id
        # get object
        tag_id = Tag.objects.get(tag_name='tag_1').tag_id
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create url
        destination = urllib.parse.quote('/api/system/' + str(system_api_1.system_id) + '/', safe='/')
        # create PUT string
        putstring = {
            "system_name": "new_system_api_1",
            "analysisstatus": analysisstatus_id,
            "case": [
                case_id,
            ],
            "company": [
                company_id,
            ],
            "contact": contact_id,
            "dnsname": dnsname_id,
            "domain": domain_id,
            "hostsystem": hostsystem_id,
            "ip": [
                ip_id,
            ],
            "location": location_id,
            "os": os_id,
            "osarch": osarch_id,
            "reason": reason_id,
            "recommendation": recommendation_id,
            "serviceprovider": serviceprovider_id,
            "systemstatus": systemstatus_id,
            "systemtype": systemtype_id,
            "tag": [
                tag_id,
            ],
            "system_lastbooted_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_deprecated_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_is_vm": True,
            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
            "system_created_by_user_id": test_user_id,
            "system_modified_by_user_id": test_user_id,
            "system_export_markdown": False,
            "system_export_spreadsheet": False,
        }
        # get response
        response = self.client.put(destination, data=putstring, content_type='application/json')
        # compare
        self.assertEqual(response.status_code, 200)

# TODO: is it possible to declare (and therefore test) nested serializers this way (like with analysisstatus in this example)?
#    def test_system_detail_api_method_put_all_fk(self):
#        """ PUT is allowed """
#
#        # get user
#        test_user_id = User.objects.get(username='testuser_system_api').id
#        # get object
#        system_api_1 = System.objects.get(system_name='system_api_1')
#        # get object
#        analysisstatus_name = Analysisstatus.objects.get(analysisstatus_name='analysisstatus_1').analysisstatus_name
#        # get object
#        systemstatus_id = Systemstatus.objects.get(systemstatus_name='systemstatus_1').systemstatus_id
#        # login testuser
#        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
#        # create url
#        destination = urllib.parse.quote('/api/system/' + str(system_api_1.system_id) + '/', safe='/')
#        # create PUT string
#        putstring = {
#            "system_name": "new_system_api_1",
#            "analysisstatus": {
#                "analysisstatus_name": analysisstatus_name,
#            },
#            "systemstatus": systemstatus_id,
#            "system_modify_time": timezone.now().strftime('%Y-%m-%dT%H:%M'),
#            "system_created_by_user_id": test_user_id,
#            "system_modified_by_user_id": test_user_id,
#        }
#        # get response
#        response = self.client.put(destination, data=putstring, content_type='application/json')
#        # compare
#        self.assertEqual(response.status_code, 200)

    def test_system_detail_api_redirect(self):
        """ test redirect with appending slash """

        # get object
        system_api_1 = System.objects.get(system_name='system_api_1')
        # login testuser
        self.client.login(username='testuser_system_api', password='Pqtg7fic7FfB2ESEwaPc')
        # create url
        destination = urllib.parse.quote('/api/system/' + str(system_api_1.system_id) + '/', safe='/')
        # get response
        response = self.client.get('/api/system/' + str(system_api_1.system_id), follow=True)
        # compare
        self.assertRedirects(response, destination, status_code=301, target_status_code=200)
