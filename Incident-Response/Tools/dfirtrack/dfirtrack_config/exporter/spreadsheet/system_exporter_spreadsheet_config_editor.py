from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from dfirtrack_config.forms import SystemExporterSpreadsheetCsvConfigForm, SystemExporterSpreadsheetXlsConfigForm
from dfirtrack_config.models import SystemExporterSpreadsheetCsvConfigModel, SystemExporterSpreadsheetXlsConfigModel
from dfirtrack_main.logger.default_logger import info_logger

@login_required(login_url="/login")
def system_exporter_spreadsheet_csv_config_view(request):

    # form was valid to post
    if request.method == "POST":

        # get config model
        model = SystemExporterSpreadsheetCsvConfigModel.objects.get(system_exporter_spreadsheet_csv_config_name = 'SystemExporterSpreadsheetCsvConfig')
        # get form
        form = SystemExporterSpreadsheetCsvConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()

            # create message
            messages.success(request, 'System exporter spreadsheet CSV config changed')

            # call logger
            info_logger(str(request.user), " SYSTEM_EXPORTER_SPREADSHEET_CSV_CONFIG_CHANGED")

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        # TODO: with only non-mandatory model attributes, it is not possible to get an invalid form
        # TODO: finish prepared tests in 'dfirtrack_config.tests.system.test_system_exporter_spreadsheet_csv_config_views'
        # TODO: remove the coverage limitation with further mandatory model attributes
        else:   # coverage: ignore branch
            # show form page again
            return render(
                request,
                'dfirtrack_config/system/system_exporter_spreadsheet_csv_config_popup.html',
                {
                    'form': form,
                }
            )

    else:

        # get config model
        model = SystemExporterSpreadsheetCsvConfigModel.objects.get(system_exporter_spreadsheet_csv_config_name = 'SystemExporterSpreadsheetCsvConfig')
        # get form
        form = SystemExporterSpreadsheetCsvConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/system/system_exporter_spreadsheet_csv_config_popup.html',
        {
            'form': form,
        }
    )

@login_required(login_url="/login")
def system_exporter_spreadsheet_xls_config_view(request):

    # form was valid to post
    if request.method == "POST":

        # get config model
        model = SystemExporterSpreadsheetXlsConfigModel.objects.get(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')
        # get form
        form = SystemExporterSpreadsheetXlsConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()

            # create message
            messages.success(request, 'System exporter spreadsheet XLS config changed')

            # call logger
            info_logger(str(request.user), " SYSTEM_EXPORTER_SPREADSHEET_XLS_CONFIG_CHANGED")

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        # TODO: with only non-mandatory model attributes, it is not possible to get an invalid form
        # TODO: finish prepared tests in 'dfirtrack_config.tests.system.test_system_exporter_spreadsheet_xls_config_views'
        # TODO: remove the coverage limitation with further mandatory model attributes
        else:   # coverage: ignore branch
            # show form page again
            return render(
                request,
                'dfirtrack_config/system/system_exporter_spreadsheet_xls_config_popup.html',
                {
                    'form': form,
                }
            )

    else:

        # get config model
        model = SystemExporterSpreadsheetXlsConfigModel.objects.get(system_exporter_spreadsheet_xls_config_name = 'SystemExporterSpreadsheetXlsConfig')
        # get form
        form = SystemExporterSpreadsheetXlsConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/system/system_exporter_spreadsheet_xls_config_popup.html',
        {
            'form': form,
        }
    )
