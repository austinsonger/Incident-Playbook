from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from dfirtrack_config.forms import ArtifactExporterSpreadsheetXlsConfigForm
from dfirtrack_config.models import ArtifactExporterSpreadsheetXlsConfigModel
from dfirtrack_main.logger.default_logger import info_logger

@login_required(login_url="/login")
def artifact_exporter_spreadsheet_xls_config_view(request):

    # form was valid to post
    if request.method == "POST":

        # get config model
        model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name = 'ArtifactExporterSpreadsheetXlsConfig')
        # get form
        form = ArtifactExporterSpreadsheetXlsConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()
            form.save_m2m()

            # create message
            messages.success(request, 'Artifact exporter spreadsheet XLS config changed')

            # call logger
            info_logger(str(request.user), " ARTIFACT_EXPORTER_SPREADSHEET_XLS_CONFIG_CHANGED")

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        else:
            # show form page
            return render(
                request,
                'dfirtrack_config/artifact/artifact_exporter_spreadsheet_xls_config_popup.html',
                {
                    'form': form,
                }
            )

    else:

        # get config model
        model = ArtifactExporterSpreadsheetXlsConfigModel.objects.get(artifact_exporter_spreadsheet_xls_config_name = 'ArtifactExporterSpreadsheetXlsConfig')
        # get form
        form = ArtifactExporterSpreadsheetXlsConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/artifact/artifact_exporter_spreadsheet_xls_config_popup.html',
        {
            'form': form,
        }
    )
