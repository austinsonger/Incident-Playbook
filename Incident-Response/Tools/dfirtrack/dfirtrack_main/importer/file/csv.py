from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from dfirtrack_config.models import SystemImporterFileCsvConfigModel
from dfirtrack_main.importer.file.csv_checks import check_config_attributes, check_config_cron_user, check_content_file_system
from dfirtrack_main.importer.file.csv_importer_forms import SystemImporterFileCsvForm
from dfirtrack_main.importer.file.csv_main import system_handler
from dfirtrack_main.logger.default_logger import debug_logger


@login_required(login_url="/login")
def system_create_cron(request):

    # get config model
    model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

    """ check config user """

    # call check function
    stop_system_importer_file_csv = check_config_cron_user(model, request)

    # check stop condition
    if stop_system_importer_file_csv:
        # return to 'system_list'
        return redirect(reverse('system_list'))

    """ check file system """

    # call check function
    stop_system_importer_file_csv = check_content_file_system(model, request)

    # check stop condition
    if stop_system_importer_file_csv:
        # return to 'system_list'
        return redirect(reverse('system_list'))

    """ check config attributes """

    # call check function
    stop_system_importer_file_csv = check_config_attributes(model, request)

    # check stop condition
    if stop_system_importer_file_csv:
        # return to 'system_list'
        return redirect(reverse('system_list'))
    else:
        # TODO: [logic] build url with python
        # open django admin with pre-filled form for scheduled task
        return redirect('/admin/django_q/schedule/add/?name=system_importer_file_csv&func=dfirtrack_main.importer.file.csv.system_cron')

def system_cron():
    """  CSV import via scheduled task, file is on server file system """

    # get config model
    model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

    """ check config user """

    # check config user
    stop_system_importer_file_csv = check_config_cron_user(model)

    # leave system_importer_file_csv if config caused errors
    if stop_system_importer_file_csv:
        # return to scheduled task
        return

    """ check file system """

    # check file system
    stop_system_importer_file_csv = check_content_file_system(model)

    # leave system_importer_file_csv if config caused errors
    if stop_system_importer_file_csv:
        # return to scheduled task
        return

    """ check config attributes """

    # call check function
    stop_system_importer_file_csv = check_config_attributes(model)

    # leave system_importer_file_csv if config caused errors
    if stop_system_importer_file_csv:
        # return to scheduled task
        return

    """ main function """

    # call CSV importer
    system_handler()

    # return to scheduled task
    return

@login_required(login_url="/login")
def system_instant(request):
    """  CSV import via button, file is on server file system """

    # get config model
    model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

    """ check file system """

    # check file system
    stop_system_importer_file_csv = check_content_file_system(model, request)

    # leave system_importer_file_csv if config caused errors
    if stop_system_importer_file_csv:
        # return to 'system_list'
        return redirect(reverse('system_list'))

    """ check config attributes """

    # call check function
    stop_system_importer_file_csv = check_config_attributes(model, request)

    # leave system_importer_file_csv if config caused errors
    if stop_system_importer_file_csv:
        # return to 'system_list'
        return redirect(reverse('system_list'))

    """ main function """

    # call CSV importer
    system_handler(request)

    # return to 'system_list'
    return redirect(reverse('system_list'))

@login_required(login_url="/login")
def system_upload(request):
    """  CSV import via upload form, file is on user system  """

    # POST request
    if request.method == "POST":

        # get systemcsv from request (no submitted file only relevant for tests, normally form enforces file submitting)
        check_systemcsv = request.FILES.get('systemcsv', False)

        # check request for systemcsv (file submitted - no submitted file only relevant for tests, normally form enforces file submitting)
        if check_systemcsv:

            # get config model
            model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

            """ check config attributes """

            # call check function
            stop_system_importer_file_csv = check_config_attributes(model, request)

            # leave system_importer_file_csv if config caused errors
            if stop_system_importer_file_csv:
                # return to 'system_list'
                return redirect(reverse('system_list'))

            """ main function """

            # call CSV importer
            system_handler(request, True)

        # check request for systemcsv (file not submitted - no submitted file only relevant for tests, normally form enforces file submitting)
        else:

            # get empty form
            form = SystemImporterFileCsvForm()

            # show form again
            return render(
                request,
                'dfirtrack_main/system/system_importer_file_csv.html',
                {
                    'form': form,
                }
            )

        # return to 'system_list'
        return redirect(reverse('system_list'))

    # GET request
    else:

        # get config model
        model = SystemImporterFileCsvConfigModel.objects.get(system_importer_file_csv_config_name = 'SystemImporterFileCsvConfig')

        """ check config attributes """

        # call check function
        stop_system_importer_file_csv = check_config_attributes(model, request)

        # leave system_importer_file_csv if config caused errors
        if stop_system_importer_file_csv:
            # return to 'system_list'
            return redirect(reverse('system_list'))

        # show warning if existing systems will be updated
        if not model.csv_skip_existing_system:
            # call message
            messages.warning(request, 'WARNING: Existing systems will be updated!')

        # get empty form
        form = SystemImporterFileCsvForm()

        # call logger
        debug_logger(str(request.user), ' SYSTEM_IMPORTER_FILE_CSV_ENTERED')

    # show form
    return render(
        request,
        'dfirtrack_main/system/system_importer_file_csv.html',
        {
            'form': form,
        }
    )
