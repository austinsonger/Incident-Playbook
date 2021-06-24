from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from dfirtrack_config.forms import SystemImporterFileCsvConfigForm
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.logger.default_logger import info_logger
import os


@login_required(login_url="/login")
def system_importer_file_csv_config_view(request):

    # POST request
    if request.method == "POST":

        # get config model
        model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')
        # get form
        form = SystemImporterFileCsvConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()
            form.save_m2m()

            # create message
            messages.success(request, 'System importer file CSV config changed')

            # call logger
            info_logger(str(request.user), " SYSTEM_IMPORTER_FILE_CSV_CONFIG_CHANGED")

            """ check file system """

            # build csv file path
            csv_path = model.csv_import_path + '/' + model.csv_import_filename

            """
            CSV import path does not exist - handled in dfirtrack_config.form
            CSV import path is not readable - handled in dfirtrack_config.form
            CSV import file does exist but is not readable - handled in dfirtrack_config.form
            """

            # CSV import file does not exist - show warning
            if not os.path.isfile(csv_path):
                # create message
                messages.warning(request, 'CSV import file does not exist at the moment. Make sure the file is available during import.')
            # CSV import file is empty - show warning
            if os.path.isfile(csv_path):
                if os.path.getsize(csv_path) == 0:
                    # create message
                    messages.warning(request, 'CSV import file is empty. Make sure the file contains systems during import.')

            # show warning if existing systems will be updated
            if not model.csv_skip_existing_system:
                # call message
                messages.warning(request, 'WARNING: Existing systems will be updated!')

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        else:
            # show form page again
            return render(
                request,
                'dfirtrack_config/system/system_importer_file_csv_config_popup.html',
                {
                    'form': form,
                }
            )

    # GET request
    else:

        # get config model
        model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')
        # get form
        form = SystemImporterFileCsvConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/system/system_importer_file_csv_config_popup.html',
        {
            'form': form,
        }
    )
