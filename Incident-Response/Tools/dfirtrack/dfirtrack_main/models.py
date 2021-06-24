from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import logging
from time import strftime
import uuid
import os
from dfirtrack.config import EVIDENCE_PATH

# initialize logger
stdlogger = logging.getLogger(__name__)

class Analysisstatus(models.Model):

    # primary key
    analysisstatus_id = models.AutoField(primary_key=True)

    # main entity information
    analysisstatus_name = models.CharField(max_length=30, unique=True)
    analysisstatus_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.analysisstatus_name

    # define logger
    def logger(analysisstatus, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " analysisstatus_id:" + str(analysisstatus.analysisstatus_id) +
            "|analysisstatus_name:" + str(analysisstatus.analysisstatus_name) +
            "|analysisstatus_note:" + str(analysisstatus.analysisstatus_note)
        )

    def get_absolute_url(self):
        return reverse('analysisstatus_detail', args=(self.pk,))

class Analystmemo(models.Model):

    # primary key
    analystmemo_id = models.AutoField(primary_key=True)

    # foreign key(s)
    system = models.ForeignKey('System', on_delete=models.CASCADE)

    # main entity information
    analystmemo_note = models.TextField()

    # meta information
    analystmemo_create_time = models.DateTimeField(auto_now_add=True)
    analystmemo_modify_time = models.DateTimeField(auto_now=True)
    analystmemo_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='analystmemo_created_by')
    analystmemo_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='analystmemo_modified_by')

    # string representation
    def __str__(self):
        return 'Analystmemo %s (%s)' % (str(self.analystmemo_id), self.system)

    # define logger
    def logger(analystmemo, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " analystmemo_id:" + str(analystmemo.analystmemo_id) +
            "|system:" + str(analystmemo.system) +
            "|analystmemo_note:" + str(analystmemo.analystmemo_note)
        )

    def get_absolute_url(self):
        return reverse('analystmemo_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('analystmemo_update', args=(self.pk,))

class Case(models.Model):

    # primary key
    case_id = models.AutoField(primary_key=True)

    # main entity information
    case_name = models.CharField(max_length=50, unique=True)
    case_is_incident = models.BooleanField()

    # meta information
    case_create_time = models.DateTimeField(auto_now_add=True)
    case_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='case_created_by')

    # string representation
    def __str__(self):
        return self.case_name

    # define logger
    def logger(case, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " case_id:" + str(case.case_id) +
            "|case_name:" + str(case.case_name) +
            "|case_is_incident:" + str(case.case_is_incident)
        )

    def get_absolute_url(self):
        return reverse('case_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('case_update', args=(self.pk,))

class Company(models.Model):

    # primary key
    company_id = models.AutoField(primary_key=True)

    # foreign key(s)
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, blank=True, null=True)

    # main entity information
    company_name = models.CharField(max_length=50, unique=True)
    company_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.company_name

    # define logger
    def logger(company, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " company_id:" + str(company.company_id) +
            "|division:" + str(company.division) +
            "|company_name:" + str(company.company_name) +
            "|company_note:" + str(company.company_note)
        )

    def get_absolute_url(self):
        return reverse('company_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('company_update', args=(self.pk,))

class Contact(models.Model):

    # primary key
    contact_id = models.AutoField(primary_key=True)

    # main entity information
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    contact_email = models.CharField(max_length=100, unique=True)
    contact_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.contact_name

    # define logger
    def logger(contact, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " contact_id:" + str(contact.contact_id) +
            "|contact_name:" + str(contact.contact_name) +
            "|contact_phone:" + str(contact.contact_phone) +
            "|contact_email:" + str(contact.contact_email) +
            "|contact_note:" + str(contact.contact_note)
        )

    def get_absolute_url(self):
        return reverse('contact_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('contact_update', args=(self.pk,))

class Division(models.Model):

    # primary key
    division_id = models.AutoField(primary_key=True)

    # main entity information
    division_name = models.CharField(max_length=50, unique=True)
    division_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.division_name

    # define logger
    def logger(division, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " division_id:" + str(division.division_id) +
            "|division_name:" + str(division.division_name) +
            "|division_note:" + str(division.division_note)
        )

    def get_absolute_url(self):
        return reverse('division_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('division_update', args=(self.pk,))

class Dnsname(models.Model):

    # primary key
    dnsname_id = models.AutoField(primary_key=True)

    # foreign key(s)
    domain = models.ForeignKey('Domain', on_delete=models.PROTECT, blank=True, null=True)

    # main entity information
    dnsname_name = models.CharField(max_length=100, unique=True)
    dnsname_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.dnsname_name

    # define logger
    def logger(dnsname, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " dnsname_id:" + str(dnsname.dnsname_id) +
            "|dnsname_name:" + str(dnsname.dnsname_name) +
            "|dnsname_note:" + str(dnsname.dnsname_note) +
            "|domain:" + str(dnsname.domain)
        )

    def get_absolute_url(self):
        return reverse('dnsname_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('dnsname_update', args=(self.pk,))

class Domain(models.Model):

    # primary key
    domain_id = models.AutoField(primary_key=True)

    # main entity information
    domain_name = models.CharField(max_length=100, unique=True)
    domain_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.domain_name

    # define logger
    def logger(domain, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " domain_id:" + str(domain.domain_id) +
            "|domain_name:" + str(domain.domain_name) +
            "|domain_note:" + str(domain.domain_note)
        )

    def get_absolute_url(self):
        return reverse('domain_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('domain_update', args=(self.pk,))

class Domainuser(models.Model):

    # primary key
    domainuser_id = models.AutoField(primary_key=True)

    # foreign key(s)
    domain = models.ForeignKey('Domain', on_delete=models.CASCADE)
    system_was_logged_on = models.ManyToManyField('System', blank=True)

    # main entity information
    domainuser_name = models.CharField(max_length=50)
    domainuser_is_domainadmin = models.BooleanField(blank=True, null=True)

    # define unique together
    class Meta:
        unique_together = ('domain', 'domainuser_name')

    # string representation
    def __str__(self):
        return '%s (%s)' % (self.domainuser_name, self.domain)

    # define logger
    def logger(domainuser, request_user, log_text):

        """
        ManyToMany-Relationsship don't get the default 'None' string if they are empty.
        So the default string is set to 'None'.
        If there are existing entities, their strings will be used instead and concatenated and separated by comma.
        """

        # get objects
        systems = domainuser.system_was_logged_on.all()
        # create empty list
        systemlist = []
        # set default string if there is no object at all
        systemstring = 'None'
        # iterate over objects
        for system in systems:
            # append object to list
            systemlist.append(system.system_name)
            # join list to comma separated string if there are any objects, else default string will remain
            systemstring = ','.join(systemlist)

        stdlogger.info(
            request_user +
            log_text +
            " domainuser_id:" + str(domainuser.domainuser_id) +
            "|domainuser_name:" + str(domainuser.domainuser_name) +
            "|domainuser_is_domainadmin:" + str(domainuser.domainuser_is_domainadmin) +
            "|domain:" + str(domainuser.domain) +
            "|system_was_logged_on:" + systemstring
        )

    def get_absolute_url(self):
        return reverse('domainuser_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('domainuser_update', args=(self.pk,))

class Entry(models.Model):

    # primary key
    entry_id = models.AutoField(primary_key=True)

    # foreign key(s)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    case = models.ForeignKey('Case', on_delete=models.SET_NULL, blank=True, null=True)

    # main entity information
    entry_time = models.DateTimeField()
    entry_sha1 = models.CharField(max_length=40, blank=True, null=True)
    entry_date = models.CharField(max_length=10, blank=True, null=True)
    entry_utc = models.CharField(max_length=8, blank=True, null=True)
    entry_system = models.CharField(max_length=30, blank=True, null=True)
    entry_type = models.CharField(max_length=30, blank=True, null=True)
    entry_content = models.TextField(blank=True, null=True)
    entry_note = models.TextField(blank=True, null=True)

    # meta information
    entry_create_time = models.DateTimeField(auto_now_add=True)
    entry_modify_time = models.DateTimeField(auto_now=True)
    entry_api_time = models.DateTimeField(null=True)
    entry_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entry_created_by')
    entry_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entry_modified_by')

    # define unique together
    class Meta:
        unique_together = ('system', 'entry_sha1')

    # string representation
    def __str__(self):
        return '%s | %s | %s' % (str(self.entry_id), self.system, self.entry_sha1)

    # define logger
    def logger(entry, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " entry_id:" + str(entry.entry_id) +
            "|system:" + str(entry.system) +
            "|entry_sha1:" + str(entry.entry_sha1) +
            "|entry_note:" + str(entry.entry_note) +
            "|case:" + str(entry.case)
        )

    def get_absolute_url(self):
        return reverse('entry_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('entry_update', args=(self.pk,))

class Headline(models.Model):

    # primary key
    headline_id = models.AutoField(primary_key=True)

    # main entity information
    headline_name = models.CharField(max_length=100, unique=True)

    # string representation
    def __str__(self):
        return self.headline_name

    # define logger
    def logger(headline, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " headline_id:" + str(headline.headline_id) +
            "|headline_name:" + str(headline.headline_name)
        )

    def get_absolute_url(self):
        return reverse('headline_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('headline_update', args=(self.pk,))

class Ip(models.Model):

    # primary key
    ip_id = models.AutoField(primary_key=True)

    # main entity information
    ip_ip = models.GenericIPAddressField(unique=True)

    # string representation
    def __str__(self):
        return self.ip_ip

    # define logger
    def logger(ip, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " ip_id:" + str(ip.ip_id) +
            "|ip_ip:" + str(ip.ip_ip)
        )

    def get_absolute_url(self):
        return reverse('ip_detail', args=(self.pk,))

class Location(models.Model):

    # primary key
    location_id = models.AutoField(primary_key=True)

    # main entity information
    location_name = models.CharField(max_length=50, unique=True)
    location_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.location_name

    # define logger
    def logger(location, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " location_id:" + str(location.location_id) +
            "|location_name:" + str(location.location_name) +
            "|location_note:" + str(location.location_note)
        )

    def get_absolute_url(self):
        return reverse('location_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('location_update', args=(self.pk,))

class Os(models.Model):

    # primary key
    os_id = models.AutoField(primary_key=True)

    # main entity information
    os_name = models.CharField(max_length=30, unique=True)

    # string representation
    def __str__(self):
        return self.os_name

    # define logger
    def logger(os, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " os_id:" + str(os.os_id) +
            "|os_name:" + str(os.os_name)
        )

    def get_absolute_url(self):
        return reverse('os_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('os_update', args=(self.pk,))

class Osarch(models.Model):

    # primary key
    osarch_id = models.AutoField(primary_key=True)

    # main entity information
    osarch_name = models.CharField(max_length=10, unique=True)

    # string representation
    def __str__(self):
        return self.osarch_name

    # define logger
    def logger(osarch, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " osarch_id:" + str(osarch.osarch_id) +
            "|osarch_name:" + str(osarch.osarch_name)
        )

    def get_absolute_url(self):
        return reverse('osarch_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('osarch_update', args=(self.pk,))

class Osimportname(models.Model):

    # primary key
    osimportname_id = models.AutoField(primary_key=True)

    # foreign key(s)
    os = models.ForeignKey('Os', on_delete=models.CASCADE)

    # main entity information
    osimportname_name = models.CharField(max_length=30, unique=True)
    osimportname_importer = models.CharField(max_length=30)

    # string representation
    def __str__(self):
        return '%s (%s)' % (self.osimportname_name, self.os)

    # define logger
    def logger(osimportname, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " osimportname_id:" + str(osimportname.osimportname_id) +
            "|osimportname_name:" + str(osimportname.osimportname_name) +
            "|osimportname_importer:" + str(osimportname.osimportname_importer) +
            "|os:" + str(osimportname.os)
        )

    def get_update_url(self):
        return reverse('osimportname_update', args=(self.pk,))

class Reason(models.Model):

    # primary key
    reason_id = models.AutoField(primary_key=True)

    # main entity information
    reason_name = models.CharField(max_length=30, unique=True)
    reason_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.reason_name

    # define logger
    def logger(reason, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " reason_id:" + str(reason.reason_id) +
            "|reason_name:" + str(reason.reason_name) +
            "|reason_note:" + str(reason.reason_note)
        )

    def get_absolute_url(self):
        return reverse('reason_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('reason_update', args=(self.pk,))

class Recommendation(models.Model):

    # primary key
    recommendation_id = models.AutoField(primary_key=True)

    # main entity information
    recommendation_name = models.CharField(max_length=30, unique=True)
    recommendation_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.recommendation_name

    # define logger
    def logger(recommendation, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " recommendation_id:" + str(recommendation.recommendation_id) +
            "|recommendation_name:" + str(recommendation.recommendation_name) +
            "|recommendation_note:" + str(recommendation.recommendation_note)
        )

    def get_absolute_url(self):
        return reverse('recommendation_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('recommendation_update', args=(self.pk,))

class Reportitem(models.Model):

    # primary key
    reportitem_id = models.AutoField(primary_key=True)

    # foreign key(s)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    headline = models.ForeignKey('Headline', on_delete=models.PROTECT)

    # main entity information
    reportitem_subheadline = models.CharField(max_length=100, blank=True, null=True)
    reportitem_note = models.TextField()

    # meta information
    reportitem_create_time = models.DateTimeField(auto_now_add=True)
    reportitem_modify_time = models.DateTimeField(auto_now=True)
    reportitem_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reportitem_created_by')
    reportitem_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reportitem_modified_by')

    # define unique together
    class Meta:
        unique_together = (('system', 'headline', 'reportitem_subheadline'),)

    # string representation
    def __str__(self):
        return '%s | %s | %s' % (self.system, self.headline.headline_name, self.reportitem_subheadline)

    # define logger
    def logger(reportitem, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " reportitem_id:" + str(reportitem.reportitem_id) +
            "|system:" + str(reportitem.system) +
            "|headline:" + str(reportitem.headline) +
            "|reportitem_subheadline:" + str(reportitem.reportitem_subheadline) +
            "|reportitem_note:" + str(reportitem.reportitem_note)
        )

    def get_absolute_url(self):
        return reverse('reportitem_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('reportitem_update', args=(self.pk,))

class Serviceprovider(models.Model):

    # primary key
    serviceprovider_id = models.AutoField(primary_key=True)

    # main entity information
    serviceprovider_name = models.CharField(max_length=50, unique=True)
    serviceprovider_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.serviceprovider_name

    # define logger
    def logger(serviceprovider, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " serviceprovider_id:" + str(serviceprovider.serviceprovider_id) +
            "|serviceprovider_name:" + str(serviceprovider.serviceprovider_name) +
            "|serviceprovider_note:" + str(serviceprovider.serviceprovider_note)
        )

    def get_absolute_url(self):
        return reverse('serviceprovider_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('serviceprovider_update', args=(self.pk,))

class System(models.Model):

    # primary key
    system_id = models.AutoField(primary_key=True)

    # foreign key(s)
    systemstatus = models.ForeignKey('Systemstatus', on_delete=models.PROTECT, related_name='systemstatus')
    analysisstatus = models.ForeignKey('Analysisstatus', on_delete=models.PROTECT, blank=True, null=True, related_name='analysisstatus')
    reason = models.ForeignKey('Reason', on_delete=models.PROTECT, blank=True, null=True)
    recommendation = models.ForeignKey('Recommendation', on_delete=models.PROTECT, blank=True, null=True)
    systemtype = models.ForeignKey('Systemtype', on_delete=models.PROTECT, blank=True, null=True)
    ip = models.ManyToManyField('Ip', blank=True)
    domain = models.ForeignKey('Domain', on_delete=models.PROTECT, blank=True, null=True)
    dnsname = models.ForeignKey('Dnsname', on_delete=models.PROTECT, blank=True, null=True)
    os = models.ForeignKey('Os', on_delete=models.PROTECT, blank=True, null=True)
    osarch = models.ForeignKey('Osarch', on_delete=models.PROTECT, blank=True, null=True)
    host_system = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    company = models.ManyToManyField('Company', blank=True)
    location = models.ForeignKey('Location', on_delete=models.PROTECT, blank=True, null=True)
    serviceprovider = models.ForeignKey('Serviceprovider', on_delete=models.PROTECT, blank=True, null=True)
    contact = models.ForeignKey('Contact', on_delete=models.PROTECT, blank=True, null=True)
    tag = models.ManyToManyField('Tag', blank=True)
    case = models.ManyToManyField('Case', blank=True)

    # main entity information
    system_uuid = models.UUIDField(editable=False, null=True, unique=True)
    system_name = models.CharField(max_length=50)
    system_install_time = models.DateTimeField(blank=True, null=True)
    system_lastbooted_time = models.DateTimeField(blank=True, null=True)
    system_deprecated_time = models.DateTimeField(blank=True, null=True)
    system_is_vm = models.BooleanField(blank=True, null=True)

    # history information
    previous_systemstatus = models.ForeignKey('Systemstatus', on_delete=models.PROTECT, null=True, related_name='previous_systemstatus')
    previous_analysisstatus = models.ForeignKey('Analysisstatus', on_delete=models.PROTECT, blank=True, null=True, related_name='previous_analysisstatus')

    # meta information
    system_create_time = models.DateTimeField(auto_now_add=True)
    system_modify_time = models.DateTimeField()
    system_api_time = models.DateTimeField(null=True)
    system_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='system_created_by')
    system_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='system_modified_by')
    system_export_markdown = models.BooleanField(default=True)
    system_export_spreadsheet = models.BooleanField(default=True)

    # define unique together
    class Meta:
        unique_together = ('system_name', 'domain', 'system_install_time')

    # string representation
    def __str__(self):
        if self.system_install_time == None:
            return '[%s] %s' % (str(self.system_id), self.system_name)
        else:
            installtime = self.system_install_time.strftime('%Y-%m-%d')
            return '[%s] %s (%s)' % (str(self.system_id), self.system_name, installtime)

    # extend save method
    def save(self, *args, **kwargs):

        # check for existing system
        if self.pk:

            ''' systemhistory '''

            ''' systemstatus (null = False) '''

            # compare previous with actual status
            if self.previous_systemstatus != self.systemstatus:
                # create systemhistory object reflecting status change
                systemhistory = Systemhistory(
                    system = self,
                    systemhistory_type = 'Systemstatus',
                    systemhistory_old_value = self.previous_systemstatus.systemstatus_name,
                    systemhistory_new_value = self.systemstatus.systemstatus_name,
                    # TODO: systemhistory_user_id
                )
                systemhistory.save()
                # set previous status to new value
                self.previous_systemstatus = self.systemstatus

            ''' analysisstatus (null = True) '''

            # existing previous status / actual status provided
            if self.previous_analysisstatus and self.analysisstatus:
                # compare previous with actual status
                if self.previous_analysisstatus != self.analysisstatus:
                    # create systemhistory object reflecting status change
                    systemhistory = Systemhistory(
                        system = self,
                        systemhistory_type = 'Analysisstatus',
                        systemhistory_old_value = self.previous_analysisstatus.analysisstatus_name,
                        systemhistory_new_value = self.analysisstatus.analysisstatus_name,
                        # TODO: systemhistory_user_id
                    )
                    systemhistory.save()
                    # set previous status to new value
                    self.previous_analysisstatus = self.analysisstatus

            # existing previous status / no actual status provided
            elif self.previous_analysisstatus and not self.analysisstatus:
                systemhistory = Systemhistory(
                    system = self,
                    systemhistory_type = 'Analysisstatus',
                    systemhistory_old_value = self.previous_analysisstatus.analysisstatus_name,
                    systemhistory_new_value = 'No analysisstatus',
                    # TODO: systemhistory_user_id
                )
                systemhistory.save()
                # set previous status to new value
                self.previous_analysisstatus = self.analysisstatus

            # no previous status / actual status provided
            elif not self.previous_analysisstatus and self.analysisstatus:
                systemhistory = Systemhistory(
                    system = self,
                    systemhistory_type = 'Analysisstatus',
                    systemhistory_old_value = 'No analysisstatus',
                    systemhistory_new_value = self.analysisstatus.analysisstatus_name,
                    # TODO: systemhistory_user_id
                )
                systemhistory.save()
                # set previous status to new value
                self.previous_analysisstatus = self.analysisstatus

        # check for new system
        if not self.pk:

            ''' systemhistory '''

            # initial set previous status (null = False)
            self.previous_systemstatus = self.systemstatus

            # initial set previous status (null = True)
            if self.analysisstatus:
                self.previous_analysisstatus = self.analysisstatus

            """ create uuid """

            # generate uuid type4 (completely random type)
            self.system_uuid = uuid.uuid4()

        return super().save(*args, **kwargs)

    # define logger
    def logger(system, request_user, log_text):

        """
        ManyToMany-Relationsship don't get the default 'None' string if they are empty.
        So the default string is set to 'None'.
        If there are existing entities, their strings will be used instead and concatenated and separated by comma.
        """

        # get objects
        ips = system.ip.all()
        # create empty list
        iplist = []
        # set default string if there is no object at all
        ipstring = 'None'
        # iterate over objects
        for ip in ips:
            # append object to list
            iplist.append(ip.ip_ip)
            # join list to comma separated string if there are any objects, else default string will remain
            ipstring = ','.join(iplist)

        if system.system_install_time != None:
            # cast datetime object to string
            installtime = system.system_install_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            installtime = 'None'

        if system.system_lastbooted_time != None:
            # cast datetime object to string
            lastbootedtime = system.system_lastbooted_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            lastbootedtime = 'None'

        if system.system_deprecated_time != None:
            # cast datetime object to string
            deprecatedtime = system.system_deprecated_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            deprecatedtime = 'None'

        # get objects
        companys = system.company.all()
        # create empty list
        companylist = []
        # set default string if there is no object at all
        companystring = 'None'
        # iterate over objects
        for company in companys:
            # append object to list
            companylist.append(company.company_name)
            # join list to comma separated string if there are any objects, else default string will remain
            companystring = ','.join(companylist)

        # get objects
        tags = system.tag.all()
        # create empty list
        taglist = []
        # set default string if there is no object at all
        tagstring = 'None'
        # iterate over objects
        for tag in tags:
            # append object to list
            taglist.append(tag.tag_name)
            # join list to comma separated string if there are any objects, else default string will remain
            tagstring = ','.join(taglist)

        # get objects
        cases = system.case.all()
        # create empty list
        caselist = []
        # set default string if there is no object at all
        casestring = 'None'
        # iterate over objects
        for case in cases:
            # append object to list
            caselist.append(case.case_name)
            # join list to comma separated string if there are any objects, else default string will remain
            casestring = ','.join(caselist)

        # finally write log
        stdlogger.info(
            request_user +
            log_text +
            " system_id:" + str(system.system_id) +
            "|system_uuid:" + str(system.system_uuid) +
            "|system_name:" + str(system) +
            "|systemstatus:" + str(system.systemstatus) +
            "|analyisstatus:" + str(system.analysisstatus) +
            "|reason:" + str(system.reason) +
            "|recommendation:" + str(system.recommendation) +
            "|systemtype:" + str(system.systemtype) +
            "|ip:" + ipstring +
            "|domain:" + str(system.domain) +
            "|dnsname:" + str(system.dnsname) +
            "|os:" + str(system.os) +
            "|osarch:" + str(system.osarch) +
            "|system_install_time:" + installtime +
            "|system_lastbooted_time:" + lastbootedtime +
            "|system_deprecated_time:" + deprecatedtime +
            "|system_is_vm:" + str(system.system_is_vm) +
            "|host_system:" + str(system.host_system) +
            "|company:" + companystring +
            "|location:" + str(system.location) +
            "|serviceprovider:" + str(system.serviceprovider) +
            "|contact:" + str(system.contact) +
            "|tag:" + tagstring +
            "|case:" + casestring +
            "|system_export_markdown:" + str(system.system_export_markdown) +
            "|system_export_spreadsheet:" + str(system.system_export_spreadsheet)
        )

    def create_evidence_directory(self):
        """
        Check if the evidence directory for the system was already created
        otherwise it will be created.
        """
        system_evidence_path = (EVIDENCE_PATH + '/' + str(self.uuid))
        if os.path.exists(system_evidence_path):
            self.logger(request_user, "System-Path: {} already exists.".format(system_evidence_path))
            return False
        else:
            os.makedirs(system_evidence_path)
            self.logger(request_user, "System-Path: {} created.".format(system_evidence_path))
            return True

    def get_absolute_url(self):
        return reverse('system_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('system_update', args=(self.pk,))

class Systemhistory(models.Model):

    # primary key
    systemhistory_id = models.AutoField(primary_key=True)

    # foreign key(s)
    system = models.ForeignKey('System', on_delete=models.CASCADE)

    # main entity information
    systemhistory_type = models.CharField(max_length=30)
    systemhistory_old_value = models.CharField(max_length=30)
    systemhistory_new_value = models.CharField(max_length=30)

    # meta information
    systemhistory_time = models.DateTimeField(auto_now_add=True)
    #systemhistory_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='systemhistory_user')

    # string representation
    def __str__(self):
        return str(self.systemhistory_id)

class Systemstatus(models.Model):

    # primary key
    systemstatus_id = models.AutoField(primary_key=True)

    # main entity information
    systemstatus_name = models.CharField(max_length=30, unique=True)
    systemstatus_note = models.TextField(blank=True, null=True)

    # string representation
    def __str__(self):
        return self.systemstatus_name

    # define logger
    def logger(systemstatus, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " systemstatus_id:" + str(systemstatus.systemstatus_id) +
            "|systemstatus_name:" + str(systemstatus.systemstatus_name) +
            "|systemstatus_note:" + str(systemstatus.systemstatus_note)
        )

    def get_absolute_url(self):
        return reverse('systemstatus_detail', args=(self.pk,))

class Systemtype(models.Model):

    # primary key
    systemtype_id = models.AutoField(primary_key=True)

    # main entity information
    systemtype_name = models.CharField(max_length=50, unique=True)

    # string representation
    def __str__(self):
        return self.systemtype_name

    # define logger
    def logger(systemtype, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " systemtype_id:" + str(systemtype.systemtype_id) +
            "|systemtype_name:" + str(systemtype.systemtype_name)
        )

    def get_absolute_url(self):
        return reverse('systemtype_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('systemtype_update', args=(self.pk,))

class Systemuser(models.Model):

    # primary key
    systemuser_id = models.AutoField(primary_key=True)

    # foreign key(s)
    system = models.ForeignKey('System', on_delete=models.CASCADE)

    # main entity information
    systemuser_name = models.CharField(max_length=50)
    systemuser_lastlogon_time = models.DateTimeField(blank=True, null=True)
    systemuser_is_systemadmin = models.BooleanField(blank=True, null=True)

    # define unique together
    class Meta:
        unique_together = ('system', 'systemuser_name')

    # string representation
    def __str__(self):
        return '%s (%s)' % (self.systemuser_name, self.system)

    # define logger
    def logger(systemuser, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " systemuser_id:" + str(systemuser.systemuser_id) +
            "|system:" + str(systemuser.system) +
            "|systemuser_name:" + str(systemuser.systemuser_name) +
            "|systemuser_lastlogon_time:" + str(systemuser.systemuser_lastlogon_time) +
            "|systemuser_is_systemadmin:" + str(systemuser.systemuser_is_systemadmin)
        )

    def get_absolute_url(self):
        return reverse('systemuser_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('systemuser_update', args=(self.pk,))

class Tag(models.Model):

    # primary key
    tag_id = models.AutoField(primary_key=True)

    # foreign key(s)
    tagcolor = models.ForeignKey('Tagcolor', on_delete=models.PROTECT)

    # main entity information
    tag_name = models.CharField(max_length=50, unique=True)
    tag_note = models.TextField(blank=True, null=True)

    # meta information
    tag_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tag_modified_by', blank=True, null=True)

    # string representation
    def __str__(self):
        return self.tag_name

    # define logger
    def logger(tag, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " tag_id:" + str(tag.tag_id) +
            "|tag_name:" + str(tag.tag_name) +
            "|tag_note:" + str(tag.tag_note) +
            "|tagcolor:" + str(tag.tagcolor)
        )

    def get_absolute_url(self):
        return reverse('tag_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('tag_update', args=(self.pk,))

    def get_delete_url(self):
        return reverse('tag_delete', args=(self.pk,))

class Tagcolor(models.Model):

    # primary key
    tagcolor_id = models.AutoField(primary_key=True)

    # main entity information
    tagcolor_name = models.CharField(max_length=20, unique=True)

    # string representation
    def __str__(self):
        return self.tagcolor_name

    # define logger
    def logger(tagcolor, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " tagcolor_id:" + str(tagcolor.tagcolor_id) +
            "|tagcolor_name:" + str(tagcolor.tagcolor_name)
        )

class Task(models.Model):

    # primary key
    task_id = models.AutoField(primary_key=True)

    # foreign key(s)
    parent_task = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
    taskname = models.ForeignKey('Taskname', on_delete=models.PROTECT)
    taskpriority = models.ForeignKey('Taskpriority', on_delete=models.PROTECT)
    taskstatus = models.ForeignKey('Taskstatus', on_delete=models.PROTECT)
    system = models.ForeignKey('System', on_delete=models.CASCADE, blank=True, null=True)
    task_assigned_to_user_id = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='task_assigned_to')
    tag = models.ManyToManyField('Tag', blank=True)

    # main entity information
    task_note = models.TextField(blank=True, null=True)
    task_scheduled_time = models.DateTimeField(blank=True, null=True)
    task_started_time = models.DateTimeField(blank=True, null=True)
    task_finished_time = models.DateTimeField(blank=True, null=True)
    task_due_time = models.DateTimeField(blank=True, null=True)

    # meta information
    task_create_time = models.DateTimeField(auto_now_add=True)
    task_modify_time = models.DateTimeField(auto_now=True)
    task_created_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='task_created_by')
    task_modified_by_user_id = models.ForeignKey(User, on_delete=models.PROTECT, related_name='task_modified_by')

    # string representation
    def __str__(self):
        return '[%s] %s (%s)' % (self.task_id, self.taskname, self.system)

    # define logger
    def logger(task, request_user, log_text):

        if task.task_scheduled_time != None:
            # cast datetime object to string
            scheduledtime = task.task_scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            scheduledtime = 'None'

        if task.task_started_time != None:
            # cast datetime object to string
            startedtime = task.task_started_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            startedtime = 'None'

        if task.task_finished_time != None:
            # cast datetime object to string
            finishedtime = task.task_finished_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            # else set default string
            finishedtime = 'None'

        if task.task_due_time != None:
            # cast datetime object to string
            duetime = task.task_due_time.strftime('%Y-%m-%d %H:%M:%S')
            # else set default string
        else:
            duetime = 'None'

        # get objects
        tags = task.tag.all()
        # create empty list
        taglist = []
        # set default string if there is no object at all
        tagstring = 'None'
        # iterate over objects
        for tag in tags:
            # append object to list
            taglist.append(tag.tag_name)
            # join list to comma separated string if there are any objects, else default string will remain
            tagstring = ','.join(taglist)

        # finally write log
        stdlogger.info(
            request_user +
            log_text +
            " task_id:" + str(task.task_id) +
            "|parent_task:" + str(task.parent_task) +
            "|taskname:" + str(task.taskname) +
            "|taskpriority:" + str(task.taskpriority) +
            "|taskstatus:" + str(task.taskstatus) +
            "|system:" + str(task.system) +
            "|task_assigned_to_user_id:" + str(task.task_assigned_to_user_id) +
            "|task_note:" + str(task.task_note) +
            "|task_scheduled_time:" + scheduledtime +
            "|task_started_time:" + startedtime +
            "|task_finished_time:" + finishedtime +
            "|task_due_time:" + duetime +
            "|tag:" + tagstring
        )

    def get_absolute_url(self):
        return reverse('task_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('task_update', args=(self.pk,))

    def get_start_url(self):
        return reverse('task_start', args=(self.pk,))

    def get_finish_url(self):
        return reverse('task_finish', args=(self.pk,))

    def get_renew_url(self):
        return reverse('task_renew', args=(self.pk,))

    def get_set_user_url(self):
        return reverse('task_set_user', args=(self.pk,))

    def get_unset_user_url(self):
        return reverse('task_unset_user', args=(self.pk,))

class Taskname(models.Model):

    # primary key
    taskname_id = models.AutoField(primary_key=True)

    # main entity information
    taskname_name = models.CharField(max_length=50, unique=True)

    # string representation
    def __str__(self):
        return self.taskname_name

    # define logger
    def logger(taskname, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " taskname_id:" + str(taskname.taskname_id) +
            "|taskname_name:" + str(taskname.taskname_name)
        )

    def get_absolute_url(self):
        return reverse('taskname_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('taskname_update', args=(self.pk,))

    def get_close_url(self):
        return reverse('taskname_close', args=(self.pk,))

class Taskpriority(models.Model):

    # primary key
    taskpriority_id = models.AutoField(primary_key=True)

    # main entity information
    taskpriority_name = models.CharField(max_length=50, unique=True)

    # string representation
    def __str__(self):
        return self.taskpriority_name

    # define logger
    def logger(taskpriority, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " taskpriority_id:" + str(taskpriority.taskpriority_id) +
            "|taskpriority_name:" + str(taskpriority.taskpriority_name)
        )

    def get_absolute_url(self):
        return reverse('taskpriority_detail', args=(self.pk,))

class Taskstatus(models.Model):

    # primary key
    taskstatus_id = models.AutoField(primary_key=True)

    # main entity information
    taskstatus_name = models.CharField(max_length=50, unique=True)

    # string representation
    def __str__(self):
        return self.taskstatus_name

    # define logger
    def logger(taskstatus, request_user, log_text):
        stdlogger.info(
            request_user +
            log_text +
            " taskstatus_id:" + str(taskstatus.taskstatus_id) +
            "|taskstatus_name:" + str(taskstatus.taskstatus_name)
        )

    def get_absolute_url(self):
        return reverse('taskstatus_detail', args=(self.pk,))
