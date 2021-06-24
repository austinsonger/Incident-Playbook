from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from dfirtrack_main.models import Analysisstatus, Analystmemo, Case, Company, Contact, Division, Dnsname, Domain, Domainuser, Entry, Headline, Location, Os, Osimportname, Reason, Recommendation, Reportitem, Serviceprovider, System, Systemstatus, Systemtype, Systemuser, Tag, Tagcolor, Task, Taskname, Taskpriority, Taskstatus


# inherit from this class if you want to use the ModelMultipleChoiceField with the FilteredSelectMultiple widget
class AdminStyleSelectorForm(forms.ModelForm):

    # needed for system selector
    class Media:
        css = {
            'all': ('/static/admin/css/widgets.css',),
        }
        js = ('/admin/jsi18n',)

class AnalystmemoForm(forms.ModelForm):

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System (*)'),
        queryset = System.objects.order_by('system_name'),
    )

    class Meta:

        # model
        model = Analystmemo

        # this HTML forms are shown
        fields = (
            'system',
            'analystmemo_note',
        )

        # non default form labeling
        labels = {
            'analystmemo_note': gettext_lazy('Analystmemo note (*)'),
        }

        # special form type or option
        widgets = {
            'analystmemo_note': forms.Textarea(attrs={'autofocus': 'autofocus','rows': 20}),
        }

class CaseForm(forms.ModelForm):

    class Meta:

        # model
        model = Case

        # this HTML forms are shown
        fields = (
            'case_name',
            'case_is_incident',
        )

        # non default form labeling
        labels = {
            'case_name': gettext_lazy('Case name (*)'),
        }

        # special form type or option
        widgets = {
            'case_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class CompanyForm(forms.ModelForm):

    # reorder field choices
    division = forms.ModelChoiceField(
        label = gettext_lazy('Division'),
        queryset = Division.objects.order_by('division_name'),
        required = False,
    )

    class Meta:

        # model
        model = Company

        # this HTML forms are shown
        fields = (
            'company_name',
            'division',
            'company_note',
        )

        # non default form labeling
        labels = {
            'company_name': gettext_lazy('Company name (*)'),
        }

        # special form type or option
        widgets = {
            'company_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class ContactForm(forms.ModelForm):

    class Meta:

        # model
        model = Contact

        # this HTML forms are shown
        fields = (
            'contact_name',
            'contact_phone',
            'contact_email',
            'contact_note',
        )

        # non default form labeling
        labels = {
            'contact_name': gettext_lazy('Contact name (*)'),
            'contact_email': gettext_lazy('Contact email (*)'),
        }

        # special form type or option
        widgets = {
            'contact_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class DivisionForm(forms.ModelForm):

    class Meta:

        # model
        model = Division

        # this HTML forms are shown
        fields = (
            'division_name',
            'division_note',
        )

        # non default form labeling
        labels = {
            'division_name': gettext_lazy('Division name (*)'),
        }

        # special form type or option
        widgets = {
            'division_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class DnsnameForm(forms.ModelForm):

    # reorder field choices
    domain = forms.ModelChoiceField(
        label = gettext_lazy('Domain'),
        queryset = Domain.objects.order_by('domain_name'),
        required = False,
    )

    class Meta:

        # model
        model = Dnsname

        # this HTML forms are shown
        fields = (
            'domain',
            'dnsname_name',
            'dnsname_note',
        )

        # non default form labeling
        labels = {
            'dnsname_name': gettext_lazy('DNS name (*)'),
            'dnsname_note': gettext_lazy('Note'),
        }

        # special form type or option
        widgets = {
            'dnsname_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class DomainForm(forms.ModelForm):

    class Meta:

        # model
        model = Domain

        # this HTML forms are shown
        fields = (
            'domain_name',
            'domain_note',
        )

        # non default form labeling
        labels = {
            'domain_name': gettext_lazy('Domain name (*)'),
        }

        # special form type or option
        widgets = {
            'domain_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class DomainuserForm(forms.ModelForm):

    # reorder field choices
    domain = forms.ModelChoiceField(
        label = gettext_lazy('Domain (*)'),
        queryset = Domain.objects.order_by('domain_name'),
    )

    # reorder field choices
    system_was_logged_on = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Systems where this domainuser was logged on'),
        queryset = System.objects.order_by('system_name'),
        required = False,
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:

        # model
        model = Domainuser

        # this HTML forms are shown
        fields = (
            'domainuser_name',
            'domainuser_is_domainadmin',
            'domain',
            'system_was_logged_on',
        )

        # non default form labeling
        labels = {
            'domainuser_name': gettext_lazy('Domainuser name (*)'),
        }

        # special form type or option
        widgets = {
            'domainuser_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class EntryForm(forms.ModelForm):

    # reorder field choices
    case = forms.ModelChoiceField(
        label = gettext_lazy('Case'),
        queryset = Case.objects.order_by('case_name'),
        required = False,
    )

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System (*)'),
        queryset = System.objects.order_by('system_name'),
    )

    class Meta:

        # model
        model = Entry

        # this HTML forms are shown
        fields = (
            'entry_time',
            'system',
            'entry_sha1',
            'entry_date',
            'entry_utc',
            'entry_system',
            'entry_type',
            'entry_content',
            'entry_note',
            'case',
        )

        # non default form labeling
        labels = {
            'entry_time': gettext_lazy('Entry time (for sorting) (YYYY-MM-DD HH:MM:SS) (*)'),
            'entry_date': gettext_lazy('Entry date (YYYY-MM-DD)'),
            'entry_utc': gettext_lazy('Entry time (for report) (HH:MM:SS)'),
            'entry_system': gettext_lazy('Entry system (for report)'),
        }

        # special form type or option
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'autofocus': 'autofocus'}),
            'entry_sha1': forms.TextInput(),
            'entry_date': forms.TextInput(),
            'entry_utc': forms.TextInput(),
            'entry_system': forms.TextInput(),
            'entry_type': forms.TextInput(),
            'entry_content': forms.Textarea(attrs={'rows': 3}),
            'entry_note': forms.Textarea(attrs={'rows': 10}),
        }

class EntryFileImport(forms.ModelForm):

    # reorder field choices
    system = forms.ModelChoiceField(queryset=System.objects.order_by('system_name'))

    # file upload field (variable is used in request object)
    entryfile = forms.FileField()

    class Meta:

        # model
        model = Entry
        fields = (
            'system',
        )

class HeadlineForm(forms.ModelForm):

    class Meta:

        # model
        model = Headline

        # this HTML forms are shown
        fields = (
            'headline_name',
        )

        # non default form labeling
        labels = {
            'headline_name': gettext_lazy('Headline (*)'),
        }

        # special form type or option
        widgets = {
            'headline_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class LocationForm(forms.ModelForm):

    class Meta:

        # model
        model = Location

        # this HTML forms are shown
        fields = (
            'location_name',
            'location_note',
        )

        # non default form labeling
        labels = {
            'location_name': gettext_lazy('Location name (*)'),
        }

        # special form type or option
        widgets = {
            'location_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class OsForm(forms.ModelForm):

    class Meta:

        # model
        model = Os

        # this HTML forms are shown
        fields = (
            'os_name',
        )

        # non default form labeling
        labels = {
            'os_name': gettext_lazy('Os name (*)'),
        }

        # special form type or option
        widgets = {
            'os_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class OsimportnameForm(forms.ModelForm):

    # reorder field choices
    os = forms.ModelChoiceField(
        label = gettext_lazy('Operating system (*)'),
        queryset = Os.objects.order_by('os_name'),
    )

    class Meta:

        # model
        model = Osimportname

        # this HTML forms are shown
        fields = (
            'osimportname_name',
            'os',
            'osimportname_importer',
        )

        # non default form labeling
        labels = {
            'osimportname_name': gettext_lazy('Importname (*)'),
            'osimportname_importer': gettext_lazy('Importer (*)'),
        }

        # special form type or option
        widgets = {
            'osimportname_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class ReasonForm(forms.ModelForm):

    class Meta:

        # model
        model = Reason

        # this HTML forms are shown
        fields = (
            'reason_name',
            'reason_note',
        )

        # non default form labeling
        labels = {
            'reason_name': gettext_lazy('Reason name (*)'),
        }

        # special form type or option
        widgets = {
            'reason_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class RecommendationForm(forms.ModelForm):

    class Meta:

        # model
        model = Recommendation

        # this HTML forms are shown
        fields = (
            'recommendation_name',
            'recommendation_note',
        )

        # non default form labeling
        labels = {
            'recommendation_name': gettext_lazy('Recommendation name (*)'),
        }

        # special form type or option
        widgets = {
            'recommendation_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class ReportitemForm(forms.ModelForm):

    # reorder field choices
    headline = forms.ModelChoiceField(
        label = gettext_lazy('Headline (*)'),
        queryset = Headline.objects.order_by('headline_name'),
    )

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System (*)'),
        queryset = System.objects.order_by('system_name'),
    )

    class Meta:

        # model
        model = Reportitem

        # this HTML forms are shown
        fields = (
            'system',
            'headline',
            'reportitem_subheadline',
            'reportitem_note',
        )

        # non default form labeling
        labels = {
            'reportitem_subheadline': gettext_lazy('Subheadline'),
            'reportitem_note': gettext_lazy('Note (*)'),
        }

        # special form type or option
        widgets = {
            'reportitem_note': forms.Textarea(attrs={
                'autofocus': 'autofocus',
                'rows': 20,
                'style': 'font-family: monospace',
            }),
        }

class ServiceproviderForm(forms.ModelForm):

    class Meta:

        # model
        model = Serviceprovider

        # this HTML forms are shown
        fields = (
            'serviceprovider_name',
            'serviceprovider_note',
        )

        # non default form labeling
        labels = {
            'serviceprovider_name': gettext_lazy('Serviceprovider name (*)'),
        }

        # special form type or option
        widgets = {
            'serviceprovider_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class SystemForm(forms.ModelForm):
    """ this form does not allow editing of system_name """

    # reorder field choices
    systemstatus = forms.ModelChoiceField(
        queryset = Systemstatus.objects.order_by('systemstatus_name'),
        label = 'Systemstatus',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    analysisstatus = forms.ModelChoiceField(
        queryset = Analysisstatus.objects.order_by('analysisstatus_name'),
        label = 'Analysisstatus',
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    reason = forms.ModelChoiceField(
        label = gettext_lazy('Reason'),
        queryset = Reason.objects.order_by('reason_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    recommendation = forms.ModelChoiceField(
        label = gettext_lazy('Recommendation'),
        queryset = Recommendation.objects.order_by('recommendation_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    systemtype = forms.ModelChoiceField(
        label = gettext_lazy('Systemtype'),
        queryset = Systemtype.objects.order_by('systemtype_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    domain = forms.ModelChoiceField(
        label = gettext_lazy('Domain'),
        queryset = Domain.objects.order_by('domain_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    dnsname = forms.ModelChoiceField(
        label = gettext_lazy('Dnsname'),
        queryset = Dnsname.objects.order_by('dnsname_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    os = forms.ModelChoiceField(
        label = gettext_lazy('Os'),
        queryset = Os.objects.order_by('os_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    company = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Company'),
        queryset = Company.objects.order_by('company_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    location = forms.ModelChoiceField(
        label = gettext_lazy('Location'),
        queryset = Location.objects.order_by('location_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    serviceprovider = forms.ModelChoiceField(
        label = gettext_lazy('Serviceprovider'),
        queryset = Serviceprovider.objects.order_by('serviceprovider_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    contact = forms.ModelChoiceField(
        label = gettext_lazy('Contact'),
        queryset = Contact.objects.order_by('contact_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    tag = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Tag'),
        queryset = Tag.objects.order_by('tag_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    case = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Case'),
        queryset = Case.objects.order_by('case_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # large text area for line separated iplist
    iplist = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'One ip address per line',
            },
        ),
        required = False,
    )

    class Meta:

        # model
        model = System

        # this HTML forms are shown
        fields = (
            'systemstatus',
            'analysisstatus',
            'reason',
            'recommendation',
            'systemtype',
            'domain',
            'dnsname',
            'os',
            'osarch',
            'system_install_time',
            'system_lastbooted_time',
            'system_deprecated_time',
            'system_is_vm',
            'host_system',
            'company',
            'location',
            'serviceprovider',
            'contact',
            'tag',
            'case',
            'system_export_markdown',
            'system_export_spreadsheet',
        )

        # special form type or option
        widgets = {
            'ip': forms.GenericIPAddressField(),
            'osarch': forms.RadioSelect(),
            'system_install_time': forms.DateTimeInput(),
            'system_lastbooted_time': forms.DateTimeInput(),
            'system_deprecated_time': forms.DateTimeInput(),
            'system_is_vm': forms.NullBooleanSelect(),
            'host_system': forms.Select(),
        }

class SystemNameForm(SystemForm):
    """ this form allows editing of system_name """

    class Meta(SystemForm.Meta):

        # add system_name to shown HTML forms
        fields = SystemForm.Meta.fields + (
            'system_name',
        )

        # special form type or option for system_name
        SystemForm.Meta.widgets['system_name'] = forms.TextInput(
            attrs={
                'autofocus': 'autofocus',
                'placeholder': 'Enter system name / hostname here',
            }
        )

class SystemCreatorForm(forms.ModelForm):

    # reorder field choices
    systemstatus = forms.ModelChoiceField(
        queryset = Systemstatus.objects.order_by('systemstatus_name'),
        label = 'Systemstatus',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    analysisstatus = forms.ModelChoiceField(
        queryset = Analysisstatus.objects.order_by('analysisstatus_name'),
        required = False,
        label = 'Analysisstatus',
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    reason = forms.ModelChoiceField(
        label = gettext_lazy('Reason'),
        queryset = Reason.objects.order_by('reason_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    systemtype = forms.ModelChoiceField(
        label = gettext_lazy('Systemtype'),
        queryset = Systemtype.objects.order_by('systemtype_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    domain = forms.ModelChoiceField(
        label = gettext_lazy('Domain'),
        queryset = Domain.objects.order_by('domain_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    dnsname = forms.ModelChoiceField(
        label = gettext_lazy('Dnsname'),
        queryset = Dnsname.objects.order_by('dnsname_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    os = forms.ModelChoiceField(
        label = gettext_lazy('Os'),
        queryset = Os.objects.order_by('os_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    company = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Company'),
        queryset = Company.objects.order_by('company_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    location = forms.ModelChoiceField(
        label = gettext_lazy('Location'),
        queryset = Location.objects.order_by('location_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    serviceprovider = forms.ModelChoiceField(
        label = gettext_lazy('Serviceprovider'),
        queryset = Serviceprovider.objects.order_by('serviceprovider_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    contact = forms.ModelChoiceField(
        label = gettext_lazy('Contact'),
        queryset = Contact.objects.order_by('contact_name'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    tag = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Tag'),
        queryset = Tag.objects.order_by('tag_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    case = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Case'),
        queryset = Case.objects.order_by('case_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # large text area for line separated systemlist
    systemlist = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 20,
                'placeholder': 'One systemname per line',
                'autofocus': 'autofocus',
            },
        ),
        label = 'System list',
    )

    class Meta:

        # model
        model = System

        # this HTML forms are shown
        fields = (
            'systemstatus',
            'analysisstatus',
            'reason',
            'systemtype',
            'domain',
            'dnsname',
            'os',
            'osarch',
            'company',
            'location',
            'serviceprovider',
            'contact',
            'tag',
            'case',
        )

        # special form type or option
        widgets = {
            'osarch': forms.RadioSelect(),
        }

class SystemModificatorForm(AdminStyleSelectorForm):

    def __init__(self, *args, **kwargs):
        self.use_system_charfield = kwargs.pop('use_system_charfield', False)
        super(SystemModificatorForm, self).__init__(*args, **kwargs)
        # if use_system_charfield is set, we replace the ModelMultipleChoiceField with the (old) CharField for system selection
        if self.use_system_charfield:
            self.fields['systemlist'] = forms.CharField(
                widget=forms.Textarea(
                    attrs={
                        'rows': 20,
                        'placeholder': 'One systemname per line',
                        'autofocus': 'autofocus',
                    },
                ),
                label = 'System list',
            )

    # admin UI style system chooser
    systemlist = forms.ModelMultipleChoiceField(
        queryset = System.objects.order_by('system_name'),
        widget = FilteredSelectMultiple('Systems', is_stacked=False),
        required = True,
        label = 'System list',
    )

    # show all existing tag objects as multiple choice field
    tag = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.order_by('tag_name'),
        widget = forms.CheckboxSelectMultiple(),
        required = False,
        label = 'Tag',
    )

    # show all existing company objects as multiple choice field
    company = forms.ModelMultipleChoiceField(
        queryset = Company.objects.order_by('company_name'),
        widget = forms.CheckboxSelectMultiple(),
        required = False,
        label = 'Company',
    )

    # reorder field choices
    systemstatus = forms.ModelChoiceField(
        queryset = Systemstatus.objects.order_by('systemstatus_name'),
        label = 'Systemstatus',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    analysisstatus = forms.ModelChoiceField(
        queryset = Analysisstatus.objects.order_by('analysisstatus_name'),
        label = 'Analysisstatus',
        required = False,
        widget = forms.RadioSelect(),
    )

    class Meta:
        model = System
        # this HTML forms are shown
        fields = (
            'location',
            'serviceprovider',
            'contact',
            'systemstatus',
            'analysisstatus',
        )
        # special form type or option
        widgets = {
            'location': forms.RadioSelect(),
            'serviceprovider': forms.RadioSelect(),
            'contact': forms.RadioSelect(),
        }

class SystemtypeForm(forms.ModelForm):

    class Meta:

        # model
        model = Systemtype

        # this HTML forms are shown
        fields = (
            'systemtype_name',
        )

        # non default form labeling
        labels = {
            'systemtype_name': gettext_lazy('Systemtype name (*)'),
        }

        # special form type or option
        widgets = {
            'systemtype_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class SystemuserForm(forms.ModelForm):

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System (*)'),
        queryset = System.objects.order_by('system_name'),
    )

    class Meta:

        # model
        model = Systemuser

        # this HTML forms are shown
        fields = (
            'systemuser_name',
            'systemuser_lastlogon_time',
            'systemuser_is_systemadmin',
            'system',
        )

        # non default form labeling
        labels = {
            'systemuser_name': gettext_lazy('Systemuser name (*)'),
            'systemuser_lastlogon_time': gettext_lazy('Last logon time (YYYY-MM-DD HH:MM:SS)'),
        }

        # special form type or option
        widgets = {
            'systemuser_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class TagForm(forms.ModelForm):

    # reorder field choices
    tagcolor = forms.ModelChoiceField(
        label = gettext_lazy('Tag color (*)'),
        queryset = Tagcolor.objects.order_by('tagcolor_name'),
    )

    class Meta:

        # model
        model = Tag

        # this HTML forms are shown
        fields = (
            'tag_name',
            'tagcolor',
            'tag_note',
        )

        # non default form labeling
        labels = {
            'tag_name': gettext_lazy('Tag name (*)'),
            'tag_note': gettext_lazy('Tag note'),
        }

        # special form type or option
        widgets = {
            'tag_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }

class TagCreatorForm(forms.Form):

    # show all existing tag objects as multiple choice field
    tag = forms.ModelMultipleChoiceField(
        queryset = Tag.objects.order_by('tag_name'),
        widget = forms.CheckboxSelectMultiple(),
        label = 'Tags (*)',
    )

    # show all existing system objects as multiple choice field
    system = forms.ModelMultipleChoiceField(
        queryset = System.objects.order_by('system_name'),
        widget = forms.CheckboxSelectMultiple(),
        label = 'Systems (*)',
    )

class TaskForm(forms.ModelForm):

    # reorder field choices
    taskpriority = forms.ModelChoiceField(
        queryset = Taskpriority.objects.order_by('taskpriority_name'),
        label = 'Taskpriority',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    taskstatus = forms.ModelChoiceField(
        queryset = Taskstatus.objects.order_by('taskstatus_name'),
        label = 'Taskstatus',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    taskname = forms.ModelChoiceField(
        label = gettext_lazy('Taskname'),
        queryset = Taskname.objects.order_by('taskname_name'),
    )

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System'),
        queryset = System.objects.order_by('system_name'),
        required = False,
    )

    # reorder field choices
    task_assigned_to_user_id = forms.ModelChoiceField(
        label = gettext_lazy('Task assigned to user id'),
        queryset = User.objects.order_by('username'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    tag = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Tag'),
        queryset = Tag.objects.order_by('tag_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:

        # model
        model = Task

        # this HTML forms are shown
        fields = (
            'taskname',
            'parent_task',
            'taskpriority',
            'taskstatus',
            'system',
            'task_assigned_to_user_id',
            'task_note',
            'tag',
            'task_scheduled_time',
            'task_due_time',
        )

        # special form type or option
        widgets = {
            'parent_task': forms.Select(),
            'task_note': forms.Textarea(attrs={'rows': 10}),
            'task_scheduled_time': forms.DateTimeInput(),
            'task_due_time': forms.DateTimeInput(),
        }

class TaskCreatorForm(AdminStyleSelectorForm):

    # show all existing taskname objects as multiple choice field
    taskname = forms.ModelMultipleChoiceField(
        queryset = Taskname.objects.order_by('taskname_name'),
        widget = forms.CheckboxSelectMultiple(),
        label = 'Tasknames',
    )

    # reorder field choices
    taskpriority = forms.ModelChoiceField(
        queryset = Taskpriority.objects.order_by('taskpriority_name'),
        label = 'Taskpriority',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    taskstatus = forms.ModelChoiceField(
        queryset = Taskstatus.objects.order_by('taskstatus_name'),
        label = 'Taskstatus',
        required = True,
        widget = forms.RadioSelect(),
    )

    # admin UI style system chooser
    system = forms.ModelMultipleChoiceField(
        queryset = System.objects.order_by('system_name'),
        widget = FilteredSelectMultiple('Systems', is_stacked=False),
        label = 'Systems',
    )

    # reorder field choices
    task_assigned_to_user_id = forms.ModelChoiceField(
        label = gettext_lazy('Task assigned to user id'),
        queryset = User.objects.order_by('username'),
        required = False,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    tag = forms.ModelMultipleChoiceField(
        label = gettext_lazy('Tag'),
        queryset = Tag.objects.order_by('tag_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:

        # model
        model = Task

        # this HTML forms are shown
        fields = (
            'taskpriority',
            'taskstatus',
            'task_assigned_to_user_id',
            'task_note',
            'tag',
        )

        # special form type or option
        widgets = {
            'task_note': forms.Textarea(attrs={'rows': 10}),
        }

class TasknameForm(forms.ModelForm):

    class Meta:

        # model
        model = Taskname

        # this HTML forms are shown
        fields = (
            'taskname_name',
        )

        # non default form labeling
        labels = {
            'taskname_name': gettext_lazy('Taskname (*)'),
        }

        # special form type or option
        widgets = {
            'taskname_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }
