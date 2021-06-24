from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from dfirtrack_config.forms import SystemExporterMarkdownConfigForm
from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.logger.default_logger import info_logger

@login_required(login_url="/login")
def system_exporter_markdown_config_view(request):

    # form was valid to post
    if request.method == "POST":

        # get config model
        model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        # get form
        form = SystemExporterMarkdownConfigForm(request.POST, instance = model)

        if form.is_valid():

            # save settings
            model = form.save(commit=False)
            model.save()

            # create message
            messages.success(request, 'System exporter markdown config changed')

            # call logger
            info_logger(str(request.user), " SYSTEM_EXPORTER_MARKDOWN_CONFIG_CHANGED")

            # close popup
            return HttpResponse('<script type="text/javascript">window.close();</script>')

        else:
            # show form page again
            return render(
                request,
                'dfirtrack_config/system/system_exporter_markdown_config_popup.html',
                {
                    'form': form,
                }
            )

    else:

        # get config model
        model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')
        # get form
        form = SystemExporterMarkdownConfigForm(instance = model)

    # show form page
    return render(
        request,
        'dfirtrack_config/system/system_exporter_markdown_config_popup.html',
        {
            'form': form,
        }
    )
