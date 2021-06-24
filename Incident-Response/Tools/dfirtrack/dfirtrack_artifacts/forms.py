from django import forms
from django.utils.translation import gettext_lazy
from dfirtrack_main.models import System
from dfirtrack_artifacts.models import Artifact, Artifactpriority, Artifactstatus, Artifacttype
import re


class ArtifactForm(forms.ModelForm):

    # reorder field choices
    system = forms.ModelChoiceField(
        label = gettext_lazy('System (*)'),
        queryset = System.objects.order_by('system_name'),
    )

    # reorder field choices
    artifactpriority = forms.ModelChoiceField(
        label = gettext_lazy('Artifactpriority (*)'),
        queryset = Artifactpriority.objects.order_by('artifactpriority_name'),
    )

    # reorder field choices
    artifactstatus = forms.ModelChoiceField(
        label = gettext_lazy('Artifactstatus (*)'),
        queryset = Artifactstatus.objects.order_by('artifactstatus_name'),
    )

    class Meta:

        # model
        model = Artifact

        # this HTML forms are shown
        fields = [
            'artifact_name',
            'artifactpriority',
            'artifactstatus',
            'artifacttype',
            'artifact_source_path',
            'system',
            'case',
            'artifact_md5',
            'artifact_sha1',
            'artifact_sha256',
            'artifact_note_internal',
            'artifact_note_external',
            'artifact_note_analysisresult',
        ]

        # non default form labeling
        labels = {
            'artifact_name': gettext_lazy('Artifact name (*)'),
            'artifacttype': gettext_lazy('Artifacttype (*)'),
            'artifact_md5': gettext_lazy('MD5'),
            'artifact_sha1': gettext_lazy('SHA1'),
            'artifact_sha256': gettext_lazy('SHA256'),
            'artifact_note_internal': gettext_lazy('Internal note'),
            'artifact_note_external': gettext_lazy('External note'),
            'artifact_note_analysisresult': gettext_lazy('Analysis result'),
        }

        # special form type or option
        widgets = {
            'artifact_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
            'artifact_source_path': forms.TextInput(attrs={
                'size': '100',
                'style': 'font-family: monospace',
            }),
            'artifact_md5': forms.TextInput(attrs={
                'size': '32',
                'style': 'font-family: monospace',
            }),
            'artifact_sha1': forms.TextInput(attrs={
                'size': '40',
                'style': 'font-family: monospace',
            }),
            'artifact_sha256': forms.TextInput(attrs={
                'size': '64',
                'style': 'font-family: monospace',
            }),
        }

    def clean(self):
        """ check provided hashes for their length """

        super(ArtifactForm, self).clean()

        # build regular expression that excludes valid hexadecimal characters
        hex_re = re.compile(r'[^a-fA-F0-9.]')

        # check MD5
        artifact_md5 = self.cleaned_data.get('artifact_md5')
        # check if MD5 was provided
        if artifact_md5:
            # check for length
            if len(artifact_md5) < 32:
                self.errors['artifact_md5'] = self.error_class(['MD5 is 32 alphanumeric characters in size (' + str(len(artifact_md5)) + ' were provided)'])
            # check for hexadecimal characters (only if there were enough characters submitted)
            else:
                match = hex_re.search(artifact_md5)
                if match:
                    self.errors['artifact_md5'] = self.error_class(['MD5 contains non-hexadecimal characters'])

        # check SHA1
        artifact_sha1 = self.cleaned_data.get('artifact_sha1')
        # check if SHA1 was provided
        if artifact_sha1:
            # check for length
            if len(artifact_sha1) < 40:
                self.errors['artifact_sha1'] = self.error_class(['SHA1 is 40 alphanumeric characters in size (' + str(len(artifact_sha1)) + ' were provided)'])
            # check for hexadecimal characters (only if there were enough characters submitted)
            else:
                match = hex_re.search(artifact_sha1)
                if match:
                    self.errors['artifact_sha1'] = self.error_class(['SHA1 contains non-hexadecimal characters'])

        # check SHA256
        artifact_sha256 = self.cleaned_data.get('artifact_sha256')
        # check if SHA256 was provided
        if artifact_sha256:
            # check for length
            if len(artifact_sha256) < 64:
                self.errors['artifact_sha256'] = self.error_class(['SHA256 is 64 alphanumeric characters in size (' + str(len(artifact_sha256)) + ' were provided)'])
            # check for hexadecimal characters (only if there were enough characters submitted)
            else:
                match = hex_re.search(artifact_sha256)
                if match:
                    self.errors['artifact_sha256'] = self.error_class(['SHA256 contains non-hexadecimal characters'])

        return self.cleaned_data

class ArtifacttypeForm(forms.ModelForm):

    class Meta:

        # model
        model = Artifacttype

        # this HTML forms are shown
        fields = [
            'artifacttype_name',
            'artifacttype_note',
        ]

        # non default form labeling
        labels = {
            'artifacttype_name': gettext_lazy('Artifacttype name (*)'),
        }

        # special form type or option
        widgets = {
            'artifacttype_name': forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }
