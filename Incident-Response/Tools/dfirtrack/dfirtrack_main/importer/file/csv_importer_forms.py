from django import forms

class SystemImporterFileCsvForm(forms.Form):

    # file upload field (variable is used in request object)
    systemcsv = forms.FileField(
        label = 'CSV with systems (*)',
    )
