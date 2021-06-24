from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from dfirtrack_config.models import SystemExporterMarkdownConfigModel
from dfirtrack_main.exporter.markdown.domainsorted import domainsorted
from dfirtrack_main.exporter.markdown.systemsorted import systemsorted

@login_required(login_url="/login")
def system(request):
    """ function to decide between sorted by system or sorted by domain """

    # get config model
    model = SystemExporterMarkdownConfigModel.objects.get(system_exporter_markdown_config_name = 'SystemExporterMarkdownConfig')

    if model.markdown_sorting == 'sys':
        systemsorted(request)
    if model.markdown_sorting == 'dom':
        domainsorted(request)

    return redirect(reverse('system_list'))
