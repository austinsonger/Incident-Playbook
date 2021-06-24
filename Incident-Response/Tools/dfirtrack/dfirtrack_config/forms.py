from django import forms
from django.contrib.auth.models import User
from dfirtrack_artifacts.models import Artifactstatus
from dfirtrack_config.models import ArtifactExporterSpreadsheetXlsConfigModel, MainConfigModel, SystemExporterMarkdownConfigModel, SystemExporterSpreadsheetCsvConfigModel, SystemExporterSpreadsheetXlsConfigModel, SystemImporterFileCsvConfigModel
from dfirtrack_main.models import Analysisstatus, Case, Company, Dnsname, Domain, Location, Os, Reason, Recommendation, Serviceprovider, Systemstatus, Systemtype, Tag
import os

class ArtifactExporterSpreadsheetXlsConfigForm(forms.ModelForm):
    """ artifact exporter spreadsheet xls config form """

    class Meta:

        # model
        model = ArtifactExporterSpreadsheetXlsConfigModel

        # this HTML forms are shown
        fields = (
            'artifactlist_xls_choice_artifactstatus',
            'artifactlist_xls_artifact_id',
            'artifactlist_xls_system_id',
            'artifactlist_xls_system_name',
            'artifactlist_xls_artifactstatus',
            'artifactlist_xls_artifactpriority',
            'artifactlist_xls_artifacttype',
            'artifactlist_xls_artifact_source_path',
            'artifactlist_xls_artifact_storage_path',
            'artifactlist_xls_artifact_note_internal',
            'artifactlist_xls_artifact_note_external',
            'artifactlist_xls_artifact_note_analysisresult',
            'artifactlist_xls_artifact_md5',
            'artifactlist_xls_artifact_sha1',
            'artifactlist_xls_artifact_sha256',
            'artifactlist_xls_artifact_create_time',
            'artifactlist_xls_artifact_modify_time',
            'artifactlist_xls_worksheet_artifactstatus',
            'artifactlist_xls_worksheet_artifacttype',
        )

        labels = {
            'artifactlist_xls_choice_artifactstatus': 'Export only artifacts with this artifactstatus',
            'artifactlist_xls_artifact_id': 'Export artifact ID',
            'artifactlist_xls_system_id': 'Export system ID',
            'artifactlist_xls_system_name': 'Export system name',
            'artifactlist_xls_artifactstatus': 'Export artifactstatus',
            'artifactlist_xls_artifactpriority': 'Export artifactpriority',
            'artifactlist_xls_artifacttype': 'Export artifacttype',
            'artifactlist_xls_artifact_source_path': 'Export source path',
            'artifactlist_xls_artifact_storage_path': 'Export storage path',
            'artifactlist_xls_artifact_note_internal': 'Export internal note',
            'artifactlist_xls_artifact_note_external': 'Export external note',
            'artifactlist_xls_artifact_note_analysisresult': 'Export analysis result',
            'artifactlist_xls_artifact_md5': 'Export MD5',
            'artifactlist_xls_artifact_sha1': 'Export SHA1',
            'artifactlist_xls_artifact_sha256': 'Export SHA256',
            'artifactlist_xls_artifact_create_time': 'Export create time',
            'artifactlist_xls_artifact_modify_time': 'Export modify time',
            'artifactlist_xls_worksheet_artifactstatus': 'Export worksheet to explain artifactstatus',
            'artifactlist_xls_worksheet_artifacttype': 'Export worksheet to explain artifacttype',
        }

        widgets = {
            'artifactlist_xls_choice_artifactstatus': forms.CheckboxSelectMultiple(),
        }

class MainConfigForm(forms.ModelForm):
    """ main config form """

# TODO: add logic to prevent messing up the same be editing it via admin menu

    # reorder field choices
    artifactstatus_open = forms.ModelMultipleChoiceField(
        queryset = Artifactstatus.objects.order_by('artifactstatus_name'),
        label = 'Artifactstatus to be considered open',
        required = False,
        widget = forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    artifactstatus_requested = forms.ModelMultipleChoiceField(
        queryset = Artifactstatus.objects.order_by('artifactstatus_name'),
        label = 'Artifactstatus setting the artifact requested time',
        required = False,
        widget = forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    artifactstatus_acquisition = forms.ModelMultipleChoiceField(
        queryset = Artifactstatus.objects.order_by('artifactstatus_name'),
        label = 'Artifactstatus setting the artifact acquisition time',
        required = False,
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:

        # model
        model = MainConfigModel

        # this HTML forms are shown
        fields = (
            'system_name_editable',
            'artifactstatus_open',
            'artifactstatus_requested',
            'artifactstatus_acquisition',
            'statushistory_entry_numbers',
            'cron_export_path',
            'cron_username',
        )

        labels = {
            'system_name_editable': 'Make system name editable',
            'statushistory_entry_numbers': 'Show only this number of last statushistory entries',
            'cron_export_path': 'Export files created by scheduled tasks to this path',
            'cron_username': 'Use this username for scheduled tasks (just for logging, does not have to exist)',
        }

        widgets = {
            'statushistory_entry_numbers': forms.NumberInput(
                attrs={
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'cron_export_path': forms.TextInput(
                attrs={
                    'size': '35',
                    'style': 'font-family: monospace',
                },
            ),
            'cron_username': forms.TextInput(
                attrs={
                    'size': '20',
                },
            ),
        }

    def clean(self):
        """ custom field validation """

        # get form data
        cleaned_data = super().clean()

        # get relevant values
        artifactstatus_requested = self.cleaned_data['artifactstatus_requested']
        artifactstatus_acquisition = self.cleaned_data['artifactstatus_acquisition']

        # get artifactstatus that have been choosen for both time settings
        artifactstatus_shared = artifactstatus_requested.intersection(artifactstatus_acquisition)

        # check if there are any artifactstatus in this queryset
        if artifactstatus_shared.count() !=0:
            raise forms.ValidationError('Same artifactstatus were chosen for requested an acquisition time.')

        return cleaned_data

class SystemExporterMarkdownConfigForm(forms.ModelForm):
    """ system exporter markdown config form """

    class Meta:

        # model
        model = SystemExporterMarkdownConfigModel

        # this HTML forms are shown
        fields = (
            'markdown_path',
            'markdown_sorting',
        )

        labels = {
            'markdown_path': 'Path for the markdown documentation export',
            'markdown_sorting': 'Choose sorting for system markdown export',
        }

        widgets = {
            'markdown_path': forms.TextInput(attrs={
                'size': '55',
                'style': 'font-family: monospace',
            }),
            'markdown_sorting': forms.RadioSelect(),
        }

class SystemExporterSpreadsheetCsvConfigForm(forms.ModelForm):
    """ system exporter spreadsheet CSV config form """

    class Meta:

        # model
        model = SystemExporterSpreadsheetCsvConfigModel

        # this HTML forms are shown
        fields = (
            'spread_csv_system_id',
            'spread_csv_dnsname',
            'spread_csv_domain',
            'spread_csv_systemstatus',
            'spread_csv_analysisstatus',
            'spread_csv_reason',
            'spread_csv_recommendation',
            'spread_csv_systemtype',
            'spread_csv_ip',
            'spread_csv_os',
            'spread_csv_company',
            'spread_csv_location',
            'spread_csv_serviceprovider',
            'spread_csv_tag',
            'spread_csv_case',
            'spread_csv_system_create_time',
            'spread_csv_system_modify_time',
        )

        labels = {
            'spread_csv_system_id': 'Export system ID',
            'spread_csv_dnsname': 'Export DNS name',
            'spread_csv_domain': 'Export domain',
            'spread_csv_systemstatus': 'Export systemstatus',
            'spread_csv_analysisstatus': 'Export analysisstatus',
            'spread_csv_reason': 'Export reason',
            'spread_csv_recommendation': 'Export recommendation',
            'spread_csv_systemtype': 'Export systemtype',
            'spread_csv_ip': 'Export IP',
            'spread_csv_os': 'Export OS',
            'spread_csv_company': 'Export company',
            'spread_csv_location': 'Export location',
            'spread_csv_serviceprovider': 'Export serviceprovider',
            'spread_csv_tag': 'Export tag',
            'spread_csv_case': 'Export case',
            'spread_csv_system_create_time': 'Export system create time',
            'spread_csv_system_modify_time': 'Export system modify time',
        }

class SystemExporterSpreadsheetXlsConfigForm(forms.ModelForm):
    """ system exporter spreadsheet XLS config form """

    class Meta:

        # model
        model = SystemExporterSpreadsheetXlsConfigModel

        # this HTML forms are shown
        fields = (
            'spread_xls_system_id',
            'spread_xls_dnsname',
            'spread_xls_domain',
            'spread_xls_systemstatus',
            'spread_xls_analysisstatus',
            'spread_xls_reason',
            'spread_xls_recommendation',
            'spread_xls_systemtype',
            'spread_xls_ip',
            'spread_xls_os',
            'spread_xls_company',
            'spread_xls_location',
            'spread_xls_serviceprovider',
            'spread_xls_tag',
            'spread_xls_case',
            'spread_xls_system_create_time',
            'spread_xls_system_modify_time',
            'spread_xls_worksheet_systemstatus',
            'spread_xls_worksheet_analysisstatus',
            'spread_xls_worksheet_reason',
            'spread_xls_worksheet_recommendation',
            'spread_xls_worksheet_tag',
        )

        labels = {
            'spread_xls_system_id': 'Export system ID',
            'spread_xls_dnsname': 'Export DNS name',
            'spread_xls_domain': 'Export domain',
            'spread_xls_systemstatus': 'Export systemstatus',
            'spread_xls_analysisstatus': 'Export analysisstatus',
            'spread_xls_reason': 'Export reason',
            'spread_xls_recommendation': 'Export recommendation',
            'spread_xls_systemtype': 'Export systemtype',
            'spread_xls_ip': 'Export IP',
            'spread_xls_os': 'Export OS',
            'spread_xls_company': 'Export company',
            'spread_xls_location': 'Export location',
            'spread_xls_serviceprovider': 'Export serviceprovider',
            'spread_xls_tag': 'Export tag',
            'spread_xls_case': 'Export case',
            'spread_xls_system_create_time': 'Export system create time',
            'spread_xls_system_modify_time': 'Export system modify time',
            'spread_xls_worksheet_systemstatus': 'Export worksheet to explain systemstatus',
            'spread_xls_worksheet_analysisstatus': 'Export worksheet to explain analysisstatus',
            'spread_xls_worksheet_reason': 'Export worksheet to explain reason',
            'spread_xls_worksheet_recommendation': 'Export worksheet to explain recommendation',
            'spread_xls_worksheet_tag': 'Export worksheet to explain tag',
        }

class SystemImporterFileCsvConfigForm(forms.ModelForm):
    """ system importer CSV config form """

    # reorder field choices
    csv_import_username = forms.ModelChoiceField(
        queryset = User.objects.order_by('username'),
        label = 'Use this user for the import (*)',
        required = True,
        widget = forms.RadioSelect(),
    )

    # reorder field choices
    csv_default_systemstatus = forms.ModelChoiceField(
        queryset = Systemstatus.objects.order_by('systemstatus_name'),
        label = 'Set from database (*)',
        required = True,
    )

    # reorder field choices
    csv_default_analysisstatus = forms.ModelChoiceField(
        queryset = Analysisstatus.objects.order_by('analysisstatus_name'),
        label = 'Set from database (*)',
        required = True,
    )

    # reorder field choices
    csv_default_tagfree_systemstatus = forms.ModelChoiceField(
        queryset = Systemstatus.objects.order_by('systemstatus_name'),
        label = 'Set from database (no tags assigned)',
        required = True,
    )

    # reorder field choices
    csv_default_tagfree_analysisstatus = forms.ModelChoiceField(
        queryset = Analysisstatus.objects.order_by('analysisstatus_name'),
        label = 'Set from database (no tags assigned)',
        required = True,
    )

    # reorder field choices
    csv_default_dnsname = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Dnsname.objects.order_by('dnsname_name'),
        required = False,
    )

    # reorder field choices
    csv_default_domain = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Domain.objects.order_by('domain_name'),
        required = False,
    )

    # reorder field choices
    csv_default_location = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Location.objects.order_by('location_name'),
        required = False,
    )

    # reorder field choices
    csv_default_os = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Os.objects.order_by('os_name'),
        required = False,
    )

    # reorder field choices
    csv_default_reason = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Reason.objects.order_by('reason_name'),
        required = False,
    )

    # reorder field choices
    csv_default_recommendation = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Recommendation.objects.order_by('recommendation_name'),
        required = False,
    )

    # reorder field choices
    csv_default_serviceprovider = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Serviceprovider.objects.order_by('serviceprovider_name'),
        required = False,
    )

    # reorder field choices
    csv_default_systemtype = forms.ModelChoiceField(
        label = 'Set from database',
        queryset = Systemtype.objects.order_by('systemtype_name'),
        required = False,
    )

    # reorder field choices
    csv_default_case = forms.ModelMultipleChoiceField(
        label = 'Set from database',
        queryset = Case.objects.order_by('case_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    csv_default_company = forms.ModelMultipleChoiceField(
        label = 'Set from database',
        queryset = Company.objects.order_by('company_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    # reorder field choices
    csv_default_tag = forms.ModelMultipleChoiceField(
        label = 'Set from database',
        queryset = Tag.objects.order_by('tag_name'),
        required = False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:

        # model
        model = SystemImporterFileCsvConfigModel

        # this HTML forms are shown
        fields = (
            'csv_column_system',
            'csv_skip_existing_system',
            'csv_headline',
            'csv_import_path',
            'csv_import_filename',
            'csv_import_username',
            'csv_default_systemstatus',
            'csv_remove_systemstatus',
            'csv_default_analysisstatus',
            'csv_remove_analysisstatus',
            'csv_choice_tagfree_systemstatus',
            'csv_default_tagfree_systemstatus',
            'csv_choice_tagfree_analysisstatus',
            'csv_default_tagfree_analysisstatus',
            'csv_tag_lock_systemstatus',
            'csv_tag_lock_analysisstatus',
            'csv_choice_ip',
            'csv_column_ip',
            'csv_remove_ip',
            'csv_choice_dnsname',
            'csv_column_dnsname',
            'csv_default_dnsname',
            'csv_remove_dnsname',
            'csv_choice_domain',
            'csv_column_domain',
            'csv_default_domain',
            'csv_remove_domain',
            'csv_choice_location',
            'csv_column_location',
            'csv_default_location',
            'csv_remove_location',
            'csv_choice_os',
            'csv_column_os',
            'csv_default_os',
            'csv_remove_os',
            'csv_choice_reason',
            'csv_column_reason',
            'csv_default_reason',
            'csv_remove_reason',
            'csv_choice_recommendation',
            'csv_column_recommendation',
            'csv_default_recommendation',
            'csv_remove_recommendation',
            'csv_choice_serviceprovider',
            'csv_column_serviceprovider',
            'csv_default_serviceprovider',
            'csv_remove_serviceprovider',
            'csv_choice_systemtype',
            'csv_column_systemtype',
            'csv_default_systemtype',
            'csv_remove_systemtype',
            'csv_choice_case',
            'csv_column_case',
            'csv_default_case',
            'csv_remove_case',
            'csv_choice_company',
            'csv_column_company',
            'csv_default_company',
            'csv_remove_company',
            'csv_choice_tag',
            'csv_column_tag',
            'csv_default_tag',
            'csv_remove_tag',
            'csv_tag_prefix',
            'csv_tag_prefix_delimiter',
            'csv_field_delimiter',
            'csv_text_quote',
            'csv_ip_delimiter',
            'csv_tag_delimiter',
        )

        labels = {
            'csv_column_system': 'CSV column (*)',
            'csv_skip_existing_system': 'Skip existing systems',
            'csv_headline': 'CSV file contains a headline row',
            'csv_import_path': 'Path to CSV file (*)',
            'csv_import_filename': 'File name of CSV file (*)',
            'csv_remove_systemstatus': 'Overwrite for existing systems',
            'csv_remove_analysisstatus': 'Overwrite for existing systems',
            'csv_choice_tagfree_systemstatus': 'Set alternative (no tags assigned)',
            'csv_choice_tagfree_analysisstatus': 'Set alternative (no tags assigned)',
            'csv_tag_lock_systemstatus': 'Tag that preserves systemstatus (*)',
            'csv_tag_lock_analysisstatus': 'Tag that preserves analysisstatus (*)',
            'csv_choice_ip': 'Set from CSV',
            'csv_column_ip': 'CSV column',
            'csv_remove_ip': 'Overwrite for existing systems',
            'csv_choice_dnsname': 'Set from CSV',
            'csv_column_dnsname': 'CSV column',
            'csv_remove_dnsname': 'Overwrite for existing systems',
            'csv_choice_domain': 'Set from CSV',
            'csv_column_domain': 'CSV column',
            'csv_remove_domain': 'Overwrite for existing systems',
            'csv_choice_location': 'Set from CSV',
            'csv_column_location': 'CSV column',
            'csv_remove_location': 'Overwrite for existing systems',
            'csv_choice_os': 'Set from CSV',
            'csv_column_os': 'CSV column',
            'csv_remove_os': 'Overwrite for existing systems',
            'csv_choice_reason': 'Set from CSV',
            'csv_column_reason': 'CSV column',
            'csv_remove_reason': 'Overwrite for existing systems',
            'csv_choice_recommendation': 'Set from CSV',
            'csv_column_recommendation': 'CSV column',
            'csv_remove_recommendation': 'Overwrite for existing systems',
            'csv_choice_serviceprovider': 'Set from CSV',
            'csv_column_serviceprovider': 'CSV column',
            'csv_remove_serviceprovider': 'Overwrite for existing systems',
            'csv_choice_systemtype': 'Set from CSV',
            'csv_column_systemtype': 'CSV column',
            'csv_remove_systemtype': 'Overwrite for existing systems',
            'csv_choice_case': 'Set from CSV',
            'csv_column_case': 'CSV column',
            'csv_remove_case': 'Overwrite for existing systems',
            'csv_choice_company': 'Set from CSV',
            'csv_column_company': 'CSV column',
            'csv_remove_company': 'Overwrite for existing systems',
            'csv_choice_tag': 'Set from CSV',
            'csv_column_tag': 'CSV column',
            'csv_remove_tag': 'Overwrite for existing systems',
            'csv_tag_prefix': 'Prefix for tags imported via CSV',
            'csv_tag_prefix_delimiter': 'Delimiter to separate prefix from tag',
            'csv_field_delimiter': 'CSV field delimiter',
            'csv_text_quote': 'CSV text quotation mark',
            'csv_ip_delimiter': 'IP address delimiter (within CSV field)',
            'csv_tag_delimiter': 'Tag delimiter (within CSV field)',
        }

        widgets = {
            'csv_column_system': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_import_path': forms.TextInput(
                attrs={
                    'size': '50',
                    'style': 'font-family: monospace',
                },
            ),
            'csv_import_filename': forms.TextInput(
                attrs={
                    'size': '50',
                    'style': 'font-family: monospace',
                },
            ),
            'csv_tag_lock_systemstatus': forms.TextInput(
                attrs={
                    'size': '20',
                },
            ),
            'csv_tag_lock_systemstatus': forms.TextInput(
                attrs={
                    'size': '20',
                },
            ),
            'csv_column_ip': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_dnsname': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_domain': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_location': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_os': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_reason': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_recommendation': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_serviceprovider': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_systemtype': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_case': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_company': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
            'csv_column_tag': forms.NumberInput(
                attrs={
                    #'style': 'width:6ch',
                    'min': '1',
                    'max': '99',
                    'size': '3',
                },
            ),
        }

    def clean(self):
        """ custom field validation """

        """ prepare validation errors """

        # get form data
        cleaned_data = super().clean()

        # create dict for validation errors
        validation_errors = {}

        """ prepare validation error strings """

        MISSING_CSV_CHOICE_STRING = 'Forgot to choose CSV?'
        MISSING_CSV_COLUMN_STRING = 'Add CSV column.'
        EITHER_CSV_OR_DATABASE_STRING = 'Decide between CSV or database or nothing.'
        EITHER_SKIP_OR_REMOVE_STRING = 'This choice is only valid if existing systems are not skipped. Either disable this option or disable skipping existing systems.'
        REMOVE_STRING = 'This choice is only valid if attribute is selected.'

        """ check for EITHER 'choice' and 'column' OR 'default' """

        # ip - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_ip'] and not self.cleaned_data['csv_column_ip']:
            validation_errors['csv_choice_ip'] = MISSING_CSV_COLUMN_STRING
        # ip - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_ip'] and self.cleaned_data['csv_column_ip']:
            validation_errors['csv_choice_ip'] = MISSING_CSV_CHOICE_STRING

        # dnsname - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_dnsname'] and not self.cleaned_data['csv_column_dnsname']:
            validation_errors['csv_choice_dnsname'] = MISSING_CSV_COLUMN_STRING
        # dnsname - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_dnsname'] and self.cleaned_data['csv_column_dnsname']:
            validation_errors['csv_choice_dnsname'] = MISSING_CSV_CHOICE_STRING
        # dnsname - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_dnsname'] and self.cleaned_data['csv_default_dnsname']:
            validation_errors['csv_choice_dnsname'] = EITHER_CSV_OR_DATABASE_STRING
        # dnsname - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_dnsname'] and self.cleaned_data['csv_default_dnsname']:
            validation_errors['csv_choice_dnsname'] = EITHER_CSV_OR_DATABASE_STRING

        # domain - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_domain'] and not self.cleaned_data['csv_column_domain']:
            validation_errors['csv_choice_domain'] = MISSING_CSV_COLUMN_STRING
        # domain - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_domain'] and self.cleaned_data['csv_column_domain']:
            validation_errors['csv_choice_domain'] = MISSING_CSV_CHOICE_STRING
        # domain - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_domain'] and self.cleaned_data['csv_default_domain']:
            validation_errors['csv_choice_domain'] = EITHER_CSV_OR_DATABASE_STRING
        # domain - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_domain'] and self.cleaned_data['csv_default_domain']:
            validation_errors['csv_choice_domain'] = EITHER_CSV_OR_DATABASE_STRING

        # location - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_location'] and not self.cleaned_data['csv_column_location']:
            validation_errors['csv_choice_location'] = MISSING_CSV_COLUMN_STRING
        # location - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_location'] and self.cleaned_data['csv_column_location']:
            validation_errors['csv_choice_location'] = MISSING_CSV_CHOICE_STRING
        # location - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_location'] and self.cleaned_data['csv_default_location']:
            validation_errors['csv_choice_location'] = EITHER_CSV_OR_DATABASE_STRING
        # location - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_location'] and self.cleaned_data['csv_default_location']:
            validation_errors['csv_choice_location'] = EITHER_CSV_OR_DATABASE_STRING

        # os - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_os'] and not self.cleaned_data['csv_column_os']:
            validation_errors['csv_choice_os'] = MISSING_CSV_COLUMN_STRING
        # os - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_os'] and self.cleaned_data['csv_column_os']:
            validation_errors['csv_choice_os'] = MISSING_CSV_CHOICE_STRING
        # os - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_os'] and self.cleaned_data['csv_default_os']:
            validation_errors['csv_choice_os'] = EITHER_CSV_OR_DATABASE_STRING
        # os - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_os'] and self.cleaned_data['csv_default_os']:
            validation_errors['csv_choice_os'] = EITHER_CSV_OR_DATABASE_STRING

        # reason - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_reason'] and not self.cleaned_data['csv_column_reason']:
            validation_errors['csv_choice_reason'] = MISSING_CSV_COLUMN_STRING
        # reason - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_reason'] and self.cleaned_data['csv_column_reason']:
            validation_errors['csv_choice_reason'] = MISSING_CSV_CHOICE_STRING
        # reason - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_reason'] and self.cleaned_data['csv_default_reason']:
            validation_errors['csv_choice_reason'] = EITHER_CSV_OR_DATABASE_STRING
        # reason - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_reason'] and self.cleaned_data['csv_default_reason']:
            validation_errors['csv_choice_reason'] = EITHER_CSV_OR_DATABASE_STRING

        # recommendation - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_recommendation'] and not self.cleaned_data['csv_column_recommendation']:
            validation_errors['csv_choice_recommendation'] = MISSING_CSV_COLUMN_STRING
        # recommendation - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_recommendation'] and self.cleaned_data['csv_column_recommendation']:
            validation_errors['csv_choice_recommendation'] = MISSING_CSV_CHOICE_STRING
        # recommendation - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_recommendation'] and self.cleaned_data['csv_default_recommendation']:
            validation_errors['csv_choice_recommendation'] = EITHER_CSV_OR_DATABASE_STRING
        # recommendation - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_recommendation'] and self.cleaned_data['csv_default_recommendation']:
            validation_errors['csv_choice_recommendation'] = EITHER_CSV_OR_DATABASE_STRING

        # serviceprovider - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_serviceprovider'] and not self.cleaned_data['csv_column_serviceprovider']:
            validation_errors['csv_choice_serviceprovider'] = MISSING_CSV_COLUMN_STRING
        # serviceprovider - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_serviceprovider'] and self.cleaned_data['csv_column_serviceprovider']:
            validation_errors['csv_choice_serviceprovider'] = MISSING_CSV_CHOICE_STRING
        # serviceprovider - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_serviceprovider'] and self.cleaned_data['csv_default_serviceprovider']:
            validation_errors['csv_choice_serviceprovider'] = EITHER_CSV_OR_DATABASE_STRING
        # serviceprovider - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_serviceprovider'] and self.cleaned_data['csv_default_serviceprovider']:
            validation_errors['csv_choice_serviceprovider'] = EITHER_CSV_OR_DATABASE_STRING

        # systemtype - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_systemtype'] and not self.cleaned_data['csv_column_systemtype']:
            validation_errors['csv_choice_systemtype'] = MISSING_CSV_COLUMN_STRING
        # systemtype - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_systemtype'] and self.cleaned_data['csv_column_systemtype']:
            validation_errors['csv_choice_systemtype'] = MISSING_CSV_CHOICE_STRING
        # systemtype - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_systemtype'] and self.cleaned_data['csv_default_systemtype']:
            validation_errors['csv_choice_systemtype'] = EITHER_CSV_OR_DATABASE_STRING
        # systemtype - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_systemtype'] and self.cleaned_data['csv_default_systemtype']:
            validation_errors['csv_choice_systemtype'] = EITHER_CSV_OR_DATABASE_STRING

        # case - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_case'] and not self.cleaned_data['csv_column_case']:
            validation_errors['csv_choice_case'] = MISSING_CSV_COLUMN_STRING
        # case - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_case'] and self.cleaned_data['csv_column_case']:
            validation_errors['csv_choice_case'] = MISSING_CSV_CHOICE_STRING
        # case - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_case'] and self.cleaned_data['csv_default_case']:
            validation_errors['csv_choice_case'] = EITHER_CSV_OR_DATABASE_STRING
        # case - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_case'] and self.cleaned_data['csv_default_case']:
            validation_errors['csv_choice_case'] = EITHER_CSV_OR_DATABASE_STRING

        # company - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_company'] and not self.cleaned_data['csv_column_company']:
            validation_errors['csv_choice_company'] = MISSING_CSV_COLUMN_STRING
        # company - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_company'] and self.cleaned_data['csv_column_company']:
            validation_errors['csv_choice_company'] = MISSING_CSV_CHOICE_STRING
        # company - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_company'] and self.cleaned_data['csv_default_company']:
            validation_errors['csv_choice_company'] = EITHER_CSV_OR_DATABASE_STRING
        # company - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_company'] and self.cleaned_data['csv_default_company']:
            validation_errors['csv_choice_company'] = EITHER_CSV_OR_DATABASE_STRING

        # tag - CSV chosen and no CSV column filled out
        if self.cleaned_data['csv_choice_tag'] and not self.cleaned_data['csv_column_tag']:
            validation_errors['csv_choice_tag'] = MISSING_CSV_COLUMN_STRING
        # tag - CSV not chosen and CSV column filled out
        if not self.cleaned_data['csv_choice_tag'] and self.cleaned_data['csv_column_tag']:
            validation_errors['csv_choice_tag'] = MISSING_CSV_CHOICE_STRING
        # tag - CSV chosen and DB chosen
        if self.cleaned_data['csv_choice_tag'] and self.cleaned_data['csv_default_tag']:
            validation_errors['csv_choice_tag'] = EITHER_CSV_OR_DATABASE_STRING
        # tag - CSV column filled out and DB chosen
        if self.cleaned_data['csv_column_tag'] and self.cleaned_data['csv_default_tag']:
            validation_errors['csv_choice_tag'] = EITHER_CSV_OR_DATABASE_STRING

        """ check tag pefix and delimiter in combination with CSV and DB """

        # tag - CSV chosen and prefix and / or prefix delimiter not set
        if self.cleaned_data['csv_choice_tag'] and (not self.cleaned_data['csv_tag_prefix'] or not self.cleaned_data['csv_tag_prefix_delimiter']):
            validation_errors['csv_tag_prefix'] = 'Choose prefix and delimiter for tag import from CSV to distinguish between manual set tags.'
        # tag - DB chosen and prefix and / or prefix delimiter chosen (overwrites error above)
        if self.cleaned_data['csv_default_tag'] and (self.cleaned_data['csv_tag_prefix'] or self.cleaned_data['csv_tag_prefix_delimiter']):
                validation_errors['csv_tag_prefix'] = 'Prefix and delimiter are not available when setting tags from database.'
        # tag - DB chosen but special option 'tag_remove_prefix' set
        if self.cleaned_data['csv_remove_tag'] == 'tag_remove_prefix' and self.cleaned_data['csv_default_tag']:
            validation_errors['csv_remove_tag'] = 'Removing tags with prefix is only available when setting tags from CSV.'

        """ check tagfree choices (systemstatus / analysisstatus) in combination with tag from CSV """

        # tag - alternative choice systemstatus (tagfree) chosen without tag choice from CSV
        if self.cleaned_data['csv_choice_tagfree_systemstatus'] and not self.cleaned_data['csv_choice_tag']:
            validation_errors['csv_choice_tagfree_systemstatus'] = 'Alternative systemstatus only available with tags from CSV.'
        # tag - alternative choice analysisstatus (tagfree) chosen without tag choice from CSV
        if self.cleaned_data['csv_choice_tagfree_analysisstatus'] and not self.cleaned_data['csv_choice_tag']:
            validation_errors['csv_choice_tagfree_analysisstatus'] = 'Alternative analysisstatus only available with tags from CSV.'

        """ check if the column fields are different """

        # create empty dict for column values
        all_columns_dict = {}

        # add column values to dict
        all_columns_dict['csv_column_system'] = self.cleaned_data['csv_column_system']
        if self.cleaned_data['csv_column_ip']:
            all_columns_dict['csv_column_ip'] = self.cleaned_data['csv_column_ip']
        if self.cleaned_data['csv_column_dnsname']:
            all_columns_dict['csv_column_dnsname'] = self.cleaned_data['csv_column_dnsname']
        if self.cleaned_data['csv_column_domain']:
            all_columns_dict['csv_column_domain'] = self.cleaned_data['csv_column_domain']
        if self.cleaned_data['csv_column_location']:
            all_columns_dict['csv_column_location'] = self.cleaned_data['csv_column_location']
        if self.cleaned_data['csv_column_os']:
            all_columns_dict['csv_column_os'] = self.cleaned_data['csv_column_os']
        if self.cleaned_data['csv_column_reason']:
            all_columns_dict['csv_column_reason'] = self.cleaned_data['csv_column_reason']
        if self.cleaned_data['csv_column_recommendation']:
            all_columns_dict['csv_column_recommendation'] = self.cleaned_data['csv_column_recommendation']
        if self.cleaned_data['csv_column_serviceprovider']:
            all_columns_dict['csv_column_serviceprovider'] = self.cleaned_data['csv_column_serviceprovider']
        if self.cleaned_data['csv_column_systemtype']:
            all_columns_dict['csv_column_systemtype'] = self.cleaned_data['csv_column_systemtype']
        if self.cleaned_data['csv_column_case']:
            all_columns_dict['csv_column_case'] = self.cleaned_data['csv_column_case']
        if self.cleaned_data['csv_column_company']:
            all_columns_dict['csv_column_company'] = self.cleaned_data['csv_column_company']
        if self.cleaned_data['csv_column_tag']:
            all_columns_dict['csv_column_tag'] = self.cleaned_data['csv_column_tag']

        # check all column values against each other
        for column in all_columns_dict:

            # explicitly copy dict
            pruned_columns_dict = dict(all_columns_dict)
            # remove column from copied dict
            del pruned_columns_dict[column]
            # check for the same value in pruned dict
            if all_columns_dict[column] in pruned_columns_dict.values():
                # add error to validation error dict
                validation_errors[str(column)] = 'The column has to be unique.'

        """ check remove conditions in combination with skip condition """

        # remove systemstatus
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_systemstatus']:
            validation_errors['csv_remove_systemstatus'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove analysisstatus
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_analysisstatus']:
            validation_errors['csv_remove_analysisstatus'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove ip
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_ip']:
            validation_errors['csv_remove_ip'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove dnsname
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_dnsname']:
            validation_errors['csv_remove_dnsname'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove domain
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_domain']:
            validation_errors['csv_remove_domain'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove location
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_location']:
            validation_errors['csv_remove_location'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove os
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_os']:
            validation_errors['csv_remove_os'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove reason
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_reason']:
            validation_errors['csv_remove_reason'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove recommendation
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_recommendation']:
            validation_errors['csv_remove_recommendation'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove serviceprovider
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_serviceprovider']:
            validation_errors['csv_remove_serviceprovider'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove systemtype
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_systemtype']:
            validation_errors['csv_remove_systemtype'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove case
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_case']:
            validation_errors['csv_remove_case'] = EITHER_SKIP_OR_REMOVE_STRING
        # remove company
        if self.cleaned_data['csv_skip_existing_system'] and self.cleaned_data['csv_remove_company']:
            validation_errors['csv_remove_company'] = EITHER_SKIP_OR_REMOVE_STRING

        """ check remove conditions without CSV or DB """

        # remove ip
        if not self.cleaned_data['csv_choice_ip'] and self.cleaned_data['csv_remove_ip']:
            validation_errors['csv_remove_ip'] = REMOVE_STRING
        # remove dnsname
        if not (self.cleaned_data['csv_choice_dnsname'] or self.cleaned_data['csv_default_dnsname']) and self.cleaned_data['csv_remove_dnsname']:
            validation_errors['csv_remove_dnsname'] = REMOVE_STRING
        # remove domain
        if not (self.cleaned_data['csv_choice_domain'] or self.cleaned_data['csv_default_domain']) and self.cleaned_data['csv_remove_domain']:
            validation_errors['csv_remove_domain'] = REMOVE_STRING
        # remove location
        if not (self.cleaned_data['csv_choice_location'] or self.cleaned_data['csv_default_location']) and self.cleaned_data['csv_remove_location']:
            validation_errors['csv_remove_location'] = REMOVE_STRING
        # remove os
        if not (self.cleaned_data['csv_choice_os'] or self.cleaned_data['csv_default_os']) and self.cleaned_data['csv_remove_os']:
            validation_errors['csv_remove_os'] = REMOVE_STRING
        # remove reason
        if not (self.cleaned_data['csv_choice_reason'] or self.cleaned_data['csv_default_reason']) and self.cleaned_data['csv_remove_reason']:
            validation_errors['csv_remove_reason'] = REMOVE_STRING
        # remove recommendation
        if not (self.cleaned_data['csv_choice_recommendation'] or self.cleaned_data['csv_default_recommendation']) and self.cleaned_data['csv_remove_recommendation']:
            validation_errors['csv_remove_recommendation'] = REMOVE_STRING
        # remove serviceprovider
        if not (self.cleaned_data['csv_choice_serviceprovider'] or self.cleaned_data['csv_default_serviceprovider']) and self.cleaned_data['csv_remove_serviceprovider']:
            validation_errors['csv_remove_serviceprovider'] = REMOVE_STRING
        # remove systemtype
        if not (self.cleaned_data['csv_choice_systemtype'] or self.cleaned_data['csv_default_systemtype']) and self.cleaned_data['csv_remove_systemtype']:
            validation_errors['csv_remove_systemtype'] = REMOVE_STRING
        # remove case
        if not (self.cleaned_data['csv_choice_case'] or self.cleaned_data['csv_default_case']) and self.cleaned_data['csv_remove_case']:
            validation_errors['csv_remove_case'] = REMOVE_STRING
        # remove company
        if not (self.cleaned_data['csv_choice_company'] or self.cleaned_data['csv_default_company']) and self.cleaned_data['csv_remove_company']:
            validation_errors['csv_remove_company'] = REMOVE_STRING

        """ check file system """

        # build csv file path
        csv_path = self.cleaned_data['csv_import_path'] + '/' + self.cleaned_data['csv_import_filename']

        """
        CSV import file does not exist -> only warning is shown via message to giv to opportunity to prepare the file
        CSV import file is empty -> only warning is shown via message to giv to opportunity to prepare the file
        message implemented in 'dfirtrack_config.importer.file.csv_config_editor.system_importer_file_csv_config_view'
        """

        # CSV import path does not exist - stop immediately
        if not os.path.isdir(self.cleaned_data['csv_import_path']):
            validation_errors['csv_import_path'] = 'CSV import path does not exist.'
        else:
            # CSV import path is not readable - stop immediately
            if not os.access(self.cleaned_data['csv_import_path'], os.R_OK):
                validation_errors['csv_import_path'] = 'No read permission for CSV import path.'
            else:
                # CSV import file does exist but is not readable - stop immediately
                if os.path.isfile(csv_path) and not os.access(csv_path, os.R_OK):
                    validation_errors['csv_import_filename'] = 'No read permission for CSV import file.'

        """ raise error """

        # finally raise validation error
        if validation_errors:
            raise forms.ValidationError(validation_errors)

        return cleaned_data
